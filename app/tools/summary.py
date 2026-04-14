from __future__ import annotations

from app.clients.backend_client import backend_client


async def get_portfolio_summary() -> str:
    """Get a portfolio summary."""
    return await backend_client.get("/summary")


async def health_check() -> str:
    """Check backend health."""
    return await backend_client.get("/health")
