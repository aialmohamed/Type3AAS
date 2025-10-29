from typing import Any
import unittest

from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
import aiohttp
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes


class Test_SubmodelElementbase(unittest.IsolatedAsyncioTestCase):
    
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
        
        self.sm_element_test = model.Property(
          id_short="Test_Property2",
          value_type=datatypes.String,
          category="VARIABLE",
          value="TEST2",  
        )
        await self.aas_client.initialize_aas_client()

    async def asyncTearDown(self):
        await self.aas_client.close()

    async def test_get_submodel_element_by_id(self):
        submodel_id = "https://THU.de/RA_1_SM_Operational_State"
        element_id = "Current_Operational_State"
        element = await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_element_by_id(submodel_id, element_id)

        self.assertIsNotNone(element)
        self.assertEqual(element.id_short, element_id)

    async def test_get_submodel_elements_from_collection(self):
        submodel_id = "https://THU.de/RA_1_SM_Interaction"
        collection_id ="Endpoints"
        element_id = "MQTT_Broker_Endpoint"
        property = await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_elements_from_collection(submodel_id, collection_id, element_id)

        self.assertIsNotNone(property)
        self.assertEqual(property.id_short, element_id)

    async def test_get_submodel_element_value_from_collection(self):
        submodel_id = "https://THU.de/RA_1_SM_Interaction"
        collection_id ="Endpoints"
        element_id = "MQTT_Broker_Endpoint"
        value = await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_element_value_from_collection(submodel_id, collection_id, element_id)

        # value in server : 
        value_expected = "mqtt://Place_Holder:1883"
        self.assertIsNotNone(value)
        self.assertEqual(value, value_expected)
    
    async def test_update_submodel_element_value_by_id(self):
        submodel_id = "https://THU.de/Test_Submodel"
        element_id = "Test_Property"
        new_value = "updated_test_value"

        # First, create the submodel to ensure it exists
        await self.aas_client.SubmodelRepository.create_submodel(self.submodel)

        # Update the submodel element value
        updated_element = await self.aas_client.SubmodelElementRepositoryUpdate.update_submodel_element_value_by_id(submodel_id, element_id, new_value)

        # Retrieve the updated submodel element to verify the change
        retrieved_element = await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_element_by_id(submodel_id, element_id)
        self.assertIsNotNone(retrieved_element)
        self.assertEqual(retrieved_element.value, new_value)
    
    async def test_update_submodel_element_value_from_collection(self):
        submodel_id = "https://THU.de/RA_1_SM_Interaction"
        collection_id ="Endpoints"
        element_id = "MQTT_Broker_Endpoint"
        new_value = "mqtt://Updated_Place_Holder:1883"

        # Update the submodel element value in the collection
        updated_element = await self.aas_client.SubmodelElementRepositoryUpdate.update_submodel_element_value_from_collection(submodel_id, collection_id, element_id, new_value)

        # Retrieve the updated submodel element to verify the change
        retrieved_element = await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_elements_from_collection(submodel_id, collection_id, element_id)
        self.assertIsNotNone(retrieved_element)
        self.assertEqual(retrieved_element.value, new_value)

        # reset the value to original 
        await self.aas_client.SubmodelElementRepositoryUpdate.update_submodel_element_value_from_collection(submodel_id, collection_id, element_id, "mqtt://Place_Holder:1883")
    
    async def test_invoke_operation_on_submodel_element(self):
        submodel = "https://THU.de/RA_1_SM_Capabilities"
        element_id = "Drill_Capability"
        depth = 10.0
        input_params ={"Drill_Depth": depth, "Drill_Speed": 100}

        payload = await self.aas_client.SubmodelElementRepositoryGetters._invoke_operation_payload(submodel, element_id, input_params)
        result = await self.aas_client.SubmodelElementRepositoryGetters.invoke_operation_on_submodel_element(submodel_id=submodel, element_id=element_id, input_params=payload,Async_flag="false")
        print(result)
        self.assertIsNotNone(result)
        self.assertEqual(float(result), depth * depth)
        #self.assertEqual(result.status, "success")
    
    async def test_create_submodel_element(self):
        submodel_id = "https://THU.de/Test_Submodel"
        # First, create the submodel to ensure it exists
        await self.aas_client.SubmodelRepository.create_submodel(self.submodel)

        # Create the submodel element
        created_element = await self.aas_client.SubmodelElementRepositoryCreateDelete.create_submodel_element(submodel_id, self.sm_element_test)

        # Retrieve the created submodel element to verify its existence
        retrieved_element = await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_element_by_id(submodel_id, self.sm_element_test.id_short)
        self.assertIsNotNone(retrieved_element)
        self.assertEqual(retrieved_element.id_short, self.sm_element_test.id_short)
        self.assertEqual(retrieved_element.value, self.sm_element_test.value)
    
    async def test_create_submodel_element_in_collection(self):
        submodel_id = "https://THU.de/RA_1_SM_Interaction"
        collection_id ="Endpoints"
        new_property = model.Property(
          id_short="HTTP_Broker_Endpoint",
          value_type=datatypes.String,
          category="VARIABLE",
          value="http://Place_Holder:8080",  
        )

        # Create the submodel element in the collection
        created_element = await self.aas_client.SubmodelElementRepositoryCreateDelete.create_submodel_element_in_collection(submodel_id, collection_id, new_property)

        # Retrieve the created submodel element to verify its existence
        retrieved_element = await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_elements_from_collection(submodel_id, collection_id, new_property.id_short)
        self.assertIsNotNone(retrieved_element)
        self.assertEqual(retrieved_element.id_short, new_property.id_short)
        self.assertEqual(retrieved_element.value, new_property.value)

        # Clean up by deleting the created property
        await self.aas_client.SubmodelElementRepositoryCreateDelete.delete_submodel_element_from_collection(submodel_id, collection_id, new_property.id_short)

    async def test_delete_submodel_element_by_id(self):
        submodel_id = "https://THU.de/Test_Submodel"
        element_id = "Test_Property2"

        # First, create the submodel to ensure it exists
        await self.aas_client.SubmodelRepository.create_submodel(self.submodel)

        # Create the submodel element to ensure it exists
        await self.aas_client.SubmodelElementRepositoryCreateDelete.create_submodel_element(submodel_id, self.sm_element_test)

        # Delete the submodel element
        await self.aas_client.SubmodelElementRepositoryCreateDelete.delete_submodel_element_by_id(submodel_id, element_id)

        # Try to retrieve the deleted submodel element to verify its deletion
        with self.assertRaises(aiohttp.client_exceptions.ClientResponseError):
            await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_element_by_id(submodel_id, element_id)
      
    async def test_delete_submodel_element_from_collection(self):
      submodel_id = "https://THU.de/RA_1_SM_Interaction"
      collection_id ="Endpoints"
      element_id = "HTTP_Broker_Endpoint"
      new_property = model.Property(
        id_short="HTTP_Broker_Endpoint",
        value_type=datatypes.String,
        category="VARIABLE",
        value="http://Place_Holder:8080",  
      )

      # Create the submodel element in the collection to ensure it exists
      await self.aas_client.SubmodelElementRepositoryCreateDelete.create_submodel_element_in_collection(submodel_id, collection_id, new_property)

      # Delete the submodel element from the collection
      await self.aas_client.SubmodelElementRepositoryCreateDelete.delete_submodel_element_from_collection(submodel_id, collection_id, element_id)

      # Try to retrieve the deleted submodel element to verify its deletion
      with self.assertRaises(aiohttp.client_exceptions.ClientResponseError):
          await self.aas_client.SubmodelElementRepositoryGetters.get_submodel_elements_from_collection(submodel_id, collection_id, element_id)


if __name__ == "__main__":
    unittest.main()