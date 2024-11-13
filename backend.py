import io
from typing import Union, NamedTuple, List, Optional, Any
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
from DataViz import DataVisualizationFacade, TableResponse
import os

app = FastAPI()
db_manager = DataVisualizationFacade()

# @app.get("/")
# return map of all graph ids and their corresponding tables, axes, and info (if no parameters)
class TableQueryParams(BaseModel):
    table_id: Optional[str] = None
    table_ids: Optional[List[str]] = None

    @model_validator(mode='before')
    def check_mutually_exclusive(cls, data: Any) -> Any:
        table_id, table_ids = data.get('table_id'), data.get('table_ids')
        if table_id and table_ids:
            raise HTTPException(status_code=400, detail="'table_id' and 'table_ids' cannot be used together. Please provide only one.")
        return data

def parse_table_query(
        table_id: Optional[str] = None,
        table_ids: Optional[List[str]] = Query(None)
) -> TableQueryParams:
    return TableQueryParams(table_id=table_id, table_ids=table_ids)

@app.get("/tables")
def get_tables(query: TableQueryParams = Depends(parse_table_query)):
    if query.table_id:
        return {'table': query.table_id}
    elif query.table_ids:
        return {'table': query.table_ids}
    else:
        return {'table': "lol"}
    
@app.post("/tables")
async def post_tables(table_name: str, file: UploadFile = File(...)):
    if os.path.splitext(file.filename)[-1] != ".csv":
        raise HTTPException(status_code=404, detail=".csv file was not uploaded!")
    contents = file.file.read()
    buffer = io.BytesIO(contents)
    df = pd.read_csv(buffer)
    success = db_manager.add_table(
        table_name=table_name,
        df=df
    )
    if success:
        pass

# app.get("/graphs") # return map of all graph ids and their corresponding tables, axes, and info (if no parameters)
# app.post("/graphs")

# @app.get("/dashboards")
# @app.post("/dashboards")
