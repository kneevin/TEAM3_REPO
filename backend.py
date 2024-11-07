import io
from typing import Union
from fastapi import (
    FastAPI, File, UploadFile, 
    HTTPException, Response, BackgroundTasks)
from pydantic import BaseModel
import csv
import pandas as pd
import codecs
from TableManager import TableManager
from GraphManager import GraphManager
import os

app = FastAPI()
tb = TableManager()
gm = GraphManager()

# @app.post("/upload_csv")
# @app.post("/get_table_columns/{table_name}")
# @app.post("/create_graph/{table_name}/{graph_name}/{x_axis}/{y_axis}")
# @app.post("/get_dashboard/{dashboard_id}")
# @app.post("")

@app.post("/upload_csv")
def upload_csv(file: UploadFile = File(...)):
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

@app.get("/get_table/{table_id}")
def get_table(table_id: str):
    if not tb.table_exists(table_id):
        raise HTTPException(status_code=404, detail=f"Table {table_id} does not exist.")
    df = tb.get_table_data(table_id)
    return jsonify_df(df, table_id=table_id)

@app.get("/get_all_tables_and_columns")
def get_all_table_columns():
    return tb.get_all_table_columns()

@app.post("/create_graph/{table_name}")
def create_graph(table_name: str, graph_name: str, x_axis: str, y_axis: str):
    return table_name

def jsonify_df(df: pd.DataFrame, table_id: str):
    return {
        'table_id': table_id,
        'columns': list(df.columns),
        'data': df.values.tolist()
    }