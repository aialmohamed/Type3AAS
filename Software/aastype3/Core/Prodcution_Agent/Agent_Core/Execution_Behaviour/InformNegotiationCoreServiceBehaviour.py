from spade.behaviour import  OneShotBehaviour

class InformNegotiationCoreServiceBehaviour(OneShotBehaviour):
    async def run(self):
        print("Informing negotiation core about new user request")
        # Here you would implement the logic to inform the negotiation core
        # adding a publisher 
        await self.agent.pubsub.publish("pubsub.localhost","pa_execution_service_topic",self.agent.user_request_template.body)
        # For example, publishing to a pubsub node or sending a message
