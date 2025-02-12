from src.db.duckdb_singleton import DuckDBSingleton
import os
from pathlib import Path

# TODO: get these paths from config
project_dir = Path(__file__).resolve().parent.parent.parent
dataset_metadata_csv = (project_dir / "data/csv_files/datasets_metadata.csv").as_posix()
participant_metadata_csv = (project_dir / "data/csv_files/participants_metadata.csv").as_posix()
ieeg_electrodes_metadata_csv = (project_dir / "data/csv_files/ieeg_electrodes_metadata.csv").as_posix()
ieeg_sessions_metadata_csv = (project_dir / "data/csv_files/ieeg_sessions_metadata.csv").as_posix()
eeg_sessions_metadata_csv = (project_dir / "data/csv_files/eeg_sessions_metadata.csv").as_posix()

dataset_parquet = (project_dir / "data/parquet_files/datasets_metadata.parquet").as_posix()
participants_parquet = (project_dir / "data/parquet_files/participants_data.parquet").as_posix()
ieeg_electrodes_parquet = (project_dir / "data/parquet_files/ieeg_electrodes_data.parquet").as_posix()
ieeg_sessions_parquet = (project_dir / "data/parquet_files/ieeg_sessions_data.parquet").as_posix()
eeg_sessions_parquet = (project_dir / "data/parquet_files/eeg_sessions_data.parquet").as_posix()

singleton = DuckDBSingleton()

def create_table_from_csv(table_name, csv_file_path):
    query = '''
    CREATE OR REPLACE TABLE {0} AS
        SELECT *
        FROM read_csv('{1}',
        delim = '\t',
        header = true);
    '''.format(table_name, csv_file_path)
    print("query in load script: ")
    print(query)
    print(type(query))
    singleton.write_new_data(query)
    print("New table written to new database.")
    
def write_parquet(table_name, parquet_output_path):
    query = '''
    COPY
    (SELECT * FROM {0})
    TO '{1}'
    (FORMAT 'parquet');
    '''.format(table_name, parquet_output_path)
    singleton.write_new_data(query)
    print("New parquet written with new database.")

def load_dataset_parquet():
    create_table_from_csv("t1", dataset_metadata_csv)
    write_parquet("t1", dataset_parquet)
    
def load_participants_parquet():
    create_table_from_csv("t2", participant_metadata_csv)
    write_parquet("t2", participants_parquet)
    
def load_ieeg_electrodes_parquet():
    create_table_from_csv("t3", ieeg_electrodes_metadata_csv)
    write_parquet("t3", ieeg_electrodes_parquet)
    
def load_ieeg_sessions_parquet():
    create_table_from_csv("t4", ieeg_sessions_metadata_csv)
    write_parquet("t4", ieeg_sessions_parquet)
    
def load_eeg_sessions_parquet():
    create_table_from_csv("t5", eeg_sessions_metadata_csv)
    write_parquet("t5", eeg_sessions_parquet)
    
def write_data_to_parquet():
    if os.path.exists(dataset_metadata_csv):
        load_dataset_parquet()
    if os.path.exists(participant_metadata_csv):
        load_participants_parquet()
    if os.path.exists(ieeg_electrodes_metadata_csv):
        load_ieeg_electrodes_parquet()
    if os.path.exists(ieeg_sessions_metadata_csv):
        load_ieeg_sessions_parquet()
    if os.path.exists(eeg_sessions_metadata_csv):
        load_eeg_sessions_parquet()
        
    print("All parquet files written, we can now replace the current db with the new.")
    #singleton.replace_current_with_new()