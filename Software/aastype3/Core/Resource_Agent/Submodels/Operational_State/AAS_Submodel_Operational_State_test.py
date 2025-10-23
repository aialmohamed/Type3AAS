import pathlib
import aiohttp
from basyx.aas import model 
from basyx.aas.adapter.json import json_deserialization , json_serialization
import json ,urllib
import requests
from aastype3.Core.Resource_Agent.Submodels.AAS_Resource_shell import AAS_Resource_shell
from aastype3.Core.Resource_Agent.Submodels.Utils import Shell_utills
import basyx.aas.model.datatypes as datatypes

class AAS_SM_Operational_State:
  """
  Class to create the Submodel for the Operational State of the resource Agent.
  """
  def __init__(self):
    self.__utils = Shell_utills()
    self.__configs = self.__utils.load_shell_config(self.__utils.path)
    self.__submodels_url = self.__utils.get_submodels_endpoint(self.__configs)
    self.__root_url = self.__utils.get_root_url(self.__configs)
    self.__full_url = f"{self.__root_url.rstrip('/')}/{self.__submodels_url.strip('/')}"
    self.__post_header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    self.sm_operational_state = None
    self.sm_element_current_state = None
    self.sm_element_historical_data = None
    self.__obj_store_sm : model.DictObjectStore[model.Identifiable] = model.DictObjectStore()
    self.__create_sm()



  def __create_sm_current_state(self):
    """
     a new submodel element : 
    """
    semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/Current_Operational_State'
        ),)
    )
    self.sm_element_current_state = model.Property(
      id_short="Current_Operational_State",
      value_type=datatypes.String,
      value="Idle",  # Initial state could also be "Idle" , "Running" , "Error", "Done"
      semantic_id=semantic_reference
    )
    
  def __create_sm_historical_data(self):
    """
     a new submodel element : 
    """
    semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/Historical_Operational_Data'
        ),)
    )
    self.sm_element_historical_data = model.Property(
      id_short="Historical_Operational_Data",
      value_type=datatypes.String,
      value="No Data",  # Initial historical data
      semantic_id=semantic_reference
    )


  def __create_sm(self):
    
    self.sm_operational_state = model.Submodel(
      id_ = "https://THU.de/RA_1_SM_Operational_State",
      id_short="RA_1_SM_Operational_State",
      description=[{"language": "en", "text": "Submodel for the Operational State of the Resource Agent"}],
      display_name=[{"language": "en", "text": "Operational State Submodel"}],
      
    )
    self.__create_sm_current_state()
    self.__create_sm_historical_data()
    self.sm_operational_state.submodel_element.add(self.sm_element_current_state)
    self.sm_operational_state.submodel_element.add(self.sm_element_historical_data)


  def __create_object_store_sm(self):
    self.sm_operational_state.update()
    self.__obj_store_sm.add(self.sm_operational_state)
    return self.__obj_store_sm
  
  """
    def create_file_sm(self):
    file_path = pathlib.Path(__file__).parent / "shells" / "AAS_SM_Operational_State.json"
    json_serialization.write_aas_json_file(file_path,self.obj_store_sm)
  """
  async def publish_sm(self):
    self.__create_object_store_sm()
    data = json_serialization.object_store_to_json(self.__obj_store_sm,stripped=True, indent=4,encoder=json_serialization.AASToJsonEncoder)
    if isinstance(data, str):
        try:
            data_dict = json.loads(data)
        except json.JSONDecodeError:
            return {"error": "Failed to parse serialized AAS JSON"}
    else:
        data_dict = data
    if "submodels" in data_dict:
        if len(data_dict["submodels"]) > 0:
            submodel_data = data_dict["submodels"][0]
        else:
            return {"error": "No Submodel found"}
    else:
        submodel_data = data_dict
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=self.__full_url,
            json=submodel_data,
            headers=self.__post_header
        ) as response:
            if response.status == 200:
              print("Submodel updated successfully.")
              response = await response.json()
              return response
            elif response.status == 409:
               print("Submodel already exists. Updating...")
               response = await response.json()
               return response
            else:
              response_text = await response.text()
              return {"error": response_text, "status": response.status}