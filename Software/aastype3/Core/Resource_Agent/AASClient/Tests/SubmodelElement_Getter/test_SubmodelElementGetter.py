from typing import Any
import unittest

from aastype3.Core.Resource_Agent.AASClient.Client.ResourceAASClient import ResourceAASClient
import aiohttp
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes
import json, ast

class Test_SubmodelElementGetter(unittest.IsolatedAsyncioTestCase):
    
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

    async def test_get_Operational_State_Current_State(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Operational_State_Current_State()
        self.assertIsInstance(sm, model.SubmodelElement)
        self.assertEqual(sm.id_short, "Current_Operational_State")
    
    async def test_get_Operational_State_Historical_States(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Operational_State_Historical_States()
        self.assertIsInstance(sm, model.SubmodelElement)
        self.assertEqual(sm.id_short, "Historical_Operational_Data")
    
    async def test_getvalue_Operational_State_Current_State(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Current_State()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "Idle")
    
    async def test_getvalue_Operational_State_Historical_States(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Operational_State_Historical_States()
        self.assertIsInstance(val, str)
        self.assertIn("No Data", val)  
    
    async def test_get_Knowledge_ResourceConstraints_Collection(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_ResourceConstraints_Collection()
        self.assertIsInstance(sm, model.SubmodelElementCollection)
        self.assertEqual(sm.id_short, "Resource_Constraints")
    
    
    async def test_getvalue_Knowledge_ResourceConstraints_Collection(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_ResourceConstraints_Collection()
        #print(val)
        if isinstance(val, str):
   
          try:
              parsed = json.loads(val)
          except Exception:
              parsed = ast.literal_eval(val)
        else:
          parsed = val

        self.assertIsInstance(parsed,dict )
        expected = {
            "MaxDepth": {"MaxDepthValue": "20.0", "MaxDepthUnit": "centimeters", "MaxDepthUnitShort": "cm"},
            "MinDepth": {"MinDepthValue": "1.0", "MinDepthUnit": "centimeters", "MinDepthUnitShort": "cm"}
        }
        self.assertDictEqual(expected, parsed)
    
    async def test_get_Knowledge_MaxDepth_Collection(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MaxDepth_Collection()
        self.assertIsInstance(sm, model.SubmodelElementCollection)
        self.assertEqual(sm.id_short, "MaxDepth")
    
    async def test_getvalue_Knowledge_MaxDepth_Collection(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MaxDepth_Collection()
        #print(val)
        if isinstance(val, str):
   
          try:
              parsed = json.loads(val)
          except Exception:
              parsed = ast.literal_eval(val)
        else:
          parsed = val

        self.assertIsInstance(parsed,dict )
        expected = {
            "MaxDepthValue": "20.0",
            "MaxDepthUnit": "centimeters",
            "MaxDepthUnitShort": "cm"
        }
        self.assertDictEqual(expected, parsed)

    async def test_get_Knowledge_MaxDepth_Collection_Value(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MaxDepth_Collection_Value()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "MaxDepthValue")
    
    async def test_getvalue_Knowledge_MaxDepth_Collection_Value(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MaxDepth_Collection_Value()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "20.0")
      
    async def test_get_Knowledge_MaxDepth_Collection_Unit(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MaxDepth_Collection_Unit()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "MaxDepthUnit")

    async def test_getvalue_Knowledge_MaxDepth_Collection_Unit(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MaxDepth_Collection_Unit()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "centimeters")
    
    async def test_get_Knowledge_MaxDepth_Collection_Unit_short(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MaxDepth_Collection_Unit_short()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "MaxDepthUnitShort")
    
    async def test_getvalue_Knowledge_MaxDepth_Collection_Unit_short(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MaxDepth_Collection_Unit_short()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "cm")
    
    async def test_get_Knowledge_MinDepth_Collection(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MinDepth_Collection()
        self.assertIsInstance(sm, model.SubmodelElementCollection)
        self.assertEqual(sm.id_short, "MinDepth")
    
    async def test_getvalue_Knowledge_MinDepth_Collection(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MinDepth_Collection()
        #print(val)
        if isinstance(val, str):
   
          try:
              parsed = json.loads(val)
          except Exception:
              parsed = ast.literal_eval(val)
        else:
          parsed = val

        self.assertIsInstance(parsed,dict )
        expected = {
            "MinDepthValue": "1.0",
            "MinDepthUnit": "centimeters",
            "MinDepthUnitShort": "cm"
        }
        self.assertDictEqual(expected, parsed)
    async def test_get_Knowledge_MinDepth_Collection_Value(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MinDepth_Collection_Value()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "MinDepthValue")
    async def test_getvalue_Knowledge_MinDepth_Collection_Value(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MinDepth_Collection_Value()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "1.0")
    async def test_get_Knowledge_MinDepth_Collection_Unit(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MinDepth_Collection_Unit()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "MinDepthUnit")
    async def test_getvalue_Knowledge_MinDepth_Collection_Unit(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MinDepth_Collection_Unit()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "centimeters")
    async def test_get_Knowledge_MinDepth_Collection_Unit_short(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Knowledge_MinDepth_Collection_Unit_short()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "MinDepthUnitShort")
    async def test_getvalue_Knowledge_MinDepth_Collection_Unit_short(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Knowledge_MinDepth_Collection_Unit_short()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "cm")
    async def test_get_Interaction_Endpoints_Collection(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Interaction_Endpoints_Collection()
        self.assertIsInstance(sm, model.SubmodelElementCollection)
        self.assertEqual(sm.id_short, "Endpoints")
    
    async def test_getvalue_Interaction_Endpoints_Collection(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Interaction_Endpoints_Collection()
        #print(val) 
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
            except Exception:
                parsed = ast.literal_eval(val)
        else:
            parsed = val

        self.assertIsInstance(parsed, dict)
        expected = {'Machine_OPCUA_Endpoint': 'opc.tcp://Place_Holder:4840/freeopcua/server/', 'MQTT_Broker_Endpoint': 'mqtt://Place_Holder:1883'}
        self.assertDictEqual(expected, parsed)
    
    async def test_get_Interaction_Machine_OPCUA_Endpoint(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Interaction_OPCUA_Endpoint()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "Machine_OPCUA_Endpoint")
    
    async def test_getvalue_Interaction_Machine_OPCUA_Endpoint(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Interaction_OPCUA_Endpoint()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "opc.tcp://Place_Holder:4840/freeopcua/server/")
    
    async def test_get_Interaction_MQTT_Endpoint(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Interaction_MQTT_Endpoint()
        self.assertIsInstance(sm, model.Property)
        self.assertEqual(sm.id_short, "MQTT_Broker_Endpoint")

    async def test_getvalue_Interaction_MQTT_Endpoint(self):
        val = await self.aas_client.SubmodelElementRepositoryGetters.getvalue_Interaction_MQTT_Endpoint()
        self.assertIsInstance(val, str)
        self.assertEqual(val, "mqtt://Place_Holder:1883")

    async def test_get_Capabilities_Drill_Capability(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Capabilities_Drill_Capability()
        self.assertIsInstance(sm, model.Operation)
        self.assertEqual(sm.id_short, "Drill_Capability")
    
    async def test_get_Capabilities_MoveXY_Capability(self):
        sm = await self.aas_client.SubmodelElementRepositoryGetters.get_Capabilities_MoveXY_Capability()
        self.assertIsInstance(sm, model.Operation)
        self.assertEqual(sm.id_short, "MoveXY_Capability")
    
    async def test_invoke_drill(self):
        depth = 10.0
        result = await self.aas_client.SubmodelElementRepositoryGetters.invoke_drill(depth=depth, speed=5.0)
        self.assertIsInstance(result, str)
        self.assertEqual(float(result),depth*depth)
    
    async def test_invoke_movexy(self):
        x = 5.0
        y = 7.0
        result = await self.aas_client.SubmodelElementRepositoryGetters.invoke_move_xy(x=x, y=y)
        self.assertIsInstance(result, dict)
    



if __name__ == "__main__":
    unittest.main()