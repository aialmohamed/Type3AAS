from dataclasses import dataclass, field
from typing import Dict, Optional
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
@dataclass
class ResourceConfig:
    """Configuration for any resource machine."""
    resource_name: str  # "drill_1", "conveyor_1", "lathe_1"
    resource_type: str  # "drill", "conveyor", "lathe"
    aas_global_id: str  # Unique AAS identifier RA_1_Global_Asset_ID
    shell_id: str  # "https://THU.de/RA_1"
    aas_short_id: str  # "RA_1_Shell"
    
    # Time slot config
    slot_start_time: str = "08:00"
    slot_end_time: str = "17:00"
    slot_duration_minutes: int = 30
    
    # Capabilities/Knowledge (resource-specific)
    capabilities: Dict[str,model.Operation] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = {}
  