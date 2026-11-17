from app.schemas import Request_DTO, Platform_Result, Response_DTO
import httpx

class Platform_Base:
            
   async def proccess_request(self, client: httpx.AsyncClient, request: Request_DTO) -> Response_DTO:
        raise NotImplementedError("Subclasses must implement this method.")