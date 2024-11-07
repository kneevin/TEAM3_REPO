from typing import Dict, List
import matplotlib.pyplot as pl
import sqlite3
import seaborn as sns
import pandas as pd
import numpy as np
import os

class TableManager:
    DB_FNAME = './table_manager.db'
    def __init__(self):
        self.conn = sqlite3.connect(self.DB_FNAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.__create_master_table()

    def __create_master_table(self):
        create_master_table_query = '''
        CREATE TABLE IF NOT EXISTS master_tables (
            table_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT UNIQUE
        )
        '''
        self.cursor.execute(create_master_table_query)
        self.conn.commit()

    def add_table(self, table_name: str, dataframe: pd.DataFrame):
        insert_query = '''
        INSERT INTO master_tables (table_name)
        VALUES (?)
        '''
        self.cursor.execute(insert_query, (table_name,))
        
        columns = ', '.join([f'{col} TEXT' for col in dataframe.columns])
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        )
        '''
        self.cursor.execute(create_table_query)
        
        placeholders = ', '.join(['?' for _ in dataframe.columns])
        insert_query = f'''
        INSERT INTO {table_name} ({', '.join(dataframe.columns)})
        VALUES ({placeholders})
        '''
        self.cursor.executemany(insert_query, dataframe.values.tolist())
        self.conn.commit()

    def get_all_table_names(self) -> List[str]:
        select_query = '''
        SELECT table_name FROM master_tables
        '''
        cursor = self.conn.execute(select_query)
        table_names = [row[0] for row in cursor.fetchall()]
        return table_names

    def get_table_data(self, table_name: str) -> pd.DataFrame:
        select_query = f'''
        SELECT * FROM {table_name}
        '''
        cursor = self.conn.execute(select_query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=columns)

    def __del__(self):
        self.cursor.close()
        self.conn.close()