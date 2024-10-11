from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Allow CORS to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FOLDER = './data/'

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    file_location = f"{DATA_FOLDER}{file.filename}"
    
    with open(file_location, "wb+") as f:
        f.write(file.file.read())
    
    return {"message": f"File '{file.filename}' uploaded successfully"}

@app.get("/csv_files/")
async def get_csv_files():
    files = os.listdir(DATA_FOLDER)
    return {"files": files}

@app.get("/get_data/{filename}")
async def get_data(filename: str):
    file_path = f"{DATA_FOLDER}{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')
