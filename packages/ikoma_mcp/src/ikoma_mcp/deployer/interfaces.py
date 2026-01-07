"""Interfaces du Deployer (exécution contrôlée)."""

from typing import Protocol

from ..core.orders.order import Order


class DeployerInterface(Protocol):
    """Contrat d'exécution sans décision."""

    def execute(self, order: Order) -> None:
        """Exécute un ordre explicite."""
        ...
