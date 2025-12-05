from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
from aastype3.Core.Submodels_base.Resource_Base.submodels.AAS_Submodel_base import AASSubmodelBase
from aastype3.Core.Datamodels.TimeSlot_DataType import TimeSlotDataType
from aastype3.Core.Datamodels.ResourceConfig_DataType import ResourceConfig 

class AAS_Submodel_Operational_State(AASSubmodelBase):
    """
    Submodel for the Operational State of the Resource Agent.
    Inherits from AASSubmodelBase.
    """
    def __init__(self, resource_config: ResourceConfig):
        
        self.resource_config = resource_config
        self.time_slot_manager = TimeSlotDataType(start_time=f"{resource_config.slot_start_time}", end_time=f"{resource_config.slot_end_time}", duration_minutes=resource_config.slot_duration_minutes)
        super().__init__()
        
    
    def create_submodel_elements(self):
        """
        Creates the submodel elements for the Operational State submodel.
        """
        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value=f"https://THU.de/Properties/{self.resource_config.resource_name}_Current_Operational_State"
            ),)
        )
        self.sm_element_current_state = model.Property(
          id_short="Current_Operational_State",
          value_type=datatypes.String,
          category="VARIABLE",
          value="Idle",  # Initial state could also be "Idle" , "Running" , "Error", "Done"
          semantic_id=semantic_reference,
          display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Current Operational State"}],
          description=[{"language": "en", "text": "Current operational state of the resource"}]
        )


        # time slots operational data element
        # collection 3 properties: free slots, booked slots , slot duration
        # normal time format HH:MM for each slot
        # duration is set to a mock value of 10 minutes for demonstration purposes
        # work day from 08:00 to 17:00
        # time slots are created for each 10-minute interval within the workday
        self.time_slot_manager.get_free_slots()


        semantic_reference = model.ExternalReference(
        (model.Key(
            type_=model.KeyTypes.GLOBAL_REFERENCE,
            value=f"https://THU.de/Properties/{self.resource_config.resource_name}_TimeSlots_Operational_Data"
            ),)
        )
        self.sm_element_time_slots_data = model.SubmodelElementCollection(
          id_short=f"{self.resource_config.resource_name}_TimeSlots_Operational_Data",
          semantic_id=semantic_reference,
          display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Time Slots Operational Data"}],
          value=[
              model.Property(
                  id_short="Free_Slots",
                  value_type=datatypes.String,
                  category="PARAMETER",
                  value=self.time_slot_manager.get_free_slots_json()
              ),
              model.Property(
                  id_short="Booked_Slots",
                  value_type=datatypes.String,
                  category="PARAMETER",
                  value=self.time_slot_manager.get_booked_slots_json()
              ),
              model.Property(
                  id_short="Slot_Duration",
                  value_type=datatypes.Integer,
                  category="PARAMETER",
                  value=self.time_slot_manager.get_duration_minutes()
              )
          ]
        )
        self.get_submodel_elements().append(self.sm_element_current_state)
        self.get_submodel_elements().append(self.sm_element_time_slots_data)
    def create_submodel(self):
      self._submodel = model.Submodel(
      id_ = f"https://THU.de/{self.resource_config.resource_name}_RA_Operational_State",
      id_short=f"{self.resource_config.resource_name}_RA_Operational_State",
      description=[{"language": "en", "text": "Submodel for the Operational State of the Resource Agent"}],
      display_name=[{"language": "en", "text": f"{self.resource_config.resource_name} Operational State Submodel"}],
      
    )
      self.create_submodel_elements()
      for element in self._submodel_elements:
          self._submodel.submodel_element.add(element)