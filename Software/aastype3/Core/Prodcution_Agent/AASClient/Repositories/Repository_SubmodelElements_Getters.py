
from typing import Any, List
import aiohttp
from basyx.aas import model
import asyncio
from aastype3.Core.Prodcution_Agent.AASClient.Repositories.base.Repository_base_SubmodelElement import SubmodelElementRepositoryBase

class SubmodelElementRepositoryGetters(SubmodelElementRepositoryBase):
      """
            This class is first part of the Submodel Element ( only reading them either as
            values or as model.SubmodelElement , SubmodelCollection .... etc )
            - method naming: get_submodelName_submodelElementName().... this returns the model.SubmodelElement
            - method naming: getvalue_submodelName_submodelElementName().... this returns the value of the model.SubmodelElement
            - method naming start with invoke -> are method for invokation
      """
      def __init__(self, session: aiohttp.ClientSession,prefix:str=""):
            super().__init__(session)
            self.prefix = prefix

        
      def _inject_prefix_for_submodel(self,prefix:str,submodel_id:str):
            return submodel_id.replace("_PA_",f"{prefix}_PA_")
      def _inject_prefix_for_collection_id(self,prefix:str,collection_id:str):
            return collection_id.replace("_",f"{prefix}_",1)
      
      # region Execution Tracking Submodel Elements Getters

      async def get_Execution_Tracking_Submodel_Current_Node(self) -> model.Property:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            cs_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[0]
            return await self.get_submodel_element_by_id(op_sm_id, cs_sme_id)
      async def getvalue_Execution_Tracking_Submodel_Current_Node(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            cs_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[0]
            return await self.get_submodel_element_value_by_id(op_sm_id, cs_sme_id)
      
      async def get_Execution_Tracking_Submodel_Token_Position(self) -> model.Property:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            tp_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[1]
            return await self.get_submodel_element_by_id(op_sm_id, tp_sme_id)
      async def getvalue_Execution_Tracking_Submodel_Token_Position(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            tp_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[1]
            return await self.get_submodel_element_value_by_id(op_sm_id, tp_sme_id)
      
      async def get_Execution_Tracking_Submodel_TimeStamp(self) -> model.Property:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            ts_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[2]
            return await self.get_submodel_element_by_id(op_sm_id, ts_sme_id)
      async def getvalue_Execution_Tracking_Submodel_TimeStamp(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            ts_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[2]
            return await self.get_submodel_element_value_by_id(op_sm_id, ts_sme_id)
      
      async def get_Execution_Tracking_Submodel_Step_Status(self) -> model.Property:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            ss_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[3]
            return await self.get_submodel_element_by_id(op_sm_id, ss_sme_id)
      async def getvalue_Execution_Tracking_Submodel_Step_Status(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Execution_Tracking_Submodel_id())
            ss_sme_id = self.loader.get_Execution_Tracking_Submodel_elements()[3]
            return await self.get_submodel_element_value_by_id(op_sm_id, ss_sme_id)

# endregion

# region Interface and Endpoints Elements Getters
      async def get_Interface_Endpoints_Submodel_Endpoints_Collection(self) -> model.SubmodelElementCollection:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_id())
            ie_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            return await self.get_submodel_element_by_id(op_sm_id, ie_sme_id)
      
      async def getvalue_Interface_Endpoints_Submodel_Endpoints_Collection(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_id())
            ie_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            return await self.get_submodel_element_value_by_id(op_sm_id, ie_sme_id)
      
      async def get_Interface_Endpoints_Submodel_Drill_Command_Endpoint(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_id())
            ie_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            drill_cmd_ep_sme_id = self.loader.get_Interface_and_Endpoints_Submodel_elements()[1]
            return await self.get_submodel_elements_from_collection(op_sm_id, ie_sme_id, drill_cmd_ep_sme_id)
      async def getvalue_Interface_Endpoints_Submodel_Drill_Command_Endpoint(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_id())
            ie_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            drill_cmd_ep_sme_id = self.loader.get_Interface_and_Endpoints_Submodel_elements()[1]
            return await self.get_submodel_element_value_from_collection(op_sm_id, ie_sme_id, drill_cmd_ep_sme_id)
      
      async def get_Interface_Endpoints_Submodel_MoveXY_Command_Endpoint(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_id())
            ie_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            movexy_cmd_ep_sme_id = self.loader.get_Interface_and_Endpoints_Submodel_elements()[2]
            return await self.get_submodel_elements_from_collection(op_sm_id, ie_sme_id, movexy_cmd_ep_sme_id)
      async def getvalue_Interface_Endpoints_Submodel_MoveXY_Command_Endpoint(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_id())
            ie_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Interface_and_Endpoints_Submodel_elements()[0])
            movexy_cmd_ep_sme_id = self.loader.get_Interface_and_Endpoints_Submodel_elements()[2]
            return await self.get_submodel_element_value_from_collection(op_sm_id, ie_sme_id, movexy_cmd_ep_sme_id)

#endregion

# region Process Plan  Submodel Elements Getters
      
      async def get_Process_Plan_Submodel_Nodes_Collection(self) -> model.SubmodelElementCollection:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            nodes_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[0])
            return await self.get_submodel_element_by_id(op_sm_id, nodes_sme_id)
      async def getvalue_Process_Plan_Submodel_Nodes_Collection(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            nodes_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[0])
            return await self.get_submodel_element_value_by_id(op_sm_id, nodes_sme_id)
      
      async def get_Process_Plan_Submodel_Move_Node(self)-> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            nodes_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[0])
            move_node_sme_id = self.loader.get_Process_Plan_Submodel_elements()[1]
            return await self.get_submodel_elements_from_collection(op_sm_id, nodes_sme_id, move_node_sme_id)
      async def getvalue_Process_Plan_Submodel_Move_Node(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            nodes_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[0])
            move_node_sme_id = self.loader.get_Process_Plan_Submodel_elements()[1]
            return await self.get_submodel_element_value_from_collection(op_sm_id, nodes_sme_id, move_node_sme_id)
      
      async def get_Process_Plan_Submodel_Drill_Node(self) -> model.Submodel:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            nodes_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[0])
            drill_node_sme_id = self.loader.get_Process_Plan_Submodel_elements()[2]
            return await self.get_submodel_elements_from_collection(op_sm_id, nodes_sme_id, drill_node_sme_id)
      async def getvalue_Process_Plan_Submodel_Drill_Node(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            nodes_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[0])
            drill_node_sme_id = self.loader.get_Process_Plan_Submodel_elements()[2]
            return await self.get_submodel_element_value_from_collection(op_sm_id, nodes_sme_id, drill_node_sme_id)

      async def get_Process_Plan_Submodel_Edges_Collection(self) -> model.SubmodelElementCollection:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            edges_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[3])
            return await self.get_submodel_element_by_id(op_sm_id, edges_sme_id)
      async def getvalue_Process_Plan_Submodel_Edges_Collection(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            edges_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[3])
            return await self.get_submodel_element_value_by_id(op_sm_id, edges_sme_id)
      
      async def get_Process_Plan_Submodel_Edge1(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            edges_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[3])
            edge1_sme_id = self.loader.get_Process_Plan_Submodel_elements()[4]
            return await self.get_submodel_elements_from_collection(op_sm_id, edges_sme_id, edge1_sme_id) 
      async def getvalue_Process_Plan_Submodel_Edge1(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            edges_sme_id = self._inject_prefix_for_collection_id(self.prefix,self.loader.get_Process_Plan_Submodel_elements()[3])
            edge1_sme_id = self.loader.get_Process_Plan_Submodel_elements()[4]
            return await self.get_submodel_element_value_from_collection(op_sm_id, edges_sme_id, edge1_sme_id)
      
      async def get_Process_Plan_Submodel_Entry_Point(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            entry_point_sme_id = self.loader.get_Process_Plan_Submodel_elements()[5]
            return await self.get_submodel_element_by_id(op_sm_id, entry_point_sme_id)
      async def getvalue_Process_Plan_Submodel_Entry_Point(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            entry_point_sme_id = self.loader.get_Process_Plan_Submodel_elements()[5]
            return await self.get_submodel_element_value_by_id(op_sm_id, entry_point_sme_id)
      
      async def get_Process_Plan_Submodel_Exit_Point(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            exit_point_sme_id = self.loader.get_Process_Plan_Submodel_elements()[6]
            return await self.get_submodel_element_by_id(op_sm_id, exit_point_sme_id)
      async def getvalue_Process_Plan_Submodel_Exit_Point(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            exit_point_sme_id = self.loader.get_Process_Plan_Submodel_elements()[6]
            return await self.get_submodel_element_value_by_id(op_sm_id, exit_point_sme_id)
      
      async def get_Process_Plan_Submodel_Preconditions(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            preconditions_sme_id = self.loader.get_Process_Plan_Submodel_elements()[7]
            return await self.get_submodel_element_by_id(op_sm_id, preconditions_sme_id)
      async def getvalue_Process_Plan_Submodel_Preconditions(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            preconditions_sme_id = self.loader.get_Process_Plan_Submodel_elements()[7]
            return await self.get_submodel_element_value_by_id(op_sm_id, preconditions_sme_id)
      
      async def get_Process_Plan_Submodel_Postconditions(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            postconditions_sme_id = self.loader.get_Process_Plan_Submodel_elements()[8]
            return await self.get_submodel_element_by_id(op_sm_id, postconditions_sme_id)
      async def getvalue_Process_Plan_Submodel_Postconditions(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            postconditions_sme_id = self.loader.get_Process_Plan_Submodel_elements()[8]
            return await self.get_submodel_element_value_by_id(op_sm_id, postconditions_sme_id)
      
      async def get_Process_Plan_Submodel_Required_Capabilities(self) -> model.SubmodelElement:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            req_cap_sme_id = self.loader.get_Process_Plan_Submodel_elements()[9]
            return await self.get_submodel_element_by_id(op_sm_id, req_cap_sme_id)
      async def getvalue_Process_Plan_Submodel_Required_Capabilities(self) -> Any:
            op_sm_id = self._inject_prefix_for_submodel(self.prefix,self.loader.get_Process_Plan_Submodel_id())
            req_cap_sme_id = self.loader.get_Process_Plan_Submodel_elements()[9]
            return await self.get_submodel_element_value_by_id(op_sm_id, req_cap_sme_id)

# endregion



async def main():
      async with aiohttp.ClientSession() as session:
            repo = SubmodelElementRepositoryGetters(session,prefix="Production_1")
            result = await repo.getvalue_Process_Plan_Submodel_Drill_Node()
            print(result)


if __name__ == "__main__":
    asyncio.run(main()) 