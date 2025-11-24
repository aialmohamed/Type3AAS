
from spade.behaviour import OneShotBehaviour
import asyncio

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
