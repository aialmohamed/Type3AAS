import argparse
import asyncio
import getpass
from datetime import datetime, timedelta

import spade
from spade.behaviour import OneShotBehaviour
from spade.template import Template

from spade_bdi.bdi import BDIAgent

class SimpleBehaviour(OneShotBehaviour):
    async def run(self):
        print("Simple Behaviour is running...")
        await asyncio.sleep(1)  # Wait for BDI initialization
        
        data = self.agent.bdi.get_belief_value("job")
        self.agent.bdi.set_belief("something_todo", "no")
        print("Belief 'something_todo' set to 'no'.")
        print(f"Belief 'job' has value: {data}")

class SimpleAgent(BDIAgent):
    async def setup(self):
        print(f"Simple Agent {self.jid} starting...")
        self.add_behaviour(SimpleBehaviour())
        print("Simple Agent setup complete!")

async def main():
    import os
    asl_path = os.path.join(os.path.dirname(__file__), "simple.asl")
    print(f"Looking for ASL file at: {asl_path}")
    
    simple_agent = SimpleAgent("simpleagent@localhost", "password123", asl_path)
    await simple_agent.start(auto_register=True)
    
    await asyncio.sleep(10)
    await simple_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())