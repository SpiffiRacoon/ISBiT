from .connection import MongoConnection
from ..types import Node

def add_one_node_to(node: Node, collection: str) -> None:
    """
    Add one node to a collection
    """
    with MongoConnection() as (_, db):
        db[collection].insert_one(node.dict())
