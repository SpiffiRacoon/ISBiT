# own
from ..db import (
    get_all_collections as db_get_all_collections
)
from ..types import DatasetsResponse
from ..utils import write_dataset, write_info

# pip
from fastapi import APIRouter, HTTPException, UploadFile
import pandas as pd
from io import StringIO
import json

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
    uploaded_file: UploadFile,
    filename: str,
    uploaded_info_file: UploadFile,
    delimiter: str | None = None
):
    """
    Upload a dataset

    Currently only csv files are supported.

    Paramaters:
        uploaded_file, dataset to upload.   
        filename, name to save uploaded_file as. 
        uploaded_info_file, accompanying .info file to the uploaded dataset.
    """
    try:
        contents = uploaded_file.file.read().decode("utf-8")
        string_content = StringIO(contents)
        df = pd.read_csv(string_content, delimiter=delimiter)
        write_dataset(filename=filename, df=df)

        info_contents = uploaded_info_file.file.read().decode("utf-8")
        meta_data = json.loads(info_contents)
        write_info(info_filename=filename, metadata=meta_data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Uploaded info file must be in valid JSON format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "details": f"File '{filename}' uploaded"}


@router.delete("/", status_code=204)
def delete_collection(collection: str) -> None:
    """
    Delete a collection in the database.

    OBS, this is permanent!
    """

    # db_delete_collection(collection=collection)
    raise HTTPException(status_code=501, detail="Not implemented")



