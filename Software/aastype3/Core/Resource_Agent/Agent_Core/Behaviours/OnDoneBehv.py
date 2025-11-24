
from spade.behaviour import OneShotBehaviour


class OnDoneBehaviour(OneShotBehaviour):
    async def run(self):      
        state = "Free"
        await self.agent.resource_client.SubmodelElementRepositoryUpdate.update_Operational_State_Current_State(state)
        self.agent.bdi.set_belief("current_state", state)
        # free the time slot :
        time_slot = self.agent.bdi.get_belief_value("cfp_at_time")[0]
        await self.agent.resource_client.release_time_slot(time_slot)
        # inform the PA :
        task = self.agent.bdi.get_belief_value("cfp_skill")[0] 
        await self.agent.pubsub.publish("pubsub.localhost","job_completion_topic",f"Task {task} completed successfully.")