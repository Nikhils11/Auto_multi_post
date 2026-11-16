from typing import Literal
from pydantic import BaseModel
from datetime import date, time, datetime, timezone

class Request_Model(BaseModel):
    message: str
    
class Result_Model(BaseModel):
    platform: str
    status: str
    posted_url: str | None
    public_access: bool
    date: date
    time: datetime
    error: str | None

class Response_Model(BaseModel):
    success: bool
    results: list[Result_Model]
    