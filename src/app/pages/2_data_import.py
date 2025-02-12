from pathlib import Path
import streamlit as st
from bids_extraction import bids_indexer
import src.Configuration as config
import subprocess
import sys

default_user_folder = "Documents"
extraction_script_path = Path(__file__).resolve().parent.parent.parent / 'bids_extraction' / 'data_extraction_pipeline.py'

def save_path():
   config.update_user_path(current_bids_folder)
      
def extract_data():
   subprocess.run([f"{sys.executable}", extraction_script_path])

# Définir les extensions de fichiers que vous souhaitez inclure
allowed_extensions = ('.json', '.csv', '.tsv', '.TRC', '.eeg', '.edf')

# Fonction pour filtrer et trier les fichiers selon les extensions autorisées et la taille
def filter_and_sort_files(files):
   filtered_files = [file for file in files if file['path'].endswith(allowed_extensions)]# or file['is_dir']]
   return sorted(filtered_files, key=lambda x: x["size"])

def run_extraction():
   extract_button = st.button("Start Extraction", disabled=not is_bids_compliant) # Give button a variable name
   if extract_button: # Make button a condition.
      st.text("Extracting data...")
      extract_data()
      if(config.get_extraction_successful()):
         st.text("BIDS data extracted successfully! Please click 'Continue'...")
         st.button("Continue")
      else:
         st.text("Something went wrong :'(")

 
 
st.subheader("Data import")

user_path = config.get_user_bids_path()
if(user_path is None or not Path(user_path).is_dir()):
   default_path = Path(Path.home(), default_user_folder)
   print(default_path)
   current_bids_folder = str(default_path)
   save_path()
else:
   current_bids_folder = config.get_user_bids_path()
   
current_bids_folder = st.text_input(label='Enter the path to the files folder:', value=current_bids_folder)   

is_bids_compliant = bids_indexer.is_bids_path(current_bids_folder)

is_bids_compliant = bids_indexer.is_bids_path(current_bids_folder)
st.write("Current folder is: " + current_bids_folder)
if is_bids_compliant:
   st.write("✅ The selected folder contains at least 1 BIDS compliant dataset.")
else:
   st.markdown(''':red[❌ No BIDS compliant dataset(s) found in this path, please try again.]''')

st.markdown(''':red[Don't forget to SAVE your path!]''')
save_button = st.button(label="Save path", on_click=save_path, disabled= not is_bids_compliant)

run_extraction()