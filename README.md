## Rent Manager MCP Server

Small MCP server for a rent management demo backend.

The project has two parts:

- A FastAPI backend with a few sample endpoints
- A FastMCP server that exposes those endpoints as MCP tools

### Project layout

```text
.
|-- app
|   |-- clients
|   |   `-- backend_client.py
|   |-- core
|   |   `-- config.py
|   |-- tools
|   |   |-- maintenance.py
|   |   |-- summary.py
|   |   |-- tenants.py
|   |   `-- units.py
|   `-- utils
|       |-- logger.py
|       `-- response.py
|-- backend
|   |-- data.py
|   `-- main.py
|-- .env
|-- README.md
|-- requirements.txt
`-- server.py
```

### Requirements

- Python 3.12+
- Claude Code if you want to use the MCP server from Claude

### Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Local configuration lives in `.env`:

```env
BACKEND_URL=http://localhost:8000
TIMEOUT=5
MAX_RETRIES=2
MCP_SERVER_NAME=rent_manager_mcp
```

### Run the backend

Start the demo API first:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Quick health check:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health | Select-Object -ExpandProperty Content
```

### Run the MCP server

In a second terminal, from the project root:

```powershell
python server.py
```

This is a stdio MCP server, so Claude Code should launch it as a command, not as an HTTP service.

### Connect with Claude Code

Add the server to the current project:

```powershell
claude mcp add --transport stdio --scope project rent_manager_mcp -- python server.py
```

Then open Claude Code in the same folder:

```powershell
claude
```

Inside Claude Code, run `/mcp` to confirm the server is connected.

### Available tools

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

### Notes

- The backend uses in-memory data, so changes are reset when the API restarts.
- MCP tool responses follow one shape: `success`, `data`, and `error`.
- If a tool fails, check the backend URL in `.env` and make sure the FastAPI app is running.
