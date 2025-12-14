from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class ProjectTracksModel(BaseModel):
    track_location: str
    track_start_time: float 
    track_duration: Optional[float] = None  # Duration in seconds
    track_type: str = "video" 

    @field_validator("track_start_time", mode="before")
    @classmethod
    def convert_time_to_float(cls, v):
        """Convert time string (HH:MM:SS) to float seconds, or pass through float"""
        if isinstance(v, str):
            # Parse HH:MM:SS format
            parts = v.split(":")
            if len(parts) == 3:
                hours, minutes, seconds = map(float, parts)
                return hours * 3600 + minutes * 60 + seconds
            elif len(parts) == 2:
                minutes, seconds = map(float, parts)
                return minutes * 60 + seconds
            else:
                return float(v)
        return float(v)


class ProjectFilesModel(BaseModel):
    version: str
    project_tracks: list[ProjectTracksModel] = Field(default_factory=list)


class ProjectModel(BaseModel):
    project_id: str
    user_id: str
    project_directory: str
    project_versions: list[ProjectFilesModel] = Field(default_factory=list)
    thumbnail: str
    last_edited: datetime
    name: str
