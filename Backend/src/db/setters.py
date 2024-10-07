from .connection import MongoConnection
from ..types import Node
from ..validators import validate_endpoint_args

@validate_endpoint_args
def add_one_node_to(node: Node, collection: str, ConnectionClass = MongoConnection) -> None:
    """
    Add one node to a collection.

    Id needs to be unique, otherwise the node will not be added
    """
    with ConnectionClass() as (_, db):
        same_node = db[collection].find({"id": node.id})
        if len(list(same_node)) > 0:
            raise Exception(f"Node with id: {node.id} already exists")

        db[collection].insert_one(node.dict())
