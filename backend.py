from typing import Union
from fastapi import FastAPI, File, UploadFile
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

