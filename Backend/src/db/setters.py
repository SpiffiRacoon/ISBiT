# own
from .connection import MongoConnection
from ..types import Node, MlStatus, VersionName
from ..validators import validate_endpoint_args
from .utils import get_collection_name
from .getters import get_latest_version_number

# pip
import pandas as pd


@validate_endpoint_args
def add_dataset_to_db(df: pd.DataFrame, collection: str, ConnectionClass=MongoConnection) -> None:
    """
    Add a dataset to the database.

    If there is a collection with the same name, it will be dropped.
    """
    with ConnectionClass() as (_, db):
        if collection in db.list_collection_names():
            raise Exception(f"Error: Tried to add collection {collection}, but it already exists")

        db[collection].insert_many(df.to_dict(orient="records"))


@validate_endpoint_args
def add_versioned_nodes(
    nodes: list[Node], collection: str, version_name: VersionName, ConnectionClass=MongoConnection
) -> None:
    """
    Add data nodes with versioning.

    If there is a collection with the same name, error will be raised.
    """
    version_number = get_latest_version_number(collection=collection)

    collection = get_collection_name(
        dataset_name=collection, version_name=version_name, version_number=str(version_number)
    )
    nodes_to_insert = [one_node.dict() for one_node in nodes]

    with ConnectionClass() as (_, db):
        if collection in db.list_collection_names() and "data" in db[collection].list_collection_names():
            raise Exception(f"Error: Tried to add nodes to {collection}, but it already exists")

        db[collection]["data"].insert_many(nodes_to_insert)


@validate_endpoint_args
def label_one_node(
    node_id: str, label: str, collection: str, version_name: VersionName, ConnectionClass=MongoConnection
) -> None:
    """
    Label one node.

    If there is no labeled nodes, a new collection will be created and the node will be updated.
    If the collection already exists, the node will be updated.
    """
    version_number = get_latest_version_number(collection=collection)

    collection = get_collection_name(
        dataset_name=collection, version_name=version_name, version_number=str(version_number), label=True
    )
    prev_collection = get_collection_name(
        dataset_name=collection, version_name=version_name, version_number=str(version_number), label=False
    )

    with ConnectionClass() as (_, db):
        if collection not in db.list_collection_names():
            db[collection] = db[prev_collection].copy()

        query = {"_id": node_id}
        update = {"$set": {"data.input_label": label}}
        db[collection].update_one(query, update)


@validate_endpoint_args
def add_one_node_to(node: Node, collection: str, ConnectionClass=MongoConnection) -> None:
    """
    Add one node to a collection.
    """
    with ConnectionClass() as (_, db):
        db[collection]["data"].insert_one(node.dict())


@validate_endpoint_args
def add_multiple_nodes_to_id(
    nodes: list[Node], collection: str, document_id: str, ConnectionClass=MongoConnection
) -> None:
    """
    Bulk function for adding multiple nodes at once to a specific id.
    """
    nodes_to_insert = [one_node.dict() for one_node in nodes]

    with ConnectionClass() as (_, db):
        db[collection].update_one({"_id": document_id}, {"$push": {"data": {"$each": nodes_to_insert}}}, upsert=True)


@validate_endpoint_args
def add_about_node_to_id(about_node: dict, collection: str, document_id: str, ConnectionClass=MongoConnection) -> None:
    """
    Adds an "about" field with a document from a datasets accompanying .info file to a specific id.
    """
    with ConnectionClass() as (_, db):
        db[collection].update_one(
            {"_id": document_id},
            {"$set": {"about": about_node}},
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
