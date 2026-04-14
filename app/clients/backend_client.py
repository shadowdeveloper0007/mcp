from __future__ import annotations

import asyncio
from time import perf_counter
from typing import Any

import httpx

from app import __version__
from app.core.config import settings
from app.core.errors import AppError
from app.utils.logger import get_logger, log_event


logger = get_logger(__name__)


class BackendClient:
    def __init__(
        self,
        base_url: str,
        timeout: float,
        max_retries: int,
        retry_backoff_seconds: float,
        *,
        api_key: str | None = None,
        auth_header: str = "X-API-Key",
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.api_key = api_key
        self.auth_header = auth_header
        self.transport = transport

    async def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "GET",
            path,
            retryable=True,
            params=params,
        )

    async def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        return await self._request("POST", path, retryable=False, json=payload)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        retryable: bool,
        **kwargs: Any,
    ) -> dict[str, Any]:
        for attempt in range(self.max_retries + 1):
            started = perf_counter()
            try:
                async with self._build_client() as client:
                    response = await client.request(method, path, **kwargs)
                duration_ms = round((perf_counter() - started) * 1000, 2)

                if response.status_code >= 500 and retryable and attempt < self.max_retries:
                    await self._wait_before_retry(attempt)
                    continue

                response.raise_for_status()
                payload = response.json()
                log_event(
                    logger,
                    "info",
                    "backend.request",
                    method=method,
                    path=path,
                    status_code=response.status_code,
                    duration_ms=duration_ms,
                    attempt=attempt + 1,
                )
                return payload
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                should_retry = retryable and status_code in {429, 502, 503, 504}
                if should_retry and attempt < self.max_retries:
                    await self._wait_before_retry(attempt)
                    continue

                raise AppError(
                    self._status_message(status_code, path),
                    code=self._error_code_from_status(status_code),
                    retryable=should_retry,
                    details={"status_code": status_code, "path": path},
                ) from exc
            except httpx.TimeoutException as exc:
                if retryable and attempt < self.max_retries:
                    await self._wait_before_retry(attempt)
                    continue

                raise AppError(
                    "Backend request timed out",
                    code="backend_timeout",
                    retryable=retryable,
                    details={"path": path},
                ) from exc
            except httpx.RequestError as exc:
                if retryable and attempt < self.max_retries:
                    await self._wait_before_retry(attempt)
                    continue

                raise AppError(
                    "Could not reach backend",
                    code="backend_unreachable",
                    retryable=retryable,
                    details={"path": path},
                ) from exc
            except ValueError as exc:
                raise AppError(
                    "Backend returned invalid JSON",
                    code="invalid_backend_response",
                    details={"path": path},
                ) from exc

        raise AppError("Backend request failed", code="backend_request_failed")

    def _build_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            transport=self.transport,
            headers=self._headers(),
        )

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "User-Agent": f"rent-manager-mcp/{__version__}",
        }
        if self.api_key:
            headers[self.auth_header] = self.api_key
        return headers

    async def _wait_before_retry(self, attempt: int) -> None:
        delay = self.retry_backoff_seconds * (attempt + 1)
        if delay > 0:
            await asyncio.sleep(delay)

    @staticmethod
    def _status_message(status_code: int, path: str) -> str:
        if status_code == 404:
            return f"Resource not found: {path}"
        if status_code == 401:
            return "Backend authentication failed"
        if status_code == 403:
            return "Backend request was forbidden"
        if status_code == 422:
            return "Backend rejected the request"
        if status_code >= 500:
            return "Backend error"
        return f"Backend returned {status_code}"

    @staticmethod
    def _error_code_from_status(status_code: int) -> str:
        if status_code == 404:
            return "not_found"
        if status_code in {401, 403}:
            return "authentication_error"
        if status_code == 422:
            return "validation_error"
        if status_code >= 500:
            return "backend_error"
        return "backend_http_error"


backend_client = BackendClient(
    base_url=settings.backend_url,
    timeout=settings.timeout,
    max_retries=settings.max_retries,
    retry_backoff_seconds=settings.retry_backoff_seconds,
    api_key=settings.backend_api_key,
    auth_header=settings.backend_auth_header,
)
