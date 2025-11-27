from typing import Dict
from aastype3.Core.Resource_Agent.Datamodels.ProductionConfig_DataType import ProductionConfig
from basyx.aas import model
import basyx.aas.model.datatypes as datatypes

class ProductionMachineShell:
    def __init__(self):
        self.production_name = "Production_1"
        self.production_type = "workpiece_1"
        self.aas_global_id = "PA_Production1_Global_Asset_ID"
        self.shell_id = "https://THU.de/Production_1"
        self.aas_short_id = "PA_Production_1_Shell"
        self.config = self._create_production_config()
    def _create_production_config(self) -> ProductionConfig:
        return ProductionConfig(
            production_name=self.production_name,
            production_type=self.production_type,
            aas_global_id=self.aas_global_id,
            shell_id=self.shell_id,
            aas_short_id=self.aas_short_id,
        )