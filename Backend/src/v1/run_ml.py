# own
from ..ml_lib import get_model_instance
from ..types import Node
from ..db import add_multiple_nodes_to

# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/run_ml",
    tags=["Run ML"],
)

@router.get("/", status_code=200)
def run(model_name: str, file: str, dim_red_method: str) -> dict:
    """
    Run a ML model on a file

    Ex)
    model: qaqc_main

    file: swe_qaqc_lib_test

    dim_red_method: COMBO

    NOTE: If you want to use the test model, the dim_red_method will not be read, but has to be filled in with something.
    """

    model_obj = get_model_instance(model_name)
    try:
        model_obj.run(file_name=file, is_first=True, dim = dim_red_method)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    df = model_obj.df
    list_of_nodes = [Node(**one_node) for one_node in df.to_dict("records")]
    add_multiple_nodes_to(list_of_nodes, collection=file)

    return {"status": "success"}