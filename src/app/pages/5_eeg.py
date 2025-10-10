import streamlit as st
import logging
from queries import eeg_data_queries
from queries import query_helper
import src.app.app_utils as app_utils

logger = logging.getLogger(__name__)

@st.cache_resource
def init_field_values(field):
    values = eeg_data_queries.get_field_values(field)
    return values.df()

@st.cache_resource
def init_task_name_field_values():
    task_name_values = eeg_data_queries.get_field_values()
    return task_name_values.df()

### Check what fields exist in paquet files
available_fields = query_helper.get_available_eeg_fields()
logger.debug(f"Available EEG fields: {available_fields}")

if "RecordingDuration" in available_fields:
    max_duration = int(eeg_data_queries.get_max_field_value("RecordingDuration")[0])
    min_duration = int(eeg_data_queries.get_min_field_value("RecordingDuration")[0])

if "RecordingType" in available_fields:
    recording_types = init_field_values("RecordingType")
    
if "TaskName" in available_fields:
    task_names = init_field_values("TaskName")
    
# Initialize fields
task_name = []
recording_type = []
min_recording_duration = 0
max_recording_duration = 0

with st.sidebar:
    st.header("EEG sessions search:")
    if "RecordingType" in available_fields:
        recording_type = st.multiselect("Recording type", recording_types)
    if "RecordingDuration" in available_fields:
        duration_range = st.slider("Recording Duration", min_duration, max_duration, (min_duration, max_duration), key="duration_slider")
        min_recording_duration = duration_range[0]
        max_recording_duration = duration_range[-1]
    if "TaskName" in available_fields:
        task_name = st.multiselect("Task Name", task_names)
            
st.subheader("EEG runs")

df_eeg =eeg_data_queries.fetch_sessions_by_criteria(task_name, recording_type, min_recording_duration, max_recording_duration).df()
app_utils.display_large_df(df_eeg)
buffer = app_utils.df_to_excel_buffer(df_eeg)
st.download_button(
        label="Download data as Excel",
        data=buffer.getvalue(),
        file_name='eeg_runs.xlsx'
    )