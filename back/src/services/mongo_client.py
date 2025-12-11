from pymongo import MongoClient

class MongoClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoClientSingleton, cls).__new__(cls)
            cls._instance._client = None
        return cls._instance

    def __init__(self):
        if self._client is None:
            mongo_uri = 'mongodb://root:rootpassword@localhost:27017'
            self._client = MongoClient(mongo_uri)

    def close_client(self):
        if self._client is not None:
            self._client.close()
            self._client = None

    def get_client(self):
        return self._client