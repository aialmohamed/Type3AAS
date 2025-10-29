import json
from aastype3.Core.Resource_Agent.Datamodels.TimeSlot_DataType import TimeSlotDataType
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

def allocate_time_slots(free_slots: Dict[str, str], booked_slots: Dict[str, str], slot_to_allocate: str):
    if slot_to_allocate in free_slots:
        booked_slots[slot_to_allocate] = free_slots.pop(slot_to_allocate)
        print(f"Allocated slot: {slot_to_allocate}")
    else:
        print(f"Slot {slot_to_allocate} is not available for allocation.")

async def main():
    async with ResourceAASClient() as client:
        slot_to_allocate = "09:30-10:00"
        try:
            allocation_success = await client.allocate_time_slot(slot_to_allocate)
            if allocation_success:
                print(f"Successfully allocated slot: {slot_to_allocate}")
            else:
                print(f"Failed to allocate slot: {slot_to_allocate}")
        except RuntimeError as e:
            print(str(e))


if __name__ == "__main__":
    asyncio.run(main()) 
