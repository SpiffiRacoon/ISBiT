# own
from ..db import (
    get_all_nodes_from as db_get_all_nodes_from,
    add_one_node_to as db_add_one_node_to,
    get_all_labels_from as db_get_all_labels
)
from ..types import Node

# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/data",
    tags=["Data"],
)


@router.get("/", status_code=200)
def get_all_nodes(collection: str) -> list[Node]:
    """
    Get all nodes in one collection
    """

    nodes = db_get_all_nodes_from(collection=collection)
    return nodes

@router.get("/labels", status_code=200)
def get_all_labels(collection: str,) -> list[str] | None:
    """
    Get all labels for a collection from database.
    """
    label_dict = db_get_all_labels(collection=collection)

    # TODO: need to find a good way not to hardcode key strings like this..
    for label_doc in label_dict:
        if "about" in label_doc and "labels" in label_doc["about"]:
            for _, value in label_doc["about"]["labels"].items(): # only returns first labels attribute for now.
                if isinstance(value, list):
                    return value
                
    return None


@router.post("/", status_code=201)
def add_one_node(node: Node, collection: str) -> None:
    """
    Add one node to a collection
    """

    try:
        db_add_one_node_to(node=node, collection=collection)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return None


@router.post("/categorize", status_code=204)
def categorize_node(node_id: str, category: str, colletion: str) -> None:
    """
    Categorize a node
    """

    raise HTTPException(status_code=501, detail="Not implemented")
