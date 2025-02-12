from db.duckdb_singleton import DuckDBSingleton
from options import iEEGData
from pathlib import Path

# TODO Get this from config
project_dir = Path(__file__).resolve().parent.parent.parent
ieeg_sessions_parquet_path = (project_dir / 'data/parquet_files/ieeg_sessions_data.parquet').as_posix()
ieeg_electrodes_parquet_path = (project_dir / 'data/parquet_files/ieeg_electrodes_data.parquet').as_posix()

singleton = DuckDBSingleton()

def get_column_values(dataType):
    if(dataType is iEEGData.TASKS):
        query = '''
        SELECT * FROM '{0}'
        '''.format(ieeg_sessions_parquet_path)
    if(dataType is iEEGData.ELECTRODES):
        query = '''
        SELECT * FROM '{0}'
        '''.format(ieeg_electrodes_parquet_path)
    
    return singleton.query(query)
    

def get_field_values(field, dataType):
    if dataType is iEEGData.TASKS:
        parquet_file = ieeg_sessions_parquet_path
    if dataType is iEEGData.ELECTRODES:
        parquet_file = ieeg_electrodes_parquet_path

    query = "SELECT DISTINCT {0} FROM '{1}'".format(field, parquet_file)
        
    return singleton.query(query)

def get_max_field_value(field, dataType):
    if dataType is iEEGData.TASKS:
        parquet_file = ieeg_sessions_parquet_path
    if dataType is iEEGData.ELECTRODES:
        parquet_file = ieeg_electrodes_parquet_path
    
    query = "SELECT MAX({0}) FROM '{1}'".format(field, parquet_file)
    max_value= singleton.query(query).fetchall()

    return max_value[0]

def get_min_field_value(field, dataType):
    if dataType is iEEGData.TASKS:
        parquet_file = ieeg_sessions_parquet_path
    if dataType is iEEGData.ELECTRODES:
        parquet_file = ieeg_electrodes_parquet_path
        
    query = "SELECT MIN({0}) FROM '{1}'".format(field, parquet_file)
    min_value= singleton.query(query).fetchall()

    return min_value[0]

# Similar to get_field_values but values are from several columns
def get_regions():
    query = '''
    SELECT DISTINCT "ind.region", "das.region", "stein.region", "wb.region", "lobe", "region1", "region2" FROM '{0}'
    '''.format(ieeg_electrodes_parquet_path)
    values = singleton.query(query).fetchall()
    flat_list = list_flattening(values)
    return set(flat_list)

def fetch_data(dataType):
    if dataType is iEEGData.TASKS:
        parquet_file = ieeg_sessions_parquet_path
    if dataType is iEEGData.ELECTRODES:
        parquet_file = ieeg_electrodes_parquet_path
    query = "SELECT * FROM '{0}'".format(ieeg_electrodes_parquet_path)
    
    return singleton.query(query, parameters=parquet_file)

def fetch_electrodes_by_criteria(hemisphere, type, region): 
    in_statement_hemisphere = f"""('{"', '".join(hemisphere)}')"""
    in_statement_type = f"""('{"', '".join(type)}')"""
    in_statement_region = f"""('{"', '".join(region)}')"""

    if(len(hemisphere) == 0 and len(type) == 0 and len(region) == 0):
        query = '''
        SELECT * EXCLUDE (participant_fk, dataset_fk) FROM '{0}'
        '''.format(ieeg_electrodes_parquet_path)
        return singleton.query(query)
    
    parameters = []
    query = '''SELECT * EXCLUDE (participant_fk, dataset_fk) FROM '{0}' WHERE'''.format(ieeg_electrodes_parquet_path)

    if(len(hemisphere) > 0):
        query += ' hemisphere IN $1'
        parameters.append(in_statement_hemisphere)
        if(len(type) > 0):
            query += ' AND type IN $2'
            parameters.append(in_statement_type)
            if(len(region) > 0):
                query += ''' AND ("ind.region" IN $3 OR "das.region" IN $3 OR "stein.region" IN $3 OR "wb.region" IN $3 OR "lobe" IN $3 OR "region1" IN $3 OR "region2" IN $3)'''
                parameters.append(in_statement_region)
        if(len(type) == 0 and len(region) > 0):
            query += ''' AND ("ind.region" IN $2 OR "das.region" IN $2 OR "stein.region" IN $2 OR "wb.region" IN $2 OR "lobe" IN $2 OR "region1" IN $2 OR "region2" IN $2)'''
            parameters.append(in_statement_region)

    if(len(hemisphere) == 0):
        if(len(type) > 0):
            query += ' type IN $1'
            parameters.append(in_statement_type)
            if(len(region) > 0):
                query += ''' AND ("ind.region" IN $2 OR "das.region" IN $2 OR "stein.region" IN $2 OR "wb.region" IN $2 OR "lobe" IN $2 OR "region1" IN $2 OR "region2" IN $2) '''
                parameters.append(in_statement_region)
        if(len(type) == 0 and len(region) > 0):
            query += ''' "ind.region" IN $1 OR "das.region" IN $1 OR "stein.region" IN $1 OR "wb.region" IN $1 OR "lobe" IN $1 OR "region1" IN $1 OR "region2" IN $1 '''
            parameters.append(in_statement_region)
 
    return singleton.query(query, parameters=parameters)

# Same method as for EEG, can be merged later maybe
def fetch_sessions_by_criteria(task_name, recording_type, min_duration, max_duration):  
    in_statement_name = f"""('{"', '".join(task_name)}')"""
    in_statement_type = f"""('{"', '".join(recording_type)}')"""
    parameters = [min_duration, max_duration]

    query = ''' 
    SELECT * EXCLUDE (participant_fk, dataset_fk) FROM '{0}' WHERE RecordingDuration BETWEEN $1 AND $2
    '''.format(ieeg_sessions_parquet_path)

    if(len(task_name) == None and len(recording_type) == 0):
        return singleton.query(query)

    if(len(task_name) > 0):
        query += ' AND TaskName IN $3'
        parameters.append(in_statement_name)
        if(len(recording_type) > 0):
            query += ' AND RecordingType IN $4'
            parameters.append(in_statement_type)
    
    if(len(recording_type) > 0 and len(task_name) == 0):
            query += ' AND RecordingType IN $3'
            parameters.append(in_statement_type)
            
    return singleton.query(query, parameters=parameters)

def list_flattening(list):
    flat_list = []

    for xs in list:
        for x in xs:
            flat_list.append(x)
            
    return flat_list