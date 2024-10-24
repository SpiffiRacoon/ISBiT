# own
from ..db import (
    get_all_collections as db_get_all_collections,
    delete_collection as db_delete_collection
)
from ..types import DatasetsResponse

# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"],
)


@router.get("/", status_code=200)
def get_all_datasets() -> DatasetsResponse | None:
    """
    Get all datasets in database.
    """

    collections = db_get_all_collections()
    info = {"dataList": []}
    if collections == []:
        return None

    for one_collection in collections:
        info["dataList"].append(
            {
                "dataset": one_collection,
                "assignment": "labling",
                "datatype": "Type A",
                "id": "123",
            }
        )

    return DatasetsResponse(**info)


@router.delete("/", status_code=204)
def delete_collection(collection: str) -> None:
    """
    Delete a collection in the database.

    OBS, this is permanent!
    """

    collections = db_get_all_collections()
    if collections == []:
        raise HTTPException(status_code=400, detail="No collections found")
    
    for one_collection in collections:
        if one_collection == collection:
            db_delete_collection(collection=collection)
            return
    
    raise HTTPException(status_code=400, detail="No collection found")
