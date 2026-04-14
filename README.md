# Rent Manager MCP Server

Production-oriented MCP server for a rent management backend.

It keeps the MCP layer on `stdio`, pushes backend access into a client, and keeps business logic in a service layer so the same code can be reused by Claude Code, Claude Desktop, tests, or another host process.

## What is in the project

- `app/mcp_server.py`: builds the FastMCP server and registers tools
- `app/tools/`: MCP-facing tool definitions and input validation
- `app/services/`: business logic, caching, and cache invalidation
- `app/clients/`: outbound backend HTTP client with retries and timeouts
- `app/core/`: configuration and shared errors
- `backend/`: local demo backend for development and testing

## Project layout

```text
.
|-- app
|   |-- clients
|   |   `-- backend_client.py
|   |-- core
|   |   |-- config.py
|   |   `-- errors.py
|   |-- services
|   |   |-- cache.py
|   |   `-- rent_manager.py
|   |-- tools
|   |   |-- _common.py
|   |   |-- maintenance.py
|   |   |-- summary.py
|   |   |-- tenants.py
|   |   `-- units.py
|   |-- cli.py
|   `-- mcp_server.py
|-- backend
|   |-- cli.py
|   |-- data.py
|   `-- main.py
|-- tests
|   |-- test_backend_client.py
|   |-- test_response.py
|   `-- test_rent_manager_service.py
|-- .env.example
|-- pyproject.toml
|-- README.md
|-- requirements.txt
`-- server.py
```

## Runtime model

- MCP transport is `stdio`
- Claude launches the server as a command
- The MCP server calls the backend over HTTP
- Read operations can use an in-memory TTL cache
- Write operations invalidate related cached data

## Quick start

### 1. Create the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

If you prefer runtime-only dependencies:

```powershell
pip install -r requirements.txt
```

### 2. Create your environment file

```powershell
Copy-Item .env.example .env
```

Default local config:

```env
ENVIRONMENT=development
BACKEND_URL=http://localhost:8000
TIMEOUT=5
MAX_RETRIES=2
RETRY_BACKOFF_SECONDS=0.25
MCP_SERVER_NAME=rent_manager_mcp
LOG_LEVEL=INFO
LOG_FORMAT=text
CACHE_ENABLED=true
CACHE_TTL_SECONDS=15
BACKEND_AUTH_HEADER=X-API-Key
BACKEND_API_KEY=
```

### 3. Run the demo backend

```powershell
rent-manager-backend
```

If your virtualenv is not activated:

```powershell
.\.venv\Scripts\rent-manager-backend.exe
```

or:

```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Health check:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health | Select-Object -ExpandProperty Content
```

### 4. Run the MCP server

```powershell
rent-manager-mcp
```

If your virtualenv is not activated:

```powershell
.\.venv\Scripts\rent-manager-mcp.exe
```

or:

```powershell
python server.py
```

This is a `stdio` MCP server. It is not an HTTP MCP endpoint.

## Claude Code integration

From the project root:

```powershell
claude mcp add --transport stdio --scope project rent_manager_mcp -- rent-manager-mcp
```

If you are not installing the package, use:

```powershell
claude mcp add --transport stdio --scope project rent_manager_mcp -- python server.py
```

Then run:

```powershell
claude
```

Inside Claude Code, use `/mcp` to confirm the server is connected.

## Claude Desktop integration

Add a stdio server entry to your Claude Desktop MCP config. Example:

```json
{
  "mcpServers": {
    "rent_manager_mcp": {
      "command": "rent-manager-mcp"
    }
  }
}
```

If you are not installing the package, point it at the project interpreter:

```json
{
  "mcpServers": {
    "rent_manager_mcp": {
      "command": "D:\\verma\\backup\\backup\\.venv\\Scripts\\python.exe",
      "args": ["D:\\verma\\backup\\backup\\server.py"]
    }
  }
}
```

## Available tools

- `get_all_tenants`
- `get_unpaid_tenants`
- `get_tenant_by_id`
- `get_all_units`
- `get_vacant_units`
- `get_all_maintenance`
- `get_open_maintenance`
- `create_maintenance_request`
- `get_portfolio_summary`
- `health_check`

Every tool returns a JSON string with this shape:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {
    "generated_at": "2026-04-14T12:34:56.000000+00:00",
    "tool": "health_check"
  }
}
```

## Testing

Run the test suite with:

```powershell
pytest
```

The tests currently cover:

- backend client success and retry behavior
- non-idempotent write behavior
- response envelope shape
- service-layer caching and cache invalidation


