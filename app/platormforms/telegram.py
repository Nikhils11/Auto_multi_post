from app.platormforms.base import Platform_Base
from app.schemas import Request_DTO, Platform_Result
import httpx


class Platform_Telegram(Platform_Base):
    
    def __init__(self):
        super().__init__("Telegram")
        
    def build_request_payload(self, request: Request_DTO)-> dict:
        payload = {
                   "chat_id": self.config.telegram_channel_id,
                   "text": request.message
                }
        return payload
    
    def build_post_request_url(self) -> str:
        post_request_url = f"{self.config.telegram_base_url}bot{self.config.telegram_api_token}/sendmessage"
        return post_request_url
    
    async def proccess_request(self, client: httpx.AsyncClient, request: Request_DTO) -> Platform_Result:
        try:
          request_payload = self.build_request_payload(request)
          request_headers = self.build_base_headers()
          post_request_url = self.build_post_request_url()
          post_reqeust_response = await client.post(url=post_request_url,
                                                    json=request_payload, headers=request_headers)
          response_json = post_reqeust_response.json()
          if (post_reqeust_response.status_code == 200):
              posted_url = f"{self.config.telegram_channel_url}{response_json.get('result')["message_id"]}"
              return Platform_Result.success(platform=self.platform_name, posted_url=posted_url, public_access=True)
          else:
              return Platform_Result.failure(platform=self.platform_name, error=post_reqeust_response.text)
        except Exception as e:
            print(e.__str__())
            return Platform_Result.failure(platform=self.platform_name, error=e.__str__())
