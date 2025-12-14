import os
import shutil
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from src.services.uuid import gen_uuid_str
from src.repository.project_repository import ProjectRepository
from src.models.project_model import ProjectModel
from src.services.mongo_client import MongoClientSingleton
from src.global_constants import ASSETS_DIR, THUMBNAILS_DIR
from src.services.video_edit import gen_thumbnail
from datetime import datetime
from logging import Logger

logger = Logger("routes_logger")

router = APIRouter()

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(THUMBNAILS_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        project_unique_id = gen_uuid_str()
        os.mkdir(
            os.path.join(ASSETS_DIR, project_unique_id)
        )  # Create project directory
        project_directory = os.path.join(ASSETS_DIR, project_unique_id)
        new_filename = f"{gen_uuid_str()}{file.filename}"
        file_path = os.path.join(project_directory, new_filename)
        relative_file_path = os.path.join(project_unique_id, new_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(
            f"File uploaded successfully: {file_path} \n new_filename: {new_filename} \n relative_file_path: {relative_file_path}"
        )
        # Generate thumbnail
        result_thumbnail_path = gen_thumbnail(relative_file_path)
        logger.info(f"Thumbnail generated at: {result_thumbnail_path}")
        # create project entry in DB
        mongo_client = MongoClientSingleton()
        with ProjectRepository(mongo_client) as project_repository:
            project_repository.create_project(
                data=ProjectModel(
                    name=file.filename,
                    project_id=project_unique_id,
                    user_id="0",
                    project_directory=f"{project_unique_id}/",
                    last_edited=datetime.now().isoformat(),
                    thumbnail=result_thumbnail_path,
                    project_versions=[
                        {
                            "version": "0",
                            "project_tracks": [
                                {
                                    "track_location": relative_file_path,
                                    "track_start_time": "00:00:00",
                                    "track_type": "video",
                                }
                            ],
                        }
                    ],
                )
            )

        logger.info(f"Project created in DB with ID: {project_unique_id}")
        return {
            "project": project_unique_id,
            "url": f"/api/stream/{relative_file_path}",
        }
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent_projects", response_model=list[ProjectModel])
async def get_recent_projects():
    mongo_client = MongoClientSingleton()
    with ProjectRepository(mongo_client) as project_repository:
        projects = project_repository.get_user_projects(user_id="0", count=10, index=0)
        return [project for project in projects]
    logger.info("No recent projects found.")
    return []


@router.get("/thumbnails/{filepath:path}")
async def get_thumbnail(filepath: str):
    if not os.path.exists(filepath):
        logger.error(f"Thumbnail not found at path: {filepath}")
        raise HTTPException(status_code=404, detail="Thumbnail not found")

    def iterfile():
        with open(filepath, "rb") as thumbnail:
            yield thumbnail.read()

    return StreamingResponse(iterfile(), media_type="image/jpeg")


@router.get("/stream/{filepath:path}")
async def stream_video(filepath: str, range: Optional[str] = None):
    full_path = os.path.join(ASSETS_DIR, filepath)
    if not os.path.exists(full_path):
        logger.error(f"File not found at path: {full_path}")
        raise HTTPException(status_code=404, detail="File not found")

    file_size = os.path.getsize(full_path)
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
        with open(full_path, "rb") as video:
            video.seek(start)
            yield video.read(chunk_size)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": "video/mp4",
    }

    return StreamingResponse(iterfile(), status_code=206, headers=headers)
