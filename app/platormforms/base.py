from app.schemas import Request_Model, Response_Model, Result_Model
import httpx

class Platform_Base:
            
   async def proccess_request(self, client: httpx.AsyncClient, request: Request_Model) -> Response_Model:
        raise NotImplementedError("Subclasses must implement this method.")