from typing import Dict, List, NamedTuple, Callable, Optional
import sqlite3
from pydantic import BaseModel
import pandas as pd

class DashboardManager:
    def __init__(self, get_connection_callback: Callable[[], sqlite3.Connection]):
        self.get_sql_db_connection = get_connection_callback
        self.__create_tables()

    def __create_tables(self):
        with self.get_sql_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS master_dashboard (
                    dashboard_id INTEGER NOT NULL,
                    graph_id INTEGER NOT NULL,
                    idx INTEGER NOT NULL,
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL,
                    x_coord INTEGER GENERATED ALWAYS AS ((idx * 4) % 12) STORED,
                    y_coord INTEGER GENERATED ALWAYS AS (idx / 3) STORED,
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
            conn.commit() # is called automatically afterwards

    