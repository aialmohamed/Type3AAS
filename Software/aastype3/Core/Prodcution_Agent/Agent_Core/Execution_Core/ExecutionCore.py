import asyncio
import json
from datetime import datetime
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.GetNegotiationResultBehaviour import GetNegotiationResultBehaviour
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.GetProccesPlanBehaviour import GetProccesPlanBehaviour
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.GetUserRequestBehaviour import GetUserRequestBehaviour
from aastype3.Core.xmpp_utils.pubsub_utils import PubSubOwnerUtils
from aastype3.Core.Report.AgentsReporter import report, EventType
from spade.template import Template
from spade_pubsub.pubsub import PubSubMixin
from spade.agent import Agent
from aastype3.Core.Prodcution_Agent.AASClient.Client.ProductionAASClient import ProductionAASClient
import spade


class ExecutionAgent(PubSubMixin, Agent):
    def __init__(self, jid, password, production_client: ProductionAASClient = None):
        self.production_client = production_client
        self.user_request_template = Template()
        self.user_request_arrived = False
        self.negotiation_result: dict = None
        self.pubsub_owner: PubSubOwnerUtils = None
        self.token_position = 0
        self.current_request: dict = None  # Store the current request
        super().__init__(jid, password)

    async def setup(self):
        await self.production_client.initialize_aas_client()
        self.pubsub_owner = PubSubOwnerUtils(self.client)
        
        await self.pubsub.subscribe("pubsub.localhost", "pa_user_service_request")
        await self.pubsub.subscribe("pubsub.localhost", "pa_negotation_result")
        await self.pubsub.subscribe("pubsub.localhost", "execution_tracking_topic")
        await self.pubsub.subscribe("pubsub.localhost", "job_completion_topic")
        self.pubsub.set_on_item_published(self._on_pubsub_event)
        
        report.log(EventType.AGENT_STARTED, "ExecutionCore", "Execution Core agent started")

    async def _on_pubsub_event(self, message):
        try:
            event = message["pubsub_event"]
            node = event["items"]["node"]
            payload_elem = event["items"]["substanzas"][0]["payload"]
            payload = (
                payload_elem.text if hasattr(payload_elem, "text") else str(payload_elem)
            )
        except Exception as exc:
            report.log(EventType.ERROR, "ExecutionCore", f"Failed to parse pubsub event: {exc}")
            return

        if node == "pa_user_service_request":
            # Start report and store request
            report.start_run()
            self.current_request = json.loads(payload)
            await self.get_user_request_behaviour.handle_user_request(payload)
            
        if node == "pa_negotation_result":
            await self._handle_negotiation_result(payload)
            
        if node == "execution_tracking_topic":
            await self._handle_tracking_update(payload)
            
        if node == "job_completion_topic":
            await self._handle_job_completion(payload)

    async def _handle_negotiation_result(self, payload: str):
        """Handle negotiation result and log to report"""
        self.negotiation_result = json.loads(payload)
        
        # Log negotiation summary
        selected = self.negotiation_result.get('selected_resource', 'unknown')
        time_slot = self.negotiation_result.get('time_slot', 'unknown')
        original = self.negotiation_result.get('original_request', {})
        skill = original.get('skills_required', 'unknown')
        
        # Get all participants (not just selected)
        all_participants = self.negotiation_result.get('all_participants', [selected])
        
        # Create negotiation summary in report
        report.log_cfp_sent(skill, original.get('at_time', 'unknown'), all_participants)
        report.log_resource_selected(selected, time_slot, "Best fit resource")
        
        await self.get_negotiation_result_behaviour.handle_negotiation_response(payload)

    async def _handle_tracking_update(self, payload: str):
        """Handle tracking updates and update the Production AAS"""
        try:
            tracking_data = json.loads(payload)
            current_node = tracking_data['current_node']
            step_status = tracking_data['step_status']
            timestamp = tracking_data['timestamp']
            resource_id = tracking_data['resource_id']
            
            # Log to report
            if step_status == "running":
                self.token_position += 1
                # Log execution started on first operation
                if self.token_position == 1:
                    skill = self.current_request.get('skills_required', 'unknown') if self.current_request else 'unknown'
                    report.log_execution_started(resource_id, skill)
                report.log_operation(resource_id, current_node, "running")
            else:
                report.log_operation(resource_id, current_node, "completed", 
                                    result=tracking_data.get('result', 'OK'))
            
            # Update the Production AAS
            old_node = await self._get_current_node_value()
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_Current_Node(current_node)
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_Token_Position(str(self.token_position))
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_TimeStamp(timestamp)
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_Step_Status(step_status)
            
            # Log AAS update
            report.log_aas_update("ExecutionTracking", "Current_Node", old_node, current_node)
            report.log_aas_update("ExecutionTracking", "Step_Status", "", step_status)
            
        except Exception as e:
            report.log(EventType.ERROR, "ExecutionCore", f"Error handling tracking update: {e}")

    async def _get_current_node_value(self) -> str:
        """Get current node value from AAS (for logging old value)"""
        try:
            return await self.production_client.SubmodelElementRepositoryGetters.getvalue_Execution_Tracking_Current_Node()
        except:
            return "N/A"

    async def _handle_job_completion(self, payload: str):
        """Handle job completion notification"""
        selected_resource = self.negotiation_result.get('selected_resource', 'unknown') if self.negotiation_result else 'unknown'
        report.log_execution_completed(selected_resource, "success")
        report.end_run()
        
        # Save reports to files
        report.save_all()

    def add_behaviours(self):
        self.get_procces_plan_behaviour = GetProccesPlanBehaviour()
        self.add_behaviour(self.get_procces_plan_behaviour)
        self.get_user_request_behaviour = GetUserRequestBehaviour()
        self.add_behaviour(self.get_user_request_behaviour)
        self.get_negotiation_result_behaviour = GetNegotiationResultBehaviour()
        self.add_behaviour(self.get_negotiation_result_behaviour)


async def main():
    production_client = ProductionAASClient("Production_1")
    agent = ExecutionAgent(
        "execution_agent_1@localhost", "password123", production_client=production_client
    )
    agent.add_behaviours()
    await agent.start(auto_register=True)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await agent.stop()
        await production_client.close()


if __name__ == "__main__":
    spade.run(main())