
# own
from . import v1

# pip
from fastapi import FastAPI
import uvicorn


app = FastAPI(
    title="Te-centralen Inventory System",
    version="0.1.0",
    redoc_url=None,
)



for page in v1.__all__:
    router = getattr(v1, page)
    app.include_router(router, prefix="/V1")


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)
