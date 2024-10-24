from pydantic import BaseModel


class Node(BaseModel):
    """
    Datamodel for a node
    """

    id: str | None = None
    text: str
    x: float
    y: float
    truth: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123",
                    "text": "This is a text",
                    "x": 0.1,
                    "y": 0.2,
                    "truth": "true",
                },
            ]
        }
    }

    def __init__(self, *args, **kwargs) -> None:

        if "_id" in kwargs:
            kwargs["id"] = str(kwargs["_id"])
        super().__init__(*args, **kwargs)
