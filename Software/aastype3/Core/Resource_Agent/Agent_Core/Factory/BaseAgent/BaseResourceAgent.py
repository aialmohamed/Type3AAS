from abc import ABC, abstractmethod
import argparse
import asyncio
import getpass
from datetime import datetime, timedelta
from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient


import agentspeak
import spade
from spade.behaviour import PeriodicBehaviour, TimeoutBehaviour,CyclicBehaviour,OneShotBehaviour
from spade.template import Template
import spade_bdi
from spade_bdi.bdi import BDIAgent


class BaseResourceAgent(BDIAgent,ABC):
    def __init__(self, jid, password, asl, actions=None, resource_client: ResourceAASClient = None):
        super().__init__(jid, password, asl, actions)
        self.resource_client = resource_client

    async def setup(self):
        if self.resource_client is None:
            raise ValueError("A Resource AAS Client instance must be provided")
        if not hasattr(self.resource_client,"initialize_aas_client"):
            raise ValueError("The provided client does not have 'initialize_aas_client' method , please provide a valid ResourceAASClient instance")
        await self.resource_client.initialize_aas_client()
    
    @abstractmethod
    def get_behaviour_classes(self):
        """Return a list of behaviour classes for the agent."""
        pass
    @abstractmethod
    def get_initial_beliefs(self):
        """Return a dictionary of initial beliefs for the agent."""
        pass
    async def on_end(self):
        if self.resource_client:
            await self.resource_client.close()
