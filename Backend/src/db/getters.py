# str
from datetime import datetime

# own
from .connection import MongoConnection
from ..types import Node, MlStatus

# pip
from pandas.core.arrays import boolean


def get_all_nodes_from(collection: str, ConnectionClass=MongoConnection) -> list[Node]:
    """
    Get all nodes from a collection
    """
    with ConnectionClass() as (_, db):
        nodes = db[collection].find()
        return [Node(**one_node) for one_node in nodes]


def get_all_collections(ConnectionClass=MongoConnection) -> list:
    """
    Get all collections in database
    """
    with ConnectionClass() as (_, db):
        collections = db.list_collection_names()

        all_datasets = list(collections)
        all_datasets.remove("ml_status")

        return all_datasets

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
