from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.core.errors import AppError
from app.utils.logger import get_logger, log_event
from app.utils.response import failure, success


logger = get_logger(__name__)
InputModel = TypeVar("InputModel", bound=BaseModel)

READ_HINTS = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
}

WRITE_HINTS = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": False,
}


async def run_tool(
    tool_name: str,
    operation: Callable[[], Awaitable[object]],
) -> str:
    log_event(logger, "info", "tool.call", tool_name=tool_name)

    try:
        data = await operation()
        return success(data, meta={"tool": tool_name})
    except AppError as exc:
        log_event(
            logger,
            "warning",
            "tool.failed",
            tool_name=tool_name,
            error_code=exc.code,
            retryable=exc.retryable,
        )
        return failure(
            exc.message,
            code=exc.code,
            retryable=exc.retryable,
            details=exc.details,
            meta={"tool": tool_name},
        )
    except Exception:
        logger.exception("Unhandled error in tool %s", tool_name)
        return failure(
            "Unexpected server error",
            code="internal_error",
            meta={"tool": tool_name},
        )


def parse_input(model: type[InputModel], **payload: object) -> InputModel:
    try:
        return model(**payload)
    except ValidationError as exc:
        raise AppError(
            "Invalid tool input",
            code="validation_error",
            details={"errors": exc.errors()},
        ) from exc
