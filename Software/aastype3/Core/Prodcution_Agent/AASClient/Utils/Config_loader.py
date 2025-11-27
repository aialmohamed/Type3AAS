
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
    

    def get_shell_id(self, key: str = "Production Agent Shell") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data["shell_id"][0].get(key, {})
    

# region Submodel IDs

    def get_Execution_Tracking_Submodel_id(self, key: str = "Execution Tracking Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        submodel_list = self.data["submodels"][0].get(key, [])
        if isinstance(submodel_list, list) and len(submodel_list) > 0:
            return submodel_list[0].get("id", {})
        return {}
    def get_Interface_and_Endpoints_Submodel_id(self, key: str = "Interface and Endpoints Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        submodel_list = self.data["submodels"][1].get(key, [])
        if isinstance(submodel_list, list) and len(submodel_list) > 0:
            return submodel_list[0].get("id", {})
        return {}
    def get_Process_Plan_Submodel_id(self, key: str = "Process Plan Submodel") -> Any:
        if self.data is None:
            self.load_yaml()
        submodel_list = self.data["submodels"][2].get(key, [])
        if isinstance(submodel_list, list) and len(submodel_list) > 0:
            return submodel_list[0].get("id", {})
        return {}
    def get_base_url(self, key: str = "base_url") -> Any:
        if self.data is None:
            self.load_yaml()
        return self.data.get(key, {})
# endregion

#region Submodel Elements
    def get_Execution_Tracking_Submodel_elements(self,key: str= "Execution Tracking Submodel") -> List[str]:
        if self.data is None:
            self.load_yaml()
        val = self.data["submodels"][0].get(key, {})[1].get("elements", {})
        res = []
        for v in val:
            for k,v in v.items():
                res.append(v)
        return res

    def get_Interface_and_Endpoints_Submodel_elements(self, key: str = "Interface and Endpoints Submodel") -> List[str]:
        if self.data is None:
            self.load_yaml()
        val = self.data["submodels"][1].get(key, {})[1].get("elements", {})
        res = []
        for v in val:
            for k,v in v.items():
                res.append(v)
        return res

    def get_Process_Plan_Submodel_elements(self, key: str = "Process Plan Submodel") -> List[str]:
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
    execution_tracking_submodel_id = loader.get_Execution_Tracking_Submodel_elements()
    process_plan_submodel_id = loader.get_Process_Plan_Submodel_elements()
    interface_and_endpoints_submodel_id = loader.get_Interface_and_Endpoints_Submodel_elements()
    print(f"Process Plan Submodel ID: {process_plan_submodel_id}")
    print(f"Interface and Endpoints Submodel ID: {interface_and_endpoints_submodel_id}")
    print(f"Execution Tracking Submodel ID: {execution_tracking_submodel_id}")
    #elements = loader.get_Capabilities_submodel_elements()
    #print(f"Capabilities Submodel Elements: {elements}")

if __name__ == "__main__":
    main()
