import asyncio
from aastype3.Core.Resource_Agent.Submodels_base.AAS_Resource_shell import AAS_Resource_shell
from aastype3.Core.Resource_Agent.Submodels_base.submodels.AAS_Submodel_Operational_State import AAS_Submodel_Operational_State
from aastype3.Core.Resource_Agent.Submodels_base.submodels.AAS_Submodel_Knowledge import AAS_Submodel_Knowledge
from aastype3.Core.Resource_Agent.Submodels_base.submodels.AAS_Submodel_Capablities import AAS_Submodel_Capabilities
from aastype3.Core.Resource_Agent.Submodels_base.submodels.AAS_Submodel_Interaction import AAS_Submodel_Interaction



async def create_and_publish_Resource_Agent_Shell():
  sm_operational_state = AAS_Submodel_Operational_State()
  sm_knowledge = AAS_Submodel_Knowledge()
  sm_capabilities = AAS_Submodel_Capabilities()
  sm_interaction = AAS_Submodel_Interaction()

  sm_list = [sm_operational_state.get_submodel(), sm_knowledge.get_submodel(), sm_capabilities.get_submodel(), sm_interaction.get_submodel()]
  shell = AAS_Resource_shell(sm_list)
  shell.set_shell()
  await shell.publish_shell()
  await sm_operational_state.publish_submodel()
  await sm_knowledge.publish_submodel()
  await sm_capabilities.publish_submodel()
  await sm_interaction.publish_submodel()


async def main():
  await create_and_publish_Resource_Agent_Shell()


if __name__ == "__main__":
  asyncio.run(main())