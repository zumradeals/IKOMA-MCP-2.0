"""Interfaces du Gateway (exposition read-only)."""

from typing import Protocol

from .exposure import GatewayExposure


class GatewayInterface(Protocol):
    """Contrat d'exposition sans action."""

    def snapshot(self) -> GatewayExposure:
        """Expose un snapshot strictement read-only."""
        ...
