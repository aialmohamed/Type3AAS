import asyncio
from aastype3.Core.Submodels_base.Production_Base.Production_Shell import AAS_Production_Shell
from aastype3.Core.Submodels_base.Production_Base.submodels.AAS_Submodel_InterfaceEndpoints import AAS_Submodel_InterfaceEndpoints
from aastype3.Core.Submodels_base.Production_Base.submodels.AAS_Submodel_ProcessPlan import AAS_Submodel_ProcessPlan
from aastype3.Core.Submodels_base.Production_Base.submodels.AAS_Submodel_ExcutionTracking import AAS_Submodel_ExecutionTracking
from aastype3.Core.Submodels_base.Production_Base.ProductionInstances import ProductionMachineShell


async def main():
  production_machine_config = ProductionMachineShell().config
  sm_interface_endpoints= AAS_Submodel_InterfaceEndpoints(production_machine_config)
  sm_process_plan = AAS_Submodel_ProcessPlan(production_machine_config)
  sm_execution_tracking = AAS_Submodel_ExecutionTracking(production_machine_config)

  sm_list = [sm_interface_endpoints.get_submodel(), sm_process_plan.get_submodel(), sm_execution_tracking.get_submodel()]
  shell = AAS_Production_Shell(submodels=sm_list,production_config=production_machine_config)
  shell.set_shell()
  await shell.publish_shell()
  await sm_interface_endpoints.publish_submodel()
  await sm_process_plan.publish_submodel()
  await sm_execution_tracking.publish_submodel()

if __name__ == "__main__":
  asyncio.run(main())