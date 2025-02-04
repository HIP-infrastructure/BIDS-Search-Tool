from db.duckdb_singleton import DuckDBSingleton

# TODO Get this from config
participants_parquet_path = 'data/parquet_files/participants_data.parquet'

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

def fetch_participants_by_criteria(minAge, maxAge, minSessions, maxSessions, sex, hand):
    in_statement_hand = f"""('{"', '".join(hand)}')"""
    in_statement_sex = f"""('{"', '".join(sex)}')"""
    parameters = [minAge, maxAge, minSessions, maxSessions]
    
    query = '''
        SELECT * EXCLUDE (participant_uid, dataset_fk) FROM '{0}' WHERE (age BETWEEN $1 AND $2) AND nb_sessions BETWEEN $3 AND $4
        '''.format(participants_parquet_path)

    if(len(sex) == 0):
        if(len(hand) > 0):
            query += ' AND hand IN $5'
            parameters.append(in_statement_hand)
    if(len(sex) != 0):
        query += ' AND sex IN $5'
        parameters.append(in_statement_sex)
        if(len(hand) > 0):
            query += ' AND hand IN $6'
            parameters.append(in_statement_hand)
    
    return singleton.query(query, parameters=parameters)