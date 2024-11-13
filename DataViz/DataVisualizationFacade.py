from typing import Dict, List, NamedTuple
import sqlite3
import matplotlib.pyplot as pl
from pydantic import BaseModel
import seaborn as sns
import pandas as pd
import numpy as np
import os


class DataVisualizationFacade:
    DB_FNAME = "./unified_db.db"
    RESERVED_TABLES = [
        "master_tables",
        "graphs",
        "master_dashboard",
        "dashboard_title_mp",
    ]

    def __init__(self):
        self.__create_all_tables()

    def get_connection(self):
        return sqlite3.connect(self.DB_FNAME)

    def __create_all_tables(self):
        with sqlite3.connect(self.DB_FNAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS master_tables (
                    table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT UNIQUE NOT NULL
                )
            """)
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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS master_dashboard (
                    dashboard_id INTEGER NOT NULL,
                    graph_id INTEGER NOT NULL,
                    PRIMARY KEY (dashboard_id, graph_id),
                    FOREIGN KEY (graph_id) REFERENCES graphs(graph_id) ON DELETE CASCADE,
                    FOREIGN KEY (dashboard_id) REFERENCES dashboard_title_mp(dashboard_id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dashboard_title_mp (
                    dashboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dashboard_title TEXT NOT NULL
                )
            """)
            conn.commit()
