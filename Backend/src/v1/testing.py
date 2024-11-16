# own
from datetime import time
import os
from ..types import TestingResponse, DatasetsResponse
from ..utils import (
    download_qaqc_source_dataset as util_download_qaqc,
    get_qaqc_info_dict as util_get_info_dict,
)
from .dataset import upload_dataset, get_all_processed_datasets
from .data import get_all_labels, get_all_nodes
from .run_ml import run, get_status

#pip
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.testclient import TestClient

import asyncio
#from time import sleep
import io
import json


router = APIRouter(
    prefix="/testing",
    tags=["Testing"],
)

@router.post("/")
async def manual_test_sequence(
    filename: str,
    n_rows: int | None = None,
    ) -> TestingResponse:
    """
    Run a test sequence of following endpoints: 

    0. Downloads the source QAQC data set.
    1. Uploads a slice of the dataset based on the fraction parameter and info file to the project.
    2. Starts an async run of the ml lib.
    3. Checks for running status.
    4. Checks for complete status.
    5. Check Processed data sets.
    6. Get labels.
    7. Get all nodes.
    8. Provides a custom response catching errors in the sequence of developed components.

    This endpoint is implemented for the development team to have a one-button for the projects current state as of 2024-11-09. 
    """
    response = TestingResponse()

    try: 
        df = util_download_qaqc()
        response.download_msgs = "download successful"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download dataset: {str(e)}")
    
    df = df.sample(n=n_rows, random_state=42)

    csv_buffer  = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    info_dict = util_get_info_dict()
    info_buffer = io.BytesIO(json.dumps(info_dict).encode('utf-8'))
    info_buffer.seek(0)

    # TODO: same var path var up as read

    try:
        uploaded_file = UploadFile(filename=filename, file=csv_buffer)
        #uploaded_info_file = UploadFile(filename=f"{filename}_meta_info.json", file=info_buffer)
        uploaded_info_file = UploadFile(filename=filename, file=info_buffer)
        upload_dataset(filename=filename, uploaded_file=uploaded_file, uploaded_info_file=uploaded_info_file)
        response.upload_msgs = "Dataset uploaded successfully." # TODO : the upload endpoint should return some smart msgs

        max_attempts = 5
        wait_time = 3  # seconds

        for attempt in range(max_attempts):
            await asyncio.sleep(wait_time)
            exists = os.path.isfile(f"src/data/{filename}.csv")
            print(f"Exists value:{exists}")
            if exists:
                print(f"File found: {filename}.csv")
                break
            else:
                print(f"File not found, attempt {attempt + 1} of {max_attempts}. Retrying...")
                if attempt >= max_attempts:
                    raise FileNotFoundError(f"{filename}.csv not found after {max_attempts} attempts.")
    except Exception as e:
        raise e

    await asyncio.sleep(2)


    try:
        await run(model_name="qaqc_main", file=filename, dim_red_method="COMBO")
    except Exception as e:
        raise e
            
    await asyncio.sleep(2)

    status = None
    max_retries = 5  
    retry_interval = 5

    for _ in range(max_retries):
        status_response = get_status(model_name="qaqc_main", file=filename)
        status = status_response.status
        details = status_response.details
        response.ml_status.append(status_response) 

        print(f"STATUS IS: {status}, DETAILS: {details}")

        if status == "Not running" and "Success" in details:
            print("ML run completed successfully.")
            break
        elif status == "Not running" and "Error" in details:
            raise Exception(f"ML run encountered an error: {details}")
        elif status == "error":
            raise Exception(f"ML run encountered an error: {details}")

        await asyncio.sleep(retry_interval)

    if not (status == "Not running" and "Success" in details):
        raise Exception("ML run did not complete within the expected time frame.")

    try:
        datasets_response = get_all_processed_datasets()
        response.datasets = datasets_response
    except Exception as e:
        raise e

    try:
        labels = get_all_labels(collection=filename)
        response.labels = labels
    except Exception as e:
        raise e

    try:
        nodes = get_all_nodes(collection=filename)
        response.nodes = nodes
    except Exception as e:
        raise e

    return response
    