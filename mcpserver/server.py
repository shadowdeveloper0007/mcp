import requests
from fastmcp import FastMCP

BACKEND="http://localhost:8000"

mcp=FastMCP("RentManager")


def call(endpoint:str)->dict:
    """simple helper to call backend API"""

    try:
        response=requests.get(f"{BACKEND}{endpoint}",timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error":str(e)}
    

# MCP tools

@mcp.tool()
def get_all_tenants() ->dict:
    """
     Returns all tenants in the system
    """
    return call("/tenants")

@mcp.tool()
def get_unpaid_tenants() -> dict:
    """
    Returns tenants who have not paid rent this month.
    Use when asked about late payments or delinquencies.
    """
    return call("/tenants/unpaid")

@mcp.tool()
def get_vacant_units() -> dict:
    """
    Returns all vacant units available for leasing.
    Use when asked about empty units or vacancies.
    """
    return call("/units/vacant")

@mcp.tool()
def get_open_maintenance() -> dict:
    """
    Returns all open maintenance requests.
    Use when asked about pending repairs or work orders.
    """
    return call("/maintenance/open")

@mcp.tool()
def get_portfolio_summary() -> dict:
    """
    Returns a full summary of the portfolio — units, tenants,
    payments, and maintenance in one snapshot.
    Use for general overview or status questions.
    """
    return call("/summary")

@mcp.tool()
def create_maintenance_request(unit: str, issue: str, priority: str = "normal") -> dict:
    """
    Creates a new maintenance request.
    unit: unit number e.g. '4B'
    issue: description of the problem
    priority: low / normal / high
    """
    try:
        response = requests.post(
            f"{BACKEND}/maintenance",
            json={"unit": unit, "issue": issue, "priority": priority},
            timeout=5
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("MCP Server running...")
    mcp.run()