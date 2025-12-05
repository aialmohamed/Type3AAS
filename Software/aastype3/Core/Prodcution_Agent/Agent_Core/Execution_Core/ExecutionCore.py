import asyncio
import json
from datetime import datetime
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.GetNegotiationResultBehaviour import GetNegotiationResultBehaviour
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.GetProccesPlanBehaviour import GetProccesPlanBehaviour
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.GetUserRequestBehaviour import GetUserRequestBehaviour
from aastype3.Core.xmpp_utils.pubsub_utils import PubSubOwnerUtils
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
        self.token_position = 0  # Track token position
        super().__init__(jid, password)

    async def setup(self):
        await self.production_client.initialize_aas_client()
        self.pubsub_owner = PubSubOwnerUtils(self.client)
        
        await self.pubsub.subscribe("pubsub.localhost", "pa_user_service_request")
        await self.pubsub.subscribe("pubsub.localhost", "pa_negotation_result")
        await self.pubsub.subscribe("pubsub.localhost", "execution_tracking_topic")
        self.pubsub.set_on_item_published(self._on_pubsub_event)

    async def _on_pubsub_event(self, message):
        try:
            event = message["pubsub_event"]
            node = event["items"]["node"]
            payload_elem = event["items"]["substanzas"][0]["payload"]
            payload = (
                payload_elem.text if hasattr(payload_elem, "text") else str(payload_elem)
            )
        except Exception as exc:
            print(f"Failed to parse pubsub event: {exc}")
            return
        print(f"[DEBUG] Received event on node: {node}")
        if node == "pa_user_service_request":
            await self.get_user_request_behaviour.handle_user_request(payload)
        if node == "pa_negotation_result":
            print(f"Received negotiation response: {payload}")
            await self.get_negotiation_result_behaviour.handle_negotiation_response(payload)
        if node == "execution_tracking_topic":
            await self._handle_tracking_update(payload)

    async def _handle_tracking_update(self, payload: str):
        """Handle tracking updates and update the Production AAS"""
        try:
            tracking_data = json.loads(payload)
            current_node = tracking_data['current_node']
            step_status = tracking_data['step_status']
            timestamp = tracking_data['timestamp']
            
            #print(f"[TRACKING UPDATE] Resource: {tracking_data['resource_id']}")
            #print(f"  Node: {current_node} -> Status: {step_status}")
            #print(f"  Timestamp: {timestamp}")
            
            # Update token position when a step starts
            if step_status == "running":
                self.token_position += 1
            
            # Update the Production AAS with tracking info
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_Current_Node(current_node)
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_Token_Position(str(self.token_position))
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_TimeStamp(timestamp)
            await self.production_client.SubmodelElementRepositoryUpdate.update_Execution_Tracking_Step_Status(step_status)
            
            #print(f"[AAS UPDATED] Current Node: {current_node}, Token: {self.token_position}, Status: {step_status}")
            
        except Exception as e:
            print(f"Error handling tracking update: {e}")

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