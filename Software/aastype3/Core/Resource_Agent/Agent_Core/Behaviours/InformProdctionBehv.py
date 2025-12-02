
from aastype3.Core.Datamodels.NegotiationMessage import NegotiationMessage
from spade.behaviour import OneShotBehaviour

class InformProductionAgent(OneShotBehaviour):
    def __init__(self):
        super().__init__()
    async def on_start(self):
        # Inform production agent about  new negotiation message
        negotiation_message : NegotiationMessage = self.agent.new_cfp_proposal
        self.violation_string = negotiation_message.create_message_to_publish()


    async def run(self):
        if self.violation_string == "":
            print("No violations to report.")
            return
        await self.agent.pubsub.publish("pubsub.localhost","negotiation_message_topic",self.violation_string)

