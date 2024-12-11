# own
from ..db import (
    get_all_labels_from as db_get_all_labels,
    get_nodes_from_latest_version as db_get_nodes_from_latest_version,
    label_one_node as db_label_one_node,
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
    nodes = db_get_nodes_from_latest_version(dataset_name=collection)
    nodes = [Node(**node) for node in nodes.to_dict(orient="records")]
    return nodes


@router.get("/labels", status_code=200)
def get_all_labels(
    collection: str,
) -> list[str] | None:
    """
    Get all labels for a collection from database.
    """
    labels = db_get_all_labels(collection=collection)
    return labels


@router.post("/categorize", status_code=204)
def categorize_node(node_id: str, category: str, dataset_name: str) -> None:
    """
    Categorize a node
    """
    try:
        db_label_one_node(node_id, category, dataset_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
