from typing import Dict, List, NamedTuple
from contextlib import closing
import sqlite3
import matplotlib.pyplot as pl
from pydantic import BaseModel
import seaborn as sns
import pandas as pd
import numpy as np
import os

from .GraphManager import GraphManager, Graph, Axes, GraphQueryParam
from .TableManager import TableManager, TableResponse, TableMapResponse

class DataVisualizationFacade:
    DB_FNAME = "./unified_db.db"

    def __init__(self):
        self.table_manager = TableManager(self.__get_connection)
        self.graph_manager = GraphManager(self.__get_connection)

# ------- graph -------
    def add_graph(self, query_params: GraphQueryParam) -> Graph:
        graph_id = self.graph_manager.insert_graph_table(query_params)
        graph_mp = self.graph_manager.get_graph_metadata(graph_id=graph_id)

    # def render_graph(self, graph_id: int) -> Graph:



# ------- table -------
    def get_table(self, table_id: int) -> TableResponse:
        return self.table_manager.get_table_response_by_id(table_id=table_id)

    def get_all_tables_mp(self) -> TableMapResponse:
        return self.table_manager.get_table_id_mp()

    def add_table(self, table_name: str, dataframe: pd.DataFrame) -> TableResponse:
        res = self.table_manager.add_table(table_name, dataframe, tbl_response=True)
        return res

    def __get_connection(self) -> sqlite3.Connection:
        return closing(sqlite3.connect(self.DB_FNAME))

    # def __create_all_tables(self):
    #     with self.__get_connection() as conn:
    #         conn.execute("""
    #             CREATE TABLE IF NOT EXISTS graphs (
    #                 graph_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 table_id INTEGER NOT NULL,
    #                 graph_title TEXT NOT NULL,
    #                 graph_type TEXT CHECK(graph_type IN ('Bar', 'Line', 'Scatter')) NOT NULL,
    #                 ax0 TEXT NOT NULL,
    #                 ax1 TEXT NOT NULL,
    #                 FOREIGN KEY (table_id) REFERENCES master_tables(table_id) ON DELETE CASCADE
    #             )
    #         """)
    #         conn.execute("""
    #             CREATE TABLE IF NOT EXISTS master_dashboard (
    #                 dashboard_id INTEGER NOT NULL,
    #                 graph_id INTEGER NOT NULL,
    #                 PRIMARY KEY (dashboard_id, graph_id),
    #                 FOREIGN KEY (graph_id) REFERENCES graphs(graph_id) ON DELETE CASCADE,
    #                 FOREIGN KEY (dashboard_id) REFERENCES dashboard_title_mp(dashboard_id) ON DELETE CASCADE
    #             )
    #         """)
    #         conn.execute("""
    #             CREATE TABLE IF NOT EXISTS dashboard_title_mp (
    #                 dashboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 dashboard_title TEXT NOT NULL
    #             )
    #         """)
            # conn.commit() is called automatically afterwards