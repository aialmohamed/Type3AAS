import argparse
import asyncio
import getpass
from datetime import datetime, timedelta
import json
from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient


from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage
import agentspeak
import slixmpp.stanza
import spade
from spade.behaviour import FSMBehaviour,State
from spade.template import Template
from spade_bdi.bdi import BDIAgent
from spade_pubsub.pubsub import PubSubMixin



Message_Receiving_State = "Message_Receiving_State"
Message_Processing_State = "Message_Processing_State"
Act_State = "Act_State"


class FSMSystemBehaviour(FSMBehaviour):
    async def on_start(self):
        print("FSM Behaviour starting")
        print(f"Current state: {self.current_state}")


class MessageReceivingState(State):
    def __init__(self):
        super().__init__()
        self.message_received = False
        self.next_transition = Message_Receiving_State
    
    async def on_start(self):
        await self.agent.pubsub.subscribe("pubsub.localhost", "production_negotiation")
        self.message_received = False
        self.next_transition = Message_Receiving_State
    
    async def run(self):
        print("MessageReceivingState: Waiting for messages...")
        self.agent.pubsub.set_on_item_published(self.callback)
        
        # Wait for message or timeout
        for i in range(5):  # 5 seconds timeout
            await asyncio.sleep(1)
            if self.message_received:
                print(f"✓ Message processed, transitioning to: {self.next_transition}")
                self.set_next_state(self.next_transition)
                return
        
        print("MessageReceivingState: Timeout, staying in receiving state")
        self.set_next_state(Message_Receiving_State)

    async def callback(self, message: slixmpp.stanza.Message):
        """Handle CFP message."""
        if message and not self.message_received:  # Prevent multiple processing
            try:
                cfp_message = CfpPubSubMessage(message=message)
                new_message = cfp_message.parse_message()
                
                if cfp_message.skills:
                    self.agent.req_skills_template.body = cfp_message.skills
                    self.agent.skill_input_template.body = json.dumps(cfp_message.Input_arguments)
                    print("✓ CFP parsed, will transition to processing state")
                    
                    # Set flag and desired transition
                    self.message_received = True
                    self.next_transition = Message_Processing_State
                else:
                    print("⚠ Empty CFP")
                    self.message_received = True
                    self.next_transition = Message_Receiving_State
                    
            except Exception as e:
                print(f"✗ Error parsing CFP: {e}")
                self.message_received = True
                self.next_transition = Message_Receiving_State

    async def on_end(self):
        # Don't unsubscribe - we'll come back to this state
        pass

class MessageProcessingState(State):
    async def run(self):
        print("🔍 Processing CFP...")
        skills_needed = self.agent.req_skills_template.body
        self.agent.available_skills_template.body = await self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Capabilities_Supported_Skills()
        
        print(f"Skills needed: {skills_needed}")
        print(f"Available skills: {self.agent.available_skills_template.body}")
        
        if skills_needed in self.agent.available_skills_template.body:
            print("✅ Skills match! Moving to action state")
            self.agent.bdi.set_belief("is_skill_match", "true")
            self.agent.bdi.set_belief("capabilities", "{'skills': " + self.agent.available_skills_template.body + "}")
            self.set_next_state(Act_State)
        else:
            print("❌ Skills don't match, returning to receiving state")
            self.agent.bdi.set_belief("is_skill_match", "false")
            self.set_next_state(Message_Receiving_State)  # Always transition!

class ActState(State):
    async def run(self):
        print("🚀 Acting on matched skills...")
        
        try:
            if self.agent.bdi.get_belief_value("is_skill_match")[0] == "true":
                depth = json.loads(self.agent.skill_input_template.body).get("Depth")
                rpm = json.loads(self.agent.skill_input_template.body).get("RPM")
                print(f"Drilling: Depth={depth}, RPM={rpm}")
                
                await asyncio.sleep(3)
                res = await self.agent.resource_client.SubmodelElementRepositoryGetters.invoke_drill(depth, rpm)
                print(f"✅ Drill result: {res}")
        
        except Exception as e:
            print(f"✗ Error in ActState: {e}")
        
        finally:
            print("🔄 Returning to message receiving state")
            self.set_next_state(Message_Receiving_State)  # Always transition back




class SimpleAgent(PubSubMixin,BDIAgent):
    def __init__(self, jid, password, asl, actions=None, resource_client: ResourceAASClient = None):
        super().__init__(jid, password, asl, actions)
        self.resource_client = resource_client

    async def setup(self):
        await self.resource_client.initialize_aas_client()
        self.req_skills_template = Template()
        self.req_skills_template.set_metadata("performative", "cfp")
        self.available_skills_template = Template()
        self.available_skills_template.set_metadata("performative", "cfp")
        self.skill_input_template = Template()
        self.skill_input_template.set_metadata("performative", "inform")

        fsm = FSMSystemBehaviour()
        fsm.add_state(name=Message_Receiving_State, state=MessageReceivingState(), initial=True)
        fsm.add_state(name=Message_Processing_State, state=MessageProcessingState())
        fsm.add_state(name=Act_State, state=ActState())

        fsm.add_transition(source=Message_Receiving_State, dest=Message_Processing_State)
        fsm.add_transition(source=Message_Processing_State, dest=Message_Receiving_State)
        fsm.add_transition(source=Message_Receiving_State, dest=Message_Receiving_State)
        fsm.add_transition(source=Message_Processing_State, dest=Act_State)
        fsm.add_transition(source=Act_State, dest=Message_Receiving_State)
        self.add_behaviour(fsm)



async def main():
    import os
    asl_path = os.path.join(os.path.dirname(__file__), "resource_agent.asl")
    print(f"Looking for ASL file at: {asl_path}")
    resource_client = ResourceAASClient(prefix="Drill_1")
    a = SimpleAgent("resource_agent_1@localhost", "password123", asl_path, resource_client=resource_client)

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