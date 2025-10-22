
from basyx.aas import model
from basyx.aas.adapter.json import json_deserialization , json_serialization
from aastype3.Core.Resource_Agent.Submodels.Utils import Shell_utills
import json
import requests
import aiohttp
import pathlib
import os
class AAS_Resource_shell:
  """
  Class to create the Shell for the resource Agent.
  """
  def __init__(self):

    self.shell_information =  None
    self.id = None
    self.asset_shell = None

    self.utils = Shell_utills()
    self.configs = self.utils.load_shell_config(self.utils.path)
    self.root_url = self.utils.get_root_url(self.configs)
    self.shell_url = self.utils.get_shells_endpoint(self.configs)

    self.obj_store : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()

  def set_shell(self):
    self.id = "https://THU.de/RA_1_Shell"
    self.asset_kind = model.AssetKind.INSTANCE
    self.global_asset_id = "https://THU.de/ResourceAgent_1"
    

    self.shell_information = model.AssetInformation(asset_kind=self.asset_kind,
                                                    global_asset_id=self.global_asset_id)
    self.asset_shell = model.AssetAdministrationShell( id_=self.id,
                                                      asset_information=self.shell_information,
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
    json_string = json.dumps(self.asset_shell, cls=json_serialization.AASToJsonEncoder, indent=4)
    return json_string
  
  def creating_object_store(self):
    self.asset_shell.update()
    self.obj_store.add(self.asset_shell)
    return self.obj_store
  
  
  def creating_file(self):
    file_path = pathlib.Path(__file__).parent / "AAS_Resource_shell.json"
    json_serialization.write_aas_json_file(file_path,self.obj_store)