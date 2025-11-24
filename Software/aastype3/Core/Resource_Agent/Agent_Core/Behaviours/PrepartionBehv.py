
from spade.behaviour import OneShotBehaviour

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
            self.agent.bdi.set_belief("is_ready_for_execution", True)
        else:
            self.agent.bdi.set_belief("is_ready_for_execution", False)
