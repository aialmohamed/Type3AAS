
from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.NegotiationRespBehv import NegotationResponseBehaviour
from aastype3.Core.Datamodels.NegotiationMessage import NegotiationMessage
import spade
from spade_bdi.bdi import BDIAgent
from spade_pubsub.pubsub import PubSubMixin
import asyncio
import os
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.Utils import Utils
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.ProductionRqBehv import ProductionRequestBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.CFPProcessBehv import CFPProcessingBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.InformProdctionBehv import InformProductionAgent
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.TimeSlotBehv import TimeSlotProcessingBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.PrepartionBehv import PreparationForExecutionBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.TaskExcutionBehv import TaskExcutionBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.OnDoneBehv import OnDoneBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.DrillingBehv import DrillInvokerBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.MoveXYBehv import MoveXYInvokerBehaviour
from aastype3.Core.Resource_Agent.Agent_Core.Behaviours.AgentIntiBehv import AgentInitializationBehaviour


class ResourceAgent(PubSubMixin,BDIAgent):
    def __init__(self, jid, password, asl, actions=None, resource_client: ResourceAASClient =None):
        super().__init__(jid, password, asl, actions)
        self.resource_client = resource_client
        self.production_request_behaviour = ProductionRequestBehaviour()
        self.negotation_response_behaviour = NegotationResponseBehaviour()
        self.received_cfp = None
        self.cfp_not_valid_message = []
        self.new_cfp_proposal = NegotiationMessage()
        self.new_cfp_proposal.resource_id = str(self.jid.bare)
        self.utils = Utils()

    async def setup(self):
        await self.resource_client.initialize_aas_client()
        await super().setup()

    def add_custom_actions(self, actions):
        @actions.add(".initialize_agent",0)
        def _initialize_agent(agent, term, intention):
            agent_init_behaviour = AgentInitializationBehaviour()              
            self.add_behaviour(agent_init_behaviour)
            yield
        @actions.add(".check_request",0)
        def _check_request(agent, term, intention):           
            self.add_behaviour(self.production_request_behaviour)
            yield
        @actions.add(".process_cfp",0)
        def _process_cfp(agent, term, intention):  
            cfp_processing_behaviour = CFPProcessingBehaviour()              
            self.add_behaviour(cfp_processing_behaviour)           
            yield
        @actions.add(".inform_production_agent",0)
        def _inform_production_agent(agent, term, intention):
            inform_behaviour = InformProductionAgent()              
            self.add_behaviour(inform_behaviour)
            yield
        @actions.add(".process_time_slots",0)
        def _process_time_slots(agent, term, intention):
            time_slot_behaviour = TimeSlotProcessingBehaviour()             
            self.add_behaviour(time_slot_behaviour)
            yield
        @actions.add(".prepare_excution",0)
        def _prepare_excution(agent, term, intention):
            preparation_behaviour = PreparationForExecutionBehaviour()
            self.add_behaviour(preparation_behaviour)
            yield
        @actions.add(".excute_task",0)
        def _excute_task(agent, term, intention):
            excution_behaviour = TaskExcutionBehaviour()
            self.add_behaviour(excution_behaviour)
            yield
        @actions.add(".drill",0)
        def _drill(agent, term, intention):
            drill_behaviour = DrillInvokerBehaviour()
            self.add_behaviour(drill_behaviour)
            yield
        @actions.add(".move_xy",0)
        def _move_xy(agent, term, intention):
            move_xy_behaviour = MoveXYInvokerBehaviour()
            self.add_behaviour(move_xy_behaviour)
            yield
        @actions.add(".operation_done",0)
        def _operation_done(agent, term, intention):
            self.bdi.set_belief("execution_finished", True)
            yield
        @actions.add(".on_done",0)
        def _on_done(agent, term, intention):
            on_done_behaviour = OnDoneBehaviour()
            self.add_behaviour(on_done_behaviour)
            yield
        @actions.add(".handle_negotiation_response",0)
        def _handle_negotiation_response(agent, term, intention):
            self.add_behaviour(self.negotation_response_behaviour)
            yield

async def main():
    asl_path = os.path.join(os.path.dirname(__file__), "resource_agent_2.asl")
    print(f"Looking for ASL file at: {asl_path}")
    resource_client = ResourceAASClient(prefix="Drill_2")
    a = ResourceAgent("resource_agent_2@localhost", "password123", asl_path, resource_client=resource_client)
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