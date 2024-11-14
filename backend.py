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
from DataViz import DataVisualizationFacade, TableResponse, TableMapResponse, GraphQueryParam
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

# app.get("/graphs") # return map of all graph ids and their corresponding tables, axes, and info (if no parameters)
@app.post("/graphs")
async def post_graphs(query_params: GraphQueryParam = Depends()):
    db_manager.add_graph(query_params)

# @app.get("/dashboards")
# @app.post("/dashboards")
