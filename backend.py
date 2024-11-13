import io
from typing import Union, NamedTuple, List
from fastapi import (
    FastAPI, File, UploadFile, 
    HTTPException, Response, BackgroundTasks)
from pydantic import BaseModel
import csv
import pandas as pd
import codecs
from TableManager import TableManager
from GraphManager import GraphManager, Graph, Axes
from DashboardManager import DashboardManager, Dashboard
import os

app = FastAPI()
tb = TableManager()
gm = GraphManager()
dbm = DashboardManager()

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    if os.path.splitext(file.filename)[-1] != ".csv":
        raise HTTPException(status_code=404, detail=".csv file was not uploaded!")
    table_name, _ = os.path.splitext(file.filename)

    contents = file.file.read()
    buffer = io.BytesIO(contents)
    df = pd.read_csv(buffer)
    tb.add_table(
        table_name=table_name,
        dataframe=df
    )
    return tb.get_all_table_columns()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create_dashboard")
def post_dashboard(dashboard_title: str, graphs: List[Graph]) -> Dashboard:
    pass

@app.post("/team6_callback")
def team6_ingestion():
    pass
# @app.post("/{dashboard_id}")
# def get_

@app.get("/dashboard_id_map")
def get_dashboard_id_map():
    return {"dashboards": dbm.get_dashboard_id_mp()}

@app.get("/get_table/{table_id}")
def get_table(table_id: str):
    if not tb.table_exists(table_id):
        raise HTTPException(status_code=404, detail=f"Table {table_id} does not exist.")
    df = tb.get_table_data(table_id)
    return jsonify_df(df, table_id=table_id)

@app.get("/get_all_tables_and_columns")
def get_all_table_columns():
    return tb.get_all_table_columns()

@app.get("/table_id_map")
def get_table_id_mapping():
    return tb.get_table_id_mp()

@app.get("/graph_id_map")
def get_graph_id_mapping():
    return {"graphs": gm.get_graph_id_map()}

@app.get("/get_graph")
def get_graph(table_id: int, graph_id: int):
    graph_mp = gm.get_graph(graph_id=graph_id)
    data = tb.get_table_id_graph(table_id, graph_mp['ax0'], graph_mp['ax1'])
    return Graph(
        graph_id=graph_mp['graph_id'],
        graph_title=graph_mp['graph_title'],
        graph_type=graph_mp['graph_type'],
        ax=Axes(ax0=graph_mp['ax0'], ax1=graph_mp['ax1']),
        data=data.values.tolist()
    )

@app.post("/create_graph/{table_name}")
def create_graph(table_name: str, graph_title: str, graph_type: str, ax0: str, ax1: str) -> Graph:
    """
    ax0: x_axis
    ax1: y_axis
    """
    if not tb.table_exists(table_name):
        raise HTTPException(status_code=404, detail=f"Table {table_name} does not exist.")
    graph_mp = gm.add_graph(
        table_id=table_name,
        graph_title=graph_title,
        graph_type=graph_type,
        ax0=ax0,
        ax1=ax1
    )

    df_graph = tb.get_table_graph(table_name=table_name, ax0=ax0, ax1=ax1)

    return create_graph_response(
        df=df_graph,
        graph_id=graph_mp['graph_id'],
        graph_title=graph_mp['graph_title'],
        graph_type=graph_mp['graph_type'],
        ax0=graph_mp['ax0'],
        ax1=graph_mp['ax1']
    )

def create_graph_response(
        df: pd.DataFrame, 
        graph_id: int,
        graph_title: str, 
        graph_type: str, 
        ax0: str, 
        ax1: str) -> Graph:
    json_df = jsonify_df(df)
    return Graph(
        graph_id=graph_id,
        graph_title=graph_title,
        graph_type=graph_type,
        ax=Axes(ax0=ax0, ax1=ax1),
        data=json_df['data']
    )



def jsonify_df(df: pd.DataFrame, table_id: str | None = None):
    if not table_id:
        return {
            'columns': list(df.columns),
            'data': df.values.tolist()
        }
    else:
        return {
            'table_id': table_id,
            'columns': list(df.columns),
            'data': df.values.tolist()
        }