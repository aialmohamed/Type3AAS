from spade.behaviour import OneShotBehaviour




class PublishExecutionRequestToSubscribersBehaviour(OneShotBehaviour):
    def __init__(self):
        self.list_of_subs = None
        super().__init__()
    async def run(self):
        print("Publishing execution request to subscribers")
        await self.agent.pubsub.publish("pubsub.localhost","production_negotiation",self.agent.execution_service_template.body)

