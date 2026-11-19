from urllib.parse import urlsplit
from app.config import Config, get_config
from app.schemas import Request_DTO, Platform_Result
import httpx
from app.platormforms.base import Platform_Base


class Platform_Mastodon(Platform_Base):
    
    def __init__(self):
        super().__init__("mastodon")
        # self.config = get_config()    
    
    def build_post_request_payload(self, request: Request_DTO) -> dict:
        payload = {
            "status": request.message,
            "visibility": "public"
        }
        
        return payload
    
    async def proccess_request(self, client: httpx.AsyncClient, request: Request_DTO) -> Platform_Result:
        try:
            request_payload = self.build_post_request_payload(request)
            headers = self.build_headers_with_auth(self.config.mastodon_access_token)
            post_message_response = await client.post(self.config.mastodon_post_url, json=request_payload, headers=headers)
            if post_message_response.status_code == 200:
                response_data = post_message_response.json()
                posted_url = response_data.get("url")
                if not posted_url and response_data.get("id"):
                    instance = urlsplit(self.config.mastodon_post_url)
                    username = self.config.mastodon_username.lstrip("@")
                    posted_url = f"{instance.scheme}://{instance.netloc}/@{username}/{response_data['id']}"
                result = Platform_Result.success(platform=self.platform_name, posted_url=posted_url, public_access=True)
                return result
            else:
                error_message = f"Failed to post message. Status code: {post_message_response.status_code}, Response: {post_message_response.text}"
                result = Platform_Result.failure(platform=self.platform_name, error=error_message)
                return result
        except Exception as e:
            result = Platform_Result.failure(platform=self.platform_name, error=e.__str__())
            return result
        