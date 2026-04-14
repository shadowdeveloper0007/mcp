import sys
import traceback

from mcp.server.fastmcp import FastMCP

from app.tools import maintenance, summary, tenants, units


def register_tools(mcp: FastMCP) -> None:
    try:
        tenants.register(mcp)
        print("✓ Registered tenants tools", file=sys.stderr)
    except Exception as e:
        print(f"ERROR registering tenants: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise
    
    try:
        units.register(mcp)
        print("✓ Registered units tools", file=sys.stderr)
    except Exception as e:
        print(f"ERROR registering units: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise
    
    try:
        maintenance.register(mcp)
        print("✓ Registered maintenance tools", file=sys.stderr)
    except Exception as e:
        print(f"ERROR registering maintenance: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise
    
    try:
        summary.register(mcp)
        print("✓ Registered summary tools", file=sys.stderr)
    except Exception as e:
        print(f"ERROR registering summary: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise
