from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Submodels.submodels.AAS_Submodel_base import AASSubmodelBase


class AAS_Submodel_Capabilities(AASSubmodelBase):
    """
    Submodel for the Capabilities of the Resource Agent.
    Inherits from AASSubmodelBase.
    """
    def __init__(self):
        super().__init__()
    def create_submodel_elements(self):
        """
        Creates the submodel elements for the Capabilities submodel.
        """
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/Drill_Capability'
            ),)
        )
        self.sm_element_drill = model.Operation(
          id_short="Drill_Capability",
          qualifier=[model.Qualifier(
             kind=model.QualifierKind.CONCEPT_QUALIFIER,
             type_="invocationDelegation",
             value_type=datatypes.String,
             value="http://host.docker.internal:8090/drill_invocation"
          )],
          input_variable=[
              model.Property(
                  id_short="Drill_Depth",
                  value_type=datatypes.Double,
                  category="PARAMETER",
                  value=5.0,
                  description=[{"language": "en", "text": "Depth to drill"}],
                  display_name=[{"language": "en", "text": "Drill Depth"}]
              ),
              model.Property(
                  id_short="Drill_Speed",
                  value_type=datatypes.Double,
                  value=10.0,
                  category="PARAMETER",
                  description=[{"language": "en", "text": "Speed of the drill"}],
                  display_name=[{"language": "en", "text": "Drill Speed"}]
              )
          ],
          output_variable=[
              model.Property(
                  id_short="Drill_Result",
                  value_type=datatypes.String,
                  category="PARAMETER",
                  description=[{"language": "en", "text": "Result of the drilling operation"}],
                  display_name=[{"language": "en", "text": "Drill Result"}]
              )
          ]
        )
        
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/MoveXY_Capability'
            ),)
        )
        self.sm_element_movexy = model.Operation(
          id_short="MoveXY_Capability",
          input_variable=[
              model.Property(
                  id_short="Target_X",
                  value_type=datatypes.Double,
                  category="VARIABLE",
                  description=[{"language": "en", "text": "Target X coordinate"}],
                  display_name=[{"language": "en", "text": "Target X"}]
              ),
              model.Property(
                  id_short="Target_Y",
                  value_type=datatypes.Double,
                  category="VARIABLE",
                  description=[{"language": "en", "text": "Target Y coordinate"}],
                  display_name=[{"language": "en", "text": "Target Y"}]
              )
          ],
          output_variable=[
              model.Property(
                  id_short="Move_Result",
                  value_type=datatypes.String,
                  category="PARAMETER",
                  description=[{"language": "en", "text": "Result of the move operation"}],
                  display_name=[{"language": "en", "text": "Move Result"}]
              )
          ]
        )   
        self.get_submodel_elements().append(self.sm_element_drill)
        self.get_submodel_elements().append(self.sm_element_movexy)
    def create_submodel(self):
      self._submodel = model.Submodel(
      id_ = "https://THU.de/RA_1_SM_Capabilities",
      id_short="RA_1_SM_Capabilities",
      description=[{"language": "en", "text": "Submodel for the Capabilities of the Resource Agent"}],
      display_name=[{"language": "en", "text": "Capabilities Submodel"}],
      
    )
      self.create_submodel_elements()
      for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)
