from app.schemas import Publish_Response, Request_DTO, Platform_Result, Response_DTO 
from datetime import date, time, datetime, timezone
from app.platormforms.bluesky import Platform_Bluesky
import httpx
from app.platormforms.mastdon import Platform_Mastodon
from app.platormforms.devto import Platfrom_DevTo
from app.platormforms.gist import Platform_Gist
from app.platormforms.telegram import Platform_Telegram


class PublisherService:
    
    def __init__(self):
       self.one = 1 
        
    async def publish_message(self,request: Request_DTO) -> Response_DTO: 
        try:
            client = httpx.AsyncClient()
            platfrom_bluesky_response = await Platform_Bluesky().proccess_request(client, request)
            platform_mastodon_response = await Platform_Mastodon().proccess_request(client, request)
            platform_devto_response = await Platfrom_DevTo().porcess_request(client, request)
            platform_gist_response = await Platform_Gist().proccess_request(client, request)
            platform_telegram_result = await Platform_Telegram().proccess_request(client, request)
            return Response_DTO(publish_response=Publish_Response(success=True, results=[platform_gist_response,               platform_devto_response, platform_mastodon_response, platfrom_bluesky_response, platform_telegram_result]))
        except Exception as e:
            print(e.__str__())
            return Response_DTO(publish_response=Publish_Response(success=False))

