from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@dataclass(frozen=True)
class Settings:
    backend_url: str
    timeout: float
    max_retries: int
    mcp_server_name: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        backend_url=os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/"),
        timeout=float(os.getenv("TIMEOUT", "5")),
        max_retries=int(os.getenv("MAX_RETRIES", "2")),
        mcp_server_name=os.getenv("MCP_SERVER_NAME", "rent_manager_mcp"),
    )


settings = get_settings()
