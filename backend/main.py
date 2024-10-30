from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from PIL import Image
from io import BytesIO
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    return {"message": "Notebook uploaded successfully", "filename": file.filename}

@app.get("/notebook/{filename}")
async def run_notebook(filename: str):
    notebook_path = f"{UPLOAD_FOLDER}/{filename}"
    if not os.path.exists(notebook_path):
        return JSONResponse({"error": "Notebook not found"}, status_code=404)
    
    images = execute_notebook_and_extract_images(notebook_path)
    return JSONResponse(images)

@app.get("/notebooks")
async def list_notebooks():
    notebooks = os.listdir(UPLOAD_FOLDER)
    return JSONResponse(notebooks)

def execute_notebook_and_extract_images(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(notebook, {'metadata': {'path': UPLOAD_FOLDER}})
    
    images = []
    for cell in notebook.cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'data' in output and 'image/png' in output['data']:
                    image_data = base64.b64decode(output['data']['image/png'])
                    img = Image.open(BytesIO(image_data))
                    
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode()
                    images.append(img_base64)
    
    return images