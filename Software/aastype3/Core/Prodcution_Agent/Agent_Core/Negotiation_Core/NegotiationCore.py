import asyncio
from aastype3.Core.Prodcution_Agent.AASClient.Client.ProductionAASClient import ProductionAASClient
from aastype3.Core.Prodcution_Agent.Agent_Core.Negotiation_Behaviour.GetExecutionCoreServiceBehaviour import GetExecutionCoreServiceBehaviour
from aastype3.Core.Prodcution_Agent.Agent_Core.Negotiation_Behaviour.GetNegotiationResponseBehaviour import GetNegotiationResponseBehaviour
from spade.template import Template
from spade_pubsub.pubsub import PubSubMixin
from spade.agent import Agent
from aastype3.Core.xmpp_utils.pubsub_utils import PubSubOwnerUtils
import spade



class NeogotaitonAgent(PubSubMixin, Agent):
    def __init__(self, jid, password, production_client: ProductionAASClient = None):
        self.production_client = production_client
        self.execution_service_template = Template()
        self.pubsub_owner: PubSubOwnerUtils = None  # Changed from pub_sub_owner
        self.agents_subscriptions: list[str] = []
        self.received_responses: dict[str,str] = {}
        self.selected_resource: dict = None
        super().__init__(jid, password)

    async def setup(self):
        await self.production_client.initialize_aas_client()
        self.pubsub_owner = PubSubOwnerUtils(self.client)
        #await self.pubsub.create("pubsub.localhost", "production_negotiation")
        await self.pubsub.subscribe("pubsub.localhost", "pa_execution_service_topic")
        await self.pubsub.subscribe("pubsub.localhost", "negotiation_message_topic")
        self.pubsub.set_on_item_published(self._on_pubsub_event)
        
        subscribers = await self.pubsub_owner.get_node_subscribers("production_negotiation")
        if subscribers:
            self.agents_subscriptions = [s.split("@")[0] for s in subscribers]
        else:
            self.agents_subscriptions = []
        print(f"Subscribers (normalized): {self.agents_subscriptions}")

    def all_responses_received(self) -> bool:
        responded = set(self.received_responses.keys())
        expected = set(self.agents_subscriptions)
        return expected.issubset(responded)
    
    async def _on_pubsub_event(self, message):
        try:
            event = message["pubsub_event"]
            node = event["items"]["node"]
            payload_elem = event["items"]["substanzas"][0]["payload"]
            payload = (
                payload_elem.text if hasattr(payload_elem, "text") else str(payload_elem)
            )
            sender_jid = str(message.get("from", ""))
            print(f"[DEBUG] Received event on node: {node}")
        except Exception as exc:
            print(f"Failed to parse pubsub event: {exc}")
            return
        if node == "pa_execution_service_topic":
            await self.get_execution_core_service_behaviour.handle_execution_service_request(payload)
        elif node == "negotiation_message_topic":
            await self.get_negotiation_response_behaviour.handle_negotiation_response(payload, sender_jid)
    
    def add_behaviours(self):
        self.get_execution_core_service_behaviour = GetExecutionCoreServiceBehaviour()
        self.add_behaviour(self.get_execution_core_service_behaviour)
        self.get_negotiation_response_behaviour = GetNegotiationResponseBehaviour()
        self.add_behaviour(self.get_negotiation_response_behaviour)


async def main():
    production_client = ProductionAASClient("Production_1")
    agent = NeogotaitonAgent(
        "negotiation_agent_1@localhost", "password123", production_client=production_client
    )
    await agent.start(auto_register=True)
    agent.add_behaviours()
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await agent.stop()


if __name__ == "__main__":
    spade.run(main())