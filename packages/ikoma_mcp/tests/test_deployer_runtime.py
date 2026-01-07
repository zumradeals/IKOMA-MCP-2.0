from datetime import datetime

from ikoma_mcp.core.orders.order import Order
from ikoma_mcp.deployer.config import DeployerConfig
from ikoma_mcp.deployer.result import DeployOutcome
from ikoma_mcp.deployer.runtime import DeployerRuntime


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


def test_apply_valid_order_in_dry_run_produces_artifacts():
    runtime = DeployerRuntime(config=DeployerConfig(dry_run=True))

    result = runtime.apply(_valid_order())

    assert result.outcome is DeployOutcome.APPLIED
    assert result.order.consumed_at is not None
    assert any(trace.actor == "deployer" for trace in result.traces)
    assert any(fact.description == "deploy.attempted" for fact in result.facts)
    assert any(fact.description == "deploy.outcome" for fact in result.facts)


def test_apply_invalid_order_rejected_with_trace():
    runtime = DeployerRuntime(config=DeployerConfig())
    invalid_order = Order(
        identifier="order-2",
        scope="local",
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        metadata={"target": "app-2"},
    )

    result = runtime.apply(invalid_order)

    assert result.outcome is DeployOutcome.REJECTED
    assert any(trace.metadata.get("errors") for trace in result.traces)


def test_apply_consumed_order_rejected():
    runtime = DeployerRuntime(config=DeployerConfig())
    consumed_order = Order(
        identifier="order-3",
        scope="local",
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        consumed_at=datetime(2024, 1, 2, 0, 0, 0),
        metadata={
            "action": "deploy.up",
            "target": "app-3",
            "release_ref": "v1.0.1",
        },
    )

    result = runtime.apply(consumed_order)

    assert result.outcome is DeployOutcome.REJECTED
    assert result.order.consumed_at == consumed_order.consumed_at


def test_runtime_does_not_invoke_system_calls(monkeypatch):
    runtime = DeployerRuntime(config=DeployerConfig())

    def _raise(*_args, **_kwargs) -> None:
        raise AssertionError("system call invoked")

    monkeypatch.setattr("subprocess.run", _raise)
    monkeypatch.setattr("os.system", _raise)

    result = runtime.apply(_valid_order())

    assert result.outcome is DeployOutcome.APPLIED
