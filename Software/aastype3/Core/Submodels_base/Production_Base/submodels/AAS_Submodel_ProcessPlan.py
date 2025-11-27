
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_base import AASSubmodelBase
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Datamodels.ProductionConfig_DataType import ProductionConfig


class AAS_Submodel_ProcessPlan(AASSubmodelBase):
  def __init__(self, production_config: ProductionConfig):
    self.production_config = production_config
    super().__init__()
  def create_submodel_elements(self):
    sematic_reference = model.ExternalReference(
      (model.Key(
        type_=model.KeyTypes.GLOBAL_REFERENCE,
        value=f'https://THU.de/Properties/{self.production_config.production_name}_Process_Plan'
      ),)
    )
    sm_element_nodes = model.SubmodelElementCollection(
      id_short=f"{self.production_config.production_name}_Nodes",
      description=[{"language": "en", "text": "Collection of process plan nodes"}],
      display_name=[{"language": "en", "text": f"{self.production_config.production_name} Process Plan Nodes"}],
      semantic_id=sematic_reference,
      value=[
        model.Property(
          id_short="Move_Node",
          value_type=datatypes.String,
          value="Move Node",
          category="VARIABLE",
          description=[{"language": "en", "text": "Move operation to coordinates X,Y"}],
          display_name=[{"language": "en", "text": "Move Node"}]
        ),
        model.Property(
          id_short="Drill_Node",
          value_type=datatypes.String,
          value="Drill Node",
          category="VARIABLE",
          description=[{"language": "en", "text": "Drill operation with specified depth and RPM"}],
          display_name=[{"language": "en", "text": "Drill Node"}]
        )
      ]
    )
    sm_element_edges = model.SubmodelElementCollection(
      id_short=f"{self.production_config.production_name}_Edges",
      description=[{"language": "en", "text": "Collection of process plan edges"}],
      display_name=[{"language": "en", "text": f"{self.production_config.production_name} Process Plan Edges"}],
      semantic_id=sematic_reference,
      value=[
        model.Property(
          id_short="Edge_1",
          value_type=datatypes.String,
          value="Move_Node to Drill_Node",
          category="CONSTANT",
          description=[{"language": "en", "text": "Edge from Move Node to Drill Node"}],
          display_name=[{"language": "en", "text": "Edge 1"}]
        )
      ]
    )
    sm_enrty_point = model.Property(
      id_short="Entry_Point",
      value_type=datatypes.String,
      value="Move_Node",
      category="CONSTANT",
      description=[{"language": "en", "text": "Entry point of the process plan"}],
      display_name=[{"language": "en", "text": "Entry Point"}]
    )
    sm_exit_point = model.Property(
      id_short="Exit_Point",
      value_type=datatypes.String,
      value="Drill_Node",
      category="CONSTANT",
      description=[{"language": "en", "text": "Exit point of the process plan"}],
      display_name=[{"language": "en", "text": "Exit Point"}]
    )
    sm_precondtions = model.Property(
          id_short="Preconditions",
          value_type=datatypes.String,
          value="Material Available",
          category="CONSTANT",
          description=[{"language": "en", "text": "Precondition that material must be available"}],
          display_name=[{"language": "en", "text": "Precondition"}]
    )
    sm_postconditions = model.Property(
          id_short="Postconditions",
          value_type=datatypes.String,
          value="Operation Completed",
          category="CONSTANT",
          description=[{"language": "en", "text": "Postcondition that operation must be completed"}],
          display_name=[{"language": "en", "text": "Postcondition"}]
    )
    sm_requiered_capabilities = model.Property(
      id_short="Required_Capabilities",
      description=[{"language": "en", "text": "Collection of required capabilities for the process plan"}],
      display_name=[{"language": "en", "text": f"{self.production_config.production_name} Process Plan Required Capabilities"}],
      semantic_id=sematic_reference,
      value="[Drill_Capability, MoveXY_Capability]",
      category="CONSTANT",
      value_type=datatypes.String,
    )
    self.get_submodel_elements().append(sm_element_nodes)
    self.get_submodel_elements().append(sm_element_edges)
    self.get_submodel_elements().append(sm_enrty_point)
    self.get_submodel_elements().append(sm_exit_point)
    self.get_submodel_elements().append(sm_precondtions)
    self.get_submodel_elements().append(sm_postconditions)
    self.get_submodel_elements().append(sm_requiered_capabilities)
  def create_submodel(self):
    self._submodel = model.Submodel(
      id_=f"https://THU.de/{self.production_config.production_name}_PA_Process_Plan",
      id_short=f"{self.production_config.production_name}_Process_Plan",
      description=[{"language": "en", "text": "Submodel for the Process Plan of the Production Machine"}],
      display_name=[{"language": "en", "text": f"{self.production_config.production_name} Process Plan Submodel"}],
    )
    self.create_submodel_elements()
    for element in self._submodel_elements:
      self._submodel.submodel_element.add(element)