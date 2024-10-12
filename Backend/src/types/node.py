from pydantic import BaseModel


class Node(BaseModel):
    """
    Datamodel for a node
    """

    _id: int | None = None
    cluster: int
    text: str
    x: float
    y: float
    truth: str

    def __init__(self, **data):
        super().__init__(**data)
