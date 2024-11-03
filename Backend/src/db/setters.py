# std
from datetime import datetime

# own
from .connection import MongoConnection
from ..types import Node, MlStatus
from ..validators import validate_endpoint_args


@validate_endpoint_args
def add_one_node_to(
    node: Node, collection: str, ConnectionClass=MongoConnection
) -> None:
    """
    Add one node to a collection.

    Id needs to be unique, otherwise the node will not be added
    """
    with ConnectionClass() as (_, db):
        db[collection].insert_one(node.dict())


def add_multiple_nodes_to(
    nodes: list[Node], collection: str, ConnectionClass=MongoConnection
) -> None:
    """
    Bulk function to adding multiple nodes at once.
    """
    nodes_to_insert = [one_node.dict() for one_node in nodes]
    with ConnectionClass() as (_, db):
        db[collection].insert_many(nodes_to_insert)


def set_ml_status(new_ml_status: MlStatus, ConnectionClass=MongoConnection) -> MlStatus:
    """
    Set status of ML run, removing the old one if it exists
    """
    with ConnectionClass() as (_, db):
        query = {"ml_id": new_ml_status.ml_id}
        db["ml_status"].delete_many(query)

        db["ml_status"].insert_one(new_ml_status.dict())

    return new_ml_status
