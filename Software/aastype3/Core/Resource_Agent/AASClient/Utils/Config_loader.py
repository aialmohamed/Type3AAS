
import pathlib
from typing import Any, List
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
    

    def get_shell_id(self, key: str = "Resource Agent Shell") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["shell_id"][0].get(key, {})
    def get_machines_id(self, key: str = "machines") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data.get(key, {})
    

# region Submodel IDs

    def get_Interaction_submodel_id(self, key: str = "Interaction Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodels"][1].get(key, {})[0].get("id", {})
    def get_Capabilities_submodel_id(self, key: str = "Capabilities Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodels"][0].get(key, {})[0].get("id", {})
    def get_Operational_State_submodel_id(self, key: str = "Operational State Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodels"][3].get(key, {})[0].get("id", {})
    def get_Knowledge_submodel_id(self, key: str = "Knowledge Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["submodels"][2].get(key, {})[0].get("id", {})
    def get_base_url(self, key: str = "base_url") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data.get(key, {})
# endregion

#region Submodel Elements
    def get_Capabilities_submodel_elements(self,key: str= "Capabilities Submodel") -> List[str]:
        if self.data is None:
            self.load_yaml()
        val = self.data["submodels"][0].get(key, {})[1].get("elements", {})
        res = []
        for v in val:
            for k,v in v.items():
                res.append(v)
        return res

    def get_Interaction_submodel_elements(self, key: str = "Interaction Submodel") -> List[str]:
        if self.data is None:
            self.load_yaml()
        val = self.data["submodels"][1].get(key, {})[1].get("elements", {})
        res = []
        for v in val:
            for k,v in v.items():
                res.append(v)
        return res

    def get_Operational_State_submodel_elements(self, key: str = "Operational State Submodel") -> List[str]:
        if self.data is None:
            self.load_yaml()
        val = self.data["submodels"][3].get(key, {})[1].get("elements", {})
        res = []
        for v in val:
                for k,v in v.items():
                    res.append(v)
        return res


    def get_Knowledge_submodel_elements(self, key: str = "Knowledge Submodel") -> List[str]:
        if self.data is None:
            self.load_yaml()
        val = self.data["submodels"][2].get(key, {})[1].get("elements", {})
        res = []
        for v in val:
                for k,v in v.items():
                    res.append(v)
        return res

# endregion




def main():
    loader = IdConfigLoader()
    config_data = loader.load_yaml()
    #print(config_data)
    capabilities_submodel_id = loader.get_Capabilities_submodel_id()
    print(f"Capabilities Submodel ID: {capabilities_submodel_id}")
    elements = loader.get_Capabilities_submodel_elements()
    print(f"Capabilities Submodel Elements: {elements}")

if __name__ == "__main__":
    main()
