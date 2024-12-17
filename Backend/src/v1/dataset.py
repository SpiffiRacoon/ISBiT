# own
from ..db import (
    delete_collection as db_delete_collection,
    add_dataset_to_db,
    get_dataset_names_with_processed_data,
    get_datafiles_not_processed,
    get_all_dataset_names as db_get_all_dataset_names,
    get_latest_version_number,
)
from ..types import DatasetsResponse, DatasetFileResponse
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
def get_all_processed_datasets() -> DatasetsResponse | None:
    """
    Get all datasets in database.
    """

    # collections = db_get_all_dataset_names()
    collections = get_dataset_names_with_processed_data()
    info = {"dataList": []}
    if collections == []:
        return DatasetsResponse(**info)

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


@router.get("/files", status_code=200)
def get_all_dataset_files() -> DatasetFileResponse| None:
    """
    Get all dataset files in the data folder.
    """

    files = get_datafiles_not_processed()
    info = {"dataList": []}

    if files == []:
        return DatasetFileResponse(**info)

    for one_collection in files:
        info["dataList"].append(
            {
                "dataset": one_collection,
                "id": "123",
            }
        )

    return DatasetFileResponse(**info)


@router.post("/")
def upload_dataset(
    filename: str,
    uploaded_file: UploadFile,
    uploaded_info_file: UploadFile,
    delimiter: str | None = None
):
    """
    Upload a dataset with an accompanying .info file, the info needs to be JSON format and will get the same name as the file with a suffix "_meta_info".

    Currently only csv files are supported.

    Parameters:
        uploaded_file, dataset to upload.
        filename, name to save uploaded_file as.
        uploaded_info_file, accompanying .info file to the uploaded dataset.
    """
    try:
        contents = uploaded_file.file.read().decode("utf-8")
        string_content = StringIO(contents)
        df = pd.read_csv(string_content, delimiter=delimiter)

        info_contents = uploaded_info_file.file.read().decode("utf-8")
        meta_data = json.loads(info_contents)

        add_dataset_to_db(df=df, about=meta_data, dataset_name=filename)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Uploaded info file must be in valid JSON format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "details": f"File '{filename}' uploaded"}


@router.delete("/", status_code=204)
def delete_dataset(dataset: str) -> None:
    """
    Delete a dataset in the database.

    OBS, this is permanent!
    """

    datasets = db_get_all_dataset_names()
    if datasets == []:
        raise HTTPException(status_code=400, detail="No datasets found")

    for one_dataset in datasets:
        if one_dataset == dataset:
            db_delete_collection(collection=dataset)
            return

    raise HTTPException(status_code=400, detail="dataset not found")

@router.get("/latest_version", status_code=200)
def get_latest_dataset_version(dataset_name: str) -> int:
    """
    Get the latest version number of a dataset.
    """
    try:
        latest = get_latest_version_number(dataset_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return latest