# std
from datetime import datetime

# own
from .connection import MongoConnection
from ..types import Node, MlStatus
from ..validators import validate_endpoint_args


# TODO : this will need an update to be compatible with the new mongo doc structure
@validate_endpoint_args # db validator
def add_one_node_to(
    node: Node, collection: str, ConnectionClass=MongoConnection
) -> None:
    """
    Add one node to a collection.

    Id needs to be unique, otherwise the node will not be added.
    """
    with ConnectionClass() as (_, db):
        db[collection].insert_one(node.dict())

@validate_endpoint_args
def add_multiple_nodes_to_id(
    nodes: list[Node], collection: str, document_id: str, ConnectionClass=MongoConnection
) -> None:
    """
    Bulk function for adding multiple nodes at once to a specific id.
    """
    nodes_to_insert = [one_node.dict() for one_node in nodes]
    
    with ConnectionClass() as (_, db):
        db[collection].update_one(
            {"_id": document_id},
            {"$push": {"data": {"$each": nodes_to_insert}}},
            upsert=True
        )

@validate_endpoint_args
def add_about_node_to_id(
    about_node: dict, collection: str, document_id: str, ConnectionClass=MongoConnection
) -> None:
    """
    Adds an about field with a document from a datasets accompanying .info file to a specific id.
    """ 
    with ConnectionClass() as (_, db):
         db[collection].update_one(
             {"_id": document_id},
             {"$set" : {"about": about_node}},
             upsert=True,
            )


def set_ml_status(new_ml_status: MlStatus, ConnectionClass=MongoConnection) -> MlStatus:
    """
    Set status of ML run, removing the old one if it exists
    """
    with ConnectionClass() as (_, db):
        query = {"ml_id": new_ml_status.ml_id}
        db["ml_status"].delete_many(query)

        db["ml_status"].insert_one(new_ml_status.dict())

    return new_ml_status
