from spade.behaviour import OneShotBehaviour
from aastype3.Core.Report.AgentsReporter import report, EventType


class PreparationForExecutionBehaviour(OneShotBehaviour):
    async def run(self):
        time_slot = self.agent.bdi.get_belief_value("cfp_at_time")[0]
        allocation_res = await self.agent.resource_client.allocate_time_slot(time_slot)
        
        if allocation_res:
            state = "Busy"
            await self.agent.resource_client.SubmodelElementRepositoryUpdate.update_Operational_State_Current_State(state)
            self.agent.bdi.set_belief("current_state", state)
            Input_arguments = self.agent.bdi.get_belief_value("cfp_input_arguments")
            Input_arguments = self.agent.utils.to_dict(Input_arguments)
            
            # Log execution start
            skill = self.agent.bdi.get_belief_value("cfp_skill")[0]
            report.log_execution_started(str(self.agent.jid.bare), skill)
            
            self.agent.bdi.set_belief("is_ready_for_execution", True)
        else:
            report.log(EventType.ERROR, str(self.agent.jid.bare), 
                      f"Failed to allocate time slot: {time_slot}")
            self.agent.bdi.set_belief("is_ready_for_execution", False)