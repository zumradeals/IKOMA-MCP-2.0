"""États d'une application gouvernée."""

from enum import Enum


class AppState(str, Enum):
    """États fondamentaux d'une application gouvernée."""

    UP = "UP"
    DOWN = "DOWN"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"
