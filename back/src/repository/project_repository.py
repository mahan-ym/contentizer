from src.repository.base_repository import BaseRepository
from src.models.project_model import ProjectModel
from src.services.mongo_client import MongoClientSingleton


class ProjectRepository(BaseRepository):
    def __init__(self, mongo: MongoClientSingleton):
        super().__init__(mongo)

    def get_user_projects(self, user_id, count, index) -> list[ProjectModel]:
        cursor = (
            self.database["projects"]
            .find({"user_id": user_id})
            .skip(index)
            .limit(count)
        )
        return [ProjectModel(**project) for project in cursor]

    def get_project(self, project_id: str) -> ProjectModel:
        return self.database["projects"].find_one({"project_id": project_id})

    def create_project(self, data: ProjectModel):
        return self.database["projects"].insert_one(data.dict())

    def get_project_by_file_id(self, project_file_id: str) -> ProjectModel:
        return self.database["projects"].find_one({"project_file_id": project_file_id})
