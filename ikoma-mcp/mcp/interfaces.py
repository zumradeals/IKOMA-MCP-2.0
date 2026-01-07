"""Interfaces du noyau MCP (autorité)."""

from typing import Protocol, Sequence

from ..core.types.state import State


class MCPAuthority(Protocol):
    """Contrat d'autorité ontologique."""

    def classify(self, facts: Sequence[str]) -> State:
        """Classe des faits en un état."""
        ...
