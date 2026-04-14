from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from app.core.config import settings
from app.tools import register_tools
from app.utils.logger import get_logger, log_event


logger = get_logger(__name__)


def create_mcp_server() -> FastMCP:
    server = FastMCP(settings.mcp_server_name)
    register_tools(server)
    return server


mcp = create_mcp_server()


def run() -> None:
    log_event(
        logger,
        "info",
        "mcp_server.start",
        server_name=settings.mcp_server_name,
        backend_url=settings.backend_url,
        transport="stdio",
        environment=settings.environment,
    )
    mcp.run()
