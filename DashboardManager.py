import sqlite3
import pandas as pd
from typing import Tuple, Dict

class DashboardManager:
    DB_FNAME = "./dashboard_manager.db"

    def __init__(self):
        self.__create_dashboard_tables()

    def __create_dashboard_tables(self):
        create_dashboard_table_query = """
        CREATE TABLE IF NOT EXISTS master_dashboard (
            dashboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
            graph_id INTEGER,
            table_id INTEGER,
            graph_title TEXT,
            graph_type TEXT,
            ax0 TEXT,
            ax1 TEXT
        )
        """
        create_dashboard_mapping_query = """
        CREATE TABLE IF NOT EXISTS dashboard_mapping (
            dashboard_id INTEGER PRIMARY KEY,
            dashboard_title TEXT,
            FOREIGN KEY (dashboard_id) REFERENCES master_dashboard(dashboard_id)
        )
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(create_dashboard_table_query)
            cursor.execute(create_dashboard_mapping_query)
            conn.commit()

    def get_dashboard(self, dashboard_id: int) -> Tuple[str, pd.DataFrame]:
        GET_DASHBOARD_QUERY = """
        SELECT * FROM master_dashboard WHERE dashboard_id = ?
        """
        GET_DASHBOARD_TITLE_QUERY = """
        SELECT dashboard_title FROM dashboard_mapping WHERE dashboard_id = ?
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            dashboard_df = pd.read_sql_query(GET_DASHBOARD_QUERY, conn, params=(dashboard_id,))
            dashboard_title_df = pd.read_sql_query(GET_DASHBOARD_TITLE_QUERY, conn, params=(dashboard_id,))

        result = {
            "dashboard_title": dashboard_title_df.iloc[0]["dashboard_title"] if not dashboard_title_df.empty else None,
            "dashboard_data": dashboard_df
        }
        return result

    def add_dashboard_entry(self, 
            dashboard_id: int, graph_id: int, table_id: int, 
            graph_title: str, graph_type: str, ax0: str, ax1: str
        ) -> Dict:
        INSERT_DASHBOARD_QUERY = """
        INSERT INTO master_dashboard (dashboard_id, graph_id, table_id, graph_title, graph_type, ax0, ax1)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(INSERT_DASHBOARD_QUERY, (dashboard_id, graph_id, table_id, graph_title, graph_type, ax0, ax1))
            conn.commit()

            SELECT_QUERY = """
            SELECT * FROM master_dashboard WHERE graph_id = ?
            """
            cursor.execute(SELECT_QUERY, (graph_id,))
            row = cursor.fetchone()
            columns = [description[0] for description in cursor.description]

        return dict(zip(columns, row))