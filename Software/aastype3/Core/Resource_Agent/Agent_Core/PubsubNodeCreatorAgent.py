

import base64
from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
from aastype3.Core.Datamodels.CfpPubSubMessag import CfpPubSubMessage
import agentspeak
import slixmpp.stanza
import spade
from spade.behaviour import OneShotBehaviour,CyclicBehaviour
from spade_bdi.bdi import BDIAgent
from spade_pubsub.pubsub import PubSubMixin
import argparse
import asyncio
import getpass
from datetime import datetime, timedelta
import json
import os
from spade.agent import Agent


class PubsubNodeCreatorAgent(PubSubMixin,Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        
    async def setup(self):
        print(f"Agent {self.jid} starting PubSub node creation...")
        # Resource - Producation Nodes 
        #await self.pubsub.create("pubsub.localhost","production_negotiation")
        #await self.pubsub.delete("pubsub.localhost","production_negotiation")
        await self.pubsub.create("pubsub.localhost","capability_state_updates")
        await self.pubsub.create("pubsub.localhost","violations_topic")
        await self.pubsub.create("pubsub.localhost","counter_proposals_topic")
        await self.pubsub.create("pubsub.localhost","job_completion_topic")
        await self.pubsub.create("pubsub.localhost","negotiation_message_topic")
        await self.pubsub.create("pubsub.localhost","pa_negotation_responses")
        


        # Production Nodes 
        await self.pubsub.create("pubsub.localhost","pa_user_service_request")
        await self.pubsub.create("pubsub.localhost","pa_execution_service_topic")
        await self.pubsub.create("pubsub.localhost","pa_negotation_result")
        #await self.pubsub.create("pubsub.localhost","publish_production_negotiation_subs_topic")
        #await self.pubsub.delete("pubsub.localhost","publish_production_negotiation_subs_topic")
        print(f"PubSub node 'production_negotiation' created on pubsub.localhost by agent {self.jid}.")

async def main():
    agent = PubsubNodeCreatorAgent("node_creator_agent@localhost","password123")
    await agent.start()
    await asyncio.sleep(5)  # Wait for some time to ensure node creation
    await agent.stop()

if __name__ == "__main__":
    spade.run(main())