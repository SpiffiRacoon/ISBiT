# std
from datetime import datetime

# pip
from pydantic import BaseModel

class MlStatus(BaseModel):
    """
    Datamodel for the ml_status collection
    """
    ml_id: str
    status: str
    details: str
    running_time: str = ""
    updated: str


    def __init__(self, *args, **kwargs) -> None:
        if "_id" in kwargs:
            kwargs.pop("_id")

        if "updated" in kwargs:
            kwargs["updated"] = str(kwargs["updated"])
        else:
            kwargs["updated"] = str(datetime.now())
        super().__init__(*args, **kwargs)
