from app.schemas import Request_DTO, Platform_Result, Response_DTO 
from datetime import date, time, datetime, timezone


class PublisherService:
    
    def __init__(self):
       self.one = 1 
        
    def publish_message(self,request:               Request_DTO):
        try :
            result = Platform_Result.success(
                platform="bluesky",
                        posted_url="https://example.com/post",
                public_access=True,
                date=date.today(),
                time=datetime.now(timezone.utc),
                error=None
            )
            response = Response_DTO(success=True,   
                                    results=[result])
            return response
        except Exception as e:
            print(f"Error occurred while publishing message: {e}")
            pass



