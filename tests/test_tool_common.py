from __future__ import annotations

import json

import pytest
from pydantic import BaseModel

from app.core.errors import AppError
from app.tools._common import parse_input, run_tool


class ExampleModel(BaseModel):
    value: int


@pytest.mark.asyncio
async def test_execute_tool_returns_structured_error_response() -> None:
    async def failing_operation() -> object:
        raise AppError("Invalid input", code="validation_error")

    payload = json.loads(await run_tool("example_tool", failing_operation))

    assert payload["success"] is False
    assert payload["error"] == "Invalid input"
    assert payload["meta"]["tool"] == "example_tool"
    assert payload["meta"]["code"] == "validation_error"


def test_validate_payload_wraps_validation_errors() -> None:
    with pytest.raises(AppError) as exc_info:
        parse_input(ExampleModel, value="bad")

    assert exc_info.value.code == "validation_error"
