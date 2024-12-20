# own
from datetime import time
from ..types import TestingResponse
from ..utils import (
    download_qaqc_source_dataset as util_download_qaqc,
    get_qaqc_info_dict as util_get_info_dict,
)
from .dataset import upload_dataset, get_all_processed_datasets
from .data import get_all_labels, get_all_nodes
from .run_ml import run, get_status
from ..utils import simulate_user_input  # import the function to simulate labels
from ..db import get_nodes_from_latest_version, label_one_node
from ..types import Node

# pip
from fastapi import APIRouter, HTTPException, UploadFile

import asyncio
import time
import io
import json

router = APIRouter(
    prefix="/testing",
    tags=["Testing"],
)


@router.post("/")
async def manual_test_sequence(
    filename: str,
    model_name: str = "QaqcMainModel",
    dim_red_method: str = "COMBO",
    n_rows: int = 250,
    run_time: float = 120,
    run_unit: str = "s",
) -> TestingResponse:
    """
    Run a test sequence of following endpoints:

    0. Downloads the source QAQC data set.
    1. Uploads n_rows of the source data.
    2. Starts an async run of the ml lib.
    3. GET running statuses.
    5. GET Processed data sets.
    6. GET labels.
    7. GET 10 random nodes of from the generated collection.

    Returns a response consisting of a collection of status responses from other routes ran in the sequence.

    Parameters:

    1. filename, will name the generated collection.
    2. n_row, slices the source data with n rows.
    3. run_time, sets the expected running time of the ml lib An error will be raised if the run wont complete within the given timeframe, otherwise it will run until completed status.
    4. run_unit, 's' for seconds and 'm' for minutes.

    """
    if run_time is not None:
        if run_unit == "m":
            total_run_time = run_time * 60
        elif run_unit == "s":
            total_run_time = run_time
        else:
            raise ValueError("Invalid run_unit parameter, 's' for seconds or 'm' for minutes are valid")
    else:
        total_run_time = None

    response = TestingResponse()
    if n_rows == None:
        response.n_rows = "Full dataset."
    else:
        response.n_rows = str(n_rows)

    try:
        df = util_download_qaqc()
        response.download_msgs = "download successful"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download dataset: {str(e)}")

    df = df.sample(n=n_rows, random_state=42)
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    info_dict = util_get_info_dict()
    info_buffer = io.BytesIO(json.dumps(info_dict).encode("utf-8"))
    info_buffer.seek(0)

    try:
        uploaded_file = UploadFile(filename=filename, file=csv_buffer)
        uploaded_info_file = UploadFile(filename=filename, file=info_buffer)
        response.upload_msgs = upload_dataset(
            filename=filename,
            uploaded_file=uploaded_file,
            uploaded_info_file=uploaded_info_file,
        )
    except Exception as e:
        raise e

    try:
        await run(model_name=model_name, file=filename, dim_red_method=dim_red_method)
    except Exception as e:
        raise e

    start_time = time.time()
    retry_interval = 4  # check the status every 4s
    while True:
        status_response = get_status(model_name=model_name, file=filename)
        status = status_response.status
        details = status_response.details
        if status_response not in response.ml_status:
            response.ml_status.append(status_response)
        if status == "Not running" and "Success" in details:
            break
        elif status == "Not running" and "Error" in details:
            raise HTTPException(f"ML run error: {details}")
        elif status == "error":
            raise HTTPException(f"ML run error: {details}")
        if total_run_time is not None and (time.time() - start_time) > total_run_time:
            raise HTTPException(f"ML did not complete during run_time :{run_time}{run_unit}")
        await asyncio.sleep(retry_interval)

    try:
        datasets_response = get_all_processed_datasets()
        response.datasets = datasets_response
        labels = get_all_labels(collection=filename)
        response.labels = labels
        nodes = get_all_nodes(collection=filename)
        nodes = nodes[:9]
        response.nodes = nodes
    except Exception as e:
        raise e

    return response

@router.post("/simulate_labels", status_code=200)
def simulate_labels_route(dataset_name: str, fraction: float = 0.1):
    """
    Simulate labels for a dataset and return the modified DataFrame as JSON.
    """
    df = get_nodes_from_latest_version(dataset_name=dataset_name)
    try:
        # Simulate user input and get the updated DataFrame
        updated_df = simulate_user_input(df, dataset_name=dataset_name, fraction=fraction)
        # Convert the updated DataFrame to a list of Node objects
        list_of_nodes: list[Node] = [Node(**one_node) for one_node in updated_df.to_dict("records")]
        # Persist the updated nodes in the database
        for node in list_of_nodes:
            if node.input_label is None:
                raise Exception("Input label is not set!")
            label_one_node(node_id=node.id, label=node.input_label, dataset_name=dataset_name)

        return {"message": "Labels simulated and updated in the database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
