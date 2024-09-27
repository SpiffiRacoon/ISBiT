import pymongo

class MongoConnection:
    """
    Context manager for MongoDB connection
    """
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", port=27017)
        self.db = self.client.isbit

    def __enter__(self):
        return (self.client, self.db)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
