import argparse
import asyncio
import getpass
from datetime import datetime, timedelta

import spade
from spade.behaviour import OneShotBehaviour
from spade.template import Template

from spade_bdi.bdi import BDIAgent

class ReciverBehaviour(OneShotBehaviour):
    async def run(self):
        print("Reciver Behaviour is running...")
        # Wait a bit for BDI to initialize
        await asyncio.sleep(1)
        data = self.agent.bdi.get_belief_value("job")
        print(f"Belief 'job' has value: {data}")

class ReciverAgent(BDIAgent):
    async def setup(self):
        print(f"Reciver Agent {self.jid} starting...")
        self.add_behaviour(ReciverBehaviour())
        print("Reciver Agent setup complete!")

async def main():
    import os
    asl_path = os.path.join(os.path.dirname(__file__), "reciver.asl")
    print(f"Looking for ASL file at: {asl_path}")
    
    receiver = ReciverAgent("simplereciver@localhost", "password123", asl_path)
    await receiver.start(auto_register=True)
    
    print("Receiver agent running and waiting for messages...")
    await asyncio.sleep(30)  # Wait longer for messages
    
    await receiver.stop()
    print("Receiver agent stopped.")

if __name__ == "__main__":
    asyncio.run(main())