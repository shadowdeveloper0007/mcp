from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.clients.backend_client import backend_client


class TenantLookup(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    tenant_id: str = Field(min_length=4, max_length=10, pattern=r"^T\d+$")


async def get_all_tenants() -> str:
    """Get all tenants."""
    return await backend_client.get("/tenants")


async def get_unpaid_tenants() -> str:
    """Get unpaid tenants."""
    return await backend_client.get("/tenants/unpaid")


async def get_tenant_by_id(tenant_id: str) -> str:
    """Get a tenant by id."""
    return await backend_client.get(f"/tenants/{tenant_id}")
