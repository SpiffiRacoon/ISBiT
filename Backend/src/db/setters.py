# own
from .connection import MongoConnection
from ..types import Node, MlStatus, VersionName
from ..validators import validate_endpoint_args
from .getters import get_about_from_latest_version
from .data_version import DataVersion

# pip
import pandas as pd


@validate_endpoint_args
def add_dataset_to_db(
    df: pd.DataFrame, dataset_name: str, about: dict | None = None, ConnectionClass=MongoConnection
) -> None:
    """
    Add a dataset to the database.

    If there is a collection with the same name, it will be dropped.
    """
    v_obj = DataVersion(dataset_name=dataset_name, version_name=VersionName.DATA_FILE)

    with ConnectionClass() as (_, db):
        if v_obj.dataset_name not in db.list_collection_names():
            collection = db.create_collection(v_obj.dataset_name)
        else:
            collection = db[v_obj.dataset_name]

        query = {"about.version": v_obj.version}
        if collection.find_one(query) is not None:
            raise Exception(f"Error: Tried to add collection '{v_obj.dataset_name}', but it already exists")

        data_to_save: dict = {
            "data": df.to_dict(orient="records"),
        }

        if about is not None:
            about.update({"version": v_obj.version, "dataset_name": v_obj.dataset_name})
            data_to_save["about"] = about

        collection.insert_one(data_to_save)


@validate_endpoint_args
def add_versioned_nodes(nodes: list[Node], dataset_name: str, ConnectionClass=MongoConnection) -> None:
    """
    Add data nodes with versioning.

    If there is a collection with the same name, error will be raised.
    """
    v_obj = DataVersion(dataset_name=dataset_name)
    v_obj.upgrade(automatic=True)

    nodes_to_insert = [one_node.dict() for one_node in nodes]

    info = get_about_from_latest_version(dataset_name=v_obj.dataset_name)
    info.update(v_obj.about_dict)

    data_to_save = {"data": nodes_to_insert, "about": info}

    with ConnectionClass() as (_, db):
        query = {"about.version": v_obj.version}
        if db[v_obj.dataset_name].find_one(query) is not None:
            raise Exception(f"Error: Tried to add nodes to {v_obj.version_name}, but it already exists")

        db[v_obj.dataset_name].insert_one(data_to_save)


@validate_endpoint_args
def label_one_node(
    node_id: str, label: str, dataset_name: str, version_name: VersionName, ConnectionClass=MongoConnection
) -> None:
    """
    Label one node.

    If there is no labeled nodes, a new collection will be created and the node will be updated.
    If the collection already exists, the node will be updated.
    """
    v_obj = DataVersion(dataset_name=dataset_name)

    v_new_obj = v_obj.upgrade(label=True, copy=True)

    with ConnectionClass() as (_, db):
        if v_new_obj not in db.list_collection_names():
            db[v_new_obj.collection_name] = db[v_obj.version_name].copy()

        query = {"_id": node_id}
        update = {"$set": {"data.input_label": label}}
        db[v_new_obj.collection_name].update_one(query, update)


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
