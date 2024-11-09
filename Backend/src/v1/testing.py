# own

from ..types import testing_response
from ..utils import (
    download_qaqc_source_dataset as util_download_qaqc,
    get_qaqc_info_dict as util_get_info_dict,
)
from .dataset import upload_dataset, get_all_processed_datasets
from .data import get_all_labels, get_all_nodes
from .run_ml import run_ml_background_task, get_status

#pip
from fastapi import APIRouter, HTTPException, UploadFile
from datetime import time

import io
import json


router = APIRouter(
    prefix="/testing",
    tags=["Testing"],
)

@router.post("/")
def manual_test_sequence(
    filename: str,
    fraction: float | None = None,
    ) -> None:
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
    # saves the data set, returns a status string, use it to set some attribute in future response object.
    df = util_download_qaqc()
    if fraction is not None and 0 < fraction < 1:
        df = df.sample(frac=fraction, random_state=42)

    # TODO : fix something so files can be passed to upload endpoint.
    csv_buffer  = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    info_dict = util_get_info_dict()
    info_buffer = io.BytesIO(json.dumps(info_dict).encode('utf-8'))
    info_buffer.seek(0)


    uploaded_file = UploadFile(filename=filename, file=csv_buffer)
    uploaded_info_file = UploadFile(filename=f"{filename}_meta_info.json", file=info_buffer)

    # not sure if this will work, might have to make above vars to io buffers

    upload_dataset(filename=filename, uploaded_file=uploaded_file, uploaded_info_file=uploaded_info_file)
    # try:
    #     upload_dataset(filename=filename, uploaded_file=uploaded_file, uploaded_info_file=uploaded_info_file)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    print("after upload")

    run_ml_background_task(model_name="qaqc_main", file=filename, dim_red_method="COMBO")
    
    status = None
    max_retries = 30  
    retry_interval = 10

    for _ in range(max_retries):
        status_response = get_status(model_name="qaqc_main", file=filename)
        status = status_response.get("status")

        if status == "complete":
            break
        elif status == "error":
            raise Exception("ML run encountered an error.")
        
        time.sleep(retry_interval)

    if status != "complete":
        raise Exception("ML run did not complete within the expected time frame.")
    
    get_all_processed_datasets()
    get_all_labels(collection=filename)
    get_all_nodes(collection=filename)
    