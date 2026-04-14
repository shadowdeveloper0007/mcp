from __future__ import annotations

import logging


def _build_logger() -> logging.Logger:
    logger = logging.getLogger("rent_manager_mcp")

    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = _build_logger()
