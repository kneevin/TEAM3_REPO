from typing import Any, Dict, List, NamedTuple, Callable, Optional
import sqlite3
from fastapi import HTTPException
from pydantic import BaseModel, model_validator
import pandas as pd

class DashboardCreateQueryParams(BaseModel):
    dashboard_title: str
    graph_ids: List[int]
    indices: List[int]
    width_height: List[List[int]]

    @model_validator(mode='before')
    def check_lengths(cls, data: Any) -> Any:
        graph_ids, indices, width_height = data.get('graph_ids'), data.get('indices'), data.get('width_height')
        if not(len(graph_ids) == len(indices) == len(width_height)):
            raise HTTPException(status_code=404, detail="Arrays are not of the same length")
        if not all(2 == len(wh) for wh in width_height):
            raise HTTPException(status_code=404, 
                                detail="width_height array must contain only array elements with exactly length 2"
            )
        return data

class DashboardManager:
    def __init__(self, get_connection_callback: Callable[[], sqlite3.Connection]):
        self.get_sql_db_connection = get_connection_callback
        self.__create_tables()

    def create_new_dashboard(self, query: DashboardCreateQueryParams):
        with self.get_sql_db_connection() as conn:
            # Insert the dashboard title and get the new dashboard_id
            cursor = conn.execute(
                "INSERT INTO dashboard_title_mp (dashboard_title) VALUES (?)",
                (query.dashboard_title,)
            )
            dashboard_id = cursor.lastrowid

            # Prepare the data for bulk insertion
            data_to_insert = [
                (dashboard_id, graph_id, idx, width, height)
                for graph_id, idx, (width, height) in zip(query.graph_ids, query.indices, query.width_height)
            ]

            # Insert the data into the master_dashboard table
            conn.executemany(
                """
                INSERT INTO master_dashboard (dashboard_id, graph_id, idx, width, height)
                VALUES (?, ?, ?, ?, ?)
                """,
                data_to_insert
            )

            # Commit the transaction
            conn.commit()

            # Optionally, return the dashboard_id
            return dashboard_id

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

    