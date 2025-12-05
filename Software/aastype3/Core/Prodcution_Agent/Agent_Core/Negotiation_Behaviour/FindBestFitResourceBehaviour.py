import json
from aastype3.Core.Prodcution_Agent.Agent_Core.Negotiation_Behaviour.PublishNegotiationResultBehaviour import PublishNegotiationResultBehaviour
from aastype3.Core.Report.AgentsReporter import report
from spade.behaviour import OneShotBehaviour


class FindBestFitResourceBehaviour(OneShotBehaviour):
    async def run(self):
        if not self.agent.all_responses_received():
            return
        
        # Get request info for logging
        try:
            request_data = json.loads(self.agent.execution_service_template.body)
            skill = request_data.get("skills_required", "unknown")
            time_slot = request_data.get("at_time", "unknown")
            participants = list(self.agent.received_responses.keys())
            
            # Log CFP sent
            report.log_cfp_sent(skill, time_slot, participants)
        except:
            pass
        
        requested_start = self._get_requested_start_time()
        if requested_start is None:
            return
        
        best_resource = self._find_best_resource(requested_start)
        
        if best_resource:
            self.agent.selected_resource = best_resource
            
            # Log resource selected
            report.log_resource_selected(
                best_resource["resource_id"],
                best_resource["time_slot"],
                f"Closest available slot (diff: {best_resource['time_diff']} mins)"
            )
            
            self.agent.add_behaviour(PublishNegotiationResultBehaviour())
        else:
            print("No suitable resource found")

    def _get_requested_start_time(self) -> int | None:
        try:
            request_data = json.loads(self.agent.execution_service_template.body)
            requested_time = request_data.get("at_time", "")
            return self._parse_time(requested_time.split("-")[0])
        except (json.JSONDecodeError, IndexError, ValueError):
            return None

    def _find_best_resource(self, requested_start: int) -> dict | None:
        best_resource = None
        best_time_diff = float('inf')
        
        for resource_id, response in self.agent.received_responses.items():
            resource = self._parse_resource_response(resource_id, response, requested_start)
            
            if resource is None:
                continue
            
            # Log CFP response
            report.log_cfp_response(resource_id, {
                "time_slot_state": resource["state"],
                "time_slot_next": resource["time_slot"],
                "violations": resource["violations"]
            })
            
            if resource["violations"]:
                continue
            
            if resource["time_diff"] < best_time_diff:
                best_time_diff = resource["time_diff"]
                best_resource = resource
        
        if best_resource:
            print(f"Best fit: {best_resource['resource_id']} "
                  f"(slot: {best_resource['time_slot']}, diff: {best_resource['time_diff']} mins)")
        
        return best_resource

    def _parse_resource_response(self, resource_id: str, response: str, requested_start: int) -> dict | None:
        try:
            data = json.loads(response)
            time_slot = data.get("time_slot_next", "")
            slot_start = self._parse_time(time_slot.split("-")[0])
            time_diff = abs(slot_start - requested_start)
            
            print(f"  {resource_id}: {time_slot} (diff: {time_diff} mins)")
            
            return {
                "resource_id": resource_id,
                "time_slot": time_slot,
                "time_diff": time_diff,
                "state": data.get("time_slot_state"),
                "violations": data.get("violations", [])
            }
        except (json.JSONDecodeError, IndexError, ValueError):
            return None

    def _parse_time(self, time_str: str) -> int:
        parts = time_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])