from app.schemas import Publish_Response, Request_DTO, Platform_Result
from app.platormforms.bluesky import Platform_Bluesky
import httpx
from app.platormforms.mastdon import Platform_Mastodon
from app.platormforms.devto import Platform_DevTo
from app.platormforms.gist import Platform_Gist
from app.platormforms.telegram import Platform_Telegram
import asyncio


class PublisherService:

    async def publish_message(self, request: Request_DTO) -> Publish_Response:
        async with httpx.AsyncClient() as client:
            platform_requests = [
                ("Bluesky", Platform_Bluesky().proccess_request(client, request)),
                ("Dev.To", Platform_DevTo().proccess_request(client, request)),
                ("Gist", Platform_Gist().proccess_request(client, request)),
                ("Mastodon", Platform_Mastodon().proccess_request(client, request)),
                ("Telegram", Platform_Telegram().proccess_request(client, request)),
            ]
            raw_results = await asyncio.gather(
                *(request for _, request in platform_requests),
                return_exceptions=True,
            )

        results = [
            Platform_Result.failure(platform, str(result))
            if isinstance(result, BaseException)
            else result
            for (platform, _), result in zip(platform_requests, raw_results)
        ]
        success = any(result.status == "success" for result in results)
        return Publish_Response(success=success, results=results)
