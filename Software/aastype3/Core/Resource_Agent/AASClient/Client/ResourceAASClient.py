import json
from aastype3.Core.Datamodels.TimeSlot_DataType import TimeSlotDataType
import aiohttp
import asyncio
from typing import Any, Dict, Optional

from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_Submodel import RepositorySubmodel
from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_SubmodelElements_Getters import SubmodelElementRepositoryGetters
from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_SubmodelElements_Update import SubmodelElementRepositoryUpdate
from aastype3.Core.Resource_Agent.AASClient.Repositories.Repository_SubmodelElements_Create_Delete import SubmodelElementRepositoryCreateDelete

class ResourceAASClient:
    def __init__(self,prefix:str=""):
        self.prefix=prefix
        self.session: Optional[aiohttp.ClientSession] = None
        self.SubmodelRepository : RepositorySubmodel = None
        self.SubmodelElementRepositoryGetters : SubmodelElementRepositoryGetters = None
        self.SubmodelElementRepositoryUpdate : SubmodelElementRepositoryUpdate = None
        self.SubmodelElementRepositoryCreateDelete : SubmodelElementRepositoryCreateDelete = None

    async def initialize_aas_client(self):
        self.session = aiohttp.ClientSession()
        self.SubmodelRepository = RepositorySubmodel(self.session,prefix=self.prefix)
        self.SubmodelElementRepositoryGetters = SubmodelElementRepositoryGetters(self.session,self.prefix)
        self.SubmodelElementRepositoryUpdate = SubmodelElementRepositoryUpdate(self.session,self.prefix)
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
        
    async def allocate_time_slot(self, slot_to_allocate: str) -> bool:
        time_slot_manager: TimeSlotDataType = await self.SubmodelElementRepositoryGetters.get_time_slot_manager_from_server()
        allocation_result = time_slot_manager.allocate_slot(slot_to_allocate)
        print(f"DEBUG: Allocation result for slot {slot_to_allocate}: {allocation_result}")
        if allocation_result:
            await self.SubmodelElementRepositoryUpdate.update_time_manager_to_server(time_slot_manager)
        return allocation_result
    
    async def release_time_slot(self, slot_to_release: str) -> bool:
        time_slot_manager: TimeSlotDataType = await self.SubmodelElementRepositoryGetters.get_time_slot_manager_from_server()
        release_result = time_slot_manager.release_slot(slot_to_release)
        if release_result:
            await self.SubmodelElementRepositoryUpdate.update_time_manager_to_server(time_slot_manager)
        return release_result

async def main():
    async with ResourceAASClient(prefix="Drill_1") as client:
        skills = await client.SubmodelElementRepositoryGetters.get_Interaction_MQTT_Endpoint()
        print(f"Supported Skills: {skills.id_short}")
if __name__ == "__main__":
    asyncio.run(main()) 
