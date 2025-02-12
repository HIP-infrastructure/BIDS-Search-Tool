from db.duckdb_singleton import DuckDBSingleton
from pathlib import Path

# TODO Get these from config
project_dir = Path(__file__).resolve().parent.parent.parent
datasets_parquet_path = (project_dir / 'data/parquet_files/datasets_metadata.parquet').as_posix()
participants_parquet_path = (project_dir / 'data/parquet_files/participants_data.parquet').as_posix()
singleton = DuckDBSingleton()
### Dataset

def get_column_values():
    query = '''
    SELECT * FROM '{0}'
    '''.format(datasets_parquet_path)
    return singleton.query(query)

def get_max_field_value(field):
    query = '''
    SELECT MAX({0}) FROM '{1}'
    '''.format(field, datasets_parquet_path)
    max_value = singleton.query(query).fetchall()
    return [value[0] for value in max_value]

def get_min_field_value(field):
    query = '''
    SELECT MIN({0}) FROM '{1}'
    '''.format(field, datasets_parquet_path)
    min_value = singleton.query(query).fetchall()
    return [value[0] for value in min_value]

def get_field_values(field):
    query = '''
    SELECT DISTINCT {0} FROM '{1}'
    '''.format(field, datasets_parquet_path)
    return singleton.query(query)

def fetch_datasets_by_criteria(minParticipants, maxParticipants, authors):
    in_statement_authors = f"""('{"', '".join(authors)}')"""
    parameters = [minParticipants, maxParticipants]
    query = '''
    SELECT * FROM '{0}' WHERE (nb_participants BETWEEN $1 AND $2)
    '''.format(datasets_parquet_path)
    if(len(authors) > 0):
        query += " AND Authors IN $3"
        parameters.append(in_statement_authors)
    return singleton.query(query, parameters=parameters)

def fetch_participants_by_selected_datasets(datasets):
    in_statement = f"""('{"', '".join(datasets)}')"""
    query = '''
    SELECT * EXCLUDE (participant_uid, dataset_fk) FROM '{0}' WHERE dataset_fk IN $1
    '''.format(participants_parquet_path)
    return singleton.query(query, parameters=[in_statement])