# pip
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/clustering",
    tags=["Clustering"],
)


@router.post("/", status_code=204)
def run_clustering(colletion: str) -> None:
    """
    Run clustering on a collection
    """

    raise HTTPException(status_code=501, detail="Not implemented")
