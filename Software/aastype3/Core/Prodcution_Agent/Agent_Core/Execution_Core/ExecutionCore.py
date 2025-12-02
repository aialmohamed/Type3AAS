import asyncio
import pathlib
import json
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade_pubsub.pubsub import PubSubMixin
from spade.agent import Agent
from aastype3.Core.Datamodels.CfpPubSubMessag import CfpPubSubMessage




class GetUserRequestBehaviour(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(1)
    async def handle_user_request(self, payload: str):
        print(f"Handling user request with payload: {payload}")




class ExecutionAgent(PubSubMixin, Agent):
    def __init__(self, jid, password):

      super().__init__(jid, password)
    async def setup(self):
        await self.pubsub.subscribe("pubsub.localhost", "pa_user_service_request")
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


    def add_behaviours(self):
        self.get_user_request_behaviour = GetUserRequestBehaviour()
        self.add_behaviour(self.get_user_request_behaviour)
        

async def main():
    agent = ExecutionAgent(
        "execution_agent_1@localhost", "password123"
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


if __name__ == "__main__":
    import spade

    spade.run(main())