from app.schemas import Request_DTO, Platform_Result
from app.config import Config, get_config
import httpx   
from app.platormforms.base import Platform_Base


class Platfrom_DevTo(Platform_Base):
    
    def __init__(self, config : Config | None = None):
        super().__init__("Dev.To")
        
    
    def build_post_message_headers(self):
        headers = {
                "api-key": self.config.devto_api_key,
                "Content-Type": "application/json"                                      
                }
        return headers
    
    def build_request_payload(self, request: Request_DTO) -> dict:
        payload = {
                "article": {
                    # Over here we can have an LLM call which genrates 
                    # a unique title for every reqeust based on the request.message
                    "title": request.message,
                    "published": True,
                    "body_markdown": request.message
                }
            }
        return payload
    
    async def porcess_request(self, client : httpx.AsyncClient, request : Request_DTO) -> Platform_Result:
        try:
            headers = self.build_post_message_headers()
            request_payload = self.build_request_payload(request)
            post_message_response = await client.post(url=self.config.devto_post_url, json=request_payload,
                                                      headers=headers)
            if (post_message_response.status_code == 201):
                posted_url = post_message_response.json().get('url')
                result = Platform_Result.success(platform=self.platform_name, posted_url=posted_url, public_access=True)
                return result
            else:
                return Platform_Result.failure(platform=self.platform_name, error=post_message_response.error)
        except Exception as e:
            print(e.__str__())
            return Platform_Result.failure(platform=self.platform_name, error=e.__str__())
            
    
