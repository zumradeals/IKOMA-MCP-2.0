"""Demande d'exposition du Gateway Runtime (BUILD-8)."""

from dataclasses import dataclass
from typing import Mapping

from ...core.orders.order import Order
from .context import GatewayContext


@dataclass(frozen=True)
class GatewayRequest:
    """Demande d'exposition explicite, sans gouvernance."""

    order: Order | None
    context: GatewayContext
    metadata: Mapping[str, str]
