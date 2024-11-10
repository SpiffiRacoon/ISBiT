# own
from .connection import MongoConnection
from ..types import Node, MlStatus

# pip
import pandas as pd


def get_all_dataset_names(ConnectionClass=MongoConnection) -> list:
    """
    Get all collections in database

    This should return all unique dataset_names in the "info" table of the collections.
    """
    print("[WARNING] get_all_collections is not implemented yet.")
    return []


def get_latest_version_number(dataset_name: str, ConnectionClass=MongoConnection) -> int:
    print("[WARNING] get_latest_version_number is not implemented yet.")
    return 0


def get_nodes_from_latest_version(dataset_name: str, ConnectionClass=MongoConnection) -> pd.DataFrame:
    """
    Returns all nodes from the latest version of a collection.
    """
    print("[WARNING] get_nodes_from_latest_version is not implemented yet.")
    return pd.DataFrame()


def get_about_from_latest_version(dataset_name: str, ConnectionClass=MongoConnection) -> dict:
    """
    Returns all nodes from the latest version of a collection.
    """
    print("[WARNING] get_about_from_latest_version is not implemented yet.")
    return {}


def get_all_nodes_from(collection: str, ConnectionClass=MongoConnection) -> list[Node]:
    """
    Get all nodes from a collections node array in its data field.
    """
    with ConnectionClass() as (_, db):
        documents = db[collection].find()
        nodes = []
        for doc in documents:
            nodes.extend([Node(**data_item) for data_item in doc["data"]])
    return nodes


def get_all_labels_from(collection: str, ConnectionClass=MongoConnection) -> list[dict]:
    """
    Get list document with labels from a collection.
    """
    with ConnectionClass() as (_, db):
        labels = list(db[collection].find({}, {"about.labels": 1, "_id": 0}))
        return labels


def get_ml_status(id: str, ConnectionClass=MongoConnection) -> MlStatus:
    """
    Get a dict with info about the ML run
    """
    with ConnectionClass() as (_, db):
        query = {"ml_id": id}

        result = db["ml_status"].find_one(query)
        if result is None:
            return MlStatus(ml_id=id, status="Not running", details="Not found")

        return MlStatus(**result)
