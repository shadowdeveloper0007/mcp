from __future__ import annotations

import httpx
import pytest

from app.clients.backend_client import BackendClient
from app.core.errors import AppError


@pytest.mark.asyncio
async def test_backend_client_returns_json_payload() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Accept"] == "application/json"
        return httpx.Response(200, json={"status": "ok"})

    client = BackendClient(
        base_url="http://testserver",
        timeout=1,
        max_retries=0,
        retry_backoff_seconds=0,
        transport=httpx.MockTransport(handler),
    )

    result = await client.get("/health")

    assert result == {"status": "ok"}


@pytest.mark.asyncio
async def test_backend_client_retries_retryable_gets() -> None:
    attempts = {"count": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(503, json={"error": "busy"})
        return httpx.Response(200, json={"tenants": [], "total": 0})

    client = BackendClient(
        base_url="http://testserver",
        timeout=1,
        max_retries=1,
        retry_backoff_seconds=0,
        transport=httpx.MockTransport(handler),
    )

    result = await client.get("/tenants")

    assert attempts["count"] == 2
    assert result["total"] == 0


@pytest.mark.asyncio
async def test_backend_client_does_not_retry_writes() -> None:
    attempts = {"count": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        return httpx.Response(503, json={"error": "busy"})

    client = BackendClient(
        base_url="http://testserver",
        timeout=1,
        max_retries=2,
        retry_backoff_seconds=0,
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(AppError) as exc_info:
        await client.post("/maintenance", {"unit": "4B", "issue": "Leak"})

    assert attempts["count"] == 1
    assert exc_info.value.code == "backend_error"
