from datetime import datetime
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_base import AASSubmodelBase
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Resource_Agent.Datamodels.ProductionConfig_DataType import ProductionConfig


class AAS_Submodel_ExecutionTracking(AASSubmodelBase):
  def __init__(self, production_config: ProductionConfig):
    self.production_config = production_config
    super().__init__()
  def create_submodel_elements(self):
    sematic_reference = model.ExternalReference(
      (model.Key(
        type_=model.KeyTypes.GLOBAL_REFERENCE,
        value=f'https://THU.de/Properties/{self.production_config.production_name}_Execution_Tracking'
      ),)
    )
    sm_current_node = model.Property(
      id_short="Current_Node",
      value_type=datatypes.String,
      value="Node_ID",
      category="VARIABLE",
      description=[{"language": "en", "text": "Current node being executed in the process plan"}],
      display_name=[{"language": "en", "text": "Current Node"}],
      semantic_id=sematic_reference
    )
    sm_token_position = model.Property(
      id_short="Token_Position",
      value_type=datatypes.Integer,
      value=0,
      category="VARIABLE",
      description=[{"language": "en", "text": "Position of the execution token in the process plan"}],
      display_name=[{"language": "en", "text": "Token Position"}],
      semantic_id=sematic_reference
    )
    sm_time_stamp = model.Property(
      id_short="Time_Stamp",
      value_type=datatypes.DateTime,
      value=datetime.now(),
      category="VARIABLE",
      description=[{"language": "en", "text": "Timestamp of the last execution update"}],
      display_name=[{"language": "en", "text": "Time Stamp"}],
      semantic_id=sematic_reference
    )
    sm_step_status = model.Property(
      id_short="Step_Status",
      value_type=datatypes.String,
      value="Not Started",
      category="VARIABLE",
      description=[{"language": "en", "text": "Status of the current step in the process plan (queued, running, done, failed)"}],
      display_name=[{"language": "en", "text": "Step Status"}],
      semantic_id=sematic_reference
    )
    self.get_submodel_elements().append(sm_current_node)
    self.get_submodel_elements().append(sm_token_position)
    self.get_submodel_elements().append(sm_time_stamp)
    self.get_submodel_elements().append(sm_step_status)

  def create_submodel(self):
    self._submodel = model.Submodel(
      id_=f"https://THU.de/{self.production_config.production_name}_PA_Execution_Tracking",
      id_short=f"{self.production_config.production_name}_PA_Execution_Tracking",
      description=[{"language": "en", "text": "Submodel for the Execution Tracking of the Production Machine"}],
      display_name=[{"language": "en", "text": f"{self.production_config.production_name} Execution Tracking Submodel"}],
    )
    self.create_submodel_elements()
    for element in self._submodel_elements:
      self._submodel.submodel_element.add(element)