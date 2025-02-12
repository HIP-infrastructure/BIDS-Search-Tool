import yaml
from pathlib import Path
# Could maybe be a class at some point?

# Get the directory where the script is located
#project_dir = Path.cwd()
script_dir = Path(__file__).resolve().parent
#print("project dir = " + project_dir.as_posix())
# user_config_path = project_dir / 'src' / 'user_config.yaml'
# config_path = project_dir / 'src' / 'config.yaml'

user_config_path = script_dir / 'user_config.yaml'
config_path = script_dir / 'config.yaml'

print("User config path = " + user_config_path.as_posix())
print("Config path = " + config_path.as_posix())

def get_user_bids_path():
    with open(user_config_path, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config['bids_path']

def get_extraction_successful():
    with open(user_config_path, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config['extraction_successful']


def update_user_path(value):
    if(not value.endswith('/')):
        value = value + '/'
    with open(user_config_path, 'r') as file:
        config = yaml.safe_load(file)
  
    config['bids_path'] = value

    with open(user_config_path, 'w') as file:
        yaml.dump(config, file)

    file.close()
    
def update_extraction_value(value):
    with open(user_config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    config['extraction_successful'] = value

    with open(user_config_path, 'w') as file:
        yaml.dump(config, file)

    file.close()
    
def get_output_file_names():
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    file.close()
    config['extract_load']['output_file_names']