import os
import yaml

def load_file(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    
    with open(file_path, 'r') as file:
        if file_extension == '.yaml':
            return yaml.safe_load(file)
        else:
            return file.read()

def load_structured_yaml_file(file_path, fields):
    file_content = load_file(file_path)
    
    if not isinstance(file_content, list):
        raise ValueError("Expected a list of dictionaries in the YAML file")
    
    structured_data = []
    
    for entry in file_content:
        if not isinstance(entry, dict):
            continue
        
        new_data = entry.get(fields[0], "")
        for field in fields[1:]:
            new_data += " " + entry.get(field, "")
        
        structured_data.append(new_data)
    
    return structured_data
