from typing import Dict, List, NamedTuple
import sqlite3
import matplotlib.pyplot as pl
from pydantic import BaseModel
import seaborn as sns
import pandas as pd
import numpy as np
import os

class Axes(NamedTuple):
    ax0: str
    ax1: str

class Graph(BaseModel):
    graph_id: int
    graph_title: str
    graph_type: str
    ax: Axes
    data: list[list]

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

    def get_graph_id_map(self) -> Dict[int, Dict[int, str]]:
        SELECT_QUERY = """SELECT table_id, graph_id, graph_title FROM graphs ORDER BY table_id, graph_id"""
        with sqlite3.connect(self.DB_FNAME) as conn:
            df = pd.read_sql_query(SELECT_QUERY, conn)
        # res = df.groupby('table_id').apply(lambda x: dict(zip(x['graph_id'], x['graph_title']))).to_dict()
        return df.to_dict(orient='records')

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
            graph_id = cursor.lastrowid

            # Fetch the inserted row
            SELECT_QUERY = """
            SELECT * FROM graphs WHERE graph_id = ?
            """
            cursor.execute(SELECT_QUERY, (graph_id,))
            row = cursor.fetchone()
            columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))

    def get_graph(self, graph_id: int):
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            # Fetch the inserted row
            SELECT_QUERY = """
            SELECT * FROM graphs WHERE graph_id = ?
            """
            cursor.execute(SELECT_QUERY, (graph_id,))
            row = cursor.fetchone()
            columns = [description[0] for description in cursor.description]
        graph_mp = dict(zip(columns, row))
        return graph_mp

    def graph_df_to_obj(self, df: pd.DataFrame):
        return

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
