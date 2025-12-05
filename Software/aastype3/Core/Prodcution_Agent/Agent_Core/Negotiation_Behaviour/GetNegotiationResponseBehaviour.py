import asyncio
import json
from spade.behaviour import CyclicBehaviour
from aastype3.Core.Prodcution_Agent.Agent_Core.Negotiation_Behaviour.FindBestFitResourceBehaviour import FindBestFitResourceBehaviour



class GetNegotiationResponseBehaviour(CyclicBehaviour):
    async def run(self):
        await asyncio.sleep(1)
    async def handle_negotiation_response(self, payload: str, sender_jid: str):
        try:
            data = json.loads(payload)
            actual_sender = data.get("resource_id", sender_jid)
            actual_sender = actual_sender.split("@")[0]
        except json.JSONDecodeError:
            actual_sender = sender_jid.split("@")[0]
        
        self.agent.received_responses[actual_sender] = payload
        print(f"Response from {actual_sender}: {payload}")
        print(f"Responses so far: {list(self.agent.received_responses.keys())}")
        print(f"Expected: {self.agent.agents_subscriptions}")
        
        if self.agent.all_responses_received():
            print("All responses received. Finding best fit...")
            self.agent.add_behaviour(FindBestFitResourceBehaviour())
        else:
            print("Still waiting for more responses...")
