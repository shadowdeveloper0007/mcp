from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.services.rent_manager import rent_manager_service
from app.tools._common import READ_HINTS, run_tool


def register(mcp: FastMCP) -> None:
    @mcp.tool(name="get_all_units", annotations=READ_HINTS)
    async def get_all_units() -> str:
        """List all units."""
        return await run_tool("get_all_units", rent_manager_service.get_all_units)

    @mcp.tool(name="get_vacant_units", annotations=READ_HINTS)
    async def get_vacant_units() -> str:
        """List vacant units."""
        return await run_tool("get_vacant_units", rent_manager_service.get_vacant_units)
