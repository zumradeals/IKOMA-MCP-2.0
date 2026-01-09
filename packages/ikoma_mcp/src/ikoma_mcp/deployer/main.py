"""Deployer runtime entrypoint with file-based orders.

Order JSON schema (file-based orders):
- identifier: str (required)
- scope: str (required)
- created_at: ISO-8601 string (optional, defaults to now UTC)
- acte_parent: str (optional, defaults to ACTE_IV)
- metadata: object (optional, defaults to {})
"""

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


def _parse_order(path: Path, now: datetime) -> tuple[Order | None, list[str], bool]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        logging.error("Failed to load order from %s: %s", path, e)
        return None, ["invalid_json"], False

    if not isinstance(data, dict):
        logging.error("Failed to load order from %s: payload_not_object", path)
        return None, ["invalid_payload"], False

    errors: list[str] = []
    identifier = data.get("identifier") or "unknown"
    scope = data.get("scope") or "unknown"
    if not data.get("identifier"):
        errors.append("missing_identifier")
    if not data.get("scope"):
        errors.append("missing_scope")

    created_at_raw = data.get("created_at")
    defaulted_created_at = False
    if created_at_raw:
        try:
            created_at = datetime.fromisoformat(created_at_raw)
        except (TypeError, ValueError):
            created_at = now
            errors.append("invalid_created_at")
    else:
        created_at = now
        defaulted_created_at = True

    acte_parent = data.get("acte_parent") or "ACTE_IV"
    metadata = data.get("metadata") or {}
    if not isinstance(metadata, dict):
        errors.append("invalid_metadata")
        metadata = {}

    consumed_at = None
    if data.get("consumed_at"):
        try:
            consumed_at = datetime.fromisoformat(data["consumed_at"])
        except (TypeError, ValueError):
            errors.append("invalid_consumed_at")

    order = Order(
        identifier=identifier,
        scope=scope,
        created_at=created_at,
        acte_parent=acte_parent,
        consumed_at=consumed_at,
        metadata=metadata,
    )
    return order, errors, defaulted_created_at


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(temp_path, path)


def _write_rejection_reason(target_dir: Path, filename: str, errors: list[str], defaulted_created_at: bool) -> None:
    reason_payload = {
        "errors": errors,
        "order.created_at.defaulted": defaulted_created_at,
    }
    reason_path = target_dir / f"{Path(filename).stem}.reason.json"
    _atomic_write_json(reason_path, reason_payload)


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
    *,
    defaulted_created_at: bool,
) -> ExecutionResult:
    status, deploy_state = _map_deployer_outcome(result.outcome)
    facts = list(result.facts)
    traces = list(result.traces)
    if defaulted_created_at:
        facts.append(
            Fact(
                description="order.created_at.defaulted",
                attributes={"order_id": result.order.identifier, "defaulted": "true"},
            )
        )
        traces.append(
            Trace(
                timestamp=finished_at,
                actor="deployer",
                metadata={"order_id": result.order.identifier, "order.created_at.defaulted": "true"},
            )
        )
    return ExecutionResult(
        status=status,
        deploy_state=deploy_state,
        order=result.order,
        facts=facts,
        traces=traces,
        raw_result=f"Order {result.outcome.value}",
        raw_error=None,
        started_at=started_at,
        finished_at=finished_at,
    )


def _build_failure_result(
    order: Order,
    error: Exception,
    started_at: datetime,
    finished_at: datetime,
    *,
    defaulted_created_at: bool,
) -> ExecutionResult:
    if order.consumed_at is None:
        order = replace(order, consumed_at=finished_at)
    traces = [
        Trace(
            timestamp=finished_at,
            actor="deployer",
            metadata={
                "event": "apply_failed",
                "order_id": order.identifier,
                "scope": order.scope,
                "error": str(error),
            },
        )
    ]
    facts = [
        Fact(
            description="deployer.execution.status",
            attributes={
                "order_id": order.identifier,
                "status": ExecutionStatus.FAILED.value,
                "deploy_state": DeployState.FAILED.value,
            },
        )
    ]
    if defaulted_created_at:
        facts.append(
            Fact(
                description="order.created_at.defaulted",
                attributes={"order_id": order.identifier, "defaulted": "true"},
            )
        )
        traces.append(
            Trace(
                timestamp=finished_at,
                actor="deployer",
                metadata={"order_id": order.identifier, "order.created_at.defaulted": "true"},
            )
        )
    return ExecutionResult(
        status=ExecutionStatus.FAILED,
        deploy_state=DeployState.FAILED,
        order=order,
        facts=facts,
        traces=traces,
        raw_result=None,
        raw_error=str(error),
        started_at=started_at,
        finished_at=finished_at,
    )


def _build_rejection_result(
    order: Order,
    errors: list[str],
    started_at: datetime,
    finished_at: datetime,
    *,
    defaulted_created_at: bool,
) -> ExecutionResult:
    if order.consumed_at is None:
        order = replace(order, consumed_at=finished_at)
    facts = [
        Fact(
            description="order.validation.failed",
            attributes={"order_id": order.identifier, "errors": ",".join(errors)},
        )
    ]
    traces = [
        Trace(
            timestamp=finished_at,
            actor="deployer",
            metadata={
                "event": "validation_failed",
                "order_id": order.identifier,
                "errors": ",".join(errors),
            },
        )
    ]
    if defaulted_created_at:
        facts.append(
            Fact(
                description="order.created_at.defaulted",
                attributes={"order_id": order.identifier, "defaulted": "true"},
            )
        )
        traces.append(
            Trace(
                timestamp=finished_at,
                actor="deployer",
                metadata={"order_id": order.identifier, "order.created_at.defaulted": "true"},
            )
        )
    return ExecutionResult(
        status=ExecutionStatus.UNKNOWN,
        deploy_state=DeployState.REJECTED,
        order=order,
        facts=facts,
        traces=traces,
        raw_result="Order REJECTED",
        raw_error="validation_failed",
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

            started_at = datetime.utcnow()
            order, errors, defaulted_created_at = _parse_order(order_path, started_at)
            if errors:
                finished_at = datetime.utcnow()
                logging.warning("validation_errors file=%s errors=%s", order_path.name, ",".join(errors))
                if order is None:
                    order = Order(
                        identifier="unknown",
                        scope="unknown",
                        created_at=started_at,
                        acte_parent="ACTE_IV",
                        consumed_at=finished_at,
                        metadata={},
                    )
                exec_result = _build_rejection_result(
                    order,
                    errors,
                    started_at,
                    finished_at,
                    defaulted_created_at=defaulted_created_at,
                )
                _atomic_write_json(LAST_RESULT_FILE, serialize_deployer_last(exec_result))
                order_path.rename(REJECTED_DIR / order_path.name)
                _write_rejection_reason(REJECTED_DIR, order_path.name, errors, defaulted_created_at)
                logging.info("moved_to_rejected file=%s", order_path.name)
                continue

            if order is None:
                finished_at = datetime.utcnow()
                logging.warning("validation_errors file=%s errors=invalid_payload", order_path.name)
                exec_result = _build_rejection_result(
                    Order(
                        identifier="unknown",
                        scope="unknown",
                        created_at=started_at,
                        acte_parent="ACTE_IV",
                        consumed_at=finished_at,
                        metadata={},
                    ),
                    ["invalid_payload"],
                    started_at,
                    finished_at,
                    defaulted_created_at=False,
                )
                _atomic_write_json(LAST_RESULT_FILE, serialize_deployer_last(exec_result))
                order_path.rename(REJECTED_DIR / order_path.name)
                _write_rejection_reason(REJECTED_DIR, order_path.name, ["invalid_payload"], False)
                logging.info("moved_to_rejected file=%s", order_path.name)
                continue

            logging.info("loaded_ok file=%s order_id=%s", order_path.name, order.identifier)
            try:
                # 2. Apply order
                result = runtime.apply(order)
                finished_at = datetime.utcnow()

                # 3. Persist result (ExecutionResult for API)
                exec_result = _build_execution_result(
                    result,
                    started_at,
                    finished_at,
                    defaulted_created_at=defaulted_created_at,
                )
                _atomic_write_json(LAST_RESULT_FILE, serialize_deployer_last(exec_result))

                # 4. Move file to consumed or rejected
                target_dir = CONSUMED_DIR if result.outcome == DeployOutcome.APPLIED else REJECTED_DIR
                order_path.rename(target_dir / order_path.name)
                if target_dir is CONSUMED_DIR:
                    logging.info("moved_to_consumed file=%s", order_path.name)
                else:
                    logging.info("moved_to_rejected file=%s", order_path.name)

            except Exception as e:
                finished_at = datetime.utcnow()
                logging.error("Error applying order %s: %s", order_path.name, e)
                exec_result = _build_failure_result(
                    order,
                    e,
                    started_at,
                    finished_at,
                    defaulted_created_at=defaulted_created_at,
                )
                _atomic_write_json(LAST_RESULT_FILE, serialize_deployer_last(exec_result))
                order_path.rename(REJECTED_DIR / order_path.name)
                logging.info("moved_to_rejected file=%s", order_path.name)
        else:
            logging.debug("No orders in inbox")

        time.sleep(interval)

    logging.info("Deployer stopped")


if __name__ == "__main__":
    main()
