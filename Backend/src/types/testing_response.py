#own
from .ml_status import MlStatus
from .node import Node
from .datasets_response import DatasetsResponse
#pip
from pydantic import BaseModel

class TestingResponse(BaseModel):
    """
    Data model for the manual test chain endpoint.
    """
    download_msgs: str = ""
    upload_msgs: str = ""
    fraction: int = ""
    ml_status: list[MlStatus] = []
    datasets: list[DatasetsResponse] = []
    labels: list[str] = []
    nodes: list[Node] = []
