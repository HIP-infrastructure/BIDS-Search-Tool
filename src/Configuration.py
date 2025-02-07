import yaml
import os
# Could maybe be a class at some point?

# USER CONFIG
project_path = os.getenv('PROJECT_PATH')
print("PROJECT PATH IS " + project_path)

def get_user_bids_path():
    filename = os.path.join(project_path, 'user-config.yaml')
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config['bids_path']


def get_extraction_successful():
    filename = os.path.join(project_path, 'user-config.yaml')
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config['extraction_successful']


def update_user_path(value):
    filename = os.path.join(project_path, 'user-config.yaml')
    if(not value.endswith('/')):
        value = value + '/'
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
  
    config['bids_path'] = value

    with open(filename, 'w') as file:
        yaml.dump(config, file)

    file.close()
    
def update_extraction_value(value):
    filename = os.path.join(project_path, 'user-config.yaml')
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    
    config['extraction_successful'] = value

    with open(filename, 'w') as file:
        yaml.dump(config, file)

    file.close()
    
def get_output_file_names():
    filename = os.path.join(project_path, 'config.yaml')
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    
    file.close()
    config['extract_load']['output_file_names']


