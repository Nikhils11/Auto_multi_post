from app.schemas import Publish_Response, Request_DTO, Platform_Result, Response_DTO 
from datetime import date, time, datetime, timezone
from app.platormforms.bluesky import Platform_Bluesky
import httpx

class PublisherService:
    
    def __init__(self):
       self.one = 1 
        
    async def publish_message(self,request: Request_DTO) -> Response_DTO:
        
        client = httpx.AsyncClient()
        # breakpoint()
        platfrom_bluesky_response = await Platform_Bluesky().proccess_request(client, request)
        
        # breakpoint()
        # await client.aclose()
        return Response_DTO(publish_response=Publish_Response(success=True, results=[platfrom_bluesky_response]))
       


