# own
from ..shared import IsbitClassifierModel
from ..sub_models import QaqcTestModel


def get_instance(model_name: str) -> IsbitClassifierModel:
    """
    Factory to get a ML instance of the requested model.
    """
    match model_name:
        case "qaqc_test":
            return QaqcTestModel()
        case _:
            raise Exception("Model not found")
