from pydantic import BaseModel, Field


class Node(BaseModel):
    """
    Datamodel for a node
    """

    id: str | None = None
    cluster: int
    text: str
    x: float
    y: float
    truth: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                    {"id": "123", "cluster": 1, "text": "This is a text", "x": 0.1, "y": 0.2, "truth": "true"},
            ]
        }
    }

    def __init__(self, *args, **kwargs):

        if "_id" in kwargs:
            kwargs["id"] = str(kwargs["_id"])
        super().__init__(*args, **kwargs)
