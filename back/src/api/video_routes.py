from fastapi import APIRouter, HTTPException
import ffmpeg
import os
from pydantic import BaseModel
from typing import List
from src.repository.project_repository import ProjectRepository
from src.services.mongo_client import MongoClientSingleton
from src.services.video_edit import (
    probe,
    trim,
    get_video_duration,
    get_video_metadata,
    concatenate_videos,
    add_video_to_sequence,
)
from src.services.uuid import gen_uuid_str
from src.global_constants import ASSETS_DIR
from src.models.project_model import ProjectTracksModel
from logging import Logger

router = APIRouter()
logger = Logger("video_routes")


class TrimRequest(BaseModel):
    project_location: str
    start_time: float
    end_time: float


class AddVideoRequest(BaseModel):
    project_id: str
    video_path: str


class ConcatenateRequest(BaseModel):
    project_id: str
    output_filename: str = None


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
        logger.error(f"FFmpeg error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"FFmpeg error: {str(e)}")


@router.get("/get_info/{project_id}")
async def get_video_info(project_id: str):
    try:
        mongo_client = MongoClientSingleton()

        with ProjectRepository(mongo_client) as project_repository:
            project = project_repository.get_project(project_id)
            if not project:
                logger.error("Project not found")
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
        logger.error(f"Error retrieving project: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving project: {str(e)}"
        )


@router.post("/add_video")
async def add_video_to_project(request: AddVideoRequest):
    """Add a video to the project timeline after existing videos"""
    try:
        mongo_client = MongoClientSingleton()

        with ProjectRepository(mongo_client) as project_repository:
            project = project_repository.get_project(request.project_id)
            if not project:
                logger.error("Project not found")
                raise HTTPException(status_code=404, detail="Project not found")

            # Get existing tracks
            project_tracks = project["project_versions"][-1]["project_tracks"]

            # Normalize video path - remove ASSETS_DIR prefix if present
            video_path = request.video_path
            if video_path.startswith(ASSETS_DIR):
                # Remove the ASSETS_DIR prefix and any leading slashes
                video_path = video_path[len(ASSETS_DIR) :].lstrip("/")

            # Verify the actual file exists
            full_path = os.path.join(ASSETS_DIR, video_path)
            if not os.path.exists(full_path):
                logger.error(f"Video file not found: {full_path}")
                raise HTTPException(status_code=404, detail="Video file not found")

            # Calculate start time for new video
            start_time = add_video_to_sequence(project_tracks, video_path)

            # Get video metadata
            metadata = get_video_metadata(video_path)
            if not metadata:
                logger.error("Invalid video file metadata")
                raise HTTPException(status_code=400, detail="Invalid video file")

            # Create new track
            new_track = {
                "track_location": video_path,
                "track_start_time": start_time,
                "track_duration": metadata["duration"],
                "track_type": "video",
            }

            # Add track to project
            project_tracks.append(new_track)

            # Update project in database
            project_repository.update_project(
                request.project_id, {"project_versions": project["project_versions"]}
            )

            return {
                "message": "Video added successfully",
                "track": new_track,
                "total_tracks": len(project_tracks),
            }

    except Exception as e:
        logger.error(f"Error adding video to project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding video: {str(e)}")


@router.post("/concatenate")
async def concatenate_project_videos(request: ConcatenateRequest):
    """Concatenate all videos in a project into a single output file"""
    try:
        mongo_client = MongoClientSingleton()

        with ProjectRepository(mongo_client) as project_repository:
            project = project_repository.get_project(request.project_id)
            if not project:
                logger.error("Project not found")
                raise HTTPException(status_code=404, detail="Project not found")

            # Get all video tracks sorted by start time
            project_tracks = sorted(
                project["project_versions"][-1]["project_tracks"],
                key=lambda x: x.get("track_start_time", 0),
            )

            if len(project_tracks) < 1:
                logger.error("No videos to concatenate")
                raise HTTPException(status_code=400, detail="No videos to concatenate")

            # Extract video paths
            video_paths = [track["track_location"] for track in project_tracks]

            # Generate output filename
            output_filename = (
                request.output_filename
                or f"{request.project_id}_concatenated_{gen_uuid_str()}.mp4"
            )

            # Concatenate videos
            output_path = concatenate_videos(video_paths, output_filename)

            if not output_path:
                logger.error("Failed to concatenate videos: output_path is None")
                raise HTTPException(
                    status_code=500, detail="Failed to concatenate videos"
                )

            return {
                "message": "Videos concatenated successfully",
                "output_path": output_filename,
                "url": f"/api/stream/{output_filename}",
            }

    except Exception as e:
        logger.error(f"Error concatenating videos: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error concatenating videos: {str(e)}"
        )
    
@router.get("/video_duration/{file_path:str}")
async def get_video_duration_endpoint(file_path: str):
    """Get the duration of a video file"""
    get_video_duration(file_path)

