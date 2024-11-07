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
    return {"tables" : tb.get_all_table_names()}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_tables")
def get_tables():
    return { "table names" : tb.get_tables() }

@app.get("/get_all_table_columns")
def get_all_table_columns():
    return tb.get_all_table_columns()

@app.post("/create_graph/{table_name}")
def create_graph(table_name: str, graph_name: str, x_axis: str, y_axis: str):
    return table_name