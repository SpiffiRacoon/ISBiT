# own
from ..db import get_all_nodes_from as db_get_all_nodes_from
from ..types import Node
from ..utils import simulate_user_input  # import the function to simulate labels

# pip
from fastapi import APIRouter, HTTPException

# Define the router for testing
router = APIRouter(
    prefix="/testing",
    tags=["Testing"],
)

@router.post("/simulate_labels", status_code=200)
def simulate_labels_route(collection: str, fraction: float = 0.1):
    """
    Update a fraction of nodes in the specified collection with input labels set to the truth value.
    """
    try:
        simulate_user_input(collection=collection, fraction=fraction)
        return {"message": "Labels simulated and updated in the database"}
    except Exception as e:
        raise e
