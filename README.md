# Rent Manager MCP Server

Production-oriented MCP server for a rent management backend.

This project has two runtime pieces:

- `backend/`: a local FastAPI demo backend served over HTTP at `http://127.0.0.1:8000`.
- `app/`: a `stdio` MCP server that Claude Code, Claude Desktop, or MCP Inspector launches as a subprocess.

Important: the MCP server is not an HTTP endpoint. Do not open it in a browser and do not configure it as an SSE or streamable HTTP server. Use `STDIO`.

## Requirements

- Python `3.12` or newer.
- PowerShell on Windows.
- Node.js/npm if you want to run MCP Inspector with `npx`.
- Claude Code or Claude Desktop if you want to test with Claude.

## Project Layout

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
|-- .env.example
|-- pyproject.toml
|-- requirements.txt
|-- README.md
`-- server.py
```

## Setup

Run these commands from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Default `.env` values:

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

## Run The Backend

Open Terminal 1 from the repository root:

```powershell
.\.venv\Scripts\rent-manager-backend.exe
```

Alternative backend command:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Verify the backend in another terminal:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health | Select-Object -ExpandProperty Content
```

Expected output:

```json
{"status":"ok","service":"rent-manager-backend"}
```

Keep the backend running while testing MCP tools.

## Run The MCP Server Manually

Open Terminal 2 from the repository root:

```powershell
.\.venv\Scripts\python.exe -m app.cli
```

The MCP server uses `stdio`, so it may look like it is waiting. That is normal. MCP clients send JSON-RPC messages through stdin/stdout. Stop it with `Ctrl+C`.

You can also run the installed script:

```powershell
.\.venv\Scripts\rent-manager-mcp.exe
```

## Test With MCP Inspector

Start the backend first, then start MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector
```

Open the Inspector URL printed in the terminal. It includes an `MCP_PROXY_AUTH_TOKEN`; use the newest URL every time you restart Inspector.

Use these Inspector settings:

```text
Transport Type: STDIO
Command: <repo-root>\.venv\Scripts\python.exe
Arguments: -m app.cli
Working Directory: <repo-root>
```

Example for this repository path:

```text
Command: D:\verma\backup\backup\.venv\Scripts\python.exe
Arguments: -m app.cli
Working Directory: D:\verma\backup\backup
```

After connecting:

1. Click the `Tools` tab.
2. Click `List Tools`.
3. Select `health_check`.
4. Click `Run Tool`.

Expected `health_check` result:

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "service": "rent-manager-backend"
  },
  "error": null
}
```

If the `Resources` tab is empty, that is expected. This server exposes MCP tools, not MCP resources.

## Test With Claude Code

Start the backend first.

From the repository root, add the MCP server:

```powershell
claude mcp add --transport stdio --scope project rent_manager_mcp -- .\.venv\Scripts\python.exe -m app.cli
```

Then start Claude Code:

```powershell
claude
```

Inside Claude Code, run:

```text
/mcp
```

You should see `rent_manager_mcp` connected. Then ask Claude to call the `health_check` tool or list rent manager tools.

If Claude Code cannot resolve the relative `.venv` path, use an absolute command:

```powershell
claude mcp add --transport stdio --scope project rent_manager_mcp -- D:\path\to\repo\.venv\Scripts\python.exe -m app.cli
```

## Test With Claude Desktop

Start the backend first.

Edit your Claude Desktop config file:

```text
C:\Users\<your-user>\AppData\Roaming\Claude\claude_desktop_config.json
```

Recommended config after running the setup steps:

```json
{
  "mcpServers": {
    "rent_manager_mcp": {
      "command": "D:\\path\\to\\repo\\.venv\\Scripts\\python.exe",
      "args": ["-m", "app.cli"]
    }
  }
}
```

If you do not want to rely on module execution, use the absolute `server.py` path:

```json
{
  "mcpServers": {
    "rent_manager_mcp": {
      "command": "D:\\path\\to\\repo\\.venv\\Scripts\\python.exe",
      "args": ["D:\\path\\to\\repo\\server.py"]
    }
  }
}
```

Restart Claude Desktop after editing the config. Ask Claude to use the `health_check` tool.

## Available Tools

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

## Run Tests

Run the test suite from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The tests cover backend client retry behavior, response envelope shape, service-layer caching, cache invalidation, and common tool error handling.

## Troubleshooting

- `Connected` in Inspector but nothing appears in `Resources`: click `Tools`; this server does not define resources.
- `Connection Error` in Inspector: restart Inspector and open the newest URL with the newest `MCP_PROXY_AUTH_TOKEN`.
- `ModuleNotFoundError: No module named 'app'`: run `.\.venv\Scripts\python.exe -m pip install -e ".[dev]"` from the repository root, or set Inspector working directory to the repository root.
- Tool calls return backend connection errors: make sure Terminal 1 is running the backend and `http://127.0.0.1:8000/health` returns `ok`.
- Port `8000` is already in use: start the backend on another port with `BACKEND_PORT`, then update `BACKEND_URL` in `.env`.
- Do not configure MCP Inspector as `SSE` or `Streamable HTTP`; use `STDIO`.
