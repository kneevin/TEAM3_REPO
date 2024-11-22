import io
from typing import Dict, List, Tuple, Any
from fastapi import (
    FastAPI, File, UploadFile, Query,
    HTTPException, Response, BackgroundTasks, Depends, Form, Security)
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
    Dashboard, DashboardCreateQueryParams, DashboardMapResponse, 
    DashboardPutQueryParams, DashboardDeleteQueryParams, 
)
import os
from fastapi.middleware.cors import CORSMiddleware
# Add these new models
class DashboardPermission(BaseModel):
    user_email: str
    permission_type: str  # 'view' or 'edit'

class DashboardWithPermissions(BaseModel):
    dashboard_title: str
    permissions: List[DashboardPermission] = []

class DashboardPermissionResponse(BaseModel):
    user_email: str
    permission_type: str

class DeletePermissionParams(BaseModel):
    dashboard_id: int
    user_email: str
    requester_email: str

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

db_manager = DataVisualizationFacade()

@app.get("/tables/map")
def get_table_map() -> TableMapResponse:
    return db_manager.get_all_tables_mp()

@app.get("/tables")
async def get_tables(table_id: int) -> TableResponse:
    return db_manager.get_table(table_id=table_id)
    
@app.post("/tables")
async def post_tables(
    table_name: str = Form(...),
    file: UploadFile = File(...)
) -> TableResponse:
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
async def post_graphs(query_params: GraphQueryParam = Depends()):
    try:
        print("\nAttempting to add graph...")
        result = db_manager.add_graph(query_params)
        print("Graph added successfully")
        return result
    except Exception as e:
        print("\nERROR occurred:")
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        print(f"Error details: {e.__dict__}")
        raise

@app.get("/graphs")
async def get_graphs(graph_id: int) -> Graph:
    return db_manager.get_graph(graph_id=graph_id)

@app.get("/graphs/map") # return map of all graph ids and their corresponding tables, axes, and info (if no parameters)
async def get_graph_map() -> GraphMapResponse:
    return db_manager.get_graph_mp()

@app.get("/dashboards/map")
async def get_dashboard_mp(user_email: str) -> DashboardMapResponse:
    return db_manager.get_dashboard_id_mp(user_email=user_email)

@app.get("/dashboards")
async def get_dashboard(dashboard_id: int, user_email: str) -> Dashboard:
    return db_manager.render_dashboard(dashboard_id=dashboard_id, user_email=user_email)

@app.post("/dashboards")
async def post_new_dashboard(query_params: DashboardCreateQueryParams = Depends()) -> Dashboard:
    return db_manager.create_new_dashboard(query=query_params)

class DashboardPermissionsUpdateParams(BaseModel):
    dashboard_id: int
    permissions: List[DashboardPermission]
    requester_email: str

@app.put("/dashboards/permissions")
async def update_dashboard_permissions(
    query_params: DashboardPermissionsUpdateParams
) -> Dict[str, Any]:
    try:
        db_manager.update_dashboard_permissions(
            dashboard_id=query_params.dashboard_id,
            permissions=query_params.permissions,
            requester_email=query_params.requester_email
        )
        
        # Return a success response dictionary
        return {
            "status": "success",
            "message": "Permissions updated successfully",
            "dashboard_id": query_params.dashboard_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update permissions: {str(e)}"
        )

@app.put("/dashboards")
async def add_new_graphs_dashboard(query_params: DashboardPutQueryParams = Depends()) -> Dashboard:
    return db_manager.add_to_dashboard(query=query_params)

@app.delete("/dashboards")
async def delete_dashboards(query_params: DashboardDeleteQueryParams):
    db_manager.delete_dashboard(query=query_params)

class DashboardLayoutUpdateParams(BaseModel):
    dashboard_id: int
    graph_ids: List[int]
    xy_coords: List[List[int]]
    width_height: List[List[int]]

@app.put("/dashboards/layout")
async def update_dashboard_layout(query_params: DashboardLayoutUpdateParams) -> None:
    return db_manager.update_dashboard_layout(query=query_params)

@app.get("/dashboards/{dashboard_id}/permissions")
async def get_dashboard_permissions(
    dashboard_id: int,
    requester_email: str
) -> List[DashboardPermissionResponse]:
    try:
        permissions = db_manager.get_dashboard_permissions(
            dashboard_id=dashboard_id,
            requester_email=requester_email
        )
        return permissions
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get permissions: {str(e)}"
        )

@app.delete("/dashboards/permissions")
async def delete_dashboard_permission(
    query_params: DeletePermissionParams
) -> Dict[str, Any]:
    try:
        db_manager.delete_dashboard_permission(
            dashboard_id=query_params.dashboard_id,
            user_email=query_params.user_email,
            requester_email=query_params.requester_email
        )
        
        return {
            "status": "success",
            "message": "Permission deleted successfully",
            "dashboard_id": query_params.dashboard_id,
            "user_email": query_params.user_email
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete permission: {str(e)}"
        )
