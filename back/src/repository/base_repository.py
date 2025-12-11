from pymongo import MongoClient
from src.services.mongo_client import MongoClientSingleton


class BaseRepository:
    def __init__(self, mongo: MongoClientSingleton):
        self._mongo_instance = mongo
        self._mongo_client = mongo.get_client()
        self.database = self._mongo_client['Contentizer']

    @property
    def mongo_client(self) -> MongoClient:
        return self._mongo_client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._mongo_instance.close_client()
        self._mongo_instance = None