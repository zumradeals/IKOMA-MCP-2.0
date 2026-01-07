"""Runtime Runner minimal (BUILD-5)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import time
from typing import Callable, Optional, Sequence

from ..core.evidence.set import EvidenceSet
from ..core.types.decision import Decision
from ..core.types.fact import Fact
from ..core.types.trace import Trace
from .config import RuntimeConfig
from .ledger import LedgerEntry, LedgerWriter

FactProvider = Callable[[], Sequence[Fact]]
EvidenceProvider = Callable[[], Sequence[EvidenceSet]]
DecisionProvider = Callable[[Sequence[Fact], Sequence[EvidenceSet]], Decision]
TraceProvider = Callable[[], Sequence[Trace]]


@dataclass(frozen=True)
class RuntimeTick:
    """Résultat pur d'un tick runtime."""

    facts: Sequence[Fact]
    evidence: Sequence[EvidenceSet]
    decision: Decision
    traces: Sequence[Trace]


class RuntimeRunner:
    """Runner runtime conforme aux actes et sans exécution."""

    def __init__(
        self,
        fact_provider: FactProvider,
        evidence_provider: EvidenceProvider,
        decision_provider: DecisionProvider,
        config: RuntimeConfig,
        trace_provider: Optional[TraceProvider] = None,
    ) -> None:
        self._fact_provider = fact_provider
        self._evidence_provider = evidence_provider
        self._decision_provider = decision_provider
        self._trace_provider = trace_provider
        self._config = config
        self._ledger = (
            LedgerWriter(config.ledger_path) if config.ledger_path else None
        )

    @property
    def config(self) -> RuntimeConfig:
        return self._config

    def tick(self) -> RuntimeTick:
        """Collecte read-only → évidence → décision → trace."""

        facts = self._fact_provider()
        evidence = self._evidence_provider()
        decision = self._decision_provider(facts, evidence)
        traces = list(self._trace_provider() if self._trace_provider else [])
        traces.append(
            Trace(
                timestamp=datetime.utcnow(),
                actor="runtime",
                metadata={"acte_parent": self._config.acte_parent, "event": "tick"},
            )
        )
        return RuntimeTick(
            facts=facts,
            evidence=evidence,
            decision=decision,
            traces=traces,
        )

    def run(self, max_ticks: Optional[int] = None) -> Sequence[RuntimeTick]:
        """Boucle optionnelle run() configurable (interval)."""

        results = []
        ticks_remaining = max_ticks
        while ticks_remaining is None or ticks_remaining > 0:
            result = self.tick()
            if self._ledger:
                entry = LedgerEntry(
                    acte_parent=self._config.acte_parent,
                    created_at=datetime.utcnow(),
                    facts=result.facts,
                    evidence=result.evidence,
                    decision=result.decision,
                    traces=result.traces,
                )
                self._ledger.append(entry)
            results.append(result)
            if ticks_remaining is not None:
                ticks_remaining -= 1
            time.sleep(self._config.interval_seconds)
        return results
