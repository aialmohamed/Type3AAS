
import json
from aastype3.Core.Prodcution_Agent.Agent_Core.Negotiation_Behaviour.PublishNegotiationResultBehaviour import PublishNegotiationResultBehaviour
from spade.behaviour import  OneShotBehaviour
 




class FindBestFitResourceBehaviour(OneShotBehaviour):
    async def run(self):
        print("Finding best fit resource from received responses")
        
        if not self.agent.all_responses_received():
            print("Not all responses have been received yet.")
            return
        
        print("All responses received. Evaluating best fit resource...")
        
        requested_start = self._get_requested_start_time()
        if requested_start is None:
            return
        
        best_resource = self._find_best_resource(requested_start)
        
        if best_resource:
            self.agent.selected_resource = best_resource
            # Send decisions to resources and notify execution core
            #await self._send_negotiation_decisions(best_resource["resource_id"])
            self.agent.add_behaviour(PublishNegotiationResultBehaviour())
        else:
            print("No suitable resource found")

    def _get_requested_start_time(self) -> int | None:
        try:
            request_data = json.loads(self.agent.execution_service_template.body)
            requested_time = request_data.get("at_time", "")
            return self._parse_time(requested_time.split("-")[0])
        except (json.JSONDecodeError, IndexError, ValueError):
            print("Failed to parse requested time")
            return None

    def _find_best_resource(self, requested_start: int) -> dict | None:
        best_resource = None
        best_time_diff = float('inf')
        
        for resource_id, response in self.agent.received_responses.items():
            resource = self._parse_resource_response(resource_id, response, requested_start)
            
            if resource is None:
                continue
            
            if resource["violations"]:
                print(f"  {resource_id}: SKIPPED (violations: {resource['violations']})")
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
        except (json.JSONDecodeError, IndexError, ValueError) as e:
            print(f"Error parsing response from {resource_id}: {e}")
            return None

    async def _send_negotiation_decisions(self, selected_id: str):
        """Send 'yes' to selected resource, 'no' to others."""
        for resource_id in self.agent.agents_subscriptions:
            decision = "yes" if resource_id == selected_id else "no"
            payload = json.dumps({"target": resource_id, "decision": decision})
            
            await self.agent.pubsub.publish(
                "pubsub.localhost",
                "pa_negotation_responses",
                payload
            )
            print(f"Sent '{decision}' to {resource_id}")

    def _parse_time(self, time_str: str) -> int:
        hours, minutes = map(int, time_str.strip().split(":"))
        return hours * 60 + minutes
