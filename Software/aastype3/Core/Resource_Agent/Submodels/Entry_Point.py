import asyncio
from aastype3.Core.Resource_Agent.Submodels.AAS_Resource_shell import AAS_Resource_shell
from aastype3.Core.Resource_Agent.Submodels.Operational_State.AAS_Submodel_Operational_State_test import AAS_SM_Operational_State
from aastype3.Core.Resource_Agent.Submodels.Utils import Shell_utills




async def main():
  sm_operational_state = AAS_SM_Operational_State()



  sm_list = [sm_operational_state.sm_operational_state]
  shell = AAS_Resource_shell(sm_list)
  shell.set_shell()
  #await shell.update_shell()
  await sm_operational_state.publish_sm()
if __name__ == "__main__":
  asyncio.run(main())