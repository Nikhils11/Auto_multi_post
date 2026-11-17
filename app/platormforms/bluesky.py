from typing import Annotated
from fastapi import Depends
from app.schemas import Request_DTO, Platform_Result
from app.platormforms.base import Platform_Base
import httpx
from app.config import Config, get_config
from datetime import datetime, timezone


class Platform_Bluesky(Platform_Base):
    
    def __init__(self,  config: Config | None = None):
        self.session_url ="https://bsky.social/xrpc/com.atproto.server.createSession"
        self.create_record_url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
        self.platform_name = "bluesky"
        self.config = get_config()    
    
    def build_session_request_payload(self) -> dict:
        # breakpoint()
        payload = {
            "identifier": self.config.bluesky_username,
            "password": self.config.bluesky_password,
        }
        # breakpoint()
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

    def build_message_post_request_headers(self, access_jwt: str) -> dict:
        headers = {
            "Authorization": f"Bearer {access_jwt}",
            "Content-Type" : "application/json"
        }
        return headers
    
    def build_session_token_request_headers(self) -> dict:
        headers = {
            "Content-Type": "application/json"
        }
        return headers
    
    async def get_session_token(self, client: httpx.AsyncClient) -> str:
        request_payload = self.build_session_request_payload()
        headers = self.build_session_token_request_headers()
        # breakpoint()
        session_response = await client.post(self.session_url, json=request_payload, headers=headers)
        # breakpoint()
        access_jwt = ""
        if session_response.status_code == 200:
            session_data = session_response.json()
            access_jwt = session_data.get("accessJwt")
        else:
            raise Exception(f"Failed to create session. Status code: {session_response.status_code}, Response: {session_response.message}")
        return access_jwt
        
    async def proccess_request(self, client: httpx.AsyncClient, request: Request_DTO) -> Platform_Result:
        try:
            access_jwt = await self.get_session_token(client)
            if (access_jwt == ""):
                return Platform_Result.failure(platform=self.platform_name, error="Failed to obtain access token for BlueSky platform.")        
            post_message_reqeust_payload = self.build_post_request_payload(request)        
            post_message_request_headers = self.build_message_post_request_headers(access_jwt)
            post_message_response = await client.post(self.create_record_url, json=post_message_reqeust_payload, headers=post_message_request_headers)
            if post_message_response.status_code == 200:
                posted_url = f"https://bsky.app/profile/nikhil200411.bsky.social/post/{post_message_response.json().get('commit')['rev']}"
                result = Platform_Result.success(platform=self.platform_name, posted_url=posted_url, public_access=True)
                breakpoint()
                return result
            else:
                error_message = f"Failed to post message. Status code: {post_message_response.status_code}, Response: {post_message_response.text}"
                result = Platform_Result.failure(platform=self.platform_name, error=error_message)
                return result
        except Exception as e:
            result = Platform_Result.failure(platform=self.platform_name, error=e.__str__())
            return result
            # raise Exception(f"Error occurred while processing request for BlueSky platform: {e}")
            
        

