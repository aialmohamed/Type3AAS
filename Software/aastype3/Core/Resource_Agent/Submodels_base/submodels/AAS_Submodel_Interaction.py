
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Submodels_base.submodels.AAS_Submodel_base import AASSubmodelBase


class AAS_Submodel_Interaction(AASSubmodelBase):
    """
    Submodel representing Interaction capabilities of the AAS.
    """
    def __init__(self):
        super().__init__()
    def create_submodel_elements(self):
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value='https://THU.de/Properties/Endpoints'
            ),)
        )
        sm_element_endpoints = model.SubmodelElementCollection(
            id_short="Endpoints",
            description=[{"language": "en", "text": "Collection of interaction endpoints"}],
            display_name=[{"language": "en", "text": "Endpoints"}],
            semantic_id=semantic_reference,
            value=[
                model.Property(
                    id_short= "Machine_OPCUA_Endpoint",
                    value_type=datatypes.String,
                    value="opc.tcp://Place_Holder:4840/freeopcua/server/",
                    category="CONSTANT",
                    description=[{"language": "en", "text": "OPC UA endpoint of the machine"}],
                    display_name=[{"language": "en", "text": "Machine OPC UA Endpoint"}]
                ),
                model.Property(
                    id_short= "MQTT_Broker_Endpoint",
                    value_type=datatypes.String,
                    value="mqtt://Place_Holder:1883",
                    category="CONSTANT",
                    description=[{"language": "en", "text": "MQTT Broker endpoint for communication"}],
                    display_name=[{"language": "en", "text": "MQTT Broker Endpoint"}]
                )
            ]
        )
        self.get_submodel_elements().append(sm_element_endpoints)
    def create_submodel(self):
        self._submodel = model.Submodel(
            id_="https://THU.de/RA_1_SM_Interaction",
            id_short="RA_1_SM_Interaction",
            description=[{"language": "en", "text": "Submodel for the Interaction of the Resource Agent"}],
            display_name=[{"language": "en", "text": "Interaction Submodel"}],
        )
        self.create_submodel_elements()
        for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)