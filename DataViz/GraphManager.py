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

    def add_graph(self):
        pass

