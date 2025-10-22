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
    self.utils = Shell_utills()
    self.configs = self.utils.load_shell_config(self.utils.path)
    self.submodels_url = self.utils.get_submodels_endpoint(self.configs)
    self.root_url = self.utils.get_root_url(self.configs)
    self.full_url = f"{self.root_url}{self.submodels_url}"


    self.sm_operational_state = None
    self.sm_element_current_state = None
    self.sm_element_historical_data = None
    self.session = None
    


  def create_sm_current_state(self):
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
    
  def create_sm_historical_data(self):
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


  def create_sm(self):
    self.sm_operational_state = model.Submodel(
      id_ = "https://THU.de/RA_1_SM_Operational_State",
      id_short="RA_1_SM_Operational_State",
      description="Submodel for the Operational State of the Resource Agent",
    )
    self.sm_operational_state.submodel_element.add(self.sm_element_current_state)
    self.sm_operational_state.submodel_element.add(self.sm_element_historical_data)
