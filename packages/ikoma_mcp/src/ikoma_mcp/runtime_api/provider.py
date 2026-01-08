"""Providers for the BUILD-9 Runner Runtime API."""

from __future__ import annotations

from datetime import datetime
from typing import Callable, Protocol

from ..core.orders.order import Order
from ..core.orders.silence import Silence
from ..core.state.deploy import DeployState
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


def _build_default_cycle(timestamp: datetime) -> RuntimeCycle:
    clock = RuntimeClock(tick=0, instant=0, cycle=0)
    return RuntimeCycle(clock=clock, opened_at=timestamp)
