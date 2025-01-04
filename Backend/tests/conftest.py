from pytest import fixture
from mongomock import MongoClient

@fixture
def mock_mongo_connection(monkeypatch):
    # Create a mongomock client
    mongodb_url = "mongo"  # Container name in docker-compose
    mock_client = MongoClient(mongodb_url, port=27017)
    

    # Mock the __init__ method of MongoConnection
    def mock_init(self):
        self.client = mock_client
        self.db = self.client.isbit

    # Apply the monkeypatch
    monkeypatch.setattr("src.db.connection.MongoConnection.__init__", mock_init)