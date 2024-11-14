import io
from typing import Dict
from fastapi import (
    FastAPI, File, UploadFile, Query,
    HTTPException, Response, BackgroundTasks, Depends)
from pydantic import BaseModel, model_validator
import csv
import pandas as pd
import codecs
# from DataViz.TableManager import TableManager
# from DataViz.GraphManager import GraphManager, Graph, Axes
# from DataViz.DashboardManager import DashboardManager, Dashboard
from DataViz import (
    DataVisualizationFacade, 
    TableResponse, TableMapResponse, 
    GraphQueryParam, Graph, GraphMapResponse,
    Dashboard, DashboardCreateQueryParams, DashboardMapResponse, DashboardPutQueryParams
)
import os

app = FastAPI()
db_manager = DataVisualizationFacade()

@app.get("/tables/map")
def get_table_map() -> TableMapResponse:
    return db_manager.get_all_tables_mp()

@app.get("/tables")
async def get_tables(table_id: int) -> TableResponse:
    return db_manager.get_table(table_id=table_id)
    
@app.post("/tables")
async def post_tables(table_name: str, file: UploadFile = File(...)) -> TableResponse:
    if os.path.splitext(file.filename)[-1] != ".csv":
        raise HTTPException(status_code=404, detail=".csv file was not uploaded!")
    contents = file.file.read()
    buffer = io.BytesIO(contents)
    df = pd.read_csv(buffer)
    tbl_res = db_manager.add_table(
        table_name=table_name,
        dataframe=df
    )
    return tbl_res

# app.get("/graphs") 
@app.post("/graphs")
async def post_graphs(query_params: GraphQueryParam = Depends()) -> Graph:
    return db_manager.add_graph(query_params)

@app.get("/graphs")
async def get_graphs(graph_id: int) -> Graph:
    return db_manager.get_graph(graph_id=graph_id)

@app.get("/graphs/map") # return map of all graph ids and their corresponding tables, axes, and info (if no parameters)
async def get_graph_map() -> GraphMapResponse:
    return db_manager.get_graph_mp()

@app.get("/dashboards/map")
async def get_dashboard_mp() -> DashboardMapResponse:
    return db_manager.get_dashboard_id_mp()

@app.get("/dashboards")
async def get_dashboard(dashboard_id: int) -> Dashboard:
    return db_manager.render_dashboard(dashboard_id=dashboard_id)

@app.post("/dashboards")
async def post_new_dashboard(query_params: DashboardCreateQueryParams = Depends()) -> Dashboard:
    return db_manager.create_new_dashboard(query=query_params)

@app.put("/dashboards")
async def add_new_graphs_dashboard(query_params: DashboardPutQueryParams = Depends()) -> Dashboard:
    return db_manager.add_to_dashboard(query=query_params)
