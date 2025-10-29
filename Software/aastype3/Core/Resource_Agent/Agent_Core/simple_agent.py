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
 



class SimpleAgent(BDIAgent):

    async def setup(self):
        self.resource_client = ResourceAASClient()
        await self.resource_client.initialize_aas_client()
        
    def add_custom_actions(self, actions):
        @actions.add(".get_current_state",0 )
        def _get_current_state(agent, term, intention):
            self.add_behaviour(self.GetCurrentStatus_Behav(self.resource_client))  # schedule async work
            yield
        @actions.add(".running_job", 0)
        def _running_job(agent, term, intention):
            self.add_behaviour(self.RunningJobBehav(self.resource_client))  # schedule async work
            yield

    class GetCurrentStatus_Behav(OneShotBehaviour):
      def __init__(self,client: ResourceAASClient):
          super().__init__()
          self.resource_client = client
      async def run(self):
          current_state = await self.resource_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Current_State()
          self.agent.bdi.set_belief('current_state', f'{current_state}')  # store as quoted string so it's ground
      async def on_end(self):
          self.agent.bdi.set_belief('current_state', 'Free')

    class RunningJobBehav(OneShotBehaviour):
      def __init__(self, client: ResourceAASClient):
          super().__init__()
          self.resource_client = client
      async def run(self):

        await self.resource_client.SubmodelElementRepositoryUpdate.update_Operational_State_Current_State("Running")
        self.agent.bdi.set_belief('current_state', 'Running')
        # drilling :
        result = await self.resource_client.SubmodelElementRepositoryGetters.invoke_drill(9.0,1000,"true")
        # set belief with the actual result (as a string or number depending on result type)
        self.agent.bdi.set_belief('drill_result', str(result))
        await asyncio.sleep(3)  # simulate processing delay
        await self.resource_client.SubmodelElementRepositoryUpdate.update_Operational_State_Current_State("Done")
        self.agent.bdi.set_belief('current_state', 'Done')
async def main():
    import os
    asl_path = os.path.join(os.path.dirname(__file__), "simple_agent.asl")
    print(f"Looking for ASL file at: {asl_path}")
    a = SimpleAgent("counteragent@localhost", "password123", asl_path)
    await a.start(auto_register=True)
    await asyncio.sleep(5) 
    await a.stop()

if __name__ == "__main__":
     asyncio.run(main())