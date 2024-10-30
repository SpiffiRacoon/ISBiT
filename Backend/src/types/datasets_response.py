from pydantic import BaseModel


class DatasetsResponse(BaseModel):
    """
    Response model for datasets
    """

    dataList: list[dict]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "dataList": [
                        {
                            "dataset": "Dataset 1",
                            "assignment": "labling",
                            "datatype": "Type A",
                            "id": "123",
                        },
                    ]
                }
            ]
        }
    }


class DatasetFileResponse(BaseModel):
    """
    Response model for dataset files
    """

    dataList: list[dict]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "dataList": [
                        {
                            "dataset": "qaqc_test_data",
                            "id": "123",
                        },
                    ]
                }
            ]
        }
    }
