
from basyx.aas import model
from basyx.aas.adapter.json import json_serialization
from aastype3.Core.Resource_Agent.Submodels_base.Utils import Shell_utills
import json
import aiohttp
import pathlib


class AAS_Resource_shell:
  """
  Class to create the Shell for the resource Agent.
  """
  def __init__(self,submodels = [],test_aas:bool=False):
    self.shell_file_path = pathlib.Path(__file__).parent / "shells" / "AAS_Resource_shell.json"
    self.shell_information =  None
    self.id = None
    self.asset_shell = None

    self.utils = Shell_utills()
    self.configs = self.utils.load_shell_config(self.utils.path)
    self.root_url = self.utils.get_root_url(self.configs)
    self.shell_url = self.utils.get_shells_endpoint(self.configs)
    self.submodels = submodels
    self.submodels_refs = {model.ModelReference.from_referable(sm) for sm in submodels} 

    self.obj_store : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
    self._shell_id = ""
    self._shell_id_short = ""
    self._global_asset_id = ""
    self._check_test_aas(test_aas)
  
  def _check_test_aas(self,test_aas:bool):
    if test_aas:
      self._shell_id = "https://THU.de/ResourceAgent_1_Test_AAS"
      self._shell_id_short = "RA_1_Test_Shell"
      self._global_asset_id = "RA_1_Test_Global_Asset_ID"
    else:
      self._shell_id = "https://THU.de/ResourceAgent_1"
      self._shell_id_short = "RA_1_Shell"
      self._global_asset_id = "RA_1_Global_Asset_ID"
    return 
  
  def set_shell(self):
    self.id = self._shell_id
    self.asset_kind = model.AssetKind.INSTANCE
    self.global_asset_id = self._global_asset_id
    

    self.shell_information = model.AssetInformation(asset_kind=self.asset_kind,
                                                    global_asset_id=self.global_asset_id)
    self.asset_shell = model.AssetAdministrationShell( id_=self.id,
                                                      id_short=self._shell_id_short,
                                                      asset_information=self.shell_information,
                                                      display_name=[{"language": "en", "text": "Resource Agent Shell 1"}],
                                                      submodel=self.submodels_refs
                                                      )

    
  def get_shell_id(self):
    return self.asset_shell.id
  def get_shell_information(self):
    return self.asset_shell.asset_information
  def get_asset_kind(self):
    return self.asset_shell.asset_information.asset_kind
  def get_global_asset_id(self):
    return self.asset_shell.asset_information.global_asset_id
  

  def serialize_shell(self):
    json_string = json.dumps(self.asset_shell, cls=json_serialization.StrippedAASToJsonEncoder, indent=4)
    return json_string
  
  def creating_object_store(self):
    self.asset_shell.update()
    self.obj_store.add(self.asset_shell)
    return self.obj_store
  
  def creating_file(self):
    json_serialization.write_aas_json_file(self.shell_file_path,self.obj_store)


  def get_data_for_update(self):
    self.serialize_shell()
    self.creating_object_store()
    data = json_serialization.object_store_to_json(self.obj_store,stripped=True,encoder=json_serialization.AASToJsonEncoder)
    # Ensure we have a parsed dict — object_store_to_json may return a JSON string
    if isinstance(data, str):
        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError:
            return {"error": "Failed to parse serialized AAS JSON"}
    else:
        data_dict = data
    
    if "assetAdministrationShells" in data_dict:
        if len(data_dict["assetAdministrationShells"]) > 0:
            aas_data = data_dict["assetAdministrationShells"][0]
        else:
            return {"error": "No AAS found"}
    else:
        aas_data = data_dict
    return aas_data
  
  async def post_shell(self,data):
    url = f"{self.root_url.rstrip('/')}/{self.shell_url.strip('/')}"
    print("URL:", url)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=url,
            json=data,
            headers=headers
        ) as response:
            if response.status == 201:
              return await response.json()
            elif response.status == 409:
              print("AAS already exists.")
            else:
              response_text = await response.text()
              return {"error": response_text, "status": response.status}


  async def publish_shell(self):
    aas_data = self.get_data_for_update()

    aas_response = await self.post_shell(aas_data)
    if aas_response is None:
        print("AAS already exists, skipping POST.")
        return
    if "error" in aas_response:
        print(f"Error posting AAS: {aas_response['error']}")
        return
    print(f"AAS posted successfully: {aas_response}")

