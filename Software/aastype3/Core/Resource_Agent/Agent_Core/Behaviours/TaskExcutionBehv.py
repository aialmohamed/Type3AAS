

from spade.behaviour import OneShotBehaviour

class TaskExcutionBehaviour(OneShotBehaviour):
    async def run(self):
        supported_skills = self.agent.bdi.get_belief_value("cfp_skill")[0]
        self.agent.bdi.set_belief("excute_skills",supported_skills)