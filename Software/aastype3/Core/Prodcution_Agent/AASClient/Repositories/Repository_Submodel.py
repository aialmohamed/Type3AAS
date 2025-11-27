
import json
from typing import Any
from aastype3.Core.Prodcution_Agent.AASClient.Repositories.base.Repository_base import RepositoryBase
import aiohttp
import asyncio
from basyx.aas import model
from basyx.aas.adapter.json import json_deserialization,json_serialization
import basyx.aas.model.datatypes as datatypes



class RepositorySubmodel(RepositoryBase):
    def __init__(self, session: aiohttp.ClientSession, prefix: str = ""):
        super().__init__(session)
        self._object_store : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
        self.prefix = prefix
    def _inject_prefix_for_submode(self,prefix:str,submodel_id:str):
        return submodel_id.replace("_PA_",f"{prefix}_PA_")
    def _inject_prefix_for_shell_id(self,prefix:str,shell_id:str):
        #https://THU.de/ProdcutionAgent_
        return shell_id.replace("ProdcutionAgent_",f"ProdcutionAgent_{prefix}")
    
# region Submodels Retrieval and Storage
    async def get_Execution_Tracking_submodel_and_store(self) -> model.Submodel:
      """
      Retrieve the Execution Tracking submodel and store it in the object store.

      Returns:
          model.Submodel: The retrieved Execution Tracking submodel.
      """
      
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Execution_Tracking_Submodel_id())
      execution_tracking_submodel = await self.get_submodel_by_identifier(identifier)
      return execution_tracking_submodel
    
    async def get_Interface_and_Endpoints_submodel_and_store(self) -> model.Submodel:
      """
      Retrieve the Interface and Endpoints submodel and store it in the object store.
      Returns:
          model.Submodel: The retrieved Interface and Endpoints submodel.
      """
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Interface_and_Endpoints_Submodel_id())
      interface_and_endpoints_submodel = await self.get_submodel_by_identifier(identifier)
      return interface_and_endpoints_submodel
    
    async def get_Process_Plan_submodel_and_store(self) -> model.Submodel:
      """
      Retrieve the Process Plan submodel and store it in the object store.
      Returns:
          model.Submodel: The retrieved Process Plan submodel.
      """
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Process_Plan_Submodel_id())
      process_plan_submodel = await self.get_submodel_by_identifier(identifier)
      return process_plan_submodel
    
# endregion

# region Update
    async def update_Execution_Tracking_submodel(self, submodel_data: model.Submodel) -> Any:
      """
      Update the Execution Tracking submodel.
      Args:
          submodel_data (model.Submodel): The updated Execution Tracking submodel data.
      Returns:
          Any: The response from the update operation.
      """
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Execution_Tracking_Submodel_id())
      return await self.update_submodel_by_identifier(identifier, submodel_data)

    async def update_Interface_and_Endpoints_submodel(self, submodel_data: model.Submodel) -> Any:
        """
        Update the Interface and Endpoints submodel.
        Args:
            submodel_data (model.Submodel): The updated Interface and Endpoints submodel data.
        Returns:
            Any: The response from the update operation.
        """
        identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Interface_and_Endpoints_Submodel_id())
        return await self.update_submodel_by_identifier(identifier, submodel_data)
    
    async def update_Process_Plan_submodel(self, submodel_data: model.Submodel) -> Any:
        """
        Update the Process Plan submodel.
        Args:
            submodel_data (model.Submodel): The updated Process Plan submodel data.

        Returns:
            Any: The response from the update operation.
        """
        identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Process_Plan_Submodel_id())
        return await self.update_submodel_by_identifier(identifier, submodel_data)
# endregion

# region create submodel 
    async def create_submodel(self, submodel_data: model.Submodel) -> Any:
        """
        Create a new submodel.
        Args:
            submodel_data (model.Submodel): The submodel data to create.

        Returns:
            Any: The response from the create operation.
        """
        submodel = await self.create_submodel_base(submodel_data)
        shell_id = self._inject_prefix_for_shell_id(self.prefix, self.loader.get_shell_id())
        await self.add_submodel_to_shell(shell_id, submodel_data)
        return submodel
# endregion

#region delete submodel
    async def delete_submodel_by_identifier(self, identifier: str) -> Any:
        """
        Delete a submodel by its identifier.
        Args:
            identifier (str): The identifier of the submodel to delete.

        Returns:
            Any: The response from the delete operation.
        """
        await self.delete_submodel_by_identifier_base(identifier)
#endregion


# region Example Usage


""" def create_dummy_submodel() -> model.Submodel:
    submodel = model.Submodel(
        id_="https://THU.de/MyDummySubmodel",
        id_short="DummySubmodel",
        description=[{"language": "en", "text": "This is a dummy submodel for testing"}],
        display_name=[{"language": "en", "text": "Dummy Submodel"}],
        submodel_element=[
            model.Property(
                id_short="DummyProperty",
                value_type=datatypes.String,
                value="This is a dummy property"
            )
        ]
    )
    return submodel """

async def main():
    async with aiohttp.ClientSession() as session:
        repo = RepositorySubmodel(session,prefix="Production_1")
        capabilities_submodel = await repo.get_Execution_Tracking_submodel_and_store()
        print("Retrieved Execution Tracking Submodel:")
        print(capabilities_submodel.description)

if __name__ == "__main__":
    asyncio.run(main())

# endregion