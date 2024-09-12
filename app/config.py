from .utils.file import load_file

import os
import yaml

class Config:
    def __init__(self, config_path):
        config = load_file(config_path)
        
        for key, value in config.items():
            setattr(self, key, value)
            
    def get(self,key,default=None):
        return getattr(self, key, default)