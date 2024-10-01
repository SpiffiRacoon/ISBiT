from pydantic import BaseModel


class Node(BaseModel):
    """
    Datamodel for a node
    """

    id: int
    cluster: str
    text: str
    coordinates: tuple[float, float]
    is_categorized: bool = False
    category: str | None = None

    def __init__(self, **data):
        super().__init__(**data)
