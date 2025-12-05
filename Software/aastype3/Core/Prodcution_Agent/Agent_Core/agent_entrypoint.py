import asyncio
import pathlib
import json
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade_pubsub.pubsub import PubSubMixin
from spade.agent import Agent
from aastype3.Core.Datamodels.CfpPubSubMessag import CfpPubSubMessage




class SendNewRequestBehav(OneShotBehaviour):
    async def run(self):
        print("Publishing new user service request")
        # Create a new CFP message 
        cfp_message = CfpPubSubMessage()
        cfp_message.resource_id = str(self.agent.jid.bare)
        cfp_message.skills = "drill_capability"
        cfp_message.at_time = "10:30-11:00"
        cfp_message.Input_arguments = {"X": 60, "Y": 50, "Depth": 5, "RPM": 1500}
        message_to_publish = cfp_message.create_message_to_publish()
        await self.agent.pubsub.publish("pubsub.localhost", "pa_user_service_request", message_to_publish)




class UserAgent(PubSubMixin, Agent):
    def __init__(self, jid, password):

      super().__init__(jid, password)
    async def setup(self):
        pass
        #self.pubsub.set_on_item_published(self._on_pubsub_event)
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
    def add_behaviours(self):
        self.send_new_request_behav = SendNewRequestBehav()
        self.add_behaviour(self.send_new_request_behav)
        

async def main():
    agent = UserAgent(
        "user_agent@localhost", "password123"
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