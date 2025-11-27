import asyncio
from aastype3.Core.Submodels_base.Resource_Base.AAS_Resource_shell import AAS_Resource_shell
from aastype3.Core.Submodels_base.Resource_Base.DrillMachines import DrillMachineShell, SecondDrillMachineShell
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_Operational_State import AAS_Submodel_Operational_State
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_Knowledge import AAS_Submodel_Knowledge
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_Capablities import AAS_Submodel_Capabilities
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_Interaction import AAS_Submodel_Interaction



async def create_and_publish_drill_1():

  drill_machine_config = DrillMachineShell().config
  sm_op_state= AAS_Submodel_Operational_State(drill_machine_config)

  sm_knowledge = AAS_Submodel_Knowledge(drill_machine_config)
  sm_capabilities = AAS_Submodel_Capabilities(drill_machine_config)
  sm_interaction = AAS_Submodel_Interaction(drill_machine_config)

  sm_list = [sm_op_state.get_submodel(), sm_knowledge.get_submodel(), sm_capabilities.get_submodel(), sm_interaction.get_submodel()]
  shell = AAS_Resource_shell(submodels=sm_list,resource_config=drill_machine_config)
  shell.set_shell()
  await shell.publish_shell()
  await sm_op_state.publish_submodel()
  await sm_knowledge.publish_submodel()
  await sm_capabilities.publish_submodel()
  await sm_interaction.publish_submodel()

async def create_and_publish_drill_2():

  drill_machine_config = SecondDrillMachineShell().config
  sm_op_state= AAS_Submodel_Operational_State(drill_machine_config)

  sm_knowledge = AAS_Submodel_Knowledge(drill_machine_config)
  sm_capabilities = AAS_Submodel_Capabilities(drill_machine_config)
  sm_interaction = AAS_Submodel_Interaction(drill_machine_config)

  sm_list = [sm_op_state.get_submodel(), sm_knowledge.get_submodel(), sm_capabilities.get_submodel(), sm_interaction.get_submodel()]
  shell = AAS_Resource_shell(submodels=sm_list,resource_config=drill_machine_config)
  shell.set_shell()
  await shell.publish_shell()
  await sm_op_state.publish_submodel()
  await sm_knowledge.publish_submodel()
  await sm_capabilities.publish_submodel()
  await sm_interaction.publish_submodel()


async def main():
  await create_and_publish_drill_1()
  await create_and_publish_drill_2()


if __name__ == "__main__":
  asyncio.run(main())