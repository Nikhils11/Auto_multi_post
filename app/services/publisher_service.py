from app.schemas import Request_Model, Response_Model, Result_Model 
from datetime import date, time, datetime, timezone


class PublisherService:
    
    def __init__(self):
       self.one = 1 
        
    def publish_message(self,request:               Request_Model):
        try :
            result = Result_Model(
                platform="bluesky",
                status="success",
                posted_url=None,
                public_access=True,
                date=date.today(),
                time=datetime.now(timezone.utc),
                error=None
            )
            response = Response_Model(success=True,   
                                    results=[result])
            return response
        except Exception as e:
            print(f"Error occurred while publishing message: {e}")
            pass



