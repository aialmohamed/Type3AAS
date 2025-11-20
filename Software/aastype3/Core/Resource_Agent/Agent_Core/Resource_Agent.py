import ast
import base64
from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
from aastype3.Core.Resource_Agent.Datamodels.CfpPubSubMessag import CfpPubSubMessage
from aastype3.Core.Resource_Agent.Datamodels.Violation_Enum import ViolationEnum
import agentspeak
import slixmpp.stanza
import spade
from spade.behaviour import OneShotBehaviour,CyclicBehaviour
from spade_bdi.bdi import BDIAgent
from spade_pubsub.pubsub import PubSubMixin
import argparse
import asyncio
import getpass
from datetime import datetime, timedelta
import json
import os


class AgentInitializationBehaviour(OneShotBehaviour):
    async def run(self):
        # Constraints are always MAX,MIN values
        current_state ,skills,skills_constarints,skill_constarints_types,free_time_slots,booked_time_slots = await asyncio.gather(
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Current_State(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Capabilities_Supported_Skills(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_MaxMinDepth(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_Constraints_Type(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Free_Slots(),
            self.agent.resource_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Booked_Slots(),
            return_exceptions=True  # Continue if one fails
        )

        await asyncio.sleep(2)  # Simulate some processing delay
        self.agent.bdi.set_belief("current_state", current_state)
        self.agent.bdi.set_belief("supported_skills", skills)
        self.agent.bdi.set_belief("skills_constraints", skills_constarints)
        self.agent.bdi.set_belief("skills_constraints_types", skill_constarints_types)
        self.agent.bdi.set_belief("free_time_slots", free_time_slots)
        self.agent.bdi.set_belief("booked_time_slots", booked_time_slots)

      
        
class ProductionRequestBehaviour(CyclicBehaviour):
    # TODO : i think we need to change this from Pubsub to messages 
    async def on_start(self):
        await self.agent.pubsub.subscribe("pubsub.localhost", "production_negotiation")
        self.agent.pubsub.set_on_item_published(self.on_message)
        #self.agent.bdi.set_belief("is_cfp_received", False)
        #self.agent.bdi.remove_belief("is_cfp_received")

    async def run(self):
        await asyncio.sleep(1)

    async def on_message(self, message: slixmpp.stanza.Message):
        try:
            cfp_message = CfpPubSubMessage(message=message)
            self.agent.received_cfp = cfp_message.parse_message()
            data = self.agent.received_cfp

            #print("Updating BDI beliefs...")
            # Retract old -> set new to force +belief events
            cfp_skills = data.get("skills_required")
            cfp_at_time = data.get("at_time")
            input_arguments = data.get("input_arguments")


            try: self.agent.bdi.remove_belief("cfp_skill")
            except Exception: pass
            self.agent.bdi.set_belief("cfp_skill", cfp_skills)

            try: self.agent.bdi.remove_belief("cfp_at_time")
            except Exception: pass
            self.agent.bdi.set_belief("cfp_at_time", cfp_at_time)

            try: self.agent.bdi.remove_belief("cfp_input_arguments")
            except Exception: pass
            self.agent.bdi.set_belief("cfp_input_arguments", str(input_arguments))


            self.agent.bdi.set_belief("is_cfp_received", True)
            # for debugging only: yield to the BDI loop, then read back
            #await asyncio.sleep(5)
            #print("is_cfp_received now ->", self.agent.bdi.get_belief_value("is_cfp_received"))
            #self.kill()
        except Exception as e:
            import traceback
            print(f"Error in callback type={type(e).__name__} msg={e!r}")
            traceback.print_exc()


class CFPProcessingBehaviour(OneShotBehaviour):
    async def on_start(self):
        self.agent.cfp_not_valid_message = []
        self.violation_flag = False
        self.violation_Idle_flag = False
        self.violation_skill_flag = False
        self.violation_constraint_not_found_flag = False
        self.violation_constraint_flag = False
        self.skipping_constraint_check_flag = False


    async def run(self):
        #self.agent.bdi.set_belief("is_cfp_valid", False)
        #print("Processing CFP...")
        input_arguments = self.agent.bdi.get_belief_value("cfp_input_arguments")
        input_arguments = self.agent.utils.to_dict(input_arguments)
        #print(f"Input Arguments (raw): {input_arguments.keys()}")
        cfp_skills = self.agent.bdi.get_belief_value("cfp_skill")[0]
        #print(f"CFP Skills Required: {cfp_skills}")
        try:
            current_state = self.agent.bdi.get_belief_value("current_state")[0]
            allowed_states = ["Idle","Free"]

            # 1 - check state :
            if current_state not in allowed_states:
                self.agent.cfp_not_valid_message.append(ViolationEnum.RESOURCE_NOT_IN_IDLE_FREE_VIOLATION.name)
                self.violation_Idle_flag = True
                
            else :
                self.violation_Idle_flag = False
            # 2- check matching skills 
            resource_skills = self.agent.bdi.get_belief_value("supported_skills")
            if cfp_skills not in resource_skills:
                self.violation_skill_flag = True
                self.agent.cfp_not_valid_message.append(ViolationEnum.SKILL_MISMATCH_VIOLATION.name)
            else :
                self.violation_skill_flag = False
            # 3 - check input arguments within constraints
            constraint_types = self.agent.bdi.get_belief_value("skills_constraints_types")[0]
            constraints = list(self.agent.bdi.get_belief_value("skills_constraints"))
            
            if not constraint_types in input_arguments.keys():
                self.violation_constraint_not_found_flag = True
                self.agent.cfp_not_valid_message.append(ViolationEnum.CONSTRAINT_NOT_FOUND_VIOLATION.name)
            else :
                self.violation_constraint_not_found_flag = False
            # check the value of the input that we match to the contraint if the constraint type found
            if  constraint_types in input_arguments.keys():
                tageted_input = input_arguments[constraint_types] 
                min_constraint, max_constraint = map(float, sorted(constraints))
                tageted_input = float(tageted_input)
                if not (min_constraint <= tageted_input <= max_constraint):
                    self.violation_constraint_flag = True
                    self.agent.cfp_not_valid_message.append(ViolationEnum.CONSTRAINT_VIOLATION.name)
                else :
                    self.violation_constraint_flag = False
            else:
                self.skipping_constraint_check_flag = True
                self.agent.cfp_not_valid_message.append(ViolationEnum.SKIPPING_CONSTRAINT_CHECK_VIOLATION.name)
            # finaly set the belief
            if (self.violation_Idle_flag or self.violation_skill_flag or 
                self.violation_constraint_not_found_flag or self.violation_constraint_flag or
                self.skipping_constraint_check_flag):
                self.violation_flag = True
            else:
                self.violation_flag = False

            self.agent.bdi.set_belief("is_cfp_valid", not self.violation_flag)
        except Exception as e:
            print(f"Error processing CFP: {e}")

class InformProductionAgent(OneShotBehaviour):
    def __init__(self):
        self.violation_string = ""
        super().__init__()
    async def on_start(self):
        print("Publishing skill state...")
        self.violation_string = ','.join(self.agent.cfp_not_valid_message)
        print(self.violation_string)
        print("Skill state published.")

    async def run(self):
        # create a publisher 
        if self.violation_string == "":
            print("No violations to report.")
            return
        await self.agent.pubsub.publish("pubsub.localhost","violations_topic",self.violation_string)
        # then we need some how to snap back to the ProductionRequestBehaviour to wait for new CFPs
        #await asyncio.sleep(4)
        self.agent.bdi.set_belief("snap_back_to_listen", True)
        #self.agent.production_request_behaviour.start()



class TimeSlotProcessingBehaviour(OneShotBehaviour):
    async def on_start(self):
        self.cfp_at_time = self.agent.bdi.get_belief_value("cfp_at_time")[0]
        self.free_time_slots = self.agent.bdi.get_belief_value("free_time_slots")
        self.booked_time_slots  = self.agent.bdi.get_belief_value("booked_time_slots")
        self.new_cfp_proposal = CfpPubSubMessage()
        #print("type of CFP at_time:", type(self.cfp_at_time))
        #print("type of free_time_slots:", type(self.free_time_slots))
        #print("type of booked_time_slots:", type(self.booked_time_slots))
        
        #print(f"free slots (parsed): {self.free_time_slots}")
        #print(f"booked slots (parsed): {self.booked_time_slots}")
    async def run(self):
        print("Processing time slots...")
        print(f"CFP at_time: {self.cfp_at_time}")
        print(f"Currently booked time slots: {self.booked_time_slots}")
        if self.cfp_at_time in self.booked_time_slots:
            print(f"Time slot {self.cfp_at_time} is already booked. Cannot proceed.")
            # here is logic for the new preposal
            self.new_cfp_proposal.skills = self.agent.bdi.get_belief_value("cfp_skill")[0]
            self.new_cfp_proposal.at_time = list(self.free_time_slots) if self.free_time_slots else "No Available Slot"
            self.new_cfp_proposal.Input_arguments = self.agent.bdi.get_belief_value("cfp_input_arguments")
            self.new_cfp_proposal.Input_arguments = self.agent.utils.to_dict(self.new_cfp_proposal.Input_arguments)
            self.agent.bdi.set_belief("new_cfp_proposal", self.new_cfp_proposal.create_message_to_publish())
        else:
            print(f"Time slot {self.cfp_at_time} is available. Booking now...")
            # here is the go next logic
        await asyncio.sleep(1) 
        print("Time slots processed.")





class ResourceAgent(PubSubMixin,BDIAgent):
    def __init__(self, jid, password, asl, actions=None, resource_client: ResourceAASClient =None):
        super().__init__(jid, password, asl, actions)
        self.resource_client = resource_client
        self.production_request_behaviour = ProductionRequestBehaviour()
        self.received_cfp = None
        self.cfp_not_valid_message = []
        self.utils = Utils()
        
        
    async def setup(self):
        #print("Setting up Resource Agent...")
        await self.resource_client.initialize_aas_client()
        await super().setup()

    def add_custom_actions(self, actions):
        @actions.add(".initialize_agent",0)
        def _initialize_agent(agent, term, intention):
            #print("Action: Initializing agent via BDI action.")
            agent_init_behaviour = AgentInitializationBehaviour()              
            self.add_behaviour(agent_init_behaviour)
            #print("Action: Agent initialization complete.")
            yield
        @actions.add(".check_request",0)
        def _check_request(agent, term, intention):
            #print("Action: Checking production request via BDI action.")               
            self.add_behaviour(self.production_request_behaviour)
            #print("Action: Production request check initiated.")
            yield
        @actions.add(".process_cfp",0)
        def _process_cfp(agent, term, intention):
            #print("Action: Processing CFP via BDI action.")     
            cfp_processing_behaviour = CFPProcessingBehaviour()              
            self.add_behaviour(cfp_processing_behaviour)           
            #print("Action: CFP processing initiated.")
            yield
        @actions.add(".inform_production_agent",0)
        def _inform_production_agent(agent, term, intention):
            #print("Action: Publishing skill state via BDI action.") 
            inform_behaviour = InformProductionAgent()              
            self.add_behaviour(inform_behaviour)
            #print("Action: Skill state published.")
            yield
        @actions.add(".process_time_slots",0)
        def _process_time_slots(agent, term, intention):
            #print("Action: Processing time slots via BDI action.")
            time_slot_behaviour = TimeSlotProcessingBehaviour()             
            self.add_behaviour(time_slot_behaviour)
            #print("Action: Time slot processing initiated.")
            yield




class Utils:
    def __init__(self):
        pass
    def to_dict(self,value):
        if isinstance(value, dict):
            return value
        if isinstance(value, (list, tuple)):
            s = ",".join(str(x) for x in value)
        else:
            s = str(value)
        s = s.strip()
        # try JSON (double quotes) then Python literal (single quotes)
        try:
            return json.loads(s)
        except Exception:
            pass
        try:
            return ast.literal_eval(s)
        except Exception:
            return {}




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