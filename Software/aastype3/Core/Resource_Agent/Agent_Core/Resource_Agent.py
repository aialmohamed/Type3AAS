from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage
import slixmpp.stanza
import spade
from spade.behaviour import FSMBehaviour,State
from spade.template import Template
from spade_bdi.bdi import BDIAgent
from spade_pubsub.pubsub import PubSubMixin
import argparse
import asyncio
import getpass
from datetime import datetime, timedelta
import json
import os


Agent_Initialzation_State = "Agent_Initialization_State"
Production_Request_State = "Production_Request_State"
Dummy_State = "Dummy_State"

class AgentStateMachine(FSMBehaviour):
  async def on_start(self):
    print("FSM Behaviour starting")
    print(f"Current state: {self.current_state}")


class AgentInitializationState(State):
    def __init__(self):
        super().__init__()
    
    async def run(self):
        
        current_state ,skills,skills_constarints,free_time_slots = await asyncio.gather(
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Current_State(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Capabilities_Supported_Skills(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_MaxMinDepth(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Free_Slots(),
            return_exceptions=True  # Continue if one fails
        )
        await asyncio.sleep(2)  # Simulate some processing delay
        self.agent.bdi.set_belief("current_state", current_state)
        self.agent.bdi.set_belief("supported_skills", skills)
        self.agent.bdi.set_belief("skills_constraints", skills_constarints)
        self.agent.bdi.set_belief("free_time_slots", free_time_slots)
        self.set_next_state(Production_Request_State)


class ProductionRequestState(State):
    def __init__(self):
        super().__init__()
    async def on_start(self):
        await self.agent.pubsub.subscribe("pubsub.localhost", "production_negotiation")
        try:
            await self.agent.pubsub.purge("pubsub.localhost", "production_negotiation")
            print("✓ Cleared old messages from PubSub node")
        except Exception as e:
            print(f"Note: Could not purge node (might not have permission): {e}")

    async def run(self):
        print("ProductionRequestState: Processing production request...")

        self.agent.pubsub.set_on_item_published(self.callback)
        await asyncio.sleep(2)  # Simulate some processing delay
        self.set_next_state(Dummy_State)
        
    async def callback(self, message: slixmpp.stanza.Message):
        """Handle CFP message."""
        try:
            cfp_message = CfpPubSubMessage(message=message)
            new_message = cfp_message.parse_message()
            print(f"✓ Parsed CFP Message: {new_message}")
            #self.agent.bdi.set_belief("requested_skills", cfp_message.skills)
            self.set_next_state(Dummy_State)
        except Exception as e:
            print(f"✗ Error parsing CFP: {e}")
            self.set_next_state(Dummy_State)

class DummyState(State):
    
    def __init__(self):
        super().__init__()
    
    async def run(self):
        print("DummyState: Doing nothing, transitioning back to initialization.")
        self.set_next_state(Agent_Initialzation_State)


class ResourceAgent(PubSubMixin,BDIAgent):
    def __init__(self, jid, password, asl, actions=None,resource_client: ResourceAASClient = None):
       super().__init__(jid, password, asl, actions)
       self.resource_client = resource_client

    async def setup(self):
        await self.resource_client.initialize_aas_client()
        fsm = AgentStateMachine()
        fsm.add_state(name=Agent_Initialzation_State, state=AgentInitializationState(), initial=True)
        fsm.add_state(name=Dummy_State, state=DummyState())
        fsm.add_state(name=Production_Request_State, state=ProductionRequestState())
        fsm.add_transition(source=Agent_Initialzation_State, dest=Production_Request_State)
        fsm.add_transition(source=Production_Request_State, dest=Dummy_State)



        fsm.add_transition(source=Dummy_State, dest=Agent_Initialzation_State)
        self.add_behaviour(fsm)




async def main():

    asl_path = os.path.join(os.path.dirname(__file__), "resource_agent.asl")
    print(f"Looking for ASL file at: {asl_path}")
    resource_client = ResourceAASClient(prefix="Drill_1")
    a = ResourceAgent("resource_agent_1@localhost", "password123", asl_path, resource_client=resource_client)
    await a.start(auto_register=True)
    try : 
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
    finally:
        await resource_client.close()
        await a.stop()
if __name__ == "__main__":
    spade.run(main())