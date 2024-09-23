# pip
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/ping",
    tags=["Ping"],
)


@router.get("/", status_code=200)
def ping():
    """
    Test route, to check connection
    """

    return {"status": "success"}
