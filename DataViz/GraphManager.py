from typing import Dict, List, NamedTuple, Callable
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

class GraphQueryParam(BaseModel):
    table_id: str
    graph_title: str
    graph_type: str
    ax0: str
    ax1: str

class GraphMapResponse(BaseModel):
    table_ids: List[int]
    table_names: List[str]
    graph_ids: List[int]
    graph_titles: List[str]
    graph_types: List[str]
    axes: List[Axes]

class GraphManager:
    def __init__(self, get_connection_callback: Callable[[], sqlite3.Connection]):
        self.get_sql_db_connection = get_connection_callback
        self.__create_tables()

    def __create_tables(self):
        with self.get_sql_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS graphs (
                    graph_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id INTEGER NOT NULL,
                    graph_title TEXT NOT NULL,
                    graph_type TEXT CHECK(graph_type IN ('Bar', 'Line', 'Scatter')) NOT NULL,
                    ax0 TEXT NOT NULL,
                    ax1 TEXT NOT NULL,
                    FOREIGN KEY (table_id) REFERENCES master_tables(table_id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def get_graph_map_response(self):
        TABLE_IDS = []
        TABLE_NAMES = []
        GRAPH_IDS = []
        GRAPH_TITLES = []
        GRAPH_TYPES = []
        AXES = []
        with self.get_sql_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    mt.table_id, mt.table_name,
                    g.graph_id, g.graph_title, 
                    g.graph_type, g.ax0, g.ax1
                FROM master_tables mt
                JOIN graphs g ON mt.table_id = g.table_id
            ''')
            rows = cursor.fetchall()

            for row in rows:
                table_id, table_name, graph_id, graph_title, graph_type, ax0, ax1 = row

                TABLE_IDS.append(table_id)
                TABLE_NAMES.append(table_name)
                GRAPH_IDS.append(graph_id)
                GRAPH_TITLES.append(graph_title)
                GRAPH_TYPES.append(graph_type)
                AXES.append(Axes(ax0=ax0, ax1=ax1))

            # Create GraphMapResponse object
            response = GraphMapResponse(
                table_ids=TABLE_IDS,
                table_names=TABLE_NAMES,
                graph_ids=GRAPH_IDS,
                graph_titles=GRAPH_TITLES,
                graph_types=GRAPH_TYPES,
                axes=AXES
            )
            
            return response

    

    def add_graph(self, query: GraphQueryParam):
        pass

