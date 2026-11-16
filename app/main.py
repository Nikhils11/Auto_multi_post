from unittest import result

from fastapi import FastAPI
from app.services.publisher_service import PublisherService
from app.schemas import Request_Model, Response_Model

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/posting")
def posting(request: Request_Model):
    response = PublisherService().publish_message(request)
    return response