import re
from typing import Optional
from pydantic import AnyHttpUrl, BaseModel, Field, TypeAdapter, field_validator
from datetime import date as Date, datetime, time as Time, timezone

URL_PATTERN = re.compile(r"https?://[^\s<>]+")
URL_ADAPTER = TypeAdapter(AnyHttpUrl)


class Request_DTO(BaseModel):
    message: str = Field(max_length=200  ,                       description="The message to be posted.")
    
    @field_validator("message")
    @classmethod
    def require_one_valid_link(cls, message: str) -> str:
        links = [match.rstrip(".,!?;:") for match in URL_PATTERN.findall(message)]

        if len(links) != 1:
            raise ValueError("Message must contain exactly one URL.")

        try:
            URL_ADAPTER.validate_python(links[0])
        except ValueError as exc:
            raise ValueError("The URL must be a valid HTTP or HTTPS link.") from exc

        return message

class Platform_Result(BaseModel):
    platform: str
    status: str
    posted_url: Optional[str] = None
    public_access: Optional[bool] = False
    date: Optional[Date] = None
    time: Optional[Time] = None
    error: Optional[str] = None
    
    @classmethod
    def success(cls, platform: str, posted_url: Optional[str] = None, public_access: Optional[bool] = False) -> "Platform_Result":
        posted_at = datetime.now(timezone.utc)
        return cls(
            platform=platform,
            status="success",
            posted_url=posted_url,
            public_access=public_access,
            date=posted_at.date(),
            time=posted_at.time().replace(tzinfo=None),
            error=None
        )
        
    @classmethod
    def failure(cls, platform: str, error: str) -> "Platform_Result":
        return cls(
            platform=platform,
            status="failure",
            posted_url=None,
            public_access=False,
            error=error
        )

class Publish_Response(BaseModel):
    success: bool
    results: Optional[list[Platform_Result]] = None
