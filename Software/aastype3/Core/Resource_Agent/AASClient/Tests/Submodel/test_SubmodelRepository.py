from typing import Any
import unittest

from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
import aiohttp
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes



class Test_Submodelbase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
      self.aas_client = ResourceAASClient()
      self.test_submodel = model.Submodel(
          id_="https://THU.de/Test_Submodel",
          id_short="TestSubmodel",
          description=model.MultiLanguageNameType({"en":"test submodel"}),
          submodel_element=[
              model.Property(id_short="Test_Property", value_type=datatypes.String, value="test")
          ]
          )
      await self.aas_client.initialize_aas_client()

    async def asyncTearDown(self):
        await self.aas_client.close()

    async def test_get_Capabilities_submodel_and_store(self):
        submodel = await self.aas_client.SubmodelRepository.get_Capabilities_submodel_and_store()
        self.assertIsInstance(submodel, model.Submodel)
        self.assertEqual(submodel.id_short, "RA_1_SM_Capabilities")

    async def test_get_Interaction_submodel_and_store(self):
        submodel = await self.aas_client.SubmodelRepository.get_Interaction_submodel_and_store()
        self.assertIsInstance(submodel, model.Submodel)
        self.assertEqual(submodel.id_short, "RA_1_SM_Interaction")
    
    async def test_get_Knowledge_submodel_and_store(self):
        submodel = await self.aas_client.SubmodelRepository.get_Knowledge_submodel_and_store()
        self.assertIsInstance(submodel, model.Submodel)
        self.assertEqual(submodel.id_short, "RA_1_SM_Knowledge")

    async def test_get_Operational_State_submodel_and_store(self):
        submodel = await self.aas_client.SubmodelRepository.get_Operational_State_submodel_and_store()
        self.assertIsInstance(submodel, model.Submodel)
        self.assertEqual(submodel.id_short, "RA_1_SM_Operational_State")

    async def test_update_Capabilities_submodel(self):
        
        new_description = model.MultiLanguageNameType({"en": "Updated Capabilities description"})
        submodel = await self.aas_client.SubmodelRepository.get_Capabilities_submodel_and_store()
        submodel.description = new_description
        response = await self.aas_client.SubmodelRepository.update_Capabilities_submodel(submodel)
        updated_submodel = await self.aas_client.SubmodelRepository.get_Capabilities_submodel_and_store()

        self.assertEqual(updated_submodel.description, new_description)

        # reset the description to original
        original_description = model.MultiLanguageNameType({"en": "Submodel for the Capabilities of the Resource Agent"})
        submodel.description = original_description
        await self.aas_client.SubmodelRepository.update_Capabilities_submodel(submodel)
    
    async def test_update_Knowledge_submodel(self):
        new_description = model.MultiLanguageNameType({"en": "Updated Knowledge description"})
        submodel = await self.aas_client.SubmodelRepository.get_Knowledge_submodel_and_store()
        submodel.description = new_description
        response = await self.aas_client.SubmodelRepository.update_Knowledge_submodel(submodel)
        updated_submodel = await self.aas_client.SubmodelRepository.get_Knowledge_submodel_and_store()

        self.assertEqual(updated_submodel.description, new_description)

        # reset the description to original
        original_description = model.MultiLanguageNameType({"en": "Submodel for the Knowledge of the Resource Agent"})
        submodel.description = original_description
        await self.aas_client.SubmodelRepository.update_Knowledge_submodel(submodel)

    async def test_update_Operational_State_submodel(self):
        new_description = model.MultiLanguageNameType({"en": "Updated Operational State description"})
        submodel = await self.aas_client.SubmodelRepository.get_Operational_State_submodel_and_store()
        submodel.description = new_description
        response = await self.aas_client.SubmodelRepository.update_Operational_State_submodel(submodel)
        updated_submodel = await self.aas_client.SubmodelRepository.get_Operational_State_submodel_and_store()

        self.assertEqual(updated_submodel.description, new_description)

        # reset the description to original
        original_description = model.MultiLanguageNameType({"en": "Submodel for the Operational State of the Resource Agent"})
        submodel.description = original_description
        await self.aas_client.SubmodelRepository.update_Operational_State_submodel(submodel)

    async def test_update_Interaction_submodel(self):
        new_description = model.MultiLanguageNameType({"en": "Updated Interaction description"})
        submodel = await self.aas_client.SubmodelRepository.get_Interaction_submodel_and_store()
        submodel.description = new_description
        response = await self.aas_client.SubmodelRepository.update_Interaction_submodel(submodel)
        updated_submodel = await self.aas_client.SubmodelRepository.get_Interaction_submodel_and_store()

        self.assertEqual(updated_submodel.description, new_description)

        # reset the description to original
        original_description = model.MultiLanguageNameType({"en": "Submodel for the Interaction of the Resource Agent"})
        submodel.description = original_description
        await self.aas_client.SubmodelRepository.update_Interaction_submodel(submodel)
    
    async def test_create_submodel(self):
        created_submodel = await self.aas_client.SubmodelRepository.create_submodel(self.test_submodel)

        # get the submodel back  : 

        retrieved_submodel = await self.aas_client.SubmodelRepository.get_submodel_by_identifier(self.test_submodel.id)

        self.assertEqual(self.test_submodel.id, retrieved_submodel.id)
        self.assertEqual(self.test_submodel.id_short, retrieved_submodel.id_short)
        self.assertEqual(self.test_submodel.description, retrieved_submodel.description)

        # remove the created submodel
        # delete is already tested in the Submodelbase testcase
        await self.aas_client.SubmodelRepository.delete_submodel_by_identifier(self.test_submodel.id)


if __name__ == "__main__":
    unittest.main()
       
    