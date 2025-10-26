from typing import Any
import aiohttp
from basyx.aas import model
import asyncio
from aastype3.Core.Resource_Agent.AASClient.Repositories.base.Repository_base_SubmodelElement import SubmodelElementRepositoryBase


class SubmodelElementRepositoryUpdate(SubmodelElementRepositoryBase):
      """
            This class is second part of the Submodel Element ( only updating them either as
            values or as model.SubmodelElement , SubmodelCollection .... etc )
      """
      def __init__(self, session: aiohttp.ClientSession):
            super().__init__(session)
      
# region  Operational State Elements Update Methods
      async def update_Operational_State_Current_State(self, new_state: str) :
            op_sm_id = self.loader.get_Operational_State_submodel_id()
            cs_sme_id = self.loader.get_Operational_State_submodel_elements()[0]
            await  self.update_submodel_element_value_by_id(op_sm_id, cs_sme_id, new_state)


      async def update_Operational_State_Historical_Data(self, new_data: str) :
            op_sm_id = self.loader.get_Operational_State_submodel_id()
            hd_sme_id = self.loader.get_Operational_State_submodel_elements()[1]
            await  self.update_submodel_element_value_by_id(op_sm_id, hd_sme_id, new_data)
# endregion 

# region Knowledge Submodel Elements Update Methods
      async def update_Knowledge_MaxDepth_Collection_Value(self, new_value: str) :
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
            value_sme_id = self.loader.get_Knowledge_submodel_elements()[2]
            _id = f"{maxdepth_sme_id}.{value_sme_id}"
            await  self.update_submodel_element_value_from_collection(op_sm_id,rc_sme_id,_id, new_value)

      
      async def update_Knowledge_MaxDepth_Collection_Unit(self, new_unit: str) :
              op_sm_id = self.loader.get_Knowledge_submodel_id()
              rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
              maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
              unit_sme_id = self.loader.get_Knowledge_submodel_elements()[3]
              _id = f"{maxdepth_sme_id}.{unit_sme_id}"
              await  self.update_submodel_element_value_from_collection(op_sm_id,rc_sme_id,_id, new_unit)

      
      async def update_Knowledge_MaxDepth_Collection_Unit_short(self, new_unit_short: str) :
              op_sm_id = self.loader.get_Knowledge_submodel_id()
              rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
              maxdepth_sme_id = self.loader.get_Knowledge_submodel_elements()[1]
              unit_short_sme_id = self.loader.get_Knowledge_submodel_elements()[4]
              _id = f"{maxdepth_sme_id}.{unit_short_sme_id}"
              await  self.update_submodel_element_value_from_collection(op_sm_id,rc_sme_id,_id, new_unit_short)
     
     
      async def update_Knowledge_MinDepth_Collection_Value(self, new_value: str) :
            op_sm_id = self.loader.get_Knowledge_submodel_id()
            rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
            mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
            value_sme_id = self.loader.get_Knowledge_submodel_elements()[6]
            _id = f"{mindepth_sme_id}.{value_sme_id}"
            await  self.update_submodel_element_value_from_collection(op_sm_id,rc_sme_id,_id, new_value)

      async def update_Knowledge_MinDepth_Collection_Unit(self, new_unit: str) :
              op_sm_id = self.loader.get_Knowledge_submodel_id()
              rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
              mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
              unit_sme_id = self.loader.get_Knowledge_submodel_elements()[7]
              _id = f"{mindepth_sme_id}.{unit_sme_id}"
              await  self.update_submodel_element_value_from_collection(op_sm_id,rc_sme_id,_id, new_unit)
      

      async def update_Knowledge_MinDepth_Collection_Unit_short(self, new_unit_short: str) :
              op_sm_id = self.loader.get_Knowledge_submodel_id()
              rc_sme_id = self.loader.get_Knowledge_submodel_elements()[0]
              mindepth_sme_id = self.loader.get_Knowledge_submodel_elements()[5]
              unit_short_sme_id = self.loader.get_Knowledge_submodel_elements()[8]
              _id = f"{mindepth_sme_id}.{unit_short_sme_id}"
              await  self.update_submodel_element_value_from_collection(op_sm_id,rc_sme_id,_id, new_unit_short)

# endregion

# region Interaction Submodel Elements Update Methods
      async def update_Interaction_OPCUA_Endpoint(self, new_endpoint: str) :
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            opcua_ep_sme_id = self.loader.get_Interaction_submodel_elements()[1]
            await  self.update_submodel_element_value_from_collection(op_sm_id,ep_sme_id,opcua_ep_sme_id, new_endpoint)

      async def update_Interaction_MQTT_Endpoint(self, new_endpoint: str) :
            op_sm_id = self.loader.get_Interaction_submodel_id()
            ep_sme_id = self.loader.get_Interaction_submodel_elements()[0]
            mqtt_ep_sme_id = self.loader.get_Interaction_submodel_elements()[2]
            await  self.update_submodel_element_value_from_collection(op_sm_id,ep_sme_id,mqtt_ep_sme_id, new_endpoint)

#endregion


""" async def main():
  async with aiohttp.ClientSession() as session:
    repo = SubmodelElementRepositoryUpdate(session)
    await repo.update_Interaction_OPCUA_Endpoint("opc.tcp://new-endpoint:4840")
    await repo.update_Interaction_MQTT_Endpoint("mqtt://new-endpoint:1883")



if __name__ == "__main__":
      asyncio.run(main()) """