from datetime import datetime

from ikoma_mcp.core.evidence.primary import EvidencePrimary
from ikoma_mcp.core.evidence.secondary import EvidenceSecondary
from ikoma_mcp.core.evidence.set import EvidenceSet
from ikoma_mcp.core.types.decision import Decision
from ikoma_mcp.core.types.fact import Fact
from ikoma_mcp.core.types.trace import Trace
from ikoma_mcp.runner.config import RuntimeConfig
from ikoma_mcp.runner.emit import emit_order, emit_refusal, emit_silence
from ikoma_mcp.runner.ledger import LedgerEntry
from ikoma_mcp.runner.runtime import RuntimeRunner


def test_runtime_tick_collects_expected_structures():
    facts = [Fact(description="fact", attributes={"key": "value"})]
    evidence = [
        EvidenceSet(
            primary=EvidencePrimary(description="primary"),
            secondary=[EvidenceSecondary(description="secondary")],
        )
    ]
    decision = Decision(summary="decision", facts=facts)

    runner = RuntimeRunner(
        fact_provider=lambda: facts,
        evidence_provider=lambda: evidence,
        decision_provider=lambda current_facts, current_evidence: decision,
        config=RuntimeConfig(acte_parent="ACTE_V_TEST", interval_seconds=0.0),
        trace_provider=lambda: [
            Trace(
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                actor="test",
                metadata={"acte_parent": "ACTE_V_TEST"},
            )
        ],
    )

    tick = runner.tick()

    assert tick.facts == facts
    assert tick.evidence == evidence
    assert tick.decision == decision
    assert any(trace.actor == "runtime" for trace in tick.traces)


def test_ledger_entry_serializes_without_io():
    facts = [Fact(description="fact", attributes={"key": "value"})]
    evidence = [
        EvidenceSet(
            primary=EvidencePrimary(description="primary"),
            secondary=[EvidenceSecondary(description="secondary")],
        )
    ]
    decision = Decision(summary="decision", facts=facts)
    traces = [
        Trace(
            timestamp=datetime(2024, 1, 1, 0, 0, 0),
            actor="runtime",
            metadata={"acte_parent": "ACTE_V"},
        )
    ]

    entry = LedgerEntry(
        acte_parent="ACTE_V",
        created_at=datetime(2024, 1, 1, 0, 0, 1),
        facts=facts,
        evidence=evidence,
        decision=decision,
        traces=traces,
    )

    record = entry.to_record()

    assert record["acte_parent"] == "ACTE_V"
    assert record["decision"]["summary"] == "decision"
    assert record["facts"][0]["description"] == "fact"


def test_emit_helpers_create_declarative_expressions():
    order = emit_order(identifier="order-1", scope="local")
    refusal = emit_refusal(reason="no-op")
    silence = emit_silence(reason="silent")

    assert order.identifier == "order-1"
    assert refusal.reason == "no-op"
    assert silence.reason == "silent"
