import streamlit as st
from queries import ieeg_data_queries
from queries import query_helper
import app_utils
from options import iEEGData

@st.cache_resource
def init_region_field_values():
    region_values = ieeg_data_queries.get_regions()
    return region_values

@st.cache_resource
def init_field_values(field, dataType):
    values = ieeg_data_queries.get_field_values(field, dataType).df()
    clean_values = values.mask(values.eq('None')).dropna()
    print("init field value " + field)
    return clean_values

@st.cache_resource
def init_min_value(field, dataType):
    print("init min value of " + field)
    return ieeg_data_queries.get_min_field_value(field, dataType)[0]
    
@st.cache_resource
def init_max_value(field, dataType):
    print("init max value of " + field)
    return ieeg_data_queries.get_max_field_value(field, dataType)[0]

### Check what fields exist in paquet files
available_fields = query_helper.get_available_ieeg_fields()
region_fields = ["ind.region", "das.region", "stein.region", "wb.region", "lobe", "region1" ]


### iEEG sessions initializations

if "RecordingDuration" in available_fields:
    max_duration = int(init_max_value("RecordingDuration", iEEGData.TASKS))
    min_duration = int(init_min_value("RecordingDuration", iEEGData.TASKS))

if "RecordingType" in available_fields:
    recording_types = init_field_values("RecordingType", iEEGData.TASKS)

if "TaskName" in available_fields:
    task_names = init_field_values("TaskName", iEEGData.TASKS)

### iEEG electrodes initializations
if "type" in available_fields:
    electrode_types = init_field_values("type", iEEGData.ELECTRODES)

if "hemisphere" in available_fields:
    hemisphere_values = init_field_values("hemisphere", iEEGData.ELECTRODES)

if region_fields in available_fields:
    region_values = init_region_field_values()
    
# Initialize fields
task_name = []
recording_type = []
min_recording_duration = 0
max_recording_duration = 0
region = []
type = []
hemisphere = []

tab1, tab2 = st.tabs(["iEEG sessions", "iEEG electrodes"])

with tab1:
    with st.sidebar:
        st.header("iEEG sessions search:")
        if "RecordingType" in available_fields:
            recording_type = st.multiselect("Recording type", recording_types)
        if "RecordingDuration" in available_fields:
            duration_range = st.slider("Recording Duration", min_duration, max_duration, (min_duration, max_duration), key="duration_slider")
            min_recording_duration = duration_range[0]
            max_recording_duration = duration_range[-1]
        if "TaskName" in available_fields:
            task_name = st.multiselect("Task Name", task_names)


    st.subheader("iEEG runs")

    df_ieeg_sessions =ieeg_data_queries.fetch_sessions_by_criteria(task_name, recording_type, min_recording_duration, max_recording_duration).df()
    app_utils.display_large_df(df_ieeg_sessions)
    
    ### Excel export
    buffer = app_utils.df_to_excel_buffer(df_ieeg_sessions)
    st.download_button(
        label="Download data as Excel",
        data=buffer.getvalue(),
        file_name='ieeg_runs.xlsx'
    )

with tab2:
    with st.sidebar:
        st.header("iEEG electrodes search:")
        if "hemisphere" in available_fields:
            hemisphere = st.multiselect("Hemisphere", hemisphere_values)
        if "type" in available_fields:
            type = st.multiselect("Electrode type", electrode_types)
        if region_fields in available_fields:
            region = st.multiselect("Region",region_values)

    st.subheader("iEEG electrodes data")

    df_ieeg =ieeg_data_queries.fetch_electrodes_by_criteria(hemisphere, type, region).df()
    app_utils.display_large_df(df_ieeg)

    ### Excel export
    buffer = app_utils.df_to_excel_buffer(df_ieeg)
    st.download_button(
        label="Download data as Excel",
        data=buffer.getvalue(),
        file_name='ieeg_electrodes.xlsx'
    )