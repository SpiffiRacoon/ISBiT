# own
from ..ml_lib import get_model_instance
from ..types import Node
from ..db import add_clustered_data

# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/run_ml",
    tags=["Run ML"],
)


@router.get("/", status_code=200)
def run(model_name: str, file: str):
    """
    Run a ML model on a file

    Ex)
    model: qaqc_test

    file: swe_qaqc_lib_test
    """

    x = get_model_instance(model_name)
    try:
        x.run(file_name=file, is_first=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    df = x.df
    list_of_nodes = [Node(**one_node) for one_node in df.to_dict("records")]
    add_clustered_data(list_of_nodes, collection=file)

    return {"status": "success"}
