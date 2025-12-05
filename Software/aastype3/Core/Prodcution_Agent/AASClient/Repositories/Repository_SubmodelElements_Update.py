
import aiohttp
from aastype3.Core.Prodcution_Agent.AASClient.Repositories.base.Repository_base_SubmodelElement import SubmodelElementRepositoryBase


class SubmodelElementRepositoryUpdate(SubmodelElementRepositoryBase):
      """
            This class is second part of the Submodel Element ( only updating them either as
            values or as model.SubmodelElement , SubmodelCollection .... etc )
      """
      def __init__(self, session: aiohttp.ClientSession, prefix: str = ""):
            super().__init__(session)
            self.prefix = prefix

      def _inject_prefix_for_submodel(self,prefix:str,submodel_id:str):
            return submodel_id.replace("_PA_",f"{prefix}_PA_")
      def _inject_prefix_for_collection_id(self,prefix:str,collection_id:str):
            return collection_id.replace("_",f"{prefix}_",1)
# region   Execution Tracking  Update Methods
      async def update_Execution_Tracking_Current_Node(self, new_node: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Execution_Tracking_Submodel_id())
            element = self.loader.get_Execution_Tracking_Submodel_elements()[0]
            await  self.update_submodel_element_value_by_id(submodel, element, new_node)
      async def update_Execution_Tracking_Token_Position(self, new_position: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Execution_Tracking_Submodel_id())
            element = self.loader.get_Execution_Tracking_Submodel_elements()[1]
            await  self.update_submodel_element_value_by_id(submodel, element, new_position)
      async def update_Execution_Tracking_TimeStamp(self, new_timestamp: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Execution_Tracking_Submodel_id())
            element = self.loader.get_Execution_Tracking_Submodel_elements()[2]
            await  self.update_submodel_element_value_by_id(submodel, element, new_timestamp)
      async def update_Execution_Tracking_Step_Status(self, new_status: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Execution_Tracking_Submodel_id())
            element = self.loader.get_Execution_Tracking_Submodel_elements()[3]
            await  self.update_submodel_element_value_by_id(submodel, element, new_status)
# endregion

# region Interaction and Endpoints  Submodel Elements Update Methods

      async def update_Interface_Endpoint_Collection_Drill_Command_API_Endpoint(self, new_value: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Interface_and_Endpoints_Submodel_id())
            collection  = self._inject_prefix_for_collection_id(self.prefix, self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            element  = self.loader.get_Interface_and_Endpoints_Submodel_elements()[1]
            await  self.update_submodel_element_value_from_collection(submodel,collection,element, new_value)
      async def update_Interface_Endpoint_Collection_Move_Command_API_Endpoint(self, new_value: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Interface_and_Endpoints_Submodel_id())
            collection  = self._inject_prefix_for_collection_id(self.prefix, self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            element  = self.loader.get_Interface_and_Endpoints_Submodel_elements()[2]
            await  self.update_submodel_element_value_from_collection(submodel,collection,element, new_value)
# endregion

# region Process Plan  Elements Update Methods
      async def update_Process_Plan_Move_Node(self, new_node: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            collection  = self._inject_prefix_for_collection_id(self.prefix, self.loader.get_Process_Plan_Submodel_elements()[0])
            element = self.loader.get_Process_Plan_Submodel_elements()[1]
            await  self.update_submodel_element_value_from_collection(submodel, collection, element, new_node)
      
      async def update_Process_Plan_Drill_Node(self, new_node: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            collection  = self._inject_prefix_for_collection_id(self.prefix, self.loader.get_Process_Plan_Submodel_elements()[0])
            element = self.loader.get_Process_Plan_Submodel_elements()[2]
            print(f"Updating Drill Node to {new_node} in Submodel {submodel}, Collection {collection}, Element {element}")
            await  self.update_submodel_element_value_from_collection(submodel, collection, element, new_node)
            
      async def update_Process_Plan_Edge1(self, new_edge: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            collection  = self._inject_prefix_for_collection_id(self.prefix, self.loader.get_Process_Plan_Submodel_elements()[0])
            element = self.loader.get_Process_Plan_Submodel_elements()[4]
            await  self.update_submodel_element_value_from_collection(submodel, collection, element, new_edge)
      async def update_Process_Plan_Entry_Point(self, new_entry_point: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            element = self.loader.get_Process_Plan_Submodel_elements()[5]
            await  self.update_submodel_element_value_by_id(submodel, element, new_entry_point)
      async def update_Process_Plan_Exit_Point(self, new_exit_point: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            element = self.loader.get_Process_Plan_Submodel_elements()[6]
            await  self.update_submodel_element_value_by_id(submodel, element, new_exit_point)
      async def update_Process_Plan_Preconditions(self, new_preconditions: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            element = self.loader.get_Process_Plan_Submodel_elements()[7]
            await  self.update_submodel_element_value_by_id(submodel, element, new_preconditions)
      async def update_Process_Plan_Postconditions(self, new_postconditions: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            element = self.loader.get_Process_Plan_Submodel_elements()[8]
            await  self.update_submodel_element_value_by_id(submodel, element, new_postconditions)
      async def update_Process_Plan_Required_Capabilities(self, new_required_capabilities: str) :
            submodel = self._inject_prefix_for_submodel(self.prefix, self.loader.get_Process_Plan_Submodel_id())
            element = self.loader.get_Process_Plan_Submodel_elements()[9]
            await  self.update_submodel_element_value_by_id(submodel, element, new_required_capabilities)
#endregion

""" 
async def main():
  async with aiohttp.ClientSession() as session:
    repo = SubmodelElementRepositoryUpdate(session, prefix="Production_1")
    await repo.update_Execution_Tracking_Current_Node("Move Node")


if __name__ == "__main__":
      asyncio.run(main()) """