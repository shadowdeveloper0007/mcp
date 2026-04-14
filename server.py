from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from pydantic import ValidationError

from app.core.config import settings
from app.tools.maintenance import (
    MaintenanceRequestInput,
    create_maintenance_request,
    get_all_maintenance,
    get_open_maintenance,
)
from app.tools.summary import get_portfolio_summary, health_check
from app.tools.tenants import TenantLookup, get_all_tenants, get_tenant_by_id, get_unpaid_tenants
from app.tools.units import get_all_units, get_vacant_units
from app.utils.logger import logger
from app.utils.response import failure


READ_ONLY_TOOL = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
}

CREATE_TOOL = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": False,
}

mcp = FastMCP(settings.mcp_server_name)


@mcp.tool(name="get_all_tenants", annotations=READ_ONLY_TOOL)
async def get_all_tenants_tool() -> str:
    return await get_all_tenants()


@mcp.tool(name="get_unpaid_tenants", annotations=READ_ONLY_TOOL)
async def get_unpaid_tenants_tool() -> str:
    return await get_unpaid_tenants()


@mcp.tool(name="get_tenant_by_id", annotations=READ_ONLY_TOOL)
async def get_tenant_by_id_tool(tenant_id: str) -> str:
    try:
        payload = TenantLookup(tenant_id=tenant_id)
    except ValidationError:
        return failure("tenant_id must look like T001")

    return await get_tenant_by_id(payload.tenant_id)


@mcp.tool(name="get_all_units", annotations=READ_ONLY_TOOL)
async def get_all_units_tool() -> str:
    return await get_all_units()


@mcp.tool(name="get_vacant_units", annotations=READ_ONLY_TOOL)
async def get_vacant_units_tool() -> str:
    return await get_vacant_units()


@mcp.tool(name="get_all_maintenance", annotations=READ_ONLY_TOOL)
async def get_all_maintenance_tool() -> str:
    return await get_all_maintenance()


@mcp.tool(name="get_open_maintenance", annotations=READ_ONLY_TOOL)
async def get_open_maintenance_tool() -> str:
    return await get_open_maintenance()


@mcp.tool(name="create_maintenance_request", annotations=CREATE_TOOL)
async def create_maintenance_request_tool(
    unit: str,
    issue: str,
    priority: str = "normal",
) -> str:
    try:
        payload = MaintenanceRequestInput(unit=unit, issue=issue, priority=priority)
    except ValidationError:
        return failure("priority must be low, normal, or high")

    return await create_maintenance_request(payload)


@mcp.tool(name="get_portfolio_summary", annotations=READ_ONLY_TOOL)
async def get_portfolio_summary_tool() -> str:
    return await get_portfolio_summary()


@mcp.tool(name="health_check", annotations=READ_ONLY_TOOL)
async def health_check_tool() -> str:
    return await health_check()


if __name__ == "__main__":
    logger.info("Starting %s", settings.mcp_server_name)
    logger.info("Backend URL: %s", settings.backend_url)
    mcp.run()
