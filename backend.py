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
import os


class Dashboard(BaseModel):
    pass


app = FastAPI()
tb = TableManager()

# @app.post("/upload_csv")
# @app.post("/get_table_columns/{table_name}")
# @app.post("/create_graph/{table_name}/{graph_name}/{x_axis}/{y_axis}")
# @app.post("/get_dashboard/{dashboard_id}")
# @app.post("")
# @app.post("")




@app.post("/upload_csv")
def upload_csv(file: UploadFile = File(...)):
    print(file)
    if os.path.splitext(file.filename)[-1] != ".csv":
        raise HTTPException(status_code=404, detail=".csv file was not uploaded!")
    
    contents = file.file.read()
    buffer = io.BytesIO(contents)
    df = pd.read_csv(buffer)
    print(df)
    tb.add_table(file.filename, df)

    return get_all_table_columns()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_graph_types")
def get_graph_types():
    return tb.get_graph_types()

@app.get("/get_tables")
def get_tables():
    return { "table names" : tb.get_tables() }

@app.get("/get_all_table_columns")
def get_all_table_columns():
    return tb.get_all_table_columns()

@app.get("/{graph_type}/{table_id}/{x_column}/{y_column}")
async def graph_table(background_tasks: BackgroundTasks, graph_type: str, table_id: str, x_column: str, y_column: str):
    if not tb.table_exists(table_id): 
        raise HTTPException(status_code=404, detail=f"Table {table_id} does not exist.")
    
    if not tb.graph_exists(graph_type):
        return HTTPException(status_code=404, detail="Graph type does not exist.")
    
    fig = tb.graph_table(
        graph_type=graph_type,
        table_id=table_id,
        x_column=x_column,
        y_column=y_column
    )

    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')

    bufContents: bytes = img_buf.getvalue()
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(bufContents, headers=headers, media_type='image/png')

@app.get('/get_static_image')
async def get_img(background_tasks: BackgroundTasks):
    df = pd.read_csv("./data.csv")
    g = df.plot(kind='line', x='X', figsize=(8, 4))

    img_buf = io.BytesIO()
    g.figure.savefig(img_buf, format='png')

    bufContents: bytes = img_buf.getvalue()
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(bufContents, headers=headers, media_type='image/png')