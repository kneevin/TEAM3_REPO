from typing import Dict, List, NamedTuple
from contextlib import closing
import sqlite3
import matplotlib.pyplot as pl
from pydantic import BaseModel
from fastapi import HTTPException
import seaborn as sns
import pandas as pd
import numpy as np
import os

from .GraphManager import GraphManager, Graph, Axes, GraphQueryParam, GraphMapResponse, Coordinates, PlotSize
from .TableManager import TableManager, TableResponse, TableMapResponse
from .DashboardManager import (
    DashboardManager, DashboardCreateQueryParams, 
    DashboardMetadata, DashboardGraphMetadata, DashboardMapResponse, DashboardPutQueryParams, DashboardDeleteQueryParams, DashboardLayoutUpdateParams
    )


class Dashboard(BaseModel):
    dashboard_id: int
    dashboard_title: str
    graphs: List[Graph]

class DataVisualizationFacade:
    def __init__(self):
        self.table_manager = TableManager(self.__get_connection)
        self.graph_manager = GraphManager(self.__get_connection)
        self.dashb_manager = DashboardManager(self.__get_connection)

    DB_FNAME = "./unified_db.db"
    def __get_connection(self) -> sqlite3.Connection:
        return closing(sqlite3.connect(self.DB_FNAME))

# ------- dashboard -------
    def get_dashboard_id_mp(self) -> DashboardMapResponse:
        return self.dashb_manager.get_dashboard_id_mp()

    def delete_dashboard(self, query: DashboardDeleteQueryParams):
        self.dashb_manager.delete_dashboard(query=query)

    def add_to_dashboard(self, query: DashboardPutQueryParams) -> Dashboard:
        dashboard_id = self.dashb_manager.add_to_dashboard(query=query)
        return self.render_dashboard(dashboard_id=dashboard_id)

    def create_new_dashboard(self, query: DashboardCreateQueryParams) -> Dashboard:
        for graph_id in query.graph_ids:
            if not self.graph_manager.graph_exists(graph_id):
                raise HTTPException(status_code=404, detail=f"Graph ID {graph_id} does not exist!")
        dashboard_id = self.dashb_manager.create_new_dashboard(query)
        return self.render_dashboard(dashboard_id=dashboard_id)

    def render_dashboard(self, dashboard_id: int) -> Dashboard:
        dashb_metadata = self.dashb_manager.get_dashboard(dashboard_id=dashboard_id)
        graphs = []
        for g in dashb_metadata.metadata_graphs:
            xy_coords = Coordinates(x_coord=g.x_coord, y_coord=g.y_coord)
            plotsize = PlotSize(width=g.width, height=g.height)
            _graph = self.get_graph(g.graph_id, xy_coord=xy_coords, plotsize=plotsize)
            graphs.append(_graph)
        
        return Dashboard(
            dashboard_id=dashboard_id,
            dashboard_title=dashb_metadata.dashboard_title,
            graphs=graphs
        )

    def update_dashboard_layout(self, query: DashboardLayoutUpdateParams) -> Dashboard:
        # First update the layout
        self.dashb_manager.update_dashboard_layout(query=query)
        # Then render and return the dashboard
        return self.render_dashboard(dashboard_id=query.dashboard_id)


# ------- graph -------
    def add_graph(self, query_params: GraphQueryParam) -> Graph:
        graph_id = self.graph_manager.insert_graph_table(query_params)
        return self.get_graph(graph_id=graph_id)

    def get_graph_mp(self) -> GraphMapResponse:
        return self.graph_manager.get_graph_map_response()

    def get_graph(self, graph_id: int, *, 
                  xy_coord: Coordinates=None, plotsize: PlotSize=None) -> Graph:
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
            rows=table_response.rows,
            xy_coords=xy_coord,
            plotsize=plotsize
        )


# ------- table -------
    def get_table(self, table_id: int) -> TableResponse:
        return self.table_manager.get_table_response_by_id(table_id=table_id)

    def get_all_tables_mp(self) -> TableMapResponse:
        return self.table_manager.get_table_id_mp()

    def add_table(self, table_name: str, dataframe: pd.DataFrame) -> TableResponse:
        res = self.table_manager.add_table(table_name, dataframe, tbl_response=True)
        return res