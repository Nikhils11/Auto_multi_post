from unittest import result

from fastapi import FastAPI
from app.services.publisher_service import PublisherService
from app.routers import posting


app = FastAPI()

app.include_router(
    router=posting.router)