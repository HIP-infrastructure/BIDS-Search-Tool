import yaml
# Could maybe be a class at some point?

# USER CONFIG

def get_user_bids_path():
    with open('user_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config['bids_path']


def get_extraction_successful():
    with open('user_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config['extraction_successful']


def update_user_path(value):
    if(not value.endswith('/')):
        value = value + '/'
    with open('user_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
  
    config['bids_path'] = value

    with open('user_config.yaml', 'w') as file:
        yaml.dump(config, file)

    file.close()
    
def update_extraction_value(value):
    with open('user_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    config['extraction_successful'] = value

    with open('user_config.yaml', 'w') as file:
        yaml.dump(config, file)

    file.close()
    
def get_output_file_names():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    file.close()
    config['extract_load']['output_file_names']


