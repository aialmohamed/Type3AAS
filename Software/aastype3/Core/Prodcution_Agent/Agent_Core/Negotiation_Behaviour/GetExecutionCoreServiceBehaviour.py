import asyncio
from aastype3.Core.Prodcution_Agent.Agent_Core.Negotiation_Behaviour.PublishExecutionRequestToSubscribersBehaviour import PublishExecutionRequestToSubscribersBehaviour
from spade.behaviour import CyclicBehaviour






class GetExecutionCoreServiceBehaviour(CyclicBehaviour):
    def __init__(self):
        self.publish_execution_request_behaviour = PublishExecutionRequestToSubscribersBehaviour()
        super().__init__()
    async def run(self):
        await asyncio.sleep(1)
    async def handle_execution_service_request(self, payload: str):
        self.agent.execution_service_template.metadata = {"node":"pa_execution_service_topic"}
        self.agent.execution_service_template.body = payload
        print(f"Handling execution service request with payload: {self.agent.execution_service_template.body}")
        await asyncio.sleep(1)
        self.agent.add_behaviour(self.publish_execution_request_behaviour)
        