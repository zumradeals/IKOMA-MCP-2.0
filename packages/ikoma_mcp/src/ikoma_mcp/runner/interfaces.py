"""Interfaces du Runner (observation et décision)."""

from typing import Protocol

from ..core.types.decision import Decision


class RunnerInterface(Protocol):
    """Contrat d'observation et décision."""

    def decide(self) -> Decision:
        """Émet une décision traçable."""
        ...
