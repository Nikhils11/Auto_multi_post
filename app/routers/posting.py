from fastapi import APIRouter, Depends
from app.schemas import Request_DTO, Publish_Response
from app.services.publisher_service import PublisherService


router = APIRouter()

@router.post("/posting", response_model=Publish_Response)
async def posting(request: Request_DTO, publisher_service: PublisherService = Depends(PublisherService)) -> Publish_Response:

        response = await publisher_service.publish_message(request)
        return response
