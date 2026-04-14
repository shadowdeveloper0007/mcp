from mcp.server.fastmcp import FastMCP

from app.tools import maintenance, summary, tenants, units


def register_tools(mcp: FastMCP) -> None:
    tenants.register(mcp)
    units.register(mcp)
    maintenance.register(mcp)
    summary.register(mcp)
