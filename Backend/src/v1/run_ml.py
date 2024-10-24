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
def run(model_name: str, file: str) -> dict:
    """
    Run a ML model on a file

    Ex)
    model: qaqc_test

    file: swe_qaqc_lib_test
    """

    model_obj = get_model_instance(model_name)
    try:
        model_obj.run(file_name=file, is_first=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    df = model_obj.df
    list_of_nodes = [Node(**one_node) for one_node in df.to_dict("records")]
    add_multiple_nodes_to(list_of_nodes, collection=file)

    return {"status": "success"}

@router.get("/", status_code=200)
def runV2(model_name: str, file: str, dim_red_method: str) -> dict:
    """
    Run a ML model on a file

    Ex)
    model: qaqc_test_v2

    file: swe_qaqc_lib_test

    dim_red_method: COMBO
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