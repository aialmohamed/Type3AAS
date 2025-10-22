import argparse
import asyncio
import getpass
from datetime import datetime, timedelta

import spade
from spade.behaviour import PeriodicBehaviour, TimeoutBehaviour
from spade.template import Template

from spade_bdi.bdi import BDIAgent


class CounterAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "B1"})
        self.add_behaviour(self.UpdateCounterBehav(period=0.5, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B2"})
        self.add_behaviour(self.ResetCounterBehav(period=2, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B3"})
        self.add_behaviour(self.SwitchBeliefBehav(period=1, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B4"})
        self.add_behaviour(self.RemoveBeliefsBehav(start_at=datetime.now() + timedelta(seconds=4.5)), template)

    class UpdateCounterBehav(PeriodicBehaviour):
        async def on_start(self):
            self.counter = self.agent.bdi.get_belief_value("counter")[0]
        async def run(self):
            if self.counter != self.agent.bdi.get_belief_value("counter")[0]:
                self.counter = self.agent.bdi.get_belief_value("counter")[0]
                print(self.agent.bdi.get_belief("counter"))

    class ResetCounterBehav(PeriodicBehaviour):
        async def run(self):
            self.agent.bdi.set_belief('counter', 0)

    class SwitchBeliefBehav(PeriodicBehaviour):
        async def run(self):
            try:
                type = self.agent.bdi.get_belief_value("type")[0]
                if type == 'inc':
                    self.agent.bdi.set_belief('type', 'dec')
                else:
                    self.agent.bdi.set_belief('type', 'inc')
            except Exception as e:
                print("No belief 'type'.")

    class RemoveBeliefsBehav(TimeoutBehaviour):
        async def run(self):
            self.agent.bdi.remove_belief('type', 'inc')
            self.agent.bdi.remove_belief('type', 'dec')


async def main():
    import os
    asl_path = os.path.join(os.path.dirname(__file__), "counter.asl")
    print(f"Looking for ASL file at: {asl_path}")
    a = CounterAgent("counteragent@localhost", "password123", asl_path)
    await a.start(auto_register=True)
    a.web.start(hostname="localhost", port=10000)
    print("Counter Agent started")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
    finally:
        a.web.stop()
        await a.stop()
    #await asyncio.sleep(5)
    #await a.stop()


if __name__ == "__main__":


    spade.run(main())