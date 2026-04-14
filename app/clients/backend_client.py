from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings
from app.utils.logger import logger
from app.utils.response import failure, success


class BackendClient:
    def __init__(self, base_url: str, timeout: float, max_retries: int) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    async def get(self, path: str) -> str:
        return await self._request("GET", path)

    async def post(self, path: str, payload: dict[str, Any]) -> str:
        return await self._request("POST", path, json=payload)

    async def _request(self, method: str, path: str, **kwargs: Any) -> str:
        error_message = "Backend request failed"

        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(
                    base_url=self.base_url,
                    timeout=self.timeout,
                ) as client:
                    response = await client.request(method, path, **kwargs)
                response.raise_for_status()
                return success(response.json())
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                logger.error("Backend returned %s for %s %s", status_code, method, path)
                return failure(self._status_message(status_code, path))
            except httpx.TimeoutException:
                error_message = "Backend request timed out"
                if attempt == self.max_retries:
                    logger.error("%s: %s %s", error_message, method, path)
                    return failure(error_message)
            except httpx.RequestError:
                error_message = "Could not reach backend"
                if attempt == self.max_retries:
                    logger.error("%s: %s %s", error_message, method, path)
                    return failure(error_message)
            except ValueError:
                logger.error("Backend returned invalid JSON for %s %s", method, path)
                return failure("Backend returned invalid JSON")

        return failure(error_message)

    @staticmethod
    def _status_message(status_code: int, path: str) -> str:
        if status_code == 404:
            return f"Resource not found: {path}"
        if status_code == 422:
            return "Backend rejected the request"
        if status_code >= 500:
            return "Backend error"
        return f"Backend returned {status_code}"


backend_client = BackendClient(
    base_url=settings.backend_url,
    timeout=settings.timeout,
    max_retries=settings.max_retries,
)
