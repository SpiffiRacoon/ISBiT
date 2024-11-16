# own
from .connection import MongoConnection
from ..types import Node, MlStatus

# pip
import pandas as pd


def get_all_dataset_names() -> list:
    with MongoConnection() as (_, db):
        collections = db.list_collection_names()

        for one_collection in collections.copy():
            if one_collection in ["ml_status", "labels"]:
                collections.remove(one_collection)
    return collections

def get_dataset_names_with_processed_data(ConnectionClass=MongoConnection) -> list:
    with ConnectionClass() as (_, db):
        collections = list(db.list_collection_names())
        if collections == []:
            return []

        for one_collection in collections.copy():
            query_version_not_datafile = {"about.version": {"$gt": 0}}

            if not db[one_collection].find_one(query_version_not_datafile):
                collections.remove(one_collection)

    return collections


def get_datafiles_not_processed(ConnectionClass=MongoConnection) -> list:
    with ConnectionClass() as (_, db):
        collections = list(db.list_collection_names())
        if collections == []:
            return []

        processed = get_dataset_names_with_processed_data()

        for one_collection in collections.copy():
            query_version_not_datafile = {"about.version": 0}

            if not db[one_collection].find_one(query_version_not_datafile):
                collections.remove(one_collection)

            elif one_collection in processed:
                collections.remove(one_collection)

    return collections


def get_latest_version_number(dataset_name: str, ConnectionClass=MongoConnection) -> int:

    with ConnectionClass() as (_, db):
        result = db[dataset_name].aggregate(
            [
                {"$group": {"_id": None, "maxVersion": {"$max": "$about.version"}}},
                {"$project": {"_id": 0, "maxVersion": 1}},
            ]
        )

    latest_version = list(result)[0]["maxVersion"]
    return latest_version


def get_nodes_from_latest_version(dataset_name: str, ConnectionClass=MongoConnection) -> pd.DataFrame:
    """
    Returns all nodes from the latest version of a collection.
    """
    latest_version = get_latest_version_number(dataset_name)

    with ConnectionClass() as (_, db):
        result = db[dataset_name].find_one({"about.version": latest_version})
        if result is not None:
            df = pd.DataFrame(result["data"])
            return df

    raise Exception(f"Error: Could not find latest version of {dataset_name}")


def get_about_from_latest_version(dataset_name: str, ConnectionClass=MongoConnection) -> dict:
    """
    Returns all nodes from the latest version of a collection.
    """
    latest_version = get_latest_version_number(dataset_name)

    with ConnectionClass() as (_, db):
        result = db[dataset_name].find_one({"about.version": latest_version})
        if result is not None:
            print(result["about"])
            return result["about"]

    raise Exception(f"Error: Could not find latest version of {dataset_name}")


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


def get_all_labels_from(collection: str, ConnectionClass=MongoConnection) -> list:
    """
    Get list document with labels from a collection.
    """
    with ConnectionClass() as (_, db):
        result = db[collection].find_one({}, {"about.labels": 1, "_id": 0})
        if result is None:
            raise ValueError(f"Error: Could not find any labels in {collection}")
        return result["about"]["labels"]


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
