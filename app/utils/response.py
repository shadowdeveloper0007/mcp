from __future__ import annotations

import json
from typing import Any


def success(data: Any) -> str:
    return json.dumps({"success": True, "data": data, "error": None}, indent=2)


def failure(message: str) -> str:
    return json.dumps({"success": False, "data": None, "error": message}, indent=2)
