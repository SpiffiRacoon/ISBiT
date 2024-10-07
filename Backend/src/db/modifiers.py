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
