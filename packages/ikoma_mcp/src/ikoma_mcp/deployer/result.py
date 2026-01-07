"""Résultats typés du Deployer (BUILD-6)."""

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from ..core.orders.order import Order
from ..core.types.fact import Fact
from ..core.types.trace import Trace


class DeployOutcome(str, Enum):
    """États d'application du Deployer."""

    APPLIED = "APPLIED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class DeployResult:
    """Résultat observable de l'application d'un ordre."""

    outcome: DeployOutcome
    order: Order
    traces: Sequence[Trace]
    facts: Sequence[Fact]
