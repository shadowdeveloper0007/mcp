from __future__ import annotations

from app.clients.backend_client import backend_client


async def get_all_units() -> str:
    """Get all units."""
    return await backend_client.get("/units")


async def get_vacant_units() -> str:
    """Get vacant units."""
    return await backend_client.get("/units/vacant")
