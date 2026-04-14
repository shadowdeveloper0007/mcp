from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from mcp.server.fastmcp import FastMCP

from app.services.rent_manager import rent_manager_service
from app.tools._common import READ_HINTS, parse_input, run_tool


class TenantIdInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    tenant_id: str = Field(min_length=4, max_length=10, pattern=r"^T\d+$")


def register(mcp: FastMCP) -> None:
    @mcp.tool(name="get_all_tenants", annotations=READ_HINTS)
    async def get_all_tenants() -> str:
        """List all tenants."""
        return await run_tool("get_all_tenants", rent_manager_service.get_all_tenants)

    @mcp.tool(name="get_unpaid_tenants", annotations=READ_HINTS)
    async def get_unpaid_tenants() -> str:
        """List unpaid tenants."""
        return await run_tool("get_unpaid_tenants", rent_manager_service.get_unpaid_tenants)

    @mcp.tool(name="get_tenant_by_id", annotations=READ_HINTS)
    async def get_tenant_by_id(tenant_id: str) -> str:
        """Fetch a tenant by ID."""
        data = parse_input(TenantIdInput, tenant_id=tenant_id)
        return await run_tool(
            "get_tenant_by_id",
            lambda: rent_manager_service.get_tenant_by_id(data.tenant_id),
        )
