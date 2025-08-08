from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.ingest import process_audio_file
import os
import json

app = FastAPI()
UPLOAD_DIR = "static/uploaded_tracks"
os.makedirs(UPLOAD_DIR, exist_ok=True)

library = []

@app.post("/upload")
async def upload_track(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())
    
    track_data = process_audio_file(filepath)
    library.append(track_data)

    with open("library.json", "w") as f:
        json.dump(library, f, indent=2)
    
    return JSONResponse(content=track_data)

@app.get("/library")
def get_library():
    return JSONResponse(content=library)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
