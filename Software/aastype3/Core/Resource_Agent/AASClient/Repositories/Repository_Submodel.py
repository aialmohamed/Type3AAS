
import json
from typing import Any
from aastype3.Core.Resource_Agent.AASClient.Repositories.base.Repository_base import RepositoryBase
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
        return submodel_id.replace("_RA_",f"{prefix}_RA_")
    def _inject_prefix_for_shell_id(self,prefix:str,shell_id:str):
        #https://THU.de/ResourceAgent_
        return shell_id.replace("ResourceAgent_",f"ResourceAgent_{prefix}")
    
# region Submodels Retrieval and Storage
    async def get_Capabilities_submodel_and_store(self) -> model.Submodel:
      """
      Retrieve the Capabilities submodel and store it in the object store.

      Returns:
          model.Submodel: The retrieved Capabilities submodel.
      """
      
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Capabilities_submodel_id())
      capabilities_submodel = await self.get_submodel_by_identifier(identifier)
      return capabilities_submodel
    
    async def get_Interaction_submodel_and_store(self) -> model.Submodel:
      """
      Retrieve the Interaction submodel and store it in the object store.
      Returns:
          model.Submodel: The retrieved Interaction submodel.
      """
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Interaction_submodel_id())
      interaction_submodel = await self.get_submodel_by_identifier(identifier)
      return interaction_submodel

    async def get_Operational_State_submodel_and_store(self) -> model.Submodel:
      """
      Retrieve the Operational State submodel and store it in the object store.
      Returns:
          model.Submodel: The retrieved Operational State submodel.
      """
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Operational_State_submodel_id())
      operational_state_submodel = await self.get_submodel_by_identifier(identifier)
      return operational_state_submodel

    async def get_Knowledge_submodel_and_store(self) -> model.Submodel:
      """
      Retrieve the Knowledge submodel and store it in the object store.
      Returns:
          model.Submodel: The retrieved Knowledge submodel.
      """
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Knowledge_submodel_id())
      knowledge_submodel = await self.get_submodel_by_identifier(identifier)
      return knowledge_submodel
    
# endregion

# region Update
    async def update_Capabilities_submodel(self, submodel_data: model.Submodel) -> Any:
      """
      Update the Capabilities submodel.
      Args:
          submodel_data (model.Submodel): The updated Capabilities submodel data.

      Returns:
          Any: The response from the update operation.
      """
      identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Capabilities_submodel_id())
      return await self.update_submodel_by_identifier(identifier, submodel_data)

    async def update_Interaction_submodel(self, submodel_data: model.Submodel) -> Any:
        """
        Update the Interaction submodel.
        Args:
            submodel_data (model.Submodel): The updated Interaction submodel data.

        Returns:
            Any: The response from the update operation.
        """
        identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Interaction_submodel_id())
        return await self.update_submodel_by_identifier(identifier, submodel_data)
    async def update_Operational_State_submodel(self, submodel_data: model.Submodel) -> Any:
        """
        Update the Operational State submodel.
        Args:
            submodel_data (model.Submodel): The updated Operational State submodel data.

        Returns:
            Any: The response from the update operation.
        """
        identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Operational_State_submodel_id())
        return await self.update_submodel_by_identifier(identifier, submodel_data)
    async def update_Knowledge_submodel(self, submodel_data: model.Submodel) -> Any:
        """
        Update the Knowledge submodel.
        Args:
            submodel_data (model.Submodel): The updated Knowledge submodel data.

        Returns:
            Any: The response from the update operation.
        """
        identifier = self._inject_prefix_for_submode(self.prefix, self.loader.get_Knowledge_submodel_id())
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

"""
def create_dummy_submodel() -> model.Submodel:
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
    return submodel

async def main():
    async with aiohttp.ClientSession() as session:
        repo = RepositorySubmodel(session)
        capabilities_submodel = await repo.get_Capabilities_submodel_and_store()
        print("Capabilities Submodel Retrieved and Stored:", capabilities_submodel.id)
        capabilities_submodel.display_name = [{"language": "en", "text": "Capabilities Submodel"}]
        updated_submodel = await repo.update_Capabilities_submodel(capabilities_submodel)
        print("Capabilities Submodel Updated:", updated_submodel)
        my_dummy_submodel = create_dummy_submodel()
        create_response = await repo.create_submodel(my_dummy_submodel)
        print("Dummy Submodel Created:", create_response)
        delete = await repo.delete_submodel_by_identifier(my_dummy_submodel.id)
        print("Dummy Submodel Deleted:", delete)

if __name__ == "__main__":
    asyncio.run(main())
"""
# endregion