import streamlit as st
from queries import dataset_queries
import src.app.app_utils as app_utils
from queries import query_helper

@st.cache_resource
def init_field_values(field):
    values = dataset_queries.get_field_values(field).df()
    clean_values = values.mask(values.eq('None')).dropna()
    return clean_values

available_fields_list = query_helper.get_available_dataset_field()

print (available_fields_list)
if "nb_participants" in available_fields_list:
    max_participants = dataset_queries.get_max_field_value("nb_participants")[0]
    min_participants = dataset_queries.get_min_field_value("nb_participants")[0]
    nb_participants_range = [min_participants, max_participants]
if "Authors" in available_fields_list:
    authors_values = init_field_values("Authors")

with st.sidebar:
    st.header("Dataset search:")
    if "nb_participants" in available_fields_list and min_participants != max_participants:
        nb_participants_range = st.slider("Number of participants", min_participants, max_participants, (min_participants, max_participants))
    minParticipants = nb_participants_range[0]
    maxParticipants = nb_participants_range[-1]
    if "Authors" in available_fields_list:
        authors = st.multiselect("Authors", authors_values)

st.subheader("Dataset search result")

df4 = dataset_queries.fetch_datasets_by_criteria(minParticipants, maxParticipants, authors).df()
dataset_uid_list = df4['dataset_uid'].tolist()
df5 = dataset_queries.fetch_participants_by_selected_datasets(dataset_uid_list).df()
app_utils.display_large_df(df4)  

# Excel export
buffer1 = app_utils.df_to_excel_buffer(df4)  
st.download_button(
    label="Download result as Excel",
    data=buffer1.getvalue(),
    file_name='datasets.xlsx',
    key=1
)

# Displaying a nice little chart
st.bar_chart(df4["nb_participants"], x_label=["Dataset index"], y_label="Number of participants")
app_utils.display_large_df(df5)
buffer2 = app_utils.df_to_excel_buffer(df5)

# Excel export
st.download_button(
    label="Download data as Excel",
    data=buffer2.getvalue(),
    file_name='participants.xlsx',
    key=2
) 

# Displaying another little chart
nb_males = len(df5[df5['sex'] == 'M']) + len(df5[df5['sex'] == 'm'])
nb_females = len(df5[df5['sex'] == 'F']) + len(df5[df5['sex'] == 'f'])
sex_distribution = [nb_males, nb_females]
st.bar_chart(sex_distribution, x_label=["Male vs Female"], y_label="Number of participants")
