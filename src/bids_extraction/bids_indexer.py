import os
import glob
from pathlib import Path

# TODO: get these from config
participants_tsv = "participants.tsv"
dataset_description_json = "dataset_description.json"

def is_bids_path(user_path):
    if not Path(user_path).is_dir():
        return False
    
    compliant_dirs = get_bids_dirs(user_path)

    return len(compliant_dirs) > 0

def dataset_has_modality(ds_path, modality):
    path = Path(ds_path)
    pattern = "*sub*/ses-*/{0}".format(modality)
    return len(list(path.glob(pattern))) > 0

def root_has_modality(user_path, modality):
    path = Path(user_path)
    pattern = "*/*sub*/ses-*/{0}".format(modality)
    return len(list(path.glob(pattern))) > 0

def get_bids_dirs(user_path): 
    compliant_dirs = []
    try:
        if not Path(user_path).is_dir():
            return compliant_dirs

        folders_in_path = os.listdir(user_path)
        for folder in folders_in_path:
            folder_path = Path(user_path, folder)
            if Path(folder_path).is_dir():
                files = [f for f in os.listdir(folder_path) if Path(folder_path, f).is_file()]
                if participants_tsv in files and dataset_description_json in files:
                    compliant_dirs.append(folder_path)
        return compliant_dirs
    except PermissionError:
        return compliant_dirs
    
# Extract dataset folder names in root directory
def list_datasets_in_root_directory(root):
    datasets = []
    dirs = os.listdir(root)
    
    for dir in dirs:
        folder_path = Path(root, dir)
        if folder_path.is_dir():
            files = [f for f in os.listdir(folder_path) if Path(folder_path, f).is_file()]
            if participants_tsv in files and dataset_description_json in files:
                datasets.append(dir)
    return datasets

def get_nb_files_in_directory(dir_path):
    return len(os.listdir(dir_path))

def get_nb_participants_for_dataset(bids_path, dataset_folder):
    path = Path(bids_path, dataset_folder)
    pattern = "sub*"
    return len(list(path.glob(pattern)))

def get_session_ids_for_participant(bids_path, participant_id):
    path = Path(bids_path).as_posix()
    pattern = "**/{0}/ses*".format(participant_id)
    path_pattern = path + '/' + pattern
    return list(glob.glob(path_pattern))

def get_tasks_for_participant(session_path, modality):
    path = Path(session_path).as_posix()
    pattern = "{0}/*task*{0}.json".format(modality)
    path_pattern = path + '/' + pattern
    files = list(glob.glob(path_pattern))
    return files

def get_electrodes_tsv(session_path, modality):
    path = Path(session_path)
    pattern = "{0}/*electrodes.tsv".format(modality)

    files = list(path.glob(pattern))
    return files
