import bids_indexer
import aggregator
import load
import src.Configuration as config
import pandas as pd
import logging
from pathlib import Path
from pyinstrument import Profiler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

src_path = Path(__file__).resolve().parent.parent.parent

# Conditional profiling based on config
profiler = None
if config.get_profiling_enabled():
    profiler = Profiler()
    profiler.start()
    logger.info("Performance profiling enabled")

# TODO: get these paths from config
dataset_description_json = "dataset_description.json"
dataset_metadata_csv = "data/csv_files/datasets_metadata.csv"
participant_metadata_csv = "data/csv_files/participants_metadata.csv"
ieeg_electrodes_metadata_csv = "data/csv_files/ieeg_electrodes_metadata.csv"
eeg_electrodes_metadata_csv = "data/csv_files/eeg_electrodes_metadata.csv"
ieeg_sessions_metadata_csv = "data/csv_files/ieeg_sessions_metadata.csv"
eeg_sessions_metadata_csv = "data/csv_files/eeg_sessions_metadata.csv"

df_datasets = pd.DataFrame()
df_participants_eeg = pd.DataFrame() 
df_participants_ieeg = pd.DataFrame()
path = config.get_user_bids_path()
datasets_all = bids_indexer.list_datasets_in_root_directory(path)
logger.info(f"Found {len(datasets_all)} datasets: {datasets_all}")

ieeg_datasets = []
eeg_datasets = []
        
# Create dataset metadata file:
datasets_metadata = [] 
for dataset_id in datasets_all:
    json_path = Path(path, dataset_id, dataset_description_json)
    ds_metadata_dict = aggregator.extract_json_data_as_dataframe(json_path)
    df_ds = aggregator.build_dataset_metadata_df(path, dataset_id, ds_metadata_dict)
    datasets_metadata.append(df_ds)

df_datasets = pd.concat(datasets_metadata)
if df_datasets.empty:
        raise Exception("Dataset description data could not be extracted")

csv_path = Path(src_path, dataset_metadata_csv)
df_datasets.to_csv(csv_path, sep='\t', index=False)

df_participants_all = pd.DataFrame()

for dataset in datasets_all:
    ds_path = Path(path, dataset)
    if(bids_indexer.dataset_has_modality(ds_path, "ieeg")):
        ieeg_datasets.append(dataset)

    elif(bids_indexer.dataset_has_modality(ds_path, "eeg")):
        eeg_datasets.append(dataset)

if(not len(ieeg_datasets) == 0):
    df_participants_ieeg = aggregator.get_participants_metadata(path, ieeg_datasets, df_datasets)
    df_ieeg_electrodes = aggregator.get_electrodes_metadata(path, df_participants_ieeg, "ieeg") 
    df_ieeg_runs = aggregator.get_runs_metadata(path, df_participants_ieeg, "ieeg") 
    
    if df_ieeg_electrodes.empty or df_ieeg_runs.empty:
        raise Exception("iEEG data could not be extracted")

    csv_path_electrodes = Path(src_path, ieeg_electrodes_metadata_csv)
    df_ieeg_electrodes.to_csv(csv_path_electrodes, sep='\t', index=False) 
    csv_path_runs = Path(src_path, ieeg_sessions_metadata_csv)
    df_ieeg_runs.to_csv(csv_path_runs, sep='\t', index=False)
        
if(not len(eeg_datasets) == 0):
    df_participants_eeg = aggregator.get_participants_metadata(path, eeg_datasets, df_datasets)
    df_eeg_sessions = aggregator.get_runs_metadata(path, df_participants_eeg, "eeg")
    # TODO extract other relevant data for EEG, ask users what they want
    if df_eeg_sessions.empty:
        raise Exception("EEG data could not be extracted")
    else:
        csv_path = Path(src_path, eeg_sessions_metadata_csv)
        df_eeg_sessions.to_csv(csv_path, sep='\t', index=False)
    
    
# Participants metadata
df_participants_all = aggregator.get_participants_metadata(path, datasets_all, df_datasets)
if df_participants_all.empty:
        raise Exception("Participants data could not be extracted")

csv_path = Path(src_path, participant_metadata_csv)
df_participants_all.to_csv(csv_path, sep='\t', index=False)

load.write_data_to_parquet()
config.update_extraction_value(True)
logger.info("Data extraction completed successfully")

# End profiling conditionally
if profiler:
    profiler.stop()
    profiling_output = config.get_profiling_output()

    if profiling_output in ['console', 'both']:
        profiler.print()

    if profiling_output in ['file', 'both']:
        output_path = src_path / 'data' / 'profiling_results.html'
        with open(output_path, 'w') as f:
            f.write(profiler.output_html())
        logger.info(f"Profiling results saved to {output_path}")