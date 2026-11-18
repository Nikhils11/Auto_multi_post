from typing import Annotated
from fastapi import Depends
from app.schemas import Request_DTO, Platform_Result
from app.platormforms.base import Platform_Base
import httpx
from app.config import Config, get_config
from datetime import datetime, timezone


class Platform_Bluesky(Platform_Base):
    
    def __init__(self,  config: Config | None = None):
        super().__init__("Bluesky")
          
    
    def build_session_request_payload(self) -> dict:
        payload = {
            "identifier": self.config.bluesky_username,
            "password": self.config.bluesky_password,
        }
        return payload
    
    def build_post_request_payload(self, request: Request_DTO) -> dict:
        payload = {
            "repo": self.config.bluesky_did,
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": request.message,
                "createdAt": datetime.now(timezone.utc).isoformat()
            }
        }
        return payload
    
    async def get_session_token(self, client: httpx.AsyncClient) -> str:
        request_payload = self.build_session_request_payload()
        headers = self.build_base_headers()
        session_response = await client.post(self.config.bluesky_session_url, json=request_payload, headers=headers)
        access_jwt = ""
        if session_response.status_code == 200:
            session_data = session_response.json()
            access_jwt = session_data.get("accessJwt")
        return access_jwt
        
    async def proccess_request(self, client: httpx.AsyncClient, request: Request_DTO) -> Platform_Result:
        try:
            access_jwt = await self.get_session_token(client)
            if (access_jwt == ""):
                return Platform_Result.failure(platform=self.platform_name, error="Failed to obtain access token for BlueSky platform.")        
            post_message_reqeust_payload = self.build_post_request_payload(request)        
            post_message_request_headers = self.build_headers_with_auth(access_jwt)
            post_message_response = await client.post(url=self.config.bluesky_post_url, json=post_message_reqeust_payload, headers=post_message_request_headers)
            if post_message_response.status_code == 200:
                posted_url = f"https://bsky.app/profile/nikhil200411.bsky.social/post/{post_message_response.json().get('commit')['rev']}"
                return Platform_Result.success(platform=self.platform_name, posted_url=posted_url, public_access=True)
            else:
                error_message = f"Failed to post message. Status code: {post_message_response.status_code}, Response: {post_message_response.text}"
                return Platform_Result.failure(platform=self.platform_name, error=error_message)
        except Exception as e:
            print(e.__str__())
            return Platform_Result.failure(platform=self.platform_name, error=e.__str__())
            
            
            
        

