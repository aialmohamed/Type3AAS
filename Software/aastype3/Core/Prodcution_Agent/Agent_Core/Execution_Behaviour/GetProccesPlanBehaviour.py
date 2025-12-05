import asyncio
from spade.behaviour import OneShotBehaviour

class GetProccesPlanBehaviour(OneShotBehaviour):
    async def run(self):
        print("Getting process plan from production AAS")
        process_nodes,process_edges,entry_point,exit_point,required_capabilities= await asyncio.gather(
        self.agent.production_client.SubmodelElementRepositoryGetters.getvalue_Process_Plan_Submodel_Nodes_Collection(),
        self.agent.production_client.SubmodelElementRepositoryGetters.getvalue_Process_Plan_Submodel_Edges_Collection(),
        self.agent.production_client.SubmodelElementRepositoryGetters.getvalue_Process_Plan_Submodel_Entry_Point(),
        self.agent.production_client.SubmodelElementRepositoryGetters.getvalue_Process_Plan_Submodel_Exit_Point(),
        self.agent.production_client.SubmodelElementRepositoryGetters.getvalue_Process_Plan_Submodel_Required_Capabilities(),
        return_exceptions=True
        )