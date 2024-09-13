import os
import yaml

def load_file(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    
    with open(file_path, 'r') as file:
        if (file_extension == '.yaml'):
            return yaml.safe_load(file)
        else:
            return file.read()
        
def load_structured_yaml_file(file_path, fields):
    file = load_file(file_path)
    data = []
    
    for data in file:
        new_data = fields[0]
        for field in fields:
            if (field != fields[0]):
                new_data = new_data + " " + field
            