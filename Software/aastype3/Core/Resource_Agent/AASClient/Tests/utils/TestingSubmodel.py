
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Submodels_base.submodels.AAS_Submodel_base import AASSubmodelBase


class Testing_Submodel(AASSubmodelBase):
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
            value='https://THU.de/Properties/Testing_Property'
            ),)
        )
        self.sm_element_testproperty = model.Property(
          id_short="Testing_Property",
          value_type=datatypes.String,
          category="VARIABLE",
          value="Test Value",  # Initial state could also be "Idle" , "Running" , "Error", "Done"
          semantic_id=semantic_reference
        )

        self.get_submodel_elements().append(self.sm_element_testproperty)

    def create_submodel(self):
      self._submodel = model.Submodel(
      id_ = "https://THU.de/RA_1_SM_Testing",
      id_short="RA_1_SM_Testing",
      description=[{"language": "en", "text": "Submodel for Testing of the Resource Agent"}],
      display_name=[{"language": "en", "text": "Testing Submodel"}],

    )
      self.create_submodel_elements()
      for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)