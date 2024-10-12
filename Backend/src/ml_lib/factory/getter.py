from ..sub_models import QaqcTestModel


def get_instance(model_name: str):

    match model_name:
        case "qaqc_test":
            return QaqcTestModel()
        case _:
            raise Exception("Model not found")
