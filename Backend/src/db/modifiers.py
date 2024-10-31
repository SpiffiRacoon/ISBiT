from .connection import MongoConnection
from ..validators import validate_endpoint_args


@validate_endpoint_args
def delete_collection(collection: str, ConnectionClass=MongoConnection) -> None:
    """
    Delete a collection
    """
    with ConnectionClass() as (_, db):
        db_col = db[collection]
        db_col.drop()


def add_label(node_id: str, category: str, collection: str, ConnectionClass=MongoConnection) -> None:
    """ 
    Label a node in a collection.
    """
    query_filter = {'id': node_id} #TODO: not working
    update_operation = {'$set': {'input_label': category}}
    with ConnectionClass() as (_, db):
        db_col = db[collection]
        db_col.update_one(query_filter, update_operation)
        