import asyncio
import json
from aastype3.Core.Prodcution_Agent.Agent_Core.Execution_Behaviour.SendNegotiationDecisionsBehaviour import SendNegotiationDecisionsBehaviour
from spade.behaviour import CyclicBehaviour





class GetNegotiationResultBehaviour(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(1)
    async def handle_negotiation_response(self, payload: str):
        self.agent.negotiation_result = json.loads(payload)
        #print(f"Handling negotiation response with payload: {self.agent.negotiation_result}")
        await asyncio.sleep(2)
        self.agent.add_behaviour(SendNegotiationDecisionsBehaviour())
