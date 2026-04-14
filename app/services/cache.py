from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any


@dataclass(slots=True)
class CacheEntry:
    value: Any
    expires_at: float


class TTLCache:
    def __init__(self, ttl_seconds: int) -> None:
        self.ttl_seconds = ttl_seconds
        self._items: dict[str, CacheEntry] = {}

    def get(self, key: str) -> Any | None:
        entry = self._items.get(key)
        if entry is None:
            return None

        if entry.expires_at <= monotonic():
            self._items.pop(key, None)
            return None

        return entry.value

    def set(self, key: str, value: Any) -> None:
        self._items[key] = CacheEntry(
            value=value,
            expires_at=monotonic() + self.ttl_seconds,
        )

    def invalidate_prefix(self, prefix: str) -> None:
        for key in list(self._items):
            if key.startswith(prefix):
                self._items.pop(key, None)
