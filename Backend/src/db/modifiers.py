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


def delete_ml_status(id: str, ConnectionClass=MongoConnection) -> None:
    """
    Delete a ml_status entry
    """
    with ConnectionClass() as (_, db):
        query = {"ml_id": id}
        db["ml_status"].delete_many(query)

def add_label(node_id: str, category: str, collection: str, ConnectionClass=MongoConnection) -> None:
    """ 
    Label a node in a collection.
    """
    
    with ConnectionClass() as (_, db):
        db[collection].update_one({"data.id": node_id}, {"$set": {"data.$[elem].input_label": category}}, array_filters=[{"elem.id": node_id}])