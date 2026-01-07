"""Ordre consommable après exécution."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    """Expression explicite d'une volonté d'action."""

    identifier: str
    scope: str
