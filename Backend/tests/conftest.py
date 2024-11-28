from pytest import fixture
from mongomock import MongoClient

@fixture
def mock_mongo_connection(monkeypatch):
    # Create a mongomock client
    mock_client = MongoClient()

    # Mock the __init__ method of MongoConnection
    def mock_init(self):
        self.client = mock_client
        self.db = mock_client["test_db"]

    # Apply the monkeypatch
    monkeypatch.setattr("src.db.connection.MongoConnection.__init__", mock_init)

    # Return the mock client to use in the tests if needed
    yield mock_client