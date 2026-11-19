import json
import unittest
from datetime import date, time
from unittest.mock import patch

import app.services.publisher_service as publisher_service
from app.schemas import Platform_Result, Request_DTO


class RequestValidationTests(unittest.TestCase):
    def test_accepts_one_valid_http_url(self):
        request = Request_DTO(message="Visit us: https://example.com")

        self.assertEqual(request.message, "Visit us: https://example.com")

    def test_rejects_missing_or_multiple_urls(self):
        for message in (
            "Visit our website",
            "https://example.com and https://example.org",
        ):
            with self.subTest(message=message):
                with self.assertRaises(ValueError):
                    Request_DTO(message=message)

    def test_rejects_invalid_url(self):
        with self.assertRaises(ValueError):
            Request_DTO(message="Visit us: https://")

    def test_rejects_message_over_200_characters(self):
        message = f"https://example.com/{'a' * 200}"

        with self.assertRaises(ValueError):
            Request_DTO(message=message)


class PlatformResultTests(unittest.TestCase):
    def test_success_serializes_date_and_time_separately(self):
        result = Platform_Result.success(platform="test")
        serialized = json.loads(result.model_dump_json())

        self.assertIsInstance(result.date, date)
        self.assertIsInstance(result.time, time)
        self.assertEqual(len(serialized["date"]), 10)
        self.assertNotIn("T", serialized["time"])
        self.assertIsNone(serialized["error"])

    def test_failure_has_no_posted_date_or_time(self):
        result = Platform_Result.failure(platform="test", error="request failed")
        serialized = json.loads(result.model_dump_json())

        self.assertIsNone(serialized["date"])
        self.assertIsNone(serialized["time"])
        self.assertEqual(serialized["error"], "request failed")


class FakeAsyncClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return None


class FakePlatform:
    def __init__(self, platform, *, status="success", raises=False):
        self.platform = platform
        self.status = status
        self.raises = raises

    async def proccess_request(self, client, request):
        if self.raises:
            raise RuntimeError(f"{self.platform} crashed")
        if self.status == "failure":
            return Platform_Result.failure(self.platform, "posting failed")
        return Platform_Result.success(self.platform)


class PublisherServiceTests(unittest.IsolatedAsyncioTestCase):
    async def _publish_with(self, platform_states):
        platform_classes = (
            ("Platform_Bluesky", "Bluesky"),
            ("Platform_DevTo", "Dev.To"),
            ("Platform_Gist", "Gist"),
            ("Platform_Mastodon", "Mastodon"),
            ("Platform_Telegram", "Telegram"),
        )
        replacements = {
            class_name: (
                lambda platform=platform, state=platform_states.get(platform, {}):
                FakePlatform(platform, **state)
            )
            for class_name, platform in platform_classes
        }
        with (
            patch.object(publisher_service.httpx, "AsyncClient", FakeAsyncClient),
            patch.multiple(publisher_service, **replacements),
        ):
            request = Request_DTO(message="Visit us: https://example.com")
            return await publisher_service.PublisherService().publish_message(request)

    async def test_partial_success_returns_all_platform_results(self):
        response = await self._publish_with(
            {"Gist": {"status": "failure"}, "Telegram": {"raises": True}}
        )

        self.assertTrue(response.success)
        self.assertEqual(len(response.results), 5)
        self.assertEqual(response.results[2].status, "failure")
        self.assertEqual(response.results[4].error, "Telegram crashed")

    async def test_all_failures_returns_success_false_and_all_results(self):
        platform_states = {
            platform: {"raises": True}
            for platform in ("Bluesky", "Dev.To", "Gist", "Mastodon", "Telegram")
        }
        response = await self._publish_with(platform_states)

        self.assertFalse(response.success)
        self.assertEqual(len(response.results), 5)
        self.assertTrue(all(result.status == "failure" for result in response.results))


if __name__ == "__main__":
    unittest.main()
