
import aiohttp
import asyncio
from typing import Any, Dict, Optional

from aastype3.Core.Prodcution_Agent.AASClient.Repositories.Repository_SubmodelElements_Getters import SubmodelElementRepositoryGetters
from aastype3.Core.Prodcution_Agent.AASClient.Repositories.Repository_SubmodelElements_Update import SubmodelElementRepositoryUpdate
from aastype3.Core.Prodcution_Agent.AASClient.Repositories.Repository_SubmodelElements_Create_Delete import SubmodelElementRepositoryCreateDelete
from aastype3.Core.Prodcution_Agent.AASClient.Repositories.Repository_Submodel import RepositorySubmodel


class ProductionAASClient:
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

async def main():
    async with ProductionAASClient(prefix="Production_1") as client:
        res = await client.SubmodelElementRepositoryGetters.getvalue_Interface_Endpoints_Submodel_Endpoints_Collection()
        print(f"Supported Skills: {res}")
        
if __name__ == "__main__":
    asyncio.run(main())