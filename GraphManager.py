from typing import Dict, List
import sqlite3
import matplotlib.pyplot as pl
import seaborn as sns
import pandas as pd
import numpy as np
import os

class GraphManager:
    DB_FNAME = './graph_manager.db'
    def __init__(self, ):
        self.conn = sqlite3.connect(self.DB_FNAME, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS graphs (
            graph_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER,
            graph_title TEXT,
            graph_type TEXT,
            ax0 TEXT,
            ax1 TEXT
        )
        '''
        self.cursor.execute(create_table_query)

    def add_graph(self, table_id: int, graph_title: str, graph_type: str, ax0: str, ax1: str):
        GRAPH_INSERT_QUERY = '''
        INSERT INTO graphs (table_id, graph_title, graph_type, ax0, ax1)
        VALUES (?, ?, ?, ?, ?)
        '''
        self.cursor.execute(GRAPH_INSERT_QUERY, (table_id, graph_title, graph_type, ax0, ax1))
        self.conn.commit()
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()