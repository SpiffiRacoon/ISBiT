from .connection import MongoConnection
from ..types import Node


def get_all_nodes_from(collection: str, ConnectionClass=MongoConnection) -> list[Node]:
    """
    Get all nodes from a collection
    """
    with ConnectionClass() as (_, db):
        nodes = db[collection].find()
        return [Node(**one_node) for one_node in nodes]


def get_all_collections(ConnectionClass=MongoConnection) -> list:
    """
    Get all collections in database
    """
    with ConnectionClass() as (_, db):
        collections = db.list_collection_names()
        return list(collections)
