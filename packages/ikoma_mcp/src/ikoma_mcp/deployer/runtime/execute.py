"""Exécution minimale du Deployer Runtime (BUILD-7)."""

from dataclasses import replace
from datetime import datetime
from typing import Callable, List, Tuple

from ...core.types.fact import Fact
from ...core.types.trace import Trace
from .contracts import ExecutionRequest, ExecutionResult, ExecutionStatus, map_execution_status

ExecutionExecutor = Callable[[ExecutionRequest], Tuple[ExecutionStatus, str | None, str | None]]


def execute(
    request: ExecutionRequest,
    executor: ExecutionExecutor,
    *,
    now: Callable[[], datetime] = datetime.utcnow,
) -> ExecutionResult:
    """Exécute une instruction explicite et retourne un résultat brut."""

    started_at = now()
    status, raw_result, raw_error = executor(request)
    finished_at = now()

    consumed_order = request.order
    if request.order.consumed_at is None:
        consumed_order = replace(request.order, consumed_at=finished_at)

    deploy_state = map_execution_status(status)

    facts: List[Fact] = [
        Fact(
            description="deployer.execution.attempted",
            attributes={
                "acte_parent": request.context.acte_parent,
                "order_id": request.order.identifier,
                "action": request.action,
                "target": request.target,
            },
        ),
        Fact(
            description="deployer.execution.status",
            attributes={
                "order_id": request.order.identifier,
                "status": status.value,
                "deploy_state": deploy_state.value,
            },
        ),
    ]

    trace_metadata = {
        "acte_parent": request.context.acte_parent,
        "order_id": request.order.identifier,
        "action": request.action,
        "target": request.target,
        "status": status.value,
        "deploy_state": deploy_state.value,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
    }
    if raw_result is not None:
        trace_metadata["raw_result"] = raw_result
    if raw_error is not None:
        trace_metadata["raw_error"] = raw_error

    traces = [
        Trace(
            timestamp=finished_at,
            actor="deployer",
            metadata=trace_metadata,
        )
    ]

    return ExecutionResult(
        status=status,
        deploy_state=deploy_state,
        order=consumed_order,
        facts=facts,
        traces=traces,
        raw_result=raw_result,
        raw_error=raw_error,
        started_at=started_at,
        finished_at=finished_at,
    )
