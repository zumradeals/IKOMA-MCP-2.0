"""Providers for the BUILD-9 Runner Runtime API."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Protocol

from ..core.orders.order import Order
from ..core.orders.silence import Silence
from ..core.state.deploy import DeployState
from ..core.types.fact import Fact
from ..core.types.trace import Trace
from ..gateway.runtime.context import GatewayContext
from ..gateway.runtime.report import GatewayReport, build_gateway_report
from ..gateway.runtime.request import GatewayRequest
from ..gateway.runtime.state import GatewayExposureState
from ..runtime import RuntimeReport, RuntimeState, RuntimeClock, RuntimeCycle, RuntimeContext, build_runtime_report
from ..runner.runtime.contracts import RunnerRuntimeReport
from ..runner.runtime.decision import RunnerDecision
from ..deployer.runtime.contracts import ExecutionResult, ExecutionStatus


class RuntimeApiProvider(Protocol):
    """Read-only provider for runtime API reports."""

    def get_runtime_status(self) -> RuntimeReport:
        """Return the current runtime status report."""
        ...

    def get_runner_cycle(self) -> RunnerRuntimeReport:
        """Return the last runner cycle report."""
        ...

    def get_deployer_last(self) -> ExecutionResult:
        """Return the last deployer execution result."""
        ...

    def get_gateway_exposure(self) -> GatewayReport:
        """Return the last gateway exposure report."""
        ...


class DefaultRuntimeApiProvider:
    """Default provider returning UNKNOWN/empty reports."""

    def __init__(self, now: Callable[[], datetime] | None = None) -> None:
        self._now = now or datetime.utcnow

    def get_runtime_status(self) -> RuntimeReport:
        timestamp = self._now()
        context = RuntimeContext(
            state=RuntimeState.INIT,
            cycle=_build_default_cycle(timestamp),
            facts=(),
            evidence=(),
            traces=(),
        )
        expression = Silence(
            reason="runtime_status_unknown",
            created_at=timestamp,
            metadata={"reason": "runtime_status_unknown"},
        )
        return build_runtime_report(
            context=context,
            preflight_reports=(),
            health_reports=(),
            expression=expression,
            traces=(),
            created_at=timestamp,
        )

    def get_runner_cycle(self) -> RunnerRuntimeReport:
        timestamp = self._now()
        context = RuntimeContext(
            state=RuntimeState.INIT,
            cycle=_build_default_cycle(timestamp),
            facts=(),
            evidence=(),
            traces=(),
        )
        decision = RunnerDecision(summary="cycle_report_unavailable", reasons=())
        expression = Silence(
            reason="runner_cycle_unknown",
            created_at=timestamp,
            metadata={"reason": "runner_cycle_unknown"},
        )
        return RunnerRuntimeReport(
            context=context,
            decision=decision,
            expression=expression,
            traces=(),
            preflight_reports=(),
            health_reports=(),
            created_at=timestamp,
        )

    def get_deployer_last(self) -> ExecutionResult:
        timestamp = self._now()
        order = Order(
            identifier="unknown",
            scope="unknown",
            created_at=timestamp,
            acte_parent="ACTE_IV",
            consumed_at=None,
            metadata={},
        )
        return ExecutionResult(
            status=ExecutionStatus.UNKNOWN,
            deploy_state=DeployState.UNKNOWN,
            order=order,
            facts=(),
            traces=(),
            raw_result=None,
            raw_error=None,
            started_at=timestamp,
            finished_at=timestamp,
        )

    def get_gateway_exposure(self) -> GatewayReport:
        timestamp = self._now()
        context = GatewayContext(
            target="unknown",
            exposure_state=GatewayExposureState.UNKNOWN,
            proof_present=False,
            facts=(),
            traces=(),
        )
        request = GatewayRequest(order=None, context=context, metadata={})
        return build_gateway_report(request=request, created_at=timestamp)


class FileBasedRuntimeApiProvider(DefaultRuntimeApiProvider):
    """Provider reading state from /var/lib/ikoma files."""

    def __init__(
        self,
        lib_dir: str | Path = "/var/lib/ikoma",
        now: Callable[[], datetime] | None = None,
    ) -> None:
        super().__init__(now=now)
        self._lib_dir = Path(lib_dir)
        self._runner_cycle_file = self._lib_dir / "runner_last_cycle_id"
        self._deployer_last_file = self._lib_dir / "deployer_last.json"

    def get_runtime_status(self) -> RuntimeReport:
        report = super().get_runtime_status()
        cycle_id = self._read_cycle_id()
        if cycle_id > 0:
            timestamp = self._now()
            clock = RuntimeClock(tick=cycle_id, instant=cycle_id, cycle=cycle_id)
            cycle = RuntimeCycle(clock=clock, opened_at=timestamp)
            context = RuntimeContext(
                state=RuntimeState.RUNNING,
                cycle=cycle,
                facts=report.context.facts,
                evidence=report.context.evidence,
                traces=report.context.traces,
            )
            return build_runtime_report(
                context=context,
                preflight_reports=report.preflight_reports,
                health_reports=report.health_reports,
                expression=report.expression,
                traces=report.traces,
                created_at=timestamp,
            )
        return report

    def get_runner_cycle(self) -> RunnerRuntimeReport:
        report = super().get_runner_cycle()
        cycle_id = self._read_cycle_id()
        if cycle_id > 0:
            timestamp = self._now()
            clock = RuntimeClock(tick=cycle_id, instant=cycle_id, cycle=cycle_id)
            cycle = RuntimeCycle(clock=clock, opened_at=timestamp)
            context = RuntimeContext(
                state=RuntimeState.RUNNING,
                cycle=cycle,
                facts=report.context.facts,
                evidence=report.context.evidence,
                traces=report.context.traces,
            )
            decision = RunnerDecision(
                summary=f"cycle_id={cycle_id}",
                reasons=report.decision.reasons,
            )
            return RunnerRuntimeReport(
                context=context,
                decision=decision,
                expression=report.expression,
                traces=report.traces,
                preflight_reports=report.preflight_reports,
                health_reports=report.health_reports,
                created_at=timestamp,
            )
        return report

    def get_deployer_last(self) -> ExecutionResult:
        if not self._deployer_last_file.exists():
            return super().get_deployer_last()
        
        try:
            data = json.loads(self._deployer_last_file.read_text(encoding="utf-8"))
            
            # Reconstruct ExecutionResult from JSON
            order_data = data["order"]
            order = Order(
                identifier=order_data["identifier"],
                scope=order_data["scope"],
                created_at=datetime.fromisoformat(order_data["created_at"]),
                acte_parent=order_data.get("acte_parent", "ACTE_IV"),
                consumed_at=datetime.fromisoformat(order_data["consumed_at"]) if order_data.get("consumed_at") else None,
                metadata=order_data.get("metadata", {}),
            )
            
            facts = [
                Fact(description=f["description"], attributes=f["attributes"])
                for f in data.get("facts", [])
            ]
            
            traces = [
                Trace(
                    timestamp=datetime.fromisoformat(t["timestamp"]),
                    actor=t["actor"],
                    metadata=t["metadata"]
                )
                for t in data.get("traces", [])
            ]
            
            return ExecutionResult(
                status=ExecutionStatus(data["status"]),
                deploy_state=DeployState(data["deploy_state"]),
                order=order,
                facts=facts,
                traces=traces,
                raw_result=data.get("raw_result"),
                raw_error=data.get("raw_error"),
                started_at=datetime.fromisoformat(data["started_at"]),
                finished_at=datetime.fromisoformat(data["finished_at"]),
            )
        except Exception:
            return super().get_deployer_last()

    def _read_cycle_id(self) -> int:
        if not self._runner_cycle_file.exists():
            return 0
        try:
            return int(self._runner_cycle_file.read_text(encoding="utf-8").strip() or 0)
        except (ValueError, OSError):
            return 0


def _build_default_cycle(timestamp: datetime) -> RuntimeCycle:
    clock = RuntimeClock(tick=0, instant=0, cycle=0)
    return RuntimeCycle(clock=clock, opened_at=timestamp)
