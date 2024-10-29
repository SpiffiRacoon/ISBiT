from bson import ObjectId
from .connection import MongoConnection
from ..types import Node


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

