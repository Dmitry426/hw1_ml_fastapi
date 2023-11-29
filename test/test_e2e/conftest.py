import asyncio
import logging
from typing import Any, Dict, Optional

import pytest_asyncio
from aiohttp import ClientSession
from pydantic import BaseModel

from .settings import TestSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTTPResponse(BaseModel):
    body: Any
    headers: Dict[str, Any]
    status: int


@pytest_asyncio.fixture(name="event_loop", scope="session")
def event_loop_fixture() -> asyncio.AbstractEventLoop:
    """Create an instance of the default event loop."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="settings", scope="session")
def settings_fixture() -> TestSettings:
    return TestSettings()


@pytest_asyncio.fixture(name="http_client", scope="session")
async def http_client_fixture(settings) -> ClientSession:
    """Represents HTTP client fixture.

    """
    async with ClientSession(
            base_url=f"http://{settings.url_settings.host}:{settings.url_settings.port}"
    ) as session:
        yield session


@pytest_asyncio.fixture(name="make_request", scope="session")
def make_request_fixture(http_client: ClientSession):
    """Make HTTP-request"""

    async def inner(
            method: str,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            jwt: Optional[str] = None,
    ) -> HTTPResponse:
        params = params or {}
        json = json or {}
        headers = {}

        if jwt:
            headers = {"Authorization": "Bearer {}".format(jwt)}

        logger.debug("URL: %s", url)

        async with http_client.request(
                method, url, params=params, json=json, headers=headers
        ) as response:
            body = await response.json()
            logger.warning("Response: %s", body)

            return HTTPResponse(
                body=body,
                headers=response.headers,
                status=response.status,
            )

    return inner
