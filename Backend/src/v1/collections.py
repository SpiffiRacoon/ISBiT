# own
from ..db import get_all_collections as db_get_all_collections, delete_collection as db_delete_collection

# pip
from fastapi import APIRouter

router = APIRouter(
    prefix="/collections",
    tags=["Collections"],
)


@router.get("/", status_code=200)
def get_all_collections() -> list:
    """
    Get all collections in database.

    A collection is a version of the data (this could be iteration specific)
    """

    collections = db_get_all_collections()
    return collections


@router.delete("/", status_code=204)
def delete_collection(collection: str) -> None:
    """
    Delete a collection in the database.

    OBS, this is permanent!
    """

    db_delete_collection(collection=collection)
    return None
