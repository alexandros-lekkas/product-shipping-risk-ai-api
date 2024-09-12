import os
import yaml

def load_file(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    
    with open(file_path, 'r') as file:
        if (file_extension == '.yaml'):
            return yaml.safe_load(file)
        else:
            return file.read()