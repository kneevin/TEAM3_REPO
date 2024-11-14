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
from .DashboardManager import DashboardManager, Dashboard

class DataVisualizationFacade:
    DB_FNAME = "./unified_db.db"

    def __init__(self):
        self.table_manager = TableManager(self.__get_connection)
        self.graph_manager = GraphManager(self.__get_connection)
        self.dashb_manager = DashboardManager(self.__get_connection)

# ------- graph -------
    def add_graph(self, query_params: GraphQueryParam) -> Graph:
        graph_id = self.graph_manager.insert_graph_table(query_params)
        return self.get_graph(graph_id=graph_id)

    def get_graph(self, graph_id: int) -> Graph:
        graph_mp = self.graph_manager.get_graph_metadata(graph_id=graph_id)
        table_response = self.table_manager.get_table_response_by_id(
            table_id=graph_mp['table_id'],
            columns=[graph_mp['ax0'], graph_mp['ax1']]
        )

        return Graph(
            table_id=table_response.table_id,
            table_name=table_response.table_name,
            graph_id=graph_mp['graph_id'],
            graph_title=graph_mp['graph_title'],
            graph_type=graph_mp['graph_type'],
            ax = Axes(ax0=graph_mp['ax0'], ax1=graph_mp['ax1']),
            rows=table_response.rows
        )


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