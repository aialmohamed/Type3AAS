from aastype3.Core.Datamodels.ResourceConfig_DataType import ResourceConfig
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_base import AASSubmodelBase


class AAS_Submodel_Capabilities(AASSubmodelBase):
    """
    Submodel for the Capabilities of the Resource Agent.
    Inherits from AASSubmodelBase.
    """
    def __init__(self, resource_config: ResourceConfig):
        self.resource_config = resource_config
        super().__init__()
    def create_submodel_elements(self):
        """
        Creates the submodel elements for the Capabilities submodel.
        """
        for name, oper in self.resource_config.capabilities.items():
            self.get_submodel_elements().append(oper)
        sm_em_skill_list = model.Property(
            id_short="Supported_Skills",
            value_type=datatypes.String,
            category="PARAMETER",
            description=[{"language": "en", "text": "List of supported skills by the Resource Agent"}],
            display_name=[{"language": "en", "text": "Supported Skills"}],
            value=",".join(name.lower() for name in self.resource_config.capabilities.keys())
        )
        self.get_submodel_elements().append(sm_em_skill_list)

    def create_submodel(self):
      self._submodel = model.Submodel(
      id_ = f"https://THU.de/{self.resource_config.resource_name}_RA_Capabilities",
      id_short=f"{self.resource_config.resource_name}_RA_Capabilities",
      description=[{"language": "en", "text": "Submodel for the Capabilities of the Resource Agent"}],
      display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Capabilities Submodel"}],
      
    )
      self.create_submodel_elements()
      for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)


""" sm_element_drill = model.Operation(
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

sm_element_movexy = model.Operation(
id_short="MoveXY_Capability",
    qualifier=[model.Qualifier(
    kind=model.QualifierKind.CONCEPT_QUALIFIER,
    type_="invocationDelegation",
    value_type=datatypes.String,
    value="http://host.docker.internal:8090/movexy_invocation"
)],
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
)  """