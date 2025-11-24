
from spade.behaviour import OneShotBehaviour

class InformProductionAgent(OneShotBehaviour):
    def __init__(self):
        self.violation_string = ""
        super().__init__()
    async def on_start(self):
        self.violation_string = ','.join(self.agent.cfp_not_valid_message)


    async def run(self):
        if self.violation_string == "":
            print("No violations to report.")
            return
        await self.agent.pubsub.publish("pubsub.localhost","violations_topic",self.violation_string)
        self.agent.bdi.set_belief("snap_back_to_listen", True)

