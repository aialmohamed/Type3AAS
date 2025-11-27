
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_base import AASSubmodelBase
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Datamodels.ProductionConfig_DataType import ProductionConfig


class AAS_Submodel_InterfaceEndpoints(AASSubmodelBase):
    """
    Submodel for the Interface Endpoints of the Resource Agent.
    Inherits from AASSubmodelBase.
    """
    def __init__(self, production_config: ProductionConfig):
        self.production_config = production_config
        super().__init__()
    def create_submodel_elements(self):
        """
        Creates the submodel elements for the Interface Endpoints submodel.
        """
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value=f'https://THU.de/Properties/{self.production_config.production_name}_Interface_Endpoints'
            ),)
        )
        sm_element_endpoints = model.SubmodelElementCollection(
            id_short=f"{self.production_config.production_name}_Interface_Endpoints",
            description=[{"language": "en", "text": "Collection of interface endpoints"}],
            display_name=[{"language": "en", "text": f"{self.production_config.production_name} Interface Endpoints"}],
            semantic_id=semantic_reference,
            value=[
                model.Property(
                    id_short= "Drill_Command_Invocation_Endpoint",
                    value_type=datatypes.String,
                    value="https://0.0.0.0/8090",
                    category="CONSTANT",
                    description=[{"language": "en", "text": "REST API endpoint of the drill command (use /drill_invocation_id for different invokers where id is the machine number)"}],
                    display_name=[{"language": "en", "text": "Drill Command API Endpoint"}]
                ),
                model.Property(
                    id_short= "Move_Command_Invocation_Endpoint",
                    value_type=datatypes.String,
                    value="https://0.0.0.0/8092",
                    category="CONSTANT",
                    description=[{"language": "en", "text": "REST API endpoint of the move command  (use /movexy_invocation_id for different invokers where id is the machine number)"}],
                    display_name=[{"language": "en", "text": "Move Command API Endpoint"}]
                )
            ]
        )
        self.get_submodel_elements().append(sm_element_endpoints)
    def create_submodel(self):
        self._submodel = model.Submodel(
            id_=f"https://THU.de/{self.production_config.production_name}_PA_Interface_Endpoints",
            id_short=f"{self.production_config.production_name}_PA_Interface_Endpoints",
            description=[{"language": "en", "text": "Submodel for the Interface Endpoints of the Production Machine"}],
            display_name=[{"language": "en", "text": f"{self.production_config.production_name} Interface Endpoints Submodel"}],
        )
        self.create_submodel_elements()
        for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)
