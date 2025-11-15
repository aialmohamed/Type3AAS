import argparse
import asyncio
import getpass
from datetime import datetime, timedelta
from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient

import pathlib
from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage
import agentspeak
import spade
from spade.behaviour import PeriodicBehaviour, TimeoutBehaviour,CyclicBehaviour,OneShotBehaviour
from spade.template import Template
import spade_bdi
from spade_bdi.bdi import BDIAgent
from spade.message import Message
from spade_pubsub.pubsub import PubSubMixin
import slixmpp.stanza


#agent : simple_product_agent@localhost




class NeogotitaionPubliserBehaviour(OneShotBehaviour):

    async def run(self):
        print("Publishing negotiation message")
        cfp_message = CfpPubSubMessage()
        cfp_message.skills = "Drill_Capability"
        cfp_message.at_time = "10:30"
        cfp_message.Input_arguments = {"X": 3, "Y": 5, "Depth": 9 , "RPM":1500}
        message_to_publish = cfp_message.create_message_to_publish()
        
        print(f"Publishing: {message_to_publish}")  # Debug
        
        await self.agent.pubsub.publish("pubsub.localhost", "production_negotiation", message_to_publish)
    async def on_end(self):
        await self.agent.stop()

class InformBehaviour(OneShotBehaviour):
   async def on_start(self):
       self.cfp_message = Message("simple_resource_agent@localhost")
       self.cfp_message.set_metadata("performative", "inform")
       self.cfp_message.body = "Skills_needed: Drilling, At_time :10:30 ,X: 3 , Y:5 ,Depth:9"
   async def run(self):
        print("Inform behaviour started")
        await self.send(self.cfp_message)
        print("Inform message sent")
        await asyncio.sleep(1)
        print("Inform behaviour finished")

class SimpleProductionAgent(PubSubMixin,BDIAgent):
    def __init__(self, jid, password,asl_path):
        super().__init__(jid, password,asl_path)
        
        
    
    async def setup(self):
      self.cfp_template = Template()
      self.cfp_template.set_metadata("performative", "cfp")
      await self.pubsub.create("pubsub.localhost","production_negotiation")


async def main():
    asl = pathlib.Path(__file__).parent / "simple_production_agent.asl"
    agent = SimpleProductionAgent("simple_product_agent@localhost", "password123", str(asl))


    inform_behaviour = InformBehaviour()
    #agent.add_behaviour(inform_behaviour)
    publish_behaviour = NeogotitaionPubliserBehaviour()
    agent.add_behaviour(publish_behaviour)
    
    await agent.start(auto_register=True)

    
    try : 
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
    finally:
        await agent.stop()

if __name__ == "__main__":
    spade.run(main())
    
