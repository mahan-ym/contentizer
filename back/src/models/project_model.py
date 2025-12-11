from pydantic import BaseModel
from datetime import datetime

class ProjectModel(BaseModel):
    project_id: str
    project_file_id: str
    user_id: str
    project_location: str
    thumbnail: str
    last_edited: datetime
    name: str