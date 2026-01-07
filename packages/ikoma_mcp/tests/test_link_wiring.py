from datetime import datetime

from ikoma_mcp.core.orders.order import Order
from ikoma_mcp.core.orders.refusal import Refusal
from ikoma_mcp.core.orders.silence import Silence
from ikoma_mcp.deployer.config import DeployerConfig
from ikoma_mcp.deployer.result import DeployOutcome
from ikoma_mcp.deployer.runtime import DeployerRuntime
from ikoma_mcp.link.wiring import wire_step


def _valid_order() -> Order:
    return Order(
        identifier="order-1",
        scope="local",
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        metadata={
            "action": "deploy.up",
            "target": "app-1",
            "release_ref": "v1.0.0",
        },
    )


def test_wire_step_applies_valid_order_and_records_ledger():
    runtime = DeployerRuntime(config=DeployerConfig(dry_run=True))

    result = wire_step(_valid_order(), runtime.apply)

    assert result.apply_result is not None
    assert result.apply_result.outcome is DeployOutcome.APPLIED
    assert isinstance(result.expression, Order)
    assert result.expression.consumed_at is not None
    assert any(trace.actor == "deployer" for trace in result.ledger_entry.traces)
    assert any(trace.actor == "link" for trace in result.ledger_entry.traces)
    assert any(fact.description == "link.applied" for fact in result.ledger_entry.facts)


def test_wire_step_refuses_consumed_order():
    runtime = DeployerRuntime(config=DeployerConfig())
    consumed_order = Order(
        identifier="order-2",
        scope="local",
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        consumed_at=datetime(2024, 1, 2, 0, 0, 0),
        metadata={
            "action": "deploy.up",
            "target": "app-2",
            "release_ref": "v1.0.1",
        },
    )

    result = wire_step(consumed_order, runtime.apply)

    assert result.apply_result is None
    assert isinstance(result.expression, Refusal)
    assert any(trace.metadata.get("event") == "refusal" for trace in result.ledger_entry.traces)


def test_wire_step_silence_when_no_order():
    runtime = DeployerRuntime(config=DeployerConfig())

    result = wire_step(None, runtime.apply)

    assert result.apply_result is None
    assert isinstance(result.expression, Silence)
    assert any(trace.metadata.get("event") == "silence" for trace in result.ledger_entry.traces)


def test_wire_step_rejects_invalid_order_with_refusal():
    runtime = DeployerRuntime(config=DeployerConfig())
    invalid_order = Order(
        identifier="order-3",
        scope="local",
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        metadata={
            "action": "deploy.unknown",
            "target": "app-3",
            "release_ref": "v1.0.2",
        },
    )

    result = wire_step(invalid_order, runtime.apply)

    assert result.apply_result is not None
    assert result.apply_result.outcome is DeployOutcome.REJECTED
    assert isinstance(result.expression, Refusal)
    assert any(trace.metadata.get("errors") for trace in result.ledger_entry.traces)


def test_wire_step_refuses_missing_required_evidence():
    runtime = DeployerRuntime(config=DeployerConfig())
    missing_release_order = Order(
        identifier="order-4",
        scope="local",
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        metadata={
            "action": "deploy.up",
            "target": "app-4",
        },
    )

    result = wire_step(missing_release_order, runtime.apply)

    assert result.apply_result is not None
    assert result.apply_result.outcome is DeployOutcome.REJECTED
    assert isinstance(result.expression, Refusal)
    assert "missing_payload_release_ref" in result.expression.reason
