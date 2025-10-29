from aastype3.Core.Resource_Agent.Datamodels.ResourceConfig_DataType import ResourceConfig
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Submodels_base.submodels.AAS_Submodel_base import AASSubmodelBase


class AAS_Submodel_Knowledge(AASSubmodelBase):
    """
    Submodel for the Knowledge of the Resource Agent.
    Inherits from AASSubmodelBase.
    """
    def __init__(self, resource_config: ResourceConfig):
        self.resource_config = resource_config
        super().__init__()
    def create_submodel_elements(self):
        """
        Creates the submodel elements for the Knowledge submodel.
        """
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value=f"https://THU.de/Properties/{self.resource_config.resource_name}_Resource_Constraints"
        ),)
        )
        self.sm_element_resource_constraints = model.SubmodelElementCollection(
          id_short=f"{self.resource_config.resource_name}_Resource_Constraints",
          category="VARIABLE",
          semantic_id=semantic_reference,
          display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Resource Constraints"}],
          description=[{"language": "en", "text": "Collection of Resource Constraints"}],
          value=[
              # Use a SubmodelElementCollection for the "MaxDepth" grouping because the contained Properties
              # have mixed value types (Double and String). SubmodelElementList would require uniform value types.
              model.SubmodelElementCollection(
                  id_short="MaxDepth",
                  category="PARAMETER",
                  description=[{"language": "en", "text": "Maximum depth the resource can operate"}],
                  display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Max Depth"}],
                  value=[
                    model.Property(
                      id_short="MaxDepthValue",
                      value_type=datatypes.Double,
                      value=20.0,
                      category="PARAMETER",
                      description=[{"language": "en", "text": "Maximum Depth Value"}],
                      display_name=[{"language": "en", "text": "Max Depth Value"}]
                    ),
                    model.Property(
                      id_short="MaxDepthUnit",
                      value_type=datatypes.String,
                      value="centimeters",
                      category="CONSTANT",
                      description=[{"language": "en", "text": "Unit of Maximum Depth Value"}],
                      display_name=[{"language": "en", "text": "Max Depth Unit"}]
                    ),
                    model.Property(
                      id_short="MaxDepthUnitShort",
                      value_type=datatypes.String,
                      value="cm",
                      category="CONSTANT",
                      description=[{"language": "en", "text": "Short Unit of Maximum Depth Value"}],
                      display_name=[{"language": "en", "text": "Max Depth Unit Short"}]
                    )
                  ]
              ),
              model.SubmodelElementCollection(
                id_short="MinDepth",
                category="PARAMETER",
                description=[{"language": "en", "text": "Minimum depth the resource can operate"}],
                display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Min Depth"}],
                value=[
                  model.Property(
                    id_short="MinDepthValue",
                    value_type=datatypes.Double,
                    value=1.0,
                    category="PARAMETER",
                    description=[{"language": "en", "text": "Minimum Depth Value"}],
                    display_name=[{"language": "en", "text": "Min Depth Value"}]
                  ),
                  model.Property(
                    id_short="MinDepthUnit",
                    value_type=datatypes.String,
                    value="centimeters",
                    category="CONSTANT",
                    description=[{"language": "en", "text": "Unit of Minimum Depth Value"}],
                    display_name=[{"language": "en", "text": "Min Depth Unit"}]
                  ),
                  model.Property(
                    id_short="MinDepthUnitShort",
                    value_type=datatypes.String,
                    value="cm",
                    category="CONSTANT",
                    description=[{"language": "en", "text": "Short Unit of Minimum Depth Value"}],
                    display_name=[{"language": "en", "text": "Min Depth Unit Short"}]
                  )
                ]
              )
          ]    
        )  
        self.get_submodel_elements().append(self.sm_element_resource_constraints)
    def create_submodel(self):
      self._submodel = model.Submodel(
      id_ = f"https://THU.de/{self.resource_config.resource_name}_RA_Knowledge",
      id_short=f"{self.resource_config.resource_name}_RA_Knowledge",
      description=[{"language": "en", "text": "Submodel for the Knowledge of the Resource Agent"}],
      display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Knowledge Submodel"}],
      
    )
      self.create_submodel_elements()
      for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)
