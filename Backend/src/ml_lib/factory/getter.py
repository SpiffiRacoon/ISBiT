# own
from ..shared import IsbitClassifierModel
from ..sub_models import QaqcMainModel

import importlib
import inspect


def get_instance(model_name: str) -> IsbitClassifierModel:
    """
    Dynamic import to create a instance of a model class.
    """

    ModelClass = _get_class_instance(model_name)()

    return ModelClass


def _get_class_instance(class_name: str):
    module_path = "src.ml_lib.sub_models"

    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_path and name == class_name:
                return obj

    raise AttributeError(f"Class '{class_name}' not found in module '{module_path}'")
