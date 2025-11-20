from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage
import agentspeak
import slixmpp.stanza
import spade
from spade.behaviour import FSMBehaviour,State,OneShotBehaviour
from spade.template import Template
from spade_bdi.bdi import BDIAgent
from spade_pubsub.pubsub import PubSubMixin
import argparse
import asyncio
import getpass
from datetime import datetime, timedelta
import json
import os



agent_actions = agentspeak.Actions()



Agent_Initialization_State = "Agent_Initialization_State"
Production_Request_State = "Production_Request_State"
Negotiation_State = "Negotiation_State"
Inform_ProductionAgent_State = "Inform_ProductionAgent_State"
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
        self.message_received = False
    async def on_start(self):
        self.message_received = False
        await self.agent.pubsub.subscribe("pubsub.localhost", "production_negotiation")
        self.agent.pubsub.set_on_item_published(self.callback)

    async def run(self):
        while not self.message_received:
            await asyncio.sleep(1)

        print("✓ Message received, transitioning to process request.")
        self.set_next_state(Negotiation_State)
        
    async def callback(self, message: slixmpp.stanza.Message):
        """Handle CFP message."""
        if not self.message_received: # Process only the first message
            try:
                cfp_message = CfpPubSubMessage(message=message)
                parsed_data = cfp_message.parse_message()
                
                if parsed_data:
                    print(f"{self.agent.jid} Production Requested Skills are {parsed_data.get('skills_required')}")
                    # Store the message data in the agent for the next state to use
                    self.agent.received_cfp = parsed_data
                    self.message_received = True # This will break the run() loop
                else:
                    print("Received empty or invalid message.")
            except Exception as e:
                print(f"Error in callback: {e}")

class NegotiationState(State):
    async def run(self):
        print("State: NegotiationState. Adding BDI goal '!negotiate'.")
        if "negotiation_result" in self.agent.bdi.get_beliefs():
            self.agent.bdi.remove_belief("negotiation_result")
        self.agent.bdi.set_belief("negotiate", 'yes')
        # THIS IS THE CORRECTED LOGIC
        result_tuple = self.agent.bdi.get_belief_value("negotiation_result")
        
        # Check if the tuple is not empty and its first element is 'accepted'
        if result_tuple and str(result_tuple[0]) == "accepted":
            print("Negotiation accepted, proceeding to Dummy State.")
            self.set_next_state(Dummy_State)
        else:
            print("Negotiation rejected, informing production agent.")
            self.set_next_state(Inform_ProductionAgent_State)


class InformProductionAgentState(State):
    def __init__(self):
        super().__init__()
    
    async def run(self):
        print("Informing production agent about negotiation result.")
        await asyncio.sleep(2)  # Simulate informing process
        self.set_next_state(Dummy_State)
    

class DummyState(State):
    
    def __init__(self):
        super().__init__()
    
    async def run(self):
        print("DummyState: Doing nothing, transitioning back to initialization.")
        self.set_next_state(Agent_Initialization_State)



class NegotiationBehavior(OneShotBehaviour):
    async def run(self):
        """
        This custom action performs the negotiation checks.
        The BDI engine will pass the 'agent' object to this function.
        """
        print("[Action .check_request] Performing negotiation checks...")
        
        cfp = self.agent.received_cfp
        current_state = self.agent.bdi.get_belief_value("current_state")[0]
        supported_skills = self.agent.bdi.get_belief_value("supported_skills")[0]
        
        allowed_states = ["Idle", "Free"]

        if current_state not in allowed_states:
            print(f"[Action .check_request] ❌ State '{current_state}' is not allowed.")
            self.agent.bdi.set_belief("negotiation_result", "rejected_busy")
            return

        if cfp.get("skills_required") not in supported_skills:
            print(f"[Action .check_request] ❌ Skill '{cfp.get('skills_required')}' not supported.")
            self.agent.bdi.set_belief("negotiation_result", "rejected_skill")
            return
        print("[Action .check_request] ✅ Request is valid.")
        self.agent.bdi.set_belief("negotiation_result", "accepted")



class ResourceAgent(PubSubMixin,BDIAgent):
    def __init__(self, jid, password, asl, actions=None,resource_client: ResourceAASClient = None):
       super().__init__(jid, password, asl, actions)
       self.resource_client = resource_client
       self.received_cfp = None
       self.negotiation_behaviour = NegotiationBehavior()
       
    def add_custom_actions(self, actions):
        @actions.add(".check_request",0)
        def _check_request(agent, term, intention):
            self.add_behaviour(self.negotiation_behaviour)
            yield
    async def setup(self):
        await self.resource_client.initialize_aas_client()
        fsm = AgentStateMachine()
        fsm.add_state(name=Agent_Initialization_State, state=AgentInitializationState(), initial=True)
        fsm.add_state(name=Dummy_State, state=DummyState())
        fsm.add_state(name=Production_Request_State, state=ProductionRequestState())
        fsm.add_state(name=Negotiation_State, state=NegotiationState())
        fsm.add_state(name=Inform_ProductionAgent_State, state=InformProductionAgentState())
        fsm.add_transition(source=Agent_Initialization_State, dest=Production_Request_State)
        fsm.add_transition(source=Production_Request_State, dest=Negotiation_State)
        fsm.add_transition(source=Negotiation_State, dest=Dummy_State)
        fsm.add_transition(source=Negotiation_State, dest=Production_Request_State)
        fsm.add_transition(source=Negotiation_State, dest=Inform_ProductionAgent_State)
        fsm.add_transition(source=Inform_ProductionAgent_State, dest=Dummy_State)



        fsm.add_transition(source=Dummy_State, dest=Agent_Initialization_State)
        self.add_behaviour(fsm)


async def main():

    asl_path = os.path.join(os.path.dirname(__file__), "resource_agent_fsm.asl")
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