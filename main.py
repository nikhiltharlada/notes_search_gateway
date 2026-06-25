from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import requests
import os

from shared_data.storage import upload_file as supabase_upload
from shared_data.storage import delete_all
from shared_data.storage import list_files
app=FastAPI()

@app.get("/")
def home():
    return {"message": "Notes Search Engine API Running"}


@app.get("/health")
def health():
    return {"status": "running"}
class ChatRequest(BaseModel):
    question:str
# RAG_URL = "https://nikhiltharlada-notes-search-rag.hf.space"
RAG_URL = os.getenv("RAG_SERVICE_URL")

@app.post("/chat")
def chat(request: ChatRequest):

    try:
        response = requests.post(
            f"{RAG_URL}/chat",
            json={
                "question": request.question
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:
        os.makedirs("data", exist_ok=True)

        file_path = os.path.join("data", file.filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        supabase_upload(
        file_path,
        f"uploads/{file.filename}"
        )
        os.remove(file_path)

        return {
            "message": "File uploaded successfully",
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.delete("/delete-files")
def delete_files():

    # Delete from Supabase
    delete_all("uploads")
    delete_all("vectors")

    # Delete local data folder
    folder_path = "data"

    if os.path.exists(folder_path):

        for filename in os.listdir(folder_path):

            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)

    return {
        "message": "All files and vectors deleted successfully"
    }
@app.get("/files")
def files():
    try:
        files = list_files("uploads")

        filenames = [file["name"] for file in files]

        return {"files": filenames}

    except Exception as e:
        return {"error": str(e)}