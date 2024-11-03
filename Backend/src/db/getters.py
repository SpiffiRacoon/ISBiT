from bson import ObjectId
# str
from datetime import datetime

# own
from .connection import MongoConnection
from ..types import Node, MlStatus

# pip
from pandas.core.arrays import boolean


def get_all_nodes_from(collection: str, ConnectionClass=MongoConnection) -> list[Node]:
    """
    Get all nodes from a collection.
    """
    with ConnectionClass() as (_, db):
        documents = db[collection].find()
        nodes = []
        for doc in documents:
            if 'data' in doc:
                for data_item in doc['data']:
                    if isinstance(data_item.get("id"), ObjectId): # TODO: if we swap to hash ids this conversion should not be needed.
                        data_item["id"] = str(data_item["id"])
            nodes.extend([Node(**data_item) for data_item in doc['data']])
                
        return nodes

def get_all_collections(ConnectionClass=MongoConnection) -> list:
    """
    Get all collections in database
    """
    with ConnectionClass() as (_, db):
        collections = db.list_collection_names()
        return list(collections)

def get_all_labels_from(collection: str, ConnectionClass=MongoConnection) -> list[dict]:
    """
    Get list document with labels from a collection. 
    """
    
    with ConnectionClass() as (_, db):
        labels = list(db[collection].find({}, {"about.labels" : 1, "_id": 0}))
        return labels


        all_datasets = list(collections)
        all_datasets.remove("ml_status")

        return all_datasets

def get_ml_status(id: str, ConnectionClass=MongoConnection) -> MlStatus:
    """
    Get a dict with info about the ML run
    """

    with ConnectionClass() as (_, db):
        query = {"ml_id": id}

        result = db["ml_status"].find_one(query)
        if result is None:
            return MlStatus(ml_id=id, status="Not running", details="Not found")

        return MlStatus(**result)
