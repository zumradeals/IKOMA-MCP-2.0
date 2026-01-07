"""État: résultat d'une classification gouvernée par MCP."""

from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    """État attribué à partir de faits observables."""

    name: str
