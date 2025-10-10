import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Get the directory where the script is located
script_dir = Path(__file__).resolve().parent

user_config_path = script_dir / 'user_config.yaml'
config_path = script_dir / 'config.yaml'

logger.debug(f"User config path = {user_config_path.as_posix()}")
logger.debug(f"Config path = {config_path.as_posix()}")

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
    return config['extract_load']['output_file_names']

def get_profiling_enabled():
    with open(user_config_path, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config.get('enable_profiling', False)

def get_profiling_output():
    with open(user_config_path, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config.get('profiling_output', 'console')