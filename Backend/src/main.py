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

# CORS configuration
origins = [
    "http://localhost:3000",  # Add your frontend URL here
    "http://127.0.0.1:3000",  # In case you are using localhost
    "http://localhost:5173"
    # Add any other origins you need to allow here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

for page in v1.__all__:
    router = getattr(v1, page)
    app.include_router(router, prefix="/V1")