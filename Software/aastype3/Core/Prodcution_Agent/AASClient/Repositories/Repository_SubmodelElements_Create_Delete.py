from typing import Any
import aiohttp
from basyx.aas import model
import asyncio
from aastype3.Core.Resource_Agent.AASClient.Repositories.base.Repository_base_SubmodelElement import SubmodelElementRepositoryBase
import basyx.aas.model.datatypes as datatypes

class SubmodelElementRepositoryCreateDelete(SubmodelElementRepositoryBase):
      """
            This class is first part of the Submodel Element ( only creating them either as
            values or as model.SubmodelElement , SubmodelCollection .... etc )
      """
      def __init__(self, session: aiohttp.ClientSession):
            super().__init__(session)

# region Submodel Elements Creation Methods
      async def create_New_SubmodelElement(self,submodel_id:str ,initial_state: str):
            return await self.create_submodel_element(submodel_id, initial_state)
      

      async def create_New_SubmodelElement_in_Collection(self,submodel_id:str,collection_id:str, initial_state: str):
            return await self.create_submodel_element_in_collection(submodel_id, collection_id, initial_state)
# endregion

# region Submodel Elements Deletion Methods
      async def delete_SubmodelElement_by_id(self,submodel_id:str, element_id:str):
            await self.delete_submodel_element_by_id(submodel_id, element_id)

      async def delete_SubmodelElement_in_Collection_by_id(self,submodel_id:str, collection_id:str, element_id:str):
            await self.delete_submodel_element_from_collection(submodel_id, collection_id, element_id)
# endregion



""" 
def create_test_submodel_element() -> model.SubmodelElement:
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/test_element'
            ),)
        )
        test_element = model.Property(
          id_short="Test_Element",
          value_type=datatypes.String,
          category="VARIABLE",
          value="Idle",  # Initial state could also be "Idle" , "Running" , "Error", "Done"
          semantic_id=semantic_reference
        )
        return test_element
def create_test_submodel_element_collection() -> model.SubmodelElementCollection:
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Collections/test_collection'
            ),)
        )
        test_collection = model.SubmodelElementCollection(
          id_short="Test_Collection",
          semantic_id=semantic_reference,
          value=[
              model.Property(
                  id_short="Test_Property",
                  value_type=datatypes.String,
                  category="VARIABLE",
                  value="Test Value",
                  semantic_id=semantic_reference
              ),
              model.Property(
                  id_short="Test_Property_2",
                  value_type=datatypes.String,
                  category="VARIABLE",
                  value="Test Value 2",
                  semantic_id=semantic_reference
              )
          ]
        )
        return test_collection

async def main():
    async with aiohttp.ClientSession() as session:
        repo = SubmodelElementRepositoryCreateDelete(session)
        # Example usage of creating a new submodel element
        submodel_id = repo.loader.get_Operational_State_submodel_id()
        new_element = create_test_submodel_element()
        #await repo.create_New_SubmodelElement(submodel_id, new_element)

        # Example usage of deleting a submodel element by id
        element_id = "Test_Element"
        await repo.delete_SubmodelElement_by_id(submodel_id, element_id)
if __name__ == "__main__":
    asyncio.run(main()) """