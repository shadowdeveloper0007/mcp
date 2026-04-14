from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.clients.backend_client import backend_client


class MaintenanceRequestInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    unit: str = Field(min_length=2, max_length=5)
    issue: str = Field(min_length=5, max_length=200)
    priority: Literal["low", "normal", "high"] = "normal"


async def get_all_maintenance() -> str:
    """Get all maintenance requests."""
    return await backend_client.get("/maintenance")


async def get_open_maintenance() -> str:
    """Get open maintenance requests."""
    return await backend_client.get("/maintenance/open")


async def create_maintenance_request(payload: MaintenanceRequestInput) -> str:
    """Create a maintenance request."""
    return await backend_client.post("/maintenance", payload.model_dump())
