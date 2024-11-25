# own
from . import v1

# pip
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(
    title="Isbit API",
    version="0.1.0",
    redoc_url=None,
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for page in v1.__all__:
    router = getattr(v1, page)
    app.include_router(router, prefix="/V1")
