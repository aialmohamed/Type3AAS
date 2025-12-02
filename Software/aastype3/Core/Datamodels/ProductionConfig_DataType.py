from dataclasses import dataclass, field
from typing import Dict, Optional
from basyx.aas import model 
import basyx.aas.model.datatypes as datatypes
@dataclass
class ProductionConfig:
    """Configuration for any production machine."""
    production_name: str  # "drill_1", "conveyor_1", "lathe_1"
    production_type: str  # "drill", "conveyor", "lathe"
    aas_global_id: str  # Unique AAS identifier RA_1_Global_Asset_ID
    shell_id: str  # "https://THU.de/RA_1"
    aas_short_id: str  # "RA_1_Shell"