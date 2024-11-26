# std
from concurrent.futures import ThreadPoolExecutor

from ..ml_lib.sub_models import __all__ as ml_lib_methods


# pip
from fastapi import APIRouter

router = APIRouter(
    prefix="/ml",
    tags=["ML"],
)

executor = ThreadPoolExecutor(max_workers=10)


@router.get("/dim", status_code=200)
def get_all_dim_methods() -> list:
    """
    Returns a list of all dimensionality reduction methods.

    TODO:
        Make this dynamic. It is currently hardcoded.
    """
    return ["COMBO", "PCA", "TSNE", "UMAP"]


@router.get("/models", status_code=200)
def get_all_models() -> list:
    return ml_lib_methods
