from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Submodels.submodels.AAS_Submodel_base import AASSubmodelBase



class AAS_Submodel_Operational_State(AASSubmodelBase):
    """
    Submodel for the Operational State of the Resource Agent.
    Inherits from AASSubmodelBase.
    """
    def __init__(self):
        super().__init__()
    def create_submodel_elements(self):
        """
        Creates the submodel elements for the Operational State submodel.
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
          category="VARIABLE",
          value="Idle",  # Initial state could also be "Idle" , "Running" , "Error", "Done"
          semantic_id=semantic_reference
        )
        
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/Historical_Operational_Data'
            ),)
        )
        self.sm_element_historical_data = model.Property(
          id_short="Historical_Operational_Data",
          value_type=datatypes.String,
          category="PARAMETER",
          value="No Data",  # Initial historical data
          semantic_id=semantic_reference
        )
        self.get_submodel_elements().append(self.sm_element_current_state)
        self.get_submodel_elements().append(self.sm_element_historical_data)
    def create_submodel(self):
      self._submodel = model.Submodel(
      id_ = "https://THU.de/RA_1_SM_Operational_State",
      id_short="RA_1_SM_Operational_State",
      description=[{"language": "en", "text": "Submodel for the Operational State of the Resource Agent"}],
      display_name=[{"language": "en", "text": "Operational State Submodel"}],
      
    )
      self.create_submodel_elements()
      for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)