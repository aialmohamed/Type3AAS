import asyncio
from aastype3.Core.Resource_Agent.Submodels.AAS_Resource_shell import AAS_Resource_shell
from aastype3.Core.Resource_Agent.Submodels.AAS_Submodel_Operational_State import AAS_SM_Operational_State
from aastype3.Core.Resource_Agent.Submodels.Utils import Shell_utills




async def main():
  shell = AAS_Resource_shell()
  shell.set_shell()
  #print(shell.serialize_shell())
  obj = shell.creating_object_store()
  #print(obj.get(shell.get_shell_id()))
  shell.creating_file()

if __name__ == "__main__":
  asyncio.run(main())