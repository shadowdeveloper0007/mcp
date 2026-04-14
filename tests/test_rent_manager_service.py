from __future__ import annotations

import pytest

from app.services.cache import TTLCache
from app.services.rent_manager import RentManagerService


class StubClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    async def get(self, path: str, **_: object) -> dict:
        self.calls.append(("GET", path))
        return {"path": path}

    async def post(self, path: str, payload: dict) -> dict:
        self.calls.append(("POST", path))
        return {"path": path, "payload": payload}


@pytest.mark.asyncio
async def test_service_caches_read_requests() -> None:
    client = StubClient()
    service = RentManagerService(
        client=client,
        cache=TTLCache(30),
        cache_enabled=True,
    )

    first = await service.get_all_units()
    second = await service.get_all_units()

    assert first == second
    assert client.calls == [("GET", "/units")]


@pytest.mark.asyncio
async def test_service_invalidates_related_cache_after_write() -> None:
    client = StubClient()
    service = RentManagerService(
        client=client,
        cache=TTLCache(30),
        cache_enabled=True,
    )

    await service.get_all_maintenance()
    await service.get_portfolio_summary()
    await service.create_maintenance_request(
        {"unit": "4B", "issue": "Leaking tap", "priority": "high"}
    )
    await service.get_all_maintenance()
    await service.get_portfolio_summary()

    assert client.calls == [
        ("GET", "/maintenance"),
        ("GET", "/summary"),
        ("POST", "/maintenance"),
        ("GET", "/maintenance"),
        ("GET", "/summary"),
    ]
