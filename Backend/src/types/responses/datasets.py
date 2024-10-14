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
                        {"dataset": "Dataset 1", "assignment": "labling", "datatype": "Type A", "id": "123"},
                    ]
                }
            ]
        }
    }
