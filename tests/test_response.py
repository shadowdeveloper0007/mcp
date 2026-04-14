from __future__ import annotations

import json

from app.utils.response import failure, success


def test_success_response_has_consistent_shape() -> None:
    payload = json.loads(success({"status": "ok"}, meta={"tool": "health_check"}))

    assert payload["success"] is True
    assert payload["data"] == {"status": "ok"}
    assert payload["error"] is None
    assert payload["meta"]["tool"] == "health_check"
    assert "generated_at" in payload["meta"]


def test_failure_response_includes_error_metadata() -> None:
    payload = json.loads(
        failure(
            "Could not reach backend",
            code="backend_unreachable",
            retryable=True,
        )
    )

    assert payload["success"] is False
    assert payload["data"] is None
    assert payload["error"] == "Could not reach backend"
    assert payload["meta"]["code"] == "backend_unreachable"
    assert payload["meta"]["retryable"] is True
