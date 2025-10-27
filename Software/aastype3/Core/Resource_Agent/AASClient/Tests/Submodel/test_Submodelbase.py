from typing import Any
import unittest

from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
import aiohttp
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes


class Test_Submodelbase(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        self.aas_client = ResourceAASClient()
        self.submodel = model.Submodel(
            id_="https://THU.de/Test_Submodel",
            id_short="TestSubmodel",
            description=model.MultiLanguageTextType({"en":"test submodel"}),
            submodel_element=[
                model.Property(id_short="Test_Property", value_type=datatypes.String, value="test")
            ]
            )
        await self.aas_client.initialize_aas_client()

    async def asyncTearDown(self):
        await self.aas_client.close()

    async def test_get_submodel(self):
        submodel_id = "https://THU.de/RA_1_SM_Capabilities"
        submodel = await self.aas_client.SubmodelRepository.get_submodel_by_identifier(submodel_id)

        self.assertIsNotNone(submodel)
        self.assertEqual(submodel.id, submodel_id)

    async def test_get_not_exist_submodel(self):
        submodel_id = "https://THU.de/RA_1_SM_NotExist"
        with self.assertRaises(aiohttp.client_exceptions.ClientResponseError):
            await self.aas_client.SubmodelRepository.get_submodel_by_identifier(submodel_id)
    
    async def test_get_shell_by_id(self):
        shell_id = "https://THU.de/ResourceAgent_1"
        shell = await self.aas_client.SubmodelRepository.get_shell_by_id(shell_id)

        self.assertIsNotNone(shell)
        self.assertEqual(shell.id, shell_id)
    
    async def test_shell_dose_not_exist(self):
        shell_id = "https://THU.de/ResourceAgent_NotExist"
        with self.assertRaises(aiohttp.client_exceptions.ClientResponseError):
            await self.aas_client.SubmodelRepository.get_shell_by_id(shell_id)
    async def test_add_submodel_to_shell(self):

        shell_id = "https://THU.de/ResourceAgent_1"
        updated_shell = await self.aas_client.SubmodelRepository.add_submodel_to_shell(shell_id, self.submodel)
        self.assertIn(model.ModelReference.from_referable(self.submodel), updated_shell.submodel)
    
    async def test_update_submodel_by_identifier(self):
        submodel_id = "https://THU.de/Test_Submodel"
        await self.aas_client.SubmodelRepository.create_submodel(self.submodel)

        # Update the submodel description
        new_description = model.MultiLanguageTextType({"en": "updated test submodel"})
        self.submodel.description = new_description
        await self.aas_client.SubmodelRepository.update_submodel_by_identifier(submodel_id, self.submodel)

        # Retrieve the updated submodel
        updated_submodel = await self.aas_client.SubmodelRepository.get_submodel_by_identifier(submodel_id)
        self.assertEqual(new_description, updated_submodel.description)

    async def test_delete_submodel_by_identifier_base(self):
        submodel_id = "https://THU.de/Test_Submodel"
        await self.aas_client.SubmodelRepository.create_submodel(self.submodel)

        # Delete the submodel
        await self.aas_client.SubmodelRepository.delete_submodel_by_identifier(submodel_id)

        # Try to retrieve the deleted submodel
        with self.assertRaises(aiohttp.client_exceptions.ClientResponseError):
            await self.aas_client.SubmodelRepository.get_submodel_by_identifier(submodel_id)


if __name__ == "__main__":
    unittest.main()
    