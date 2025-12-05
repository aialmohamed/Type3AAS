import asyncio
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
        super().__init__(jid, password)

    async def setup(self):
        await self.production_client.initialize_aas_client()
        self.pubsub_owner = PubSubOwnerUtils(self.client)  # Add this
        
        await self.pubsub.subscribe("pubsub.localhost", "pa_user_service_request")
        await self.pubsub.subscribe("pubsub.localhost", "pa_negotation_result")
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
        if node == "pa_user_service_request":
            await self.get_user_request_behaviour.handle_user_request(payload)
            # publish the payload to the negotation core 
        if node == "pa_negotation_result":
            print(f"Received negotiation response: {payload}")
            await self.get_negotiation_result_behaviour.handle_negotiation_response(payload)


    def add_behaviours(self):
        self.get_procces_plan_behaviour = GetProccesPlanBehaviour()
        self.add_behaviour(self.get_procces_plan_behaviour)
        self.get_user_request_behaviour = GetUserRequestBehaviour()
        self.add_behaviour(self.get_user_request_behaviour)
        self.get_negotiation_result_behaviour = GetNegotiationResultBehaviour()
        self.add_behaviour(self.get_negotiation_result_behaviour)

        

async def main():
    # create the prodcution client 
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