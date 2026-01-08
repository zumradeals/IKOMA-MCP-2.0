"""Runtime Deployer minimal (BUILD-6)."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Mapping, Sequence

from ..core.orders.order import Order
from ..core.types.fact import Fact
from ..core.types.trace import Trace
from .config import DeployerConfig
from .result import DeployOutcome, DeployResult

Payload = Mapping[str, str]


def _now() -> datetime:
    return datetime.utcnow()


def _extract_payload(metadata: Mapping[str, str]) -> Payload:
    return metadata


def validate_order_contract(order: Order) -> Sequence[str]:
    """Valide le contrat minimal d'un ordre sans heuristique."""

    errors = []
    if not order.scope:
        errors.append("missing_scope")
    if not order.identifier:
        errors.append("missing_identifier")
    if not order.created_at:
        errors.append("missing_created_at")

    payload = _extract_payload(order.metadata or {})
    action = payload.get("action")
    target = payload.get("target")
    release_ref = payload.get("release_ref")

    if not action:
        errors.append("missing_payload_action")
    elif action not in {"deploy.up", "deploy.down", "deploy.restart"}:
        errors.append("invalid_payload_action")
    if not target:
        errors.append("missing_payload_target")
    if not release_ref:
        errors.append("missing_payload_release_ref")

    return errors


class DeployerRuntime:
    """Runtime du Deployer sans exécution système (DRY_RUN)."""

    def __init__(self, config: DeployerConfig) -> None:
        self._config = config

    @property
    def config(self) -> DeployerConfig:
        return self._config

    def apply(self, order: Order) -> DeployResult:
        """Applique un ordre conforme et retourne un résultat observable."""

        timestamp = _now()
        traces: list[Trace] = []
        facts: list[Fact] = []

        if order.consumed_at is not None:
            outcome = DeployOutcome.REJECTED
            errors = ["order_already_consumed"]
            consumed_order = order
        else:
            errors = list(validate_order_contract(order))
            outcome = DeployOutcome.REJECTED if errors else DeployOutcome.APPLIED
            consumed_order = replace(order, consumed_at=timestamp)

        facts.append(
            Fact(
                description="deploy.attempted",
                attributes={
                    "acte_parent": self._config.acte_parent,
                    "order_id": order.identifier,
                    "scope": order.scope,
                    "dry_run": str(self._config.dry_run).lower(),
                },
            )
        )
        facts.append(
            Fact(
                description="deploy.outcome",
                attributes={
                    "order_id": order.identifier,
                    "outcome": outcome.value,
                },
            )
        )

        trace_metadata = {
            "acte_parent": self._config.acte_parent,
            "event": "apply",
            "order_id": order.identifier,
            "outcome": outcome.value,
            "dry_run": str(self._config.dry_run).lower(),
        }
        if errors:
            trace_metadata["errors"] = ",".join(errors)

        traces.append(
            Trace(
                timestamp=timestamp,
                actor="deployer",
                metadata=trace_metadata,
            )
        )

        return DeployResult(
            outcome=outcome,
            order=consumed_order,
            traces=traces,
            facts=facts,
        )
