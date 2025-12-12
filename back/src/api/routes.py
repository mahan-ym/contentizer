import os
import shutil
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.services.uuid import gen_uuid_str
from src.repository.project_repository import ProjectRepository
from src.models.project_model import ProjectModel
from src.services.mongo_client import MongoClientSingleton
from datetime import datetime

router = APIRouter()

# Define assets directory relative to project root (back/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)

class PromptRequest(BaseModel):
    prompt: str
    filename: str

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        project_unique_id = gen_uuid_str()
        os.mkdir(os.path.join(ASSETS_DIR, project_unique_id))
        new_project_directory = os.path.join(ASSETS_DIR, project_unique_id)
        new_filename = f"{gen_uuid_str()}{file.filename}"
        project_location = os.path.join(project_unique_id, new_filename)

        file_path = os.path.join(new_project_directory, new_filename)
        mongo_client = MongoClientSingleton()
        with ProjectRepository(mongo_client) as project_repository:
            project_repository.create_project(data = ProjectModel(
                name=file.filename,
                project_id=project_unique_id,
                project_file_id=new_filename,
                user_id="0",
                project_location=project_location,
                last_edited= datetime.now().isoformat(),
                thumbnail="https://placehold.co/400"
                ))
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": new_filename, "url": f"/api/stream/{new_filename}"}
    except Exception as e:
        print(e.__str__())
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent_projects", response_model=list[ProjectModel])
async def get_recent_projects():
    mongo_client = MongoClientSingleton()
    with ProjectRepository(mongo_client) as project_repository:
        projects = project_repository.get_user_projects(user_id="0", count=10, index=0)
        return [project for project in projects]
    return []

@router.get("/stream/{filename}")
async def stream_video(filename: str, range: Optional[str] = None):
    mongo_client = MongoClientSingleton()
    project_path = ""
    with ProjectRepository(mongo_client) as project_repository:
        project = project_repository.get_project_by_file_id(filename)
        project_path = project["project_location"]
    file_path = os.path.join(ASSETS_DIR, project_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_size = os.path.getsize(file_path)
        
    start = 0
    end = file_size - 1
    
    if range:
        range_str = range.replace("bytes=", "")
        range_parts = range_str.split("-")
        if range_parts[0]:
            start = int(range_parts[0])
        if len(range_parts) > 1 and range_parts[1]:
            end = int(range_parts[1])
            
    chunk_size = end - start + 1
    
    def iterfile():
        with open(file_path, "rb") as video:
            video.seek(start)
            yield video.read(chunk_size)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": "video/mp4",
    }
    
    return StreamingResponse(iterfile(), status_code=206, headers=headers)

@router.post("/agent/prompt")
async def get_agent_prompt(request: PromptRequest):
    print(f"Received prompt for {request.filename}: {request.prompt}")
    
