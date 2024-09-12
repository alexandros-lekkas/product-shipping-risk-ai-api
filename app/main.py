import os
import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

class Config:
    debug = True
    reload = True
    
    def __init__(self, config_path):
        config = load_config(config_path)
        
        self.debug = config['debug']
        self.reload = config['reload']