import asyncio
import pathlib
import json
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.template import Template
from spade_pubsub.pubsub import PubSubMixin
from spade.agent import Agent
from aastype3.Core.Datamodels.CfpPubSubMessag import CfpPubSubMessage


class NeogotaitonAgent(PubSubMixin, Agent):
  pass


async def main():
    agent = NeogotaitonAgent(
        "negotiation_agent_1@localhost", "password123"
    )
    await agent.start(auto_register=True)
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await agent.stop()


if __name__ == "__main__":
    import spade

    spade.run(main())