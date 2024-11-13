import io
from typing import Union, NamedTuple, List
from fastapi import (
    FastAPI, File, UploadFile, 
    HTTPException, Response, BackgroundTasks)
from pydantic import BaseModel
import csv
import pandas as pd
import codecs
from DataViz.TableManager import TableManager
from DataViz.GraphManager import GraphManager, Graph, Axes
from DataViz.DashboardManager import DashboardManager, Dashboard
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



# @app.get("/")
# @app.post("/create_dashboard")
# @app.post("/team6_callback")
# @app.post("/{dashboard_id}")
# @app.get("/dashboard_id_map")
# @app.get("/get_table/{table_id}")
# @app.get("/get_all_tables_and_columns")
# @app.get("/table_id_map")
# @app.get("/graph_id_map")
# @app.get("/get_graph")
# @app.post("/create_graph/{table_name}")
