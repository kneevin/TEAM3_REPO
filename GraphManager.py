from typing import Dict, List
import sqlite3
import matplotlib.pyplot as pl
import seaborn as sns
import pandas as pd
import numpy as np
import os


class GraphManager:
    DB_FNAME = "./graph_manager.db"

    def __init__(self):
        self.__create_table()

    def __create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS graphs (
            graph_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER,
            graph_title TEXT,
            graph_type TEXT CHECK(graph_type IN ('Bar', 'Line', 'Scatter')),
            ax0 TEXT,
            ax1 TEXT
        )
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            conn.commit()

    def add_graph(
        self, table_id: int, graph_title: str, graph_type: str, ax0: str, ax1: str
    ):
        GRAPH_INSERT_QUERY = """
        INSERT INTO graphs (table_id, graph_title, graph_type, ax0, ax1)
        VALUES (?, ?, ?, ?, ?)
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                GRAPH_INSERT_QUERY, (table_id, graph_title, graph_type, ax0, ax1)
            )
            conn.commit()

    def get_graph_data(self, )

    def get_all_graph_types(self):
        return ['Bar', 'Line', 'Scatter']

    def get_all_graphs(self):
        GET_ALL_GRAPHS_QUERY = """
            SELECT * FROM graphs
            """
        with sqlite3.connect(self.DB_FNAME) as conn:
            # cursor = conn.cursor()
            # cursor.execute(GET_ALL_GRAPHS_QUERY)
            # graphs = cursor.fetchall()
            df: pd.DataFrame = pd.read_sql_query(GET_ALL_GRAPHS_QUERY, conn)
        return df
