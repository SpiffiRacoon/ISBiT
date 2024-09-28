import pymongo


class MongoConnection:
    """
    Context manager for MongoDB connection. This way the connection is always the same and
    closed after usage.

    Example usage:
    ```python
    with MongoConnection() as (_, db):
        db["test"].insert_one({"test": "first"})
    ```

    """

    def __init__(self):
        mongodb_url = "mongo"  # Container name in docker-compose
        self.client = pymongo.MongoClient(mongodb_url, port=27017)
        self.db = self.client.isbit

    def __enter__(self):
        return (self.client, self.db)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
