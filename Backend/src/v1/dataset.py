# own
from ..db import (
    get_all_collections as db_get_all_collections,
    delete_collection as db_delete_collection,
)

# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"],
)


@router.get("/", status_code=200)
def get_all_datasets() -> dict:
    """
    Get all datasets in database.
    """

    collections = db_get_all_collections()
    return collections

    info = {
        "dataList": [
            {"dataset": "Dataset 1", "assignment": "labling", "datatype": "Type A", "id": "123"},
            {"dataset": "Dataset 2", "assignment": "labling", "datatype": "Type B", "id": "124"},
            {"dataset": "Dataset 3", "assignment": "labling", "datatype": "Type C", "id": "125"},
            {"dataset": "Dataset 4", "assignment": "labling ", "datatype": "Type D", "id": "126"},
        ],
    }

    return info


@router.delete("/", status_code=204)
def delete_collection(collection: str) -> None:
    """
    Delete a collection in the database.

    OBS, this is permanent!
    """

    # db_delete_collection(collection=collection)
    raise HTTPException(status_code=501, detail="Not implemented")
