# own
from ..ml_lib import get_model_instance
from ..types import Node
from ..db import add_multiple_nodes_to
from ..db import add_about_node_to_id, add_multiple_nodes_to_id

# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/run_ml",
    tags=["Run ML"],
)

@router.get("/", status_code=200)
def run(model_name: str, file: str, dim_red_method: str | None = None) -> dict:
    """
    Run a ML model on a file

    Ex)
    model: qaqc_main

    file: swe_qaqc_lib_test

    dim_red_method: COMBO

    NOTE: If you want to use the qaqc_test model, the dim_red_method field can be left blank because it will only use PCA.
    """

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

    return {"status": "success"}