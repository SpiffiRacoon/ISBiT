# own
from ..db import (
    get_all_nodes_from as db_get_all_nodes_from,
    get_all_labels_from as db_get_all_labels,
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
def get_all_labels(
    collection: str,
) -> list[str] | None:
    """
    Get all labels for a collection from database.
    """
    labels = db_get_all_labels(collection=collection)
    return labels



@router.post("/categorize", status_code=204)
def categorize_node(node_id: str, category: str, collection: str) -> None:
    """
    Categorize a node
    """
    raise HTTPException(status_code=501, detail="Not implemented")
