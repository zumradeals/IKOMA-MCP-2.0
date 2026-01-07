"""Refus terminal et traçable."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Refusal:
    """Décision explicite de ne pas agir."""

    reason: str
