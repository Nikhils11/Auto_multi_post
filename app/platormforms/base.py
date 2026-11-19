from __future__ import annotations
from app.config import Config, get_config 
from app.schemas import Request_DTO, Platform_Result
import httpx


class Platform_Base:
            
    def __init__(self, platform_name : str = "Platform_Base", config : Config | None = None):
        self.platform_name = platform_name
        self.config = get_config()        

    def build_base_headers(self) -> dict:
        headers = {
            "Content-Type": "application/json"
        }
        return headers
    
    def build_headers_with_auth(self, access_token: str) -> dict:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"                                      
            
            }
        return headers
    
    async def proccess_request(self, client: httpx.AsyncClient, request: Request_DTO) -> Platform_Result:
        raise NotImplementedError("Subclasses must implement this method.")