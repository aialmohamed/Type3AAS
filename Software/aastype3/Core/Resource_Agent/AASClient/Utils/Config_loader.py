
import pathlib
from typing import Any
import yaml



class IdConfigLoader:
    def __init__(self,):
        self.config_path = pathlib.Path(__file__).parent.parent / "Config" / "AAS_ids.yaml"
        self.data = {}

    def load_yaml(self):
        with open(self.config_path, 'r') as file:
            self.data = yaml.safe_load(file)
        return self.data

    def get_submodel_id(self, key: str = "submodel_ids") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data.get(key, {})
    

    def get_shell_id(self, key: str = "Resource Agent Shell 1") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["shell_id"][0].get(key, {})
    



    def get_Interaction_submodel_id(self, key: str = "Interaction Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodel_ids"][1].get(key, {})
    def get_Capabilities_submodel_id(self, key: str = "Capabilities Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodel_ids"][0].get(key, {})
    def get_Operational_State_submodel_id(self, key: str = "Operational State Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodel_ids"][3].get(key, {})
    def get_Knowledge_submodel_id(self, key: str = "Knowledge Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodel_ids"][2].get(key, {})
    def get_base_url(self, key: str = "base_url") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data.get(key, {})



""" Example usage
def main():
    loader = IdConfigLoader()
    config_data = loader.load_yaml()
    print(config_data)
    capabilities_submodel_id = loader.get_Capabilities_submodel_id()
    print(f"Capabilities Submodel ID: {capabilities_submodel_id}")
    interaction_submodel_id = loader.get_Interaction_submodel_id()
    print(f"Interaction Submodel ID: {interaction_submodel_id}")
    operational_state_submodel_id = loader.get_Operational_State_submodel_id()
    print(f"Operational State Submodel ID: {operational_state_submodel_id}")
    knowledge_submodel_id = loader.get_Knowledge_submodel_id()
    print(f"Knowledge Submodel ID: {knowledge_submodel_id}")
    shell_id = loader.get_shell_id()
    print(f"Shell ID: {shell_id}")
    base_url = loader.get_base_url()
    print(f"Base URL: {base_url}")

if __name__ == "__main__":
    main()
"""