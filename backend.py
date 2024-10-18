import io
from typing import Union
from fastapi import (
    FastAPI, File, UploadFile, 
    HTTPException, Response, BackgroundTasks)
import csv
import pandas as pd
import codecs
from TableManager import TableManager

app = FastAPI()
tb = TableManager()

@app.post("/upload_csv")
def upload_csv(file: UploadFile = File(...)):

    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    data = {}
    for rows in csvReader:
        key = rows['X']
        data[key] = rows  
    file.file.close()

    df = pd.DataFrame(data)
    tb.add_table(file.filename, df)
    return data

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_graph_types")
def get_graph_types():
    return tb.get_graph_types()

@app.get("/get_tables")
def get_tables():
    return { "table names" : tb.get_tables() }

@app.get("/{graph_type}/{table_id}/{x_column}/{y_column}")
async def graph_table(graph_type: str, table_id: str, x_column: str, y_column: str):
    if not tb.table_exists(table_id):
        raise HTTPException(status_code=404, detail="Table does not exist.")
    if not tb.graph_exists(graph_type):
        return HTTPException(status_code=404, detail="Graph type does not exist.")
    
    return { 
        table_id: {"X": x_column, "Y": y_column}
    }


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