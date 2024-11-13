from typing import Dict, List, Tuple
import sqlite3
from pydantic import BaseModel
import pandas as pd

from .GraphManager import Graph

class Dashboard(BaseModel):
    dashboard_id: int
    dashboard_title: str
    graphs: List[Graph]

class DashboardManager:
    DB_FNAME = "./dashboard_manager.db"

    def __init__(self):
        self.__create_dashboard_tables()

    def __create_dashboard_tables(self):
        create_dashboard_table_query = """
        CREATE TABLE IF NOT EXISTS master_dashboard (
            dashboard_id INTEGER,
            graph_id INTEGER,
            table_id INTEGER,
            PRIMARY KEY (dashboard_id, graph_id)
        )
        """
        create_dashboard_title_mapping_query = """
        CREATE TABLE IF NOT EXISTS dashboard_title_mp (
            dashboard_id INTEGER PRIMARY KEY,
            dashboard_title TEXT,
            FOREIGN KEY (dashboard_id) REFERENCES master_dashboard(dashboard_id)
        )
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(create_dashboard_table_query)
            cursor.execute(create_dashboard_title_mapping_query)
            conn.commit()

    def add_dashboard_entry(self, dashboard_id: int, graph_id: int, table_id: int) -> Dict:
        INSERT_DASHBOARD_QUERY = """
        INSERT INTO master_dashboard (dashboard_id, graph_id, table_id)
        VALUES (?, ?, ?)
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(INSERT_DASHBOARD_QUERY, (dashboard_id, graph_id, table_id))
            conn.commit()

            SELECT_QUERY = """
            SELECT * FROM master_dashboard WHERE graph_id = ?
            """
            cursor.execute(SELECT_QUERY, (graph_id,))
            row = cursor.fetchone()
            columns = [description[0] for description in cursor.description]

        return dict(zip(columns, row))
    
    def get_dashboard_id_mp(self):
        SELECT_QUERY = """
        SELECT dashboard_id, dashboard_title FROM dashboard_title_mp ORDER BY dashboard_id
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            df = pd.read_sql_query(SELECT_QUERY, conn)

        return df.to_dict(orient='records')

    def add_dashboard_title(self, dashboard_id: int, dashboard_title: str) -> None:
        INSERT_TITLE_QUERY = """
        INSERT INTO dashboard_title_mp (dashboard_id, dashboard_title)
        VALUES (?, ?)
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(INSERT_TITLE_QUERY, (dashboard_id, dashboard_title))
            conn.commit()

    def get_dashboard(self, dashboard_id: int) -> Dict:
        GET_DASHBOARD_QUERY = """
        SELECT * FROM master_dashboard WHERE dashboard_id = ?
        """
        GET_DASHBOARD_TITLE_QUERY = """
        SELECT dashboard_title FROM dashboard_title_mp WHERE dashboard_id = ?
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            dashboard_df = pd.read_sql_query(GET_DASHBOARD_QUERY, conn, params=(dashboard_id,))
            dashboard_title_df = pd.read_sql_query(GET_DASHBOARD_TITLE_QUERY, conn, params=(dashboard_id,))

        result = {
            "dashboard_title": dashboard_title_df.iloc[0]["dashboard_title"] if not dashboard_title_df.empty else None,
            "dashboard_data": dashboard_df
        }
        return result