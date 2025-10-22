import yaml
import pathlib

class Shell_utills:
    def __init__(self):
        self.path = pathlib.Path(__file__).parent / "config"/ "urls.yaml"
    
    def load_shell_config(self,config_path):
        with open(config_path, 'r') as file:
            #Loaded Shell Configuration:
            # {'urls': [{'root_url': 'http://localhost:8081'}, {'shells': '/shells'}, {'submodels': '/submodels'}]}
            config = yaml.safe_load(file)
        return config
    def get_root_url(self,config):
        return config['urls'][0]['root_url']
    def get_shells_endpoint(self,config):
        return config['urls'][1]['shells']
    def get_submodels_endpoint(self,config):
        return config['urls'][2]['submodels']

