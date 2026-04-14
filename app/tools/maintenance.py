from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from mcp.server.fastmcp import FastMCP

from app.services.rent_manager import rent_manager_service
from app.tools._common import READ_HINTS, WRITE_HINTS, parse_input, run_tool


class MaintenanceRequestInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    unit: str = Field(min_length=2, max_length=5)
    issue: str = Field(min_length=5, max_length=200)
    priority: Literal["low", "normal", "high"] = "normal"


def register(mcp: FastMCP) -> None:
    @mcp.tool(name="get_all_maintenance", annotations=READ_HINTS)
    async def get_all_maintenance() -> str:
        """List all maintenance requests."""
        return await run_tool(
            "get_all_maintenance",
            rent_manager_service.get_all_maintenance,
        )

    @mcp.tool(name="get_open_maintenance", annotations=READ_HINTS)
    async def get_open_maintenance() -> str:
        """List open maintenance requests."""
        return await run_tool(
            "get_open_maintenance",
            rent_manager_service.get_open_maintenance,
        )

    @mcp.tool(name="create_maintenance_request", annotations=WRITE_HINTS)
    async def create_maintenance_request(
        unit: str,
        issue: str,
        priority: str = "normal",
    ) -> str:
        """Create a maintenance ticket."""
        data = parse_input(
            MaintenanceRequestInput,
            unit=unit,
            issue=issue,
            priority=priority,
        )
        return await run_tool(
            "create_maintenance_request",
            lambda: rent_manager_service.create_maintenance_request(data.model_dump()),
        )
