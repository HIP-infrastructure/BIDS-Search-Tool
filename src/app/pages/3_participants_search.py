import streamlit as st
import logging
from queries import participant_queries
import src.app.app_utils as app_utils
from queries import query_helper

logger = logging.getLogger(__name__)

@st.cache_resource
def init_field_values(field):
    values = participant_queries.get_field_values(field).df()
    clean_values = values.mask(values.eq('None')).dropna()
    logger.debug(f"Initialized field values for: {field}")
    return clean_values
   
available_field_list = query_helper.get_available_participants_field()
#initialize optional fields just in case:
hand = []
sex = []
age_range = [0, 100]
sessions_range = [0, 0]

with st.sidebar:
    st.header("Participants search:")
    if "age" in available_field_list:
        min_age = participant_queries.get_min_field_value("age")
        max_age = participant_queries.get_max_field_value("age")
        age_range = st.slider("Age range", int(min_age[0]), int(max_age[0]), (int(min_age[0]), int(max_age[0])))
    if "hand" in available_field_list:
        hand = st.multiselect("Handedness", init_field_values("hand"))
    if "sex" in available_field_list:
        sex = st.multiselect("Sex", init_field_values("sex"))
    
    max_sessions = participant_queries.get_max_field_value("nb_sessions")
    min_sessions = participant_queries.get_min_field_value("nb_sessions")

    if(min_sessions != max_sessions):
        sessions_range = st.slider("Nb of sessions", int(min_sessions[0]), int(max_sessions[0]), (int(min_sessions[0]), int(max_sessions[0]))) 

st.subheader("Participant ID search")
participant = st.multiselect("Participant IDs", init_field_values("participant_id"))
df2 = participant_queries.fetch_participant(participant).df()
app_utils.display_large_df(df2)
# Excel export
buffer1 = app_utils.df_to_excel_buffer(df2)  
st.download_button(
    label="Download result as Excel",
    data=buffer1.getvalue(),
    file_name='participants_df.xlsx',
    key=1
)
#############
st.subheader("Participants criteria search result")    
minAge = age_range[0] 
maxAge = age_range[-1]
minSession = sessions_range[0] 
maxSession = sessions_range[-1]
if (minSession != maxSession):  
    df3 = participant_queries.fetch_participants_by_criteria(minAge, maxAge, minSession, maxSession, sex, hand, available_field_list).df()
    app_utils.display_large_df(df3)
else:
    raise Exception("Your dataset seems incomplete, your participants don't have any sessions.")
#### Excel export
buffer2 = app_utils.df_to_excel_buffer(df3)  
st.download_button(
    label="Download result as Excel",
    data=buffer2.getvalue(),
    file_name='participants_df.xlsx',
    key=2
)  