# own
from ..shared import IsbitClassifierModel

from importlib import import_module
from inspect import getmembers, isclass


def get_instance(model_name: str) -> IsbitClassifierModel:
    """
    Dynamic import to create a instance of a model class.
    """

    ModelClass = _get_class_instance(model_name)()

    return ModelClass


def _get_class_instance(class_name: str):
    module_path = "src.ml_lib.sub_models"

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        for name, obj in getmembers(module, isclass):
            if obj.__module__ == module_path and name == class_name:
                return obj

    raise AttributeError(f"Class '{class_name}' not found in module '{module_path}'")
