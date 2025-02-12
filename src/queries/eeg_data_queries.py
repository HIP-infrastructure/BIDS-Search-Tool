from db.duckdb_singleton import DuckDBSingleton
from options import EEGData
from pathlib import Path

# TODO Get this from config
project_dir = Path(__file__).resolve().parent.parent.parent
eeg_sessions_parquet_path = (project_dir / 'data/parquet_files/eeg_sessions_data.parquet').as_posix()

singleton = DuckDBSingleton()

def get_column_values():
    query = '''
    SELECT * FROM '{0}'
    '''.format(eeg_sessions_parquet_path)
    return singleton.query(query)

def get_field_values(field):
    query = '''
    SELECT DISTINCT {0} FROM '{1}'
    '''.format(field, eeg_sessions_parquet_path)
    return singleton.query(query)

def get_max_field_value(field):
    query = "SELECT MAX({0}) FROM '{1}'".format(field, eeg_sessions_parquet_path)
    max_value= singleton.query(query).fetchall()

    return max_value[0]

def get_min_field_value(field):
    query = "SELECT MIN({0}) FROM '{1}'".format(field, eeg_sessions_parquet_path)
    min_value= singleton.query(query).fetchall()

    return min_value[0]

def fetch_sessions_by_criteria(task_name, recording_type, min_duration, max_duration):  
    in_statement_name = f"""('{"', '".join(task_name)}')"""
    in_statement_type = f"""('{"', '".join(recording_type)}')"""
    parameters = [min_duration, max_duration]

    query = ''' 
    SELECT * EXCLUDE (participant_fk, dataset_fk) FROM '{0}' WHERE RecordingDuration BETWEEN $1 AND $2
    '''.format(eeg_sessions_parquet_path)

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