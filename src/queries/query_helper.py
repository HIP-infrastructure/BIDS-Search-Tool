from queries import participant_queries
from queries import dataset_queries
from queries import ieeg_data_queries
from queries import eeg_data_queries
import options
import streamlit as st
import pandas as pd
import re


def init_field_values(field):
    field_values = participant_queries.get_field_values(field)
    return field_values.df()

def get_available_participants_field():
    data = participant_queries.get_column_values()
    data_df = data.df()
    indexes = data_df.columns.tolist()
    return indexes

def get_available_dataset_field():
    data = dataset_queries.get_column_values()
    data_df = data.df()
    indexes = data_df.columns.tolist()
    return indexes

def get_available_ieeg_fields():
    data_sessions = ieeg_data_queries.get_column_values(options.iEEGData.TASKS).df()
    data_electrodes = ieeg_data_queries.get_column_values(options.iEEGData.ELECTRODES).df()
    columns_sessions = data_sessions.columns.tolist()
    columns_electrodes = data_electrodes.columns.tolist()
    indexes = columns_sessions + columns_electrodes
    return indexes

def get_available_eeg_fields():
    data = eeg_data_queries.get_column_values()
    data_df = data.df()
    indexes = data_df.columns.tolist()
    print(indexes)
    return indexes

def get_numerical_fields(field_list):
    numerical_fields = []
    pattern = r"^-?\d+\.\d+$"
    for field in field_list:
        if re.match(pattern, field):
            numerical_fields.append(field)

            
    return numerical_fields

def get_non_numeric_fields(field_list):
    non_num_fields = []
    for field in field_list:
        if not field.isdigit():
            non_num_fields.append(field)

            
    return non_num_fields

#TODO: this is the idea of constructing UI elements according to the fields found in the data. We would separate num and non-num fields, 
# make sliders for num fields and dropdowns for non-num fields. Fetch the min/max values for sliders and possible choices for dropdown.
def get_filters():
    fields = get_available_participants_field()
    num_fields = get_numerical_fields(fields)
    non_num_fields = get_non_numeric_fields(fields)
    
    sliders = [] 
    drop_downs = [] 
    
    print("numerical fields:")
    print(num_fields)
    print("non numerical fields:")
    print(non_num_fields)
    
    for nf in num_fields:
        #get min max values here
        sliders.append(st.slider(nf, 0, 99, (0, 99)))
        
    for nnf in non_num_fields:
        #fetch possible values here
        possible_values = ["cat", "dog", "both"]
        drop_downs.append(st.multiselect(nnf, possible_values))
        
    return sliders
    