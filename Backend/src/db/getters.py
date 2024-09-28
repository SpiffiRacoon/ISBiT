from .connection import MongoConnection
from ..types import Node


def get_all_nodes_from(collection: str) -> list[Node]:
    """
    Get all nodes from a collection
    """
    with MongoConnection() as (_, db):
        nodes = db[collection].find()
        return [Node(**one_node) for one_node in nodes]
