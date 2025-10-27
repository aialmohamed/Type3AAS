
from typing import Any
import aiohttp
from basyx.aas import model
import asyncio
from aastype3.Core.Resource_Agent.AASClient.Repositories.base.Repository_base_SubmodelElement import SubmodelElementRepositoryBase

class SubmodelElementRepositoryGetters(SubmodelElementRepositoryBase):
      """
            This class is first part of the Submodel Element ( only reading them either as
            values or as model.SubmodelElement , SubmodelCollection .... etc )
            - method naming: get_submodelName_submodelElementName().... this returns the model.SubmodelElement
            - method naming: getvalue_submodelName_submodelElementName().... this returns the value of the model.SubmodelElement
            - method naming start with invoke -> are method for invokation
      """
      def __init__(self, session: aiohttp.ClientSession):
            super().__init__(session)

        # region Operational State Submodel Elements Getters


      async def get_Operational_State_Current_State(self) -> model.Property:
            op_sm_id = self.loader.get_Operational_State_submodel_id()
            cs_sme_id = self.loader.get_Operational_State_submodel_elements()[0]
            return await self.get_submodel_element_by_id(op_sm_id, cs_sme_id)


      async def get_Operational_State_Historical_States(self) -> model.Property:
            op_sm_id = self.loader.get_Operational_State_submodel_id()
            hs_sme_id = self.loader.get_Operational_State_submodel_elements()[1]
            return await self.get_submodel_element_by_id(op_sm_id, hs_sme_id)
      
      async def getvalue_Operational_State_Current_State(self) -> Any:
            op_sm_id = self.loader.get_Operational_State_submodel_id()
            cs_sme_id = self.loader.get_Operational_State_submodel_elements()[0]
            return await self.get_submodel_element_value_by_id(op_sm_id, cs_sme_id)
      

      async def getvalue_Operational_State_Historical_States(self) -> Any:
            op_sm_id = self.loader.get_Operational_State_submodel_id()
            hs_sme_id = self.loader.get_Operational_State_submodel_elements()[1]
            return await self.get_submodel_element_value_by_id(op_sm_id, hs_sme_id)


# endregion

# region Knowledge Submodel Elements Getters
      async def get_Knowledge_ResourceConstraints_Collection(self) -> model.SubmodelElementCollection:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            return await self.get_submodel_element_by_id(op_sm_id, rc_sme_id)
      

      async def getvalue_Knowledge_ResourceConstraints_Collection(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            return await self.get_submodel_element_value_by_id(op_sm_id, rc_sme_id)


      async def get_Knowledge_MaxDepth_Collection(self) -> model.SubmodelElementCollection:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, maxdepth_sme_id)
      

      async def getvalue_Knowledge_MaxDepth_Collection(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            return await self.get_submodel_element_value_by_id(op_sm_id, f"{rc_sme_id}.{maxdepth_sme_id}")


      async def get_Knowledge_MaxDepth_Collection_Value(self) -> model.Property:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            value_sme_id = self.loader.get_Knowledge_submodel_elements()[2]
            _id = f"{maxdepth_sme_id}.{value_sme_id}"
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, _id)
      

      async def getvalue_Knowledge_MaxDepth_Collection_Value(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            value_sme_id = self.loader.get_Knowledge_submodel_elements()[2]
            _id = f"{rc_sme_id}.{maxdepth_sme_id}.{value_sme_id}"
            return await self.get_submodel_element_value_by_id(op_sm_id, _id)
     
     
      async def get_Knowledge_MaxDepth_Collection_Unit(self) -> model.Property:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[3]
            _id = f"{maxdepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, _id)
      

      async def getvalue_Knowledge_MaxDepth_Collection_Unit(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[3]
            _id = f"{rc_sme_id}.{maxdepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_element_value_by_id(op_sm_id, _id)

      async def getvalue_Knowledge_MaxDepth_Collection_Unit_short(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[4]
            _id = f"{rc_sme_id}.{maxdepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_element_value_by_id(op_sm_id, _id)
      
      
      async def get_Knowledge_MaxDepth_Collection_Unit_short(self) -> model.Property:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[4]
            _id = f"{maxdepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, _id)
      

      async def getvalue_Knowledge_MinDepth_Collection(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            return await self.get_submodel_element_value_by_id(op_sm_id, f"{rc_sme_id}.{mindepth_sme_id}")

      async def get_Knowledge_MinDepth_Collection(self) -> model.SubmodelElementCollection:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, mindepth_sme_id)


      async def getvalue_Knowledge_MinDepth_Collection_Value(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            value_sme_id = self.loader.get_Knowledge_submodel_elements()[6]
            _id = f"{rc_sme_id}.{mindepth_sme_id}.{value_sme_id}"
            return await self.get_submodel_element_value_by_id(op_sm_id, _id)

      async def get_Knowledge_MinDepth_Collection_Value(self) -> model.Property:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            value_sme_id = self.loader.get_Knowledge_submodel_elements()[6]
            _id = f"{mindepth_sme_id}.{value_sme_id}"
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, _id)
      
      async def getvalue_Knowledge_MinDepth_Collection_Unit(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[7]
            _id = f"{rc_sme_id}.{mindepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_element_value_by_id(op_sm_id, _id)


      async def get_Knowledge_MinDepth_Collection_Unit(self) -> model.Property:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[7]
            _id = f"{mindepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, _id)

      async def getvalue_Knowledge_MinDepth_Collection_Unit_short(self) -> Any:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[8]
            _id = f"{rc_sme_id}.{mindepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_element_value_by_id(op_sm_id, _id)
      
      async def get_Knowledge_MinDepth_Collection_Unit_short(self) -> model.Property:
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            unit_sme_id = self.loader.get_Knowledge_submodel_elements()[8]
            _id = f"{mindepth_sme_id}.{unit_sme_id}"
            return await self.get_submodel_elements_from_collection(op_sm_id, rc_sme_id, _id)
      
#endregion

# region Interaction Submodel Elements Getters
      async def get_Interaction_Endpoints_Collection(self) -> model.SubmodelElementCollection:
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            return await self.get_submodel_element_by_id(op_sm_id, ep_sme_id)

      async def getvalue_Interaction_Endpoints_Collection(self) -> Any:
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            return await self.get_submodel_element_value_by_id(op_sm_id, ep_sme_id)

      async def get_Interaction_OPCUA_Endpoint(self) -> model.SubmodelElement:
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            opcua_ep_sme_id = self.loader.get_Interaction_submodel_elements()[1]
            return await self.get_submodel_elements_from_collection(op_sm_id, ep_sme_id, opcua_ep_sme_id)
      

      async def getvalue_Interaction_OPCUA_Endpoint(self) -> model.Property:
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            opcua_ep_sme_id = self.loader.get_Interaction_submodel_elements()[1]
            return await self.get_submodel_elements_from_collection(op_sm_id, ep_sme_id, opcua_ep_sme_id)
      
      async def get_Interaction_MQTT_Endpoint(self) -> model.SubmodelElement:
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            mqtt_ep_sme_id = self.loader.get_Interaction_submodel_elements()[2]
            return await self.get_submodel_elements_from_collection(op_sm_id, ep_sme_id, mqtt_ep_sme_id)

      async def getvalue_Interaction_MQTT_Endpoint(self) -> model.Property:
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            mqtt_ep_sme_id = self.loader.get_Interaction_submodel_elements()[2]
            return await self.get_submodel_element_value_from_collection(op_sm_id, ep_sme_id, mqtt_ep_sme_id)
#endregion

# region Capabilities Submodel Elements Getters
      async def get_Capabilities_Drill_Capability(self) -> model.Operation:
            cap_sm_id = self.loader.get_Capabilities_submodel_id()
            drill_cap_sme_id = self.loader.get_Capabilities_submodel_elements()[0]
            return await self.get_submodel_element_by_id(cap_sm_id, drill_cap_sme_id)

      async def invoke_drill(self,depth:float, speed:float,async_flage:str="false") -> Any:
            cap_sm_id = self.loader.get_Capabilities_submodel_id()
            drill_cap_sme_id = self.loader.get_Capabilities_submodel_elements()[0]
            payload = await self._invoke_operation_payload(cap_sm_id, drill_cap_sme_id, {"Drill_Depth": depth, "Drill_Speed": speed})
            result = await self.invoke_operation_on_submodel_element(cap_sm_id, drill_cap_sme_id, payload, Async_flag=async_flage)
            return result

      async def get_Capabilities_MoveXY_Capability(self) -> model.Operation:
            cap_sm_id = self.loader.get_Capabilities_submodel_id()
            move_xy_cap_sme_id = self.loader.get_Capabilities_submodel_elements()[1]
            return await self.get_submodel_element_by_id(cap_sm_id, move_xy_cap_sme_id)


      async def invoke_move_xy(self,x:float, y:float,async_flage:str="false") -> Any:
            cap_sm_id = self.loader.get_Capabilities_submodel_id()
            move_xy_cap_sme_id = self.loader.get_Capabilities_submodel_elements()[1]
            payload = await self._invoke_operation_payload(cap_sm_id, move_xy_cap_sme_id, {"Target_X": x, "Target_Y": y})
            result = await self.invoke_operation_on_submodel_element(cap_sm_id, move_xy_cap_sme_id, payload, Async_flag=async_flage)
            return result

# endregion



""" async def main():
    async with aiohttp.ClientSession() as session:
        repo = SubmodelElementRepositoryGetters(session)
        result = await repo.invoke_drill(30.0, 5.0, async_flage="false")
        print(result)


if __name__ == "__main__":
    asyncio.run(main()) """