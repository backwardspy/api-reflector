"""
This module contains everything to do with short-term persistent storage for
actions & rules in API reflector.
"""
import time
from typing import Optional

_global_storage: dict[str, tuple[str, float]] = {}


class GlobalStorage:
    """
    A simple in-memory key-value store with expiry times.
    Data is local to this process only.
    """

    def get(self, name: str) -> Optional[str]:
        """Attempt to retrieve a value from the store."""
        value, expiry = _global_storage.get(name, (None, None))
        if expiry is not None and expiry < time.time():
            del _global_storage[name]
            return None

        return value

    def set(self, name: str, value: str, expiry: float) -> None:
        """Set a value in the store with an expiry timestamp."""
        _global_storage[name] = (value, expiry)

    def __getattr__(self, name: str) -> Optional[str]:
        """Enables dot notation for getting values from the store for template rendering."""
        return self.get(name)
