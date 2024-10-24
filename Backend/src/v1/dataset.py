# own
from ..db import (
    get_all_collections as db_get_all_collections,
)
from ..types import DatasetsResponse
from ..utils import write_dataset

# pip
from fastapi import APIRouter, HTTPException, UploadFile
import pandas as pd
from io import StringIO

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


@router.post("/")
def upload_dataset(
    uploaded_file: UploadFile, filename: str, delimiter: str | None = None
):
    """
    Upload a dataset

    Currently only csv files are supported.
    """
    try:
        contents = uploaded_file.file.read().decode("utf-8")
        string_content = StringIO(contents)
        df = pd.read_csv(string_content, delimiter=delimiter)
        write_dataset(filename, df)
    except Exception as e:
        raise HTTPException(500, str(e))

    return {"status": "success", "details": f"File '{filename}' uploaded"}


@router.delete("/", status_code=204)
def delete_collection(collection: str) -> None:
    """
    Delete a collection in the database.

    OBS, this is permanent!
    """

    # db_delete_collection(collection=collection)
    raise HTTPException(status_code=501, detail="Not implemented")
