"""Deployer runtime entrypoint with file-based orders."""

from __future__ import annotations

import json
import logging
import os
import signal
import time
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from ..core.orders.order import Order
from ..core.state.deploy import DeployState
from ..core.types.fact import Fact
from ..core.types.trace import Trace
from .config import DeployerConfig
from .result import DeployOutcome, DeployResult
from .runtime.contracts import ExecutionResult, ExecutionStatus
from .runtime_impl import DeployerRuntime
from ..runtime_api.serialization import serialize_deployer_last


DEFAULT_INTERVAL_SECONDS = 15
LIB_DIR = Path(os.getenv("IKOMA_LIB_DIR", "/var/lib/ikoma"))
ORDERS_DIR = LIB_DIR / "orders"
INBOX_DIR = ORDERS_DIR / "inbox"
CONSUMED_DIR = ORDERS_DIR / "consumed"
REJECTED_DIR = ORDERS_DIR / "rejected"
LAST_RESULT_FILE = LIB_DIR / "deployer_last.json"


def _ensure_dirs():
    for d in [INBOX_DIR, CONSUMED_DIR, REJECTED_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def _load_order(path: Path) -> Order | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        # Basic reconstruction of Order dataclass
        return Order(
            identifier=data["identifier"],
            scope=data["scope"],
            created_at=datetime.fromisoformat(data["created_at"]),
            acte_parent=data.get("acte_parent", "ACTE_IV"),
            consumed_at=datetime.fromisoformat(data["consumed_at"]) if data.get("consumed_at") else None,
            metadata=data.get("metadata", {}),
        )
    except Exception as e:
        logging.error("Failed to load order from %s: %s", path, e)
        return None


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(temp_path, path)


def _map_deployer_outcome(outcome: DeployOutcome) -> tuple[ExecutionStatus, DeployState]:
    if outcome is DeployOutcome.APPLIED:
        return ExecutionStatus.APPLIED, DeployState.APPLIED
    if outcome is DeployOutcome.FAILED:
        return ExecutionStatus.FAILED, DeployState.FAILED
    if outcome is DeployOutcome.REJECTED:
        return ExecutionStatus.UNKNOWN, DeployState.REJECTED
    return ExecutionStatus.UNKNOWN, DeployState.UNKNOWN


def _build_execution_result(
    result: DeployResult,
    started_at: datetime,
    finished_at: datetime,
) -> ExecutionResult:
    status, deploy_state = _map_deployer_outcome(result.outcome)
    return ExecutionResult(
        status=status,
        deploy_state=deploy_state,
        order=result.order,
        facts=result.facts,
        traces=result.traces,
        raw_result=f"Order {result.outcome.value}",
        raw_error=None,
        started_at=started_at,
        finished_at=finished_at,
    )


def _build_failure_result(order: Order, error: Exception, started_at: datetime, finished_at: datetime) -> ExecutionResult:
    if order.consumed_at is None:
        order = replace(order, consumed_at=finished_at)
    trace = Trace(
        timestamp=finished_at,
        actor="deployer",
        metadata={
            "event": "apply_failed",
            "order_id": order.identifier,
            "scope": order.scope,
            "error": str(error),
        },
    )
    fact = Fact(
        description="deployer.execution.status",
        attributes={
            "order_id": order.identifier,
            "status": ExecutionStatus.FAILED.value,
            "deploy_state": DeployState.FAILED.value,
        },
    )
    return ExecutionResult(
        status=ExecutionStatus.FAILED,
        deploy_state=DeployState.FAILED,
        order=order,
        facts=[fact],
        traces=[trace],
        raw_result=None,
        raw_error=str(error),
        started_at=started_at,
        finished_at=finished_at,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [deployer] %(message)s")
    interval = int(os.getenv("IKOMA_DEPLOYER_INTERVAL", str(DEFAULT_INTERVAL_SECONDS)))

    _ensure_dirs()

    config = DeployerConfig(
        dry_run=os.getenv("IKOMA_DEPLOYER_DRY_RUN", "true").lower() == "true",
        acte_parent=os.getenv("IKOMA_ACTE_PARENT", "ACTE_IV"),
    )
    runtime = DeployerRuntime(config=config)

    stop = False

    def _handle_stop(signum: int, frame: object) -> None:
        nonlocal stop
        logging.info("Stopping deployer (signal=%s)", signum)
        stop = True

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    logging.info("Deployer started (dry_run=%s)", config.dry_run)
    while not stop:
        # 1. Scan inbox for orders (FIFO)
        order_files = sorted(INBOX_DIR.glob("*.json"), key=os.path.getmtime)

        if order_files:
            order_path = order_files[0]
            logging.info("Processing order: %s", order_path.name)

            order = _load_order(order_path)
            if order:
                started_at = datetime.utcnow()
                try:
                    # 2. Apply order
                    result = runtime.apply(order)
                    finished_at = datetime.utcnow()

                    # 3. Persist result (ExecutionResult for API)
                    exec_result = _build_execution_result(result, started_at, finished_at)
                    _atomic_write_json(LAST_RESULT_FILE, serialize_deployer_last(exec_result))

                    # 4. Move file to consumed or rejected
                    target_dir = CONSUMED_DIR if result.outcome == DeployOutcome.APPLIED else REJECTED_DIR
                    order_path.rename(target_dir / order_path.name)
                    logging.info("Order %s moved to %s", order_path.name, target_dir.name)

                except Exception as e:
                    finished_at = datetime.utcnow()
                    logging.error("Error applying order %s: %s", order_path.name, e)
                    exec_result = _build_failure_result(order, e, started_at, finished_at)
                    _atomic_write_json(LAST_RESULT_FILE, serialize_deployer_last(exec_result))
                    order_path.rename(REJECTED_DIR / order_path.name)
            else:
                # Invalid JSON or schema
                order_path.rename(REJECTED_DIR / order_path.name)
        else:
            logging.debug("No orders in inbox")

        time.sleep(interval)

    logging.info("Deployer stopped")


if __name__ == "__main__":
    main()
