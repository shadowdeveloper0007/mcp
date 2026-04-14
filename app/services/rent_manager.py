from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from app.clients.backend_client import BackendClient, backend_client
from app.core.config import settings
from app.services.cache import TTLCache


class RentManagerService:
    def __init__(
        self,
        client: BackendClient,
        cache: TTLCache | None = None,
        *,
        cache_enabled: bool = True,
    ) -> None:
        self.client = client
        self.cache = cache
        self.cache_enabled = cache_enabled and cache is not None

    async def get_all_tenants(self) -> dict[str, Any]:
        return await self._get_cached("tenants:all", lambda: self.client.get("/tenants"))

    async def get_unpaid_tenants(self) -> dict[str, Any]:
        return await self._get_cached("tenants:unpaid", lambda: self.client.get("/tenants/unpaid"))

    async def get_tenant_by_id(self, tenant_id: str) -> dict[str, Any]:
        return await self._get_cached(
            f"tenants:{tenant_id}",
            lambda: self.client.get(f"/tenants/{tenant_id}"),
        )

    async def get_all_units(self) -> dict[str, Any]:
        return await self._get_cached("units:all", lambda: self.client.get("/units"))

    async def get_vacant_units(self) -> dict[str, Any]:
        return await self._get_cached("units:vacant", lambda: self.client.get("/units/vacant"))

    async def get_all_maintenance(self) -> dict[str, Any]:
        return await self._get_cached("maintenance:all", lambda: self.client.get("/maintenance"))

    async def get_open_maintenance(self) -> dict[str, Any]:
        return await self._get_cached(
            "maintenance:open",
            lambda: self.client.get("/maintenance/open"),
        )

    async def create_maintenance_request(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = await self.client.post("/maintenance", payload)
        self.invalidate_maintenance_cache()
        return response

    async def get_portfolio_summary(self) -> dict[str, Any]:
        return await self._get_cached("summary:portfolio", lambda: self.client.get("/summary"))

    async def health_check(self) -> dict[str, Any]:
        return await self.client.get("/health")

    def invalidate_maintenance_cache(self) -> None:
        if not self.cache_enabled:
            return

        self.cache.invalidate_prefix("maintenance:")
        self.cache.invalidate_prefix("summary:")

    async def _get_cached(
        self,
        key: str,
        fetcher: Callable[[], Awaitable[dict[str, Any]]],
    ) -> dict[str, Any]:
        if self.cache_enabled:
            cached_value = self.cache.get(key)
            if cached_value is not None:
                return cached_value

        data = await fetcher()
        if self.cache_enabled:
            self.cache.set(key, data)
        return data


rent_manager_service = RentManagerService(
    client=backend_client,
    cache=TTLCache(settings.cache_ttl_seconds),
    cache_enabled=settings.cache_enabled,
)
