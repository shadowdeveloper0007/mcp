from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any


def success(data: Any, *, meta: dict[str, Any] | None = None) -> str:
    payload = {
        "success": True,
        "data": data,
        "error": None,
        "meta": _build_meta(meta),
    }
    return json.dumps(payload, indent=2)


def failure(
    message: str,
    *,
    code: str = "internal_error",
    retryable: bool = False,
    details: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> str:
    payload = {
        "success": False,
        "data": None,
        "error": message,
        "meta": _build_meta(
            {
                **(meta or {}),
                "code": code,
                "retryable": retryable,
                **({"details": details} if details else {}),
            }
        ),
    }
    return json.dumps(payload, indent=2)


def _build_meta(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    metadata = {"generated_at": datetime.now(UTC).isoformat()}
    if extra:
        metadata.update(extra)
    return metadata
