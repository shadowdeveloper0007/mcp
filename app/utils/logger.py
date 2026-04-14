from __future__ import annotations

import json
import logging
from typing import Any

from app.core.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        event = getattr(record, "event", None)
        fields = getattr(record, "fields", None)

        if event:
            payload["event"] = event
        if fields:
            payload.update(fields)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def get_logger(name: str = "rent_manager_mcp") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        if settings.log_format == "json":
            handler.setFormatter(JsonFormatter(datefmt="%Y-%m-%d %H:%M:%S"))
        else:
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )

        logger.addHandler(handler)
        logger.propagate = False

    logger.setLevel(settings.log_level)
    return logger


def log_event(
    logger: logging.Logger,
    level: str,
    event: str,
    **fields: Any,
) -> None:
    logger.log(
        getattr(logging, level.upper()),
        event,
        extra={"event": event, "fields": fields},
    )


logger = get_logger()
