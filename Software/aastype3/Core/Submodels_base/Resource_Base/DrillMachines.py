
from typing import Dict
from aastype3.Core.Datamodels.ResourceConfig_DataType import ResourceConfig
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes


class DrillMachineShell:
    """
    Shell configuration for a Drilling Machine Resource Agent.
    """
    def __init__(self):
        self.resource_name = "Drill_1"
        self.resource_type = "drill"
        self.aas_global_id = "RA_Drill1_Global_Asset_ID"
        self.shell_id = "https://THU.de/Drill_1"
        self.aas_short_id = "RA_Drill_1_Shell"
        self.time_slot_start = "08:00"
        self.time_slot_end = "17:00"
        self.time_slot_duration_minutes = 30
        self.capabilities = self._define_capabilities()
        self.config = self._create_resource_config()
    def _create_resource_config(self) -> ResourceConfig:
        return ResourceConfig(
            resource_name=self.resource_name,
            resource_type=self.resource_type,
            aas_global_id=self.aas_global_id,
            shell_id=self.shell_id,
            aas_short_id=self.aas_short_id,
            slot_start_time=self.time_slot_start,
            slot_end_time=self.time_slot_end,
            slot_duration_minutes=self.time_slot_duration_minutes,
            capabilities=self.capabilities
        )
    
    def _define_capabilities(self) -> Dict[str,model.Operation]:
        sm_element_drill = model.Operation(
          id_short="Drill_Capability",
          qualifier=[model.Qualifier(
              kind=model.QualifierKind.CONCEPT_QUALIFIER,
              type_="invocationDelegation",
              value_type=datatypes.String,
              value="http://host.docker.internal:8090/drill_invocation_1"
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
              value="http://host.docker.internal:8092/movexy_invocation_1"
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
          ) 
        return {
            "Drill_Capability": sm_element_drill,
            "MoveXY_Capability": sm_element_movexy
        }


class SecondDrillMachineShell:
    """
    Shell configuration for a Drilling Machine Resource Agent.
    """
    def __init__(self):
        self.resource_name = "Drill_2"
        self.resource_type = "drill"
        self.aas_global_id = "RA_Drill2_Global_Asset_ID"
        self.shell_id = "https://THU.de/Drill_2"
        self.aas_short_id = "RA_Drill_2_Shell"
        self.time_slot_start = "09:00"
        self.time_slot_end = "18:00"
        self.time_slot_duration_minutes = 20
        self.capabilities = self._define_capabilities()
        self.config = self._create_resource_config()
    def _create_resource_config(self) -> ResourceConfig:
        return ResourceConfig(
            resource_name=self.resource_name,
            resource_type=self.resource_type,
            aas_global_id=self.aas_global_id,
            shell_id=self.shell_id,
            aas_short_id=self.aas_short_id,
            slot_start_time=self.time_slot_start,
            slot_end_time=self.time_slot_end,
            slot_duration_minutes=self.time_slot_duration_minutes,
            capabilities=self.capabilities
        )
    
    def _define_capabilities(self) -> Dict[str,model.Operation]:
        sm_element_drill = model.Operation(
          id_short="Drill_Capability",
          qualifier=[model.Qualifier(
              kind=model.QualifierKind.CONCEPT_QUALIFIER,
              type_="invocationDelegation",
              value_type=datatypes.String,
              value="http://host.docker.internal:8091/drill_invocation_2"
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
              value="http://host.docker.internal:8093/movexy_invocation_2"
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
          ) 
        return {
            "Drill_Capability": sm_element_drill,
            "MoveXY_Capability": sm_element_movexy
        }
