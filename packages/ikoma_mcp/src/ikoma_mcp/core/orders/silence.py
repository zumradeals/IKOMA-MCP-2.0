"""Silence explicite et traçable."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Silence:
    """Absence volontaire d'expression."""

    reason: str
