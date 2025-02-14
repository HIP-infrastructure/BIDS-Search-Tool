from db.duckdb_singleton import DuckDBSingleton
from pathlib import Path

# TODO Get this from config
project_dir = Path(__file__).resolve().parent.parent.parent
participants_parquet_path = (project_dir / 'data/parquet_files/participants_data.parquet').as_posix()

singleton = DuckDBSingleton()

def get_column_values():
    query = '''
    SELECT * FROM '{0}'
    '''.format(participants_parquet_path)
    return singleton.query(query)

def get_field_values(field):
    query = '''
    SELECT DISTINCT {0} FROM '{1}'
    '''.format(field, participants_parquet_path)
    return singleton.query(query)

def get_max_field_value(field):
    query = '''
    SELECT MAX({0}) FROM '{1}'
    '''.format(field, participants_parquet_path)
    max_value = singleton.query(query).fetchall()
    return [value[0] for value in max_value]

def get_min_field_value(field):
    query = '''
    SELECT MIN({0}) FROM '{1}'
    '''.format(field, participants_parquet_path)
    min_value = singleton.query(query).fetchall()
    return [value[0] for value in min_value]


#####################

def fetch_participant(participants_ids):
    in_statement = f"""('{"', '".join(participants_ids)}')"""
    query = '''
    SELECT * EXCLUDE (participant_uid, dataset_fk) FROM '{0}' WHERE participant_id IN $1
    '''.format(participants_parquet_path)
    return singleton.query(query, parameters=[in_statement])

def column_exists(field, all_fields):
    if field in all_fields:
        return True
    else:
        return False

# TODO Improve this because it's clunky and won't scale with adding more filters... With the future work that I documented this should improve a lot
def fetch_participants_by_criteria(minAge, maxAge, minSessions, maxSessions, sex, hand, all_fields):
    in_statement_hand = f"""('{"', '".join(hand)}')"""
    in_statement_sex = f"""('{"', '".join(sex)}')"""
    parameters = [minSessions, maxSessions]
    
    ageExists = column_exists('age', all_fields)
    sexExists = column_exists('sex', all_fields)
    handExists = column_exists('hand', all_fields)
    
    query = '''
        SELECT * EXCLUDE (participant_uid, dataset_fk) FROM '{0}'
        WHERE nb_sessions BETWEEN $1 AND $2
        '''.format(participants_parquet_path)

    if(ageExists and (minAge != maxAge)):
        query += ' AND age BETWEEN $3 AND $4'
        parameters.append(minAge)
        parameters.append(maxAge)
        if(len(sex) == 0):
            if(len(hand) > 0 and handExists):
                query += ' AND hand IN $5'
                parameters.append(in_statement_hand)
        if(len(sex) > 0 and sexExists):
            query += ' AND sex IN $5'
            parameters.append(in_statement_sex)
            if(len(hand) > 0 and handExists):
                query += ' AND hand IN $6'
                parameters.append(in_statement_hand)
    if(not ageExists):      
        if(len(sex) == 0):
            if(len(hand) > 0 and handExists):
                query += ' AND hand IN $3'
                parameters.append(in_statement_hand)
        if(len(sex) > 0 and sexExists):
            query += ' AND sex IN $3'
            parameters.append(in_statement_sex)
            if(len(hand) > 0 and sexExists):
                query += ' AND hand IN $4'
                parameters.append(in_statement_hand)
    
    return singleton.query(query, parameters=parameters)