"""Interfaces du Gateway (exposition réseau)."""

from typing import Protocol


class GatewayInterface(Protocol):
    """Contrat d'exposition sans décision."""

    def expose(self, target: str) -> None:
        """Expose un accès selon un ordre reçu."""
        ...
