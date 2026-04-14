from __future__ import annotations

import sys
import traceback

from mcp.server.fastmcp import FastMCP

from app.core.config import settings
from app.tools import register_tools
from app.utils.logger import get_logger, log_event


logger = get_logger(__name__)


def create_mcp_server() -> FastMCP:
    try:
        server = FastMCP(settings.mcp_server_name)
        register_tools(server)
        return server
    except Exception as e:
        print(f"ERROR: Failed to create MCP server: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise


mcp = create_mcp_server()


def run() -> None:
    try:
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
    except Exception as e:
        print(f"ERROR: MCP server crashed: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise
