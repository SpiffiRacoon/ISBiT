# std
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# own
from ..types import Node, MlStatus
from ..ml_lib import get_model_instance

from ..db import add_multiple_nodes_to, set_ml_status, get_ml_status, delete_ml_status
from ..db import add_about_node_to_id, add_multiple_nodes_to_id

# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/run_ml",
    tags=["Run ML"],
)

executor = ThreadPoolExecutor(max_workers=10)


@router.post("/", status_code=200)
async def run(model_name: str, file: str, dim_red_method: str | None = None) -> MlStatus:
    """
    Run a ML model on a file asynchronously. This will start the run in the background and return the status of the run.
    If the model is already running, it will return the status of the run.

    Ex)
    model: qaqc_main

    file: swe_qaqc_lib_test

    dim_red_method: COMBO

    NOTE: If you want to use the qaqc_test model, the dim_red_method field can be left blank because it will only use PCA.
    """

    ml_id = f"{model_name}_{file}"
    ml_status = get_ml_status(ml_id)
    if ml_status.status == "Running":
        return get_ml_status(ml_id)

    ml_status = set_ml_status(
        MlStatus(ml_id=ml_id, status="Running", details="Request received")
    )
    executor.submit(run_ml_background_task, model_name, file, dim_red_method)
    return ml_status


@router.get("/")
def get_status(model_name: str, file: str) -> MlStatus:
    """
    Get the status of a ML run
    """
    ml_id = f"{model_name}_{file}"
    return get_ml_status(ml_id)


@router.post("/flush", status_code=201)
def flush_ml_status(model_name: str, file: str) -> None:
    """
    Flush the ML status collection.

    Sometimes the status of the ML run is not updated correctly. This function can be used to flush the status of the ML run.

    An example of when it can be wrong is when stopping the docker container during a ML run.
    """
    ml_id = f"{model_name}_{file}"
    delete_ml_status(ml_id)
    return None


def run_ml_background_task(
    model_name: str, file: str, dim_red_method: str | None = None
) -> None:
    """
    Synchronous function to run the ML model in the background
    This function updates the status of the ML run in the database
    """
    ml_id = f"{model_name}_{file}"

    set_ml_status(MlStatus(ml_id=ml_id, status="Running", details="Started ML run"))

    starting_time = datetime.now()
    model_obj = get_model_instance(model_name)
    try:
        about_dict = model_obj._read_meta_info(file_name=file)
        model_obj.run(file_name=file, is_first=True, dim = dim_red_method)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    ref_id = f"{file}{"_id"}"
    add_about_node_to_id(about_node=about_dict, collection=file, id=ref_id)

    df = model_obj.df
    list_of_nodes = [Node(**one_node) for one_node in df.to_dict("records")]
    add_multiple_nodes_to_id(list_of_nodes, collection=file, document_id=ref_id)

    total_running_time = datetime.now() - starting_time
    set_ml_status(
        MlStatus(
            ml_id=ml_id,
            status="Not running",
            details="Success ML run completed",
            running_time=str(total_running_time),
        )
    )
