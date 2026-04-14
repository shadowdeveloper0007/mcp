from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _validate_backend_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("BACKEND_URL must be a valid http or https URL")
    return value.rstrip("/")


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    return cleaned or None


@dataclass(frozen=True)
class Settings:
    environment: str
    backend_url: str
    timeout: float
    max_retries: int
    retry_backoff_seconds: float
    mcp_server_name: str
    log_level: str
    log_format: str
    cache_enabled: bool
    cache_ttl_seconds: int
    backend_api_key: str | None
    backend_auth_header: str


def _build_settings() -> Settings:
    timeout = float(os.getenv("TIMEOUT", "5"))
    max_retries = int(os.getenv("MAX_RETRIES", "2"))
    retry_backoff_seconds = float(os.getenv("RETRY_BACKOFF_SECONDS", "0.25"))
    cache_ttl_seconds = int(os.getenv("CACHE_TTL_SECONDS", "15"))
    log_format = os.getenv("LOG_FORMAT", "text").lower()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    if timeout <= 0:
        raise ValueError("TIMEOUT must be greater than 0")
    if max_retries < 0:
        raise ValueError("MAX_RETRIES cannot be negative")
    if retry_backoff_seconds < 0:
        raise ValueError("RETRY_BACKOFF_SECONDS cannot be negative")
    if cache_ttl_seconds < 0:
        raise ValueError("CACHE_TTL_SECONDS cannot be negative")
    if log_format not in {"text", "json"}:
        raise ValueError("LOG_FORMAT must be either 'text' or 'json'")
    if log_level not in {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}:
        raise ValueError("LOG_LEVEL must be one of CRITICAL, ERROR, WARNING, INFO, DEBUG")

    return Settings(
        environment=os.getenv("ENVIRONMENT", "development"),
        backend_url=_validate_backend_url(os.getenv("BACKEND_URL", "http://localhost:8000")),
        timeout=timeout,
        max_retries=max_retries,
        retry_backoff_seconds=retry_backoff_seconds,
        mcp_server_name=os.getenv("MCP_SERVER_NAME", "rent_manager_mcp"),
        log_level=log_level,
        log_format=log_format,
        cache_enabled=_get_bool("CACHE_ENABLED", True),
        cache_ttl_seconds=cache_ttl_seconds,
        backend_api_key=_clean_optional(os.getenv("BACKEND_API_KEY")),
        backend_auth_header=os.getenv("BACKEND_AUTH_HEADER", "X-API-Key"),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return _build_settings()


settings = get_settings()
