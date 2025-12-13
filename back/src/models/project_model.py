from pydantic import BaseModel, Field
from datetime import datetime


class ProjectTracksModel(BaseModel):
    track_location: str
    track_start_time: str


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


# project_file_id removed
