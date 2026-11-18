from app.platormforms.base import Platform_Base
from app.schemas import Request_DTO, Platform_Result
import httpx


class Platform_Gist(Platform_Base):
    
    def __init__(self):
        super().__init__(platform_name="Gist")
    
    def build_request_payload(self, request : Request_DTO) -> dict:
        payload = {
                "public": True,
                "files": {
                    "message.md": {
                    "content": request.message
                    }
                }    
            }
        return payload
            
    
    async def proccess_request(self, client: httpx.AsyncClient, request : Request_DTO):
        try:
            request_payload = self.build_request_payload(request)
            headers = self.build_headers_with_auth(self.config.gist_pat_token)
            post_request_response = await client.post(url=self.config.gist_post_url, json=request_payload, headers=headers)
            if (post_request_response.status_code == 201):
               response_json = post_request_response.json()
               posted_url = response_json.get('html_url')
               result = Platform_Result.success(platform=self.platform_name, posted_url=posted_url, public_access=response_json.get('public'))
               return result
            else :
                return Platform_Result.failure(self.platform_name, error=post_request_response.error)
        except Exception as e:
            print(e.__str__())
            return Platform_Result.failure(self.platform_name, error=e.__str__())
            