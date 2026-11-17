from typing import Literal, Optional
from pydantic import BaseModel, Field
from datetime import date, time, datetime, timezone

class Request_DTO(BaseModel):
    message: str = Field(max_length=200  ,                       description="The message to be posted.")
    
class Platform_Result(BaseModel):
    platform: str
    status: str
    posted_url: Optional[str] = None
    public_access: Optional[bool] = False
    date: Optional[datetime] = None
    time: Optional[datetime] = None
    error: Optional[str] = None
    
    @classmethod
    def success(cls, platform: str, posted_url: Optional[str] = None, public_access: Optional[bool] = False) -> "Platform_Result":
        return cls(
            platform=platform,
            status="success",
            posted_url=posted_url,
            public_access=public_access,
            date=date.today(),
            time=datetime.now(timezone.utc),
            error=None
        )
        
    @classmethod
    def failure(cls, platform: str, error: str) -> "Platform_Result":
        return cls(
            platform=platform,
            status="failure",
            posted_url=None,
            public_access=False,
            date=date.today(),
            time=datetime.now(timezone.utc),
            error=error
        )

class Publish_Response(BaseModel):
    success: bool
    results: list[Platform_Result]
    
class Response_DTO(BaseModel):
    publish_response: Publish_Response