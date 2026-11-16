from fastapi import APIRouter, Depends
from app.schemas import Platfrom_Result, Response_DTO
from app.services.publisher_service import PublisherService


router = APIRouter()

@router.post("/posting", response_model=Response_DTO)
async def posting(request: Request_DTO, publisher_service: PublisherService = Depends(PublisherService)):
    response = publisher_service.publish_message(request)
    return response