import streamlit as st
from src import Configuration as config
from bids_extraction import bids_indexer
from pathlib import Path

data_import_page = st.Page("app/pages/2_data_import.py", title="Data Import")
participants_search_page = st.Page("app/pages/3_participants_search.py", title="Participants Search")
ieeg_page = st.Page("app/pages/4_ieeg.py", title="iEEG")
eeg_page = st.Page("app/pages/5_eeg.py", title="EEG")
dataset_search_demo_page = st.Page("app/pages/6_dataset_search_demo.py", title="Plaform Search Simulation")
data_extracted = config.get_extraction_successful()
path = config.get_user_bids_path()

if(not data_extracted):
    pg = st.navigation({
        "Data import": [data_import_page],
    })
else:
    modalities = []
    print("path in app: " + path)
    print("path converted in app: ")
    print(Path(path))
    if(bids_indexer.root_has_modality(path, "ieeg")):
        modalities.append(ieeg_page)
    if(bids_indexer.root_has_modality(path, "eeg")):
        modalities.append(eeg_page)
    
    pg = st.navigation({
        "Data import": [data_import_page],
        "Participants Search": [participants_search_page],
        "Modality Search": modalities,
        "DEMO": [dataset_search_demo_page],
    })


    
#with st.sidebar:
st.header("🔎 BIDS Search Tool 🧠")
    
pg.run()
