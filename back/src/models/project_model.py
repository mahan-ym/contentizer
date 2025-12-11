from pydantic import BaseModel

class ProjectModel(BaseModel):
    project_id: str
    project_file_id: str
    user_id: str
    project_location: str