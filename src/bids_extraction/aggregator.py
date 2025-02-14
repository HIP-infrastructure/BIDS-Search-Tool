import json
import pandas as pd
import uuid
import bids_indexer
from pathlib import Path


# TODO: get this from config
participants_tsv = "participants.tsv"
        
def build_dataset_metadata_df(bids_path, dataset_id, dataset_description_df):
    dataset_uid = uuid.uuid4()
    dataset_path = Path(bids_path, dataset_id)
    nb_participants = bids_indexer.get_nb_participants_for_dataset(bids_path, dataset_id)
    nb_files = bids_indexer.get_nb_files_in_directory(dataset_path)
    df = dataset_description_df
    df.insert(0, 'dataset_uid', dataset_uid)
    df.insert(1, 'path', dataset_path)
    df.insert(2, 'folder_name', dataset_id)
    df.insert(3, 'nb_participants', nb_participants)
    df.insert(4, 'nb_files', nb_files)
    print("df dataset done")
    
    return df

def get_participants_metadata(bids_path, dataset_ids, datasets_metadata):
    content = [] 
    for dataset_id in dataset_ids:
        tsv_path = Path(bids_path, dataset_id, participants_tsv)
   
        df = pd.read_csv(tsv_path, sep='\t')
        nb_sessions = []
        participant_iuds = []
        dataset_fks = []
        for subject in df['participant_id']:
            nb_sess = len(bids_indexer.get_session_ids_for_participant(bids_path, subject))
            nb_sessions.append(nb_sess)
            participant_iuds.append(uuid.uuid4())
            dataset_fk_value = datasets_metadata.loc[datasets_metadata['folder_name'] == dataset_id, 'dataset_uid'].item()
            dataset_fks.append(dataset_fk_value)      
        df['nb_sessions'] = nb_sessions
        df['dataset_folder_name'] = dataset_id
        df['dataset path'] = bids_path + dataset_id
        df['participant_uid'] = participant_iuds
        df['dataset_fk'] = dataset_fk_value
        content.append(df)  
    participants_metadata = pd.concat(content)
    print("df participant done")
    return participants_metadata

def get_electrodes_metadata(bids_path, participants_metadata, modality):
    content = [] 
    for subject in participants_metadata['participant_uid']:
        dataset_folder = participants_metadata.loc[participants_metadata['participant_uid'] == subject, 'dataset_folder_name'].item()
        participant_id = participants_metadata.loc[participants_metadata['participant_uid'] == subject, 'participant_id'].item()
        participant_fk = subject
        dataset_fk = participants_metadata.loc[participants_metadata['participant_uid'] == subject, 'dataset_fk'].item()

        sessions = bids_indexer.get_session_ids_for_participant(bids_path, participant_id)
        for session_path in sessions:
            electrodes_data = get_electrodes(dataset_folder, participant_id, session_path, modality, dataset_fk, participant_fk)
            content.append(electrodes_data)

    electrodes_metadata = pd.concat(content)
    return electrodes_metadata

def get_electrodes(dataset_folder, participant_id, session_path, modality, dataset_fk, participant_fk):
    files = bids_indexer.get_electrodes_tsv(session_path, modality)

    if(len(files) > 0):
        tsv_path = files[0]

        df = pd.read_csv(tsv_path, sep='\t')
        df.insert(0, 'dataset_folder_name',dataset_folder)
        df.insert(1, 'participant_id', participant_id)
        df.insert(2, 'session', session_path)
        df.insert(3, 'participant_fk', participant_fk)
        df.insert(4, 'dataset_fk', dataset_fk)

        return df
    else:
        return


def get_runs_metadata(bids_path, participants_metadata, modality):
    content = [] 
    for subject in participants_metadata['participant_uid']:
        dataset_folder = participants_metadata.loc[participants_metadata['participant_uid'] == subject, 'dataset_folder_name'].item()
        participant_id = participants_metadata.loc[participants_metadata['participant_uid'] == subject, 'participant_id'].item()
        participant_fk = subject
        dataset_fk = participants_metadata.loc[participants_metadata['participant_uid'] == subject, 'dataset_fk'].item()
        
        sessions = bids_indexer.get_session_ids_for_participant(bids_path, participant_id)
        for session_path in sessions:
            eeg_runs_metadata = get_runs(dataset_folder, participant_id, session_path, modality, dataset_fk, participant_fk)
            content.append(eeg_runs_metadata)

    runs_metadata = pd.concat(content)

    print("runs metadata done")
    return runs_metadata        
    
def get_runs(dataset_folder, participant_id, session_path, modality, dataset_fk, participant_fk):
    run_files = bids_indexer.get_tasks_for_participant(session_path, modality)
    if(len(run_files) > 0):
        content = []
        i = 0
        for file in run_files:
            df = extract_json_data_as_dataframe(file)
            df.insert(0, 'folder_name',dataset_folder)
            df.insert(1, 'participant_id', participant_id)
            df.insert(2, 'session', session_path)
            df.insert(3, 'run_nb', 'run_' + str(i))
            df.insert(4, 'participant_fk', participant_fk)
            df.insert(5, 'dataset_fk', dataset_fk)
            content.append(df)
            i += 1
        runs = pd.concat(content)
        
        return runs
    else:
        return pd.DataFrame()
   
    
def extract_json_data_as_dataframe(path):
    json_path = path
    # Opening JSON file
    with open(json_path) as json_file:
        data = json.load(json_file)
    
    data = pd.json_normalize(data)
    df = pd.DataFrame(data)
    return df   