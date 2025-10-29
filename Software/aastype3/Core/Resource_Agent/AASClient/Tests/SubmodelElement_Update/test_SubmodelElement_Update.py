from typing import Any
import unittest

from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
import aiohttp
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes
import json, ast

class Test_SubmodelElementUpdate(unittest.IsolatedAsyncioTestCase):
    
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
    
    async def test_update_Operational_State_Current_State(self):
        new_state = "Running"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Operational_State_Current_State(new_state)
        # retrieve the updated value to verify
        retrieved_state = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Current_State()
        self.assertEqual(retrieved_state, new_state)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Operational_State_Current_State("Idle")
    
    async def test_update_Operational_State_Historical_Data(self):
        new_data = "Test Data Entry"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Operational_State_Historical_Data(new_data)
        # retrieve the updated value to verify
        retrieved_data = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Historical_States()
        self.assertEqual(retrieved_data, new_data)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Operational_State_Historical_Data("No Data")

    async def test_update_Knowledge_MaxDepth_Collection_Value(self):
        new_value = "5000"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MaxDepth_Collection_Value(new_value)
        # retrieve the updated value to verify
        retrieved_value = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MaxDepth_Collection_Value()
        self.assertEqual(retrieved_value, new_value)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MaxDepth_Collection_Value("20.0")
    
    async def test_update_Knowledge_MaxDepth_Collection_Unit(self):
        new_unit = "meters"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MaxDepth_Collection_Unit(new_unit)
        # retrieve the updated value to verify
        retrieved_unit = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MaxDepth_Collection_Unit()
        self.assertEqual(retrieved_unit, new_unit)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MaxDepth_Collection_Unit("centimeters")
    
    async def test_update_Knowledge_MaxDepth_Collection_Unit_short(self):
        new_unit_short = "m"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MaxDepth_Collection_Unit_short(new_unit_short)
        # retrieve the updated value to verify
        retrieved_unit_short = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MaxDepth_Collection_Unit_short()
        self.assertEqual(retrieved_unit_short, new_unit_short)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MaxDepth_Collection_Unit_short("cm")
    
    async def test_update_Knowledge_MinDepth_Collection_Value(self):
        new_value = "1000"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MinDepth_Collection_Value(new_value)
        # retrieve the updated value to verify
        retrieved_value = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MinDepth_Collection_Value()
        self.assertEqual(retrieved_value, new_value)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MinDepth_Collection_Value("5.0")
    
    async def test_update_Knowledge_MinDepth_Collection_Unit(self):
        new_unit = "meters"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MinDepth_Collection_Unit(new_unit)
        # retrieve the updated value to verify
        retrieved_unit = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MinDepth_Collection_Unit()
        self.assertEqual(retrieved_unit, new_unit)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MinDepth_Collection_Unit("centimeters")
    
    async def test_update_Knowledge_MinDepth_Collection_Unit_short(self):
        new_unit_short = "m"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MinDepth_Collection_Unit_short(new_unit_short)
        # retrieve the updated value to verify
        retrieved_unit_short = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MinDepth_Collection_Unit_short()
        self.assertEqual(retrieved_unit_short, new_unit_short)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Knowledge_MinDepth_Collection_Unit_short("cm")

    async def test_update_Interaction_OPCUA_Endpoint(self):
        new_endpoint = "opc.tcp://new-endpoint:4840"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Interaction_OPCUA_Endpoint(new_endpoint)
        # retrieve the updated value to verify
        retrieved_endpoint = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Interaction_OPCUA_Endpoint()
        self.assertEqual(retrieved_endpoint, new_endpoint)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Interaction_OPCUA_Endpoint("opc.tcp://Place_Holder:4840/freeopcua/server/")

    async def test_update_Interaction_MQTT_Endpoint(self):
        new_endpoint = "mqtt://new-endpoint:1883"
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Interaction_MQTT_Endpoint(new_endpoint)
        # retrieve the updated value to verify
        retrieved_endpoint = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Interaction_MQTT_Endpoint()
        self.assertEqual(retrieved_endpoint, new_endpoint)
        # restore the old value to not affect other tests
        await self.aas_client.SubmodelElementRepositoryUpdate.update_Interaction_MQTT_Endpoint("mqtt://Place_Holder:1883")

if __name__ == "__main__":
    unittest.main()