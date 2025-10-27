import aiohttp
import asyncio
from typing import Any, Dict, Optional

from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_Submodel import RepositorySubmodel
from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_SubmodelElements_Getters import SubmodelElementRepositoryGetters
from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_SubmodelElements_Update import SubmodelElementRepositoryUpdate
from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_SubmodelElements_Create_Delete import SubmodelElementRepositoryCreateDelete

class ResourceAASClient:
    def __init__(self,):
        self.session: Optional[aiohttp.ClientSession] = None
        self.SubmodelRepository : RepositorySubmodel = None
        self.SubmodelElementRepositoryGetters : SubmodelElementRepositoryGetters = None
        self.SubmodelElementRepositoryUpdate : SubmodelElementRepositoryUpdate = None
        self.SubmodelElementRepositoryCreateDelete : SubmodelElementRepositoryCreateDelete = None

    async def initialize_aas_client(self):
        self.session = aiohttp.ClientSession()
        self.SubmodelRepository = RepositorySubmodel(self.session)
        self.SubmodelElementRepositoryGetters = SubmodelElementRepositoryGetters(self.session)
        self.SubmodelElementRepositoryUpdate = SubmodelElementRepositoryUpdate(self.session)
        self.SubmodelElementRepositoryCreateDelete = SubmodelElementRepositoryCreateDelete(self.session)
        
    async def __aenter__(self):
        await self.initialize_aas_client()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any):
        await self.close()
        
    async def close(self):
        if self.session:
            await self.session.close()
        else:
            raise RuntimeError("Session was not initialized.")


""" async def main():
    async with ResourceAASClient() as client:
        mqtt_val = await client.SubmodelElementRepositoryGetters.getvalue_Interaction_MQTT_Endpoint()
        print(f"Current mqtt_val: {mqtt_val}")
        new_mqtt_val = "tcp://broker.hivemq.com:1883"
        await client.SubmodelElementRepositoryUpdate.update_Interaction_MQTT_Endpoint(new_mqtt_val)
        updated_mqtt_val = await client.SubmodelElementRepositoryGetters.getvalue_Interaction_MQTT_Endpoint()
        print(f"Updated mqtt_val: {updated_mqtt_val}")


if __name__ == "__main__":
    asyncio.run(main()) """
