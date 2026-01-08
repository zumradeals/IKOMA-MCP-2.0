"""Contrats du Deployer Runtime (BUILD-7)."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Mapping, Sequence

from ...core.orders.order import Order
from ...core.state.deploy import DeployState
from ...core.types.fact import Fact
from ...core.types.trace import Trace


class ExecutionStatus(str, Enum):
    """Statut observable d'une exécution minimale."""

    APPLIED = "APPLIED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ExecutionContext:
    """Contexte fourni par le Runner (read-only)."""

    acte_parent: str
    runner_decision: str
    requested_at: datetime


@dataclass(frozen=True)
class ExecutionRequest:
    """Instruction explicite d'exécution."""

    order: Order
    action: str
    target: str
    payload: Mapping[str, str]
    context: ExecutionContext


@dataclass(frozen=True)
class ExecutionResult:
    """Résultat brut, traçable et sans interprétation."""

    status: ExecutionStatus
    deploy_state: DeployState
    order: Order
    facts: Sequence[Fact]
    traces: Sequence[Trace]
    raw_result: str | None
    raw_error: str | None
    started_at: datetime
    finished_at: datetime


def map_execution_status(status: ExecutionStatus) -> DeployState:
    """Mappe un statut brut vers l'état de déploiement (Acte III)."""

    if status is ExecutionStatus.APPLIED:
        return DeployState.APPLIED
    if status is ExecutionStatus.FAILED:
        return DeployState.FAILED
    return DeployState.UNKNOWN
