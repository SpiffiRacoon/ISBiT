from .ping import router as ping_router
from .data import router as data_router
from .dataset import router as collections_router
from .run_ml import router as run_ml_router
from .testing import router as testing_router
from .ml import router as ml_router


__all__ = ["ping_router", "data_router", "collections_router", "run_ml_router", "testing_router", "ml_router"]
