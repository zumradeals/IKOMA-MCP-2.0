"""JSON serialization helpers for the BUILD-9 runtime API."""

from __future__ import annotations

from datetime import datetime
from typing import Mapping

from ..core.evidence.primary import EvidencePrimary
from ..core.evidence.secondary import EvidenceSecondary
from ..core.evidence.set import EvidenceSet
from ..core.orders.order import Order
from ..core.orders.refusal import Refusal
from ..core.orders.silence import Silence
from ..core.orders.registry import AuthorityExpression
from ..core.types.fact import Fact
from ..core.types.trace import Trace
from ..deployer.runtime.contracts import ExecutionResult
from ..gateway.runtime.context import GatewayContext
from ..gateway.runtime.report import GatewayReport
from ..gateway.runtime.request import GatewayRequest
from ..runner.health.contracts import HealthReport
from ..runner.preflight.contracts import PreflightReport
from ..runner.runtime.contracts import RunnerRuntimeReport
from ..runner.runtime.decision import RunnerDecision
from ..runtime import RuntimeReport, RuntimeContext, RuntimeCycle, RuntimeClock


def serialize_runtime_report(report: RuntimeReport) -> Mapping[str, object]:
    return {
        "context": _serialize_runtime_context(report.context),
        "preflight_reports": [_serialize_preflight_report(item) for item in report.preflight_reports],
        "health_reports": [_serialize_health_report(item) for item in report.health_reports],
        "expression": _serialize_expression(report.expression),
        "traces": [_serialize_trace(item) for item in report.traces],
        "created_at": report.created_at.isoformat(),
        "acte_parent": report.acte_parent,
    }


def serialize_runner_cycle(report: RunnerRuntimeReport) -> Mapping[str, object]:
    return {
        "context": _serialize_runtime_context(report.context),
        "decision": _serialize_runner_decision(report.decision),
        "expression": _serialize_expression(report.expression),
        "traces": [_serialize_trace(item) for item in report.traces],
        "preflight_reports": [_serialize_preflight_report(item) for item in report.preflight_reports],
        "health_reports": [_serialize_health_report(item) for item in report.health_reports],
        "created_at": report.created_at.isoformat(),
        "acte_parent": report.acte_parent,
    }


def serialize_deployer_last(result: ExecutionResult) -> Mapping[str, object]:
    return {
        "status": result.status.value,
        "deploy_state": result.deploy_state.value,
        "order": _serialize_order(result.order),
        "facts": [_serialize_fact(item) for item in result.facts],
        "traces": [_serialize_trace(item) for item in result.traces],
        "raw_result": result.raw_result,
        "raw_error": result.raw_error,
        "started_at": result.started_at.isoformat(),
        "finished_at": result.finished_at.isoformat(),
    }


def serialize_gateway_exposure(report: GatewayReport) -> Mapping[str, object]:
    return {
        "context": _serialize_gateway_context(report.context),
        "request": _serialize_gateway_request(report.request),
        "status": report.status.value,
        "expression": _serialize_expression(report.expression),
        "facts": [_serialize_fact(item) for item in report.facts],
        "traces": [_serialize_trace(item) for item in report.traces],
        "created_at": report.created_at.isoformat(),
        "acte_parent": report.acte_parent,
    }


def _serialize_runtime_context(context: RuntimeContext) -> Mapping[str, object]:
    return {
        "state": context.state.value,
        "cycle": _serialize_runtime_cycle(context.cycle),
        "facts": [_serialize_fact(item) for item in context.facts],
        "evidence": [_serialize_evidence_set(item) for item in context.evidence],
        "traces": [_serialize_trace(item) for item in context.traces],
    }


def _serialize_runtime_cycle(cycle: RuntimeCycle) -> Mapping[str, object]:
    return {
        "clock": _serialize_runtime_clock(cycle.clock),
        "opened_at": cycle.opened_at.isoformat(),
        "closed_at": _isoformat(cycle.closed_at),
    }


def _serialize_runtime_clock(clock: RuntimeClock) -> Mapping[str, object]:
    return {
        "tick": clock.tick,
        "instant": clock.instant,
        "cycle": clock.cycle,
    }


def _serialize_preflight_report(report: PreflightReport) -> Mapping[str, object]:
    return {
        "facts": [_serialize_fact(item) for item in report.facts],
        "primary_evidence": [_serialize_evidence_primary(item) for item in report.primary_evidence],
        "secondary_evidence": [_serialize_evidence_secondary(item) for item in report.secondary_evidence],
        "traces": [_serialize_trace(item) for item in report.traces],
        "status": report.status.value,
        "blocking": report.blocking,
        "created_at": report.created_at.isoformat(),
    }


def _serialize_health_report(report: HealthReport) -> Mapping[str, object]:
    return {
        "facts": [_serialize_fact(item) for item in report.facts],
        "primary_evidence": [_serialize_evidence_primary(item) for item in report.primary_evidence],
        "secondary_evidence": [_serialize_evidence_secondary(item) for item in report.secondary_evidence],
        "traces": [_serialize_trace(item) for item in report.traces],
        "observation": report.observation.value,
        "created_at": report.created_at.isoformat(),
    }


def _serialize_runner_decision(decision: RunnerDecision) -> Mapping[str, object]:
    return {
        "summary": decision.summary,
        "reasons": [item.value for item in decision.reasons],
        "acte_parent": decision.acte_parent,
    }


def _serialize_gateway_context(context: GatewayContext) -> Mapping[str, object]:
    return {
        "target": context.target,
        "exposure_state": context.exposure_state.value,
        "proof_present": context.proof_present,
        "facts": [_serialize_fact(item) for item in context.facts],
        "traces": [_serialize_trace(item) for item in context.traces],
    }


def _serialize_gateway_request(request: GatewayRequest) -> Mapping[str, object]:
    return {
        "order": _serialize_optional_order(request.order),
        "context": _serialize_gateway_context(request.context),
        "metadata": dict(request.metadata),
    }


def _serialize_fact(fact: Fact) -> Mapping[str, object]:
    return {
        "description": fact.description,
        "attributes": dict(fact.attributes),
    }


def _serialize_trace(trace: Trace) -> Mapping[str, object]:
    return {
        "timestamp": trace.timestamp.isoformat(),
        "actor": trace.actor,
        "metadata": dict(trace.metadata),
    }


def _serialize_evidence_primary(evidence: EvidencePrimary) -> Mapping[str, object]:
    return {"description": evidence.description}


def _serialize_evidence_secondary(evidence: EvidenceSecondary) -> Mapping[str, object]:
    return {"description": evidence.description}


def _serialize_evidence_set(evidence: EvidenceSet) -> Mapping[str, object]:
    return {
        "primary": _serialize_evidence_primary(evidence.primary),
        "secondary": [_serialize_evidence_secondary(item) for item in evidence.secondary],
    }


def _serialize_optional_order(order: Order | None) -> Mapping[str, object] | None:
    if order is None:
        return None
    return _serialize_order(order)


def _serialize_order(order: Order) -> Mapping[str, object]:
    return {
        "identifier": order.identifier,
        "scope": order.scope,
        "created_at": order.created_at.isoformat(),
        "acte_parent": order.acte_parent,
        "consumed_at": _isoformat(order.consumed_at),
        "metadata": dict(order.metadata or {}),
    }


def _serialize_expression(expression: AuthorityExpression) -> Mapping[str, object]:
    if isinstance(expression, Order):
        return {
            "type": "order",
            "identifier": expression.identifier,
            "scope": expression.scope,
            "created_at": expression.created_at.isoformat(),
            "acte_parent": expression.acte_parent,
            "consumed_at": _isoformat(expression.consumed_at),
            "metadata": dict(expression.metadata or {}),
        }
    if isinstance(expression, Refusal):
        return {
            "type": "refusal",
            "reason": expression.reason,
            "created_at": expression.created_at.isoformat(),
            "acte_parent": expression.acte_parent,
            "metadata": dict(expression.metadata or {}),
        }
    if isinstance(expression, Silence):
        return {
            "type": "silence",
            "reason": expression.reason,
            "created_at": expression.created_at.isoformat(),
            "acte_parent": expression.acte_parent,
            "metadata": dict(expression.metadata or {}),
        }
    raise TypeError(f"Unsupported expression type: {type(expression)!r}")


def _isoformat(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None
