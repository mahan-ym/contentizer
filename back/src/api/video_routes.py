from fastapi import APIRouter, HTTPException
import ffmpeg
import os
from pydantic import BaseModel
from src.repository.project_repository import ProjectRepository
from src.services.mongo_client import MongoClientSingleton
from src.services.video_edit import probe, trim
from src.services.uuid import gen_uuid_str
from src.global_constants import ASSETS_DIR

router = APIRouter()


class TrimRequest(BaseModel):
    project_location: str
    start_time: float
    end_time: float


# we keep the project id so that the project folder would be same
@router.post("/trim")
async def trim_video(request: TrimRequest):
    input_path = os.path.join(ASSETS_DIR, request.project_location)
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_path = os.path.join(
        ASSETS_DIR, (request.project_location + f"_{gen_uuid_str()}.mp4")
    )

    try:
        trim(
            input_path, output_path, float(request.start_time), float(request.end_time)
        )
        return {"url": f"/api/stream/{os.path.basename(output_path)}"}
    except ffmpeg.Error as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")


@router.get("/get_info/{project_id}")
async def get_video_info(project_id: str):
    try:
        mongo_client = MongoClientSingleton()

        with ProjectRepository(mongo_client) as project_repository:
            project = project_repository.get_project(project_id)
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            project_tracks = project["project_versions"][-1]["project_tracks"]
            probe_results = []
            for track in project_tracks:
                probe_results.append(probe(track["track_location"]))
            project.pop("_id", None)
            return {
                "project": project,
                "probe": probe_results,
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving project: {str(e)}"
        )
