# own
from bson import ObjectId
from .connection import MongoConnection
from ..types import Node
from ..validators import validate_endpoint_args


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
def add_multiple_nodes_to(
    nodes: list[Node], collection: str, ConnectionClass=MongoConnection
) -> None:
    """
    Bulk function to adding multiple nodes at once.
    """
    nodes_to_insert = [one_node.dict() for one_node in nodes]
    with ConnectionClass() as (_, db):
        db[collection].insert_many(nodes_to_insert)


@validate_endpoint_args
def add_multiple_nodes_to_id(
    nodes: list[Node], collection: str, document_id: str, ConnectionClass=MongoConnection
) -> None:
    """
    Bulk function to adding multiple nodes at once to a specific id.
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
    about_node: dict, collection: str, id: str, ConnectionClass=MongoConnection
) -> None:
    """
    Adds an about field with a document from a datasets accompanying .info file to a specific id.
    """ 
    with ConnectionClass() as (_, db):
         db[collection].update_one(
             {"_id": id},
             {"$set" : {"about": about_node}},
             upsert=True,
            )





