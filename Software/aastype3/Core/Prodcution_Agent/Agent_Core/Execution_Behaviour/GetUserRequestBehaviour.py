

import asyncio
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.InformNegotiationCoreServiceBehaviour import InformNegotiationCoreServiceBehaviour
from spade.behaviour import CyclicBehaviour

class GetUserRequestBehaviour(CyclicBehaviour):
    def __init__(self):
        self.inform_negotiation_core_service_behaviour = InformNegotiationCoreServiceBehaviour()
        super().__init__()
    async def run(self):
        await asyncio.sleep(1)
    async def handle_user_request(self, payload: str):
        self.agent.user_request_template.metadata = {"node":"pa_user_service_request"}
        self.agent.user_request_template.body = payload
        print(f"Handling user request with payload: {self.agent.user_request_template.body}")
        await asyncio.sleep(1)
        self.agent.add_behaviour(self.inform_negotiation_core_service_behaviour)  # Ensure behaviours are added
            