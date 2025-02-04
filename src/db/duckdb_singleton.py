import duckdb
import os
import threading

class DuckDBSingleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DuckDBSingleton, cls).__new__(cls)
                # Separate DuckDB connections: one for writing to Parquet and another for reading from Parquet
                cls._instance.write_conn = duckdb.connect()
                cls._instance.read_conn = duckdb.connect()
        return cls._instance

    def write_new_data(self, query):
        # Use write duckdb to create new parquet files
        self.write_conn.execute(query)

    def query(self, query, parameters=None):
        # Query with the read duckdb
        return self.read_conn.execute(query, parameters)