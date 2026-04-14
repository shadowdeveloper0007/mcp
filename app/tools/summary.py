from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.services.rent_manager import rent_manager_service
from app.tools._common import READ_HINTS, run_tool


def register(mcp: FastMCP) -> None:
    @mcp.tool(name="get_portfolio_summary", annotations=READ_HINTS)
    async def get_portfolio_summary() -> str:
        """Get the portfolio summary."""
        return await run_tool(
            "get_portfolio_summary",
            rent_manager_service.get_portfolio_summary,
        )

    @mcp.tool(name="health_check", annotations=READ_HINTS)
    async def health_check() -> str:
        """Check backend health."""
        return await run_tool("health_check", rent_manager_service.health_check)
