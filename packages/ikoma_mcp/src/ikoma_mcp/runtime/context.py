"""Contexte du runtime passif (BUILD-5)."""

from dataclasses import dataclass
from typing import Sequence

from ..core.evidence.set import EvidenceSet
from ..core.types.fact import Fact
from ..core.types.trace import Trace
from .cycle import RuntimeCycle
from .runtime_state import RuntimeState


@dataclass(frozen=True)
class RuntimeContext:
    """Contexte read-only pour un cycle runtime."""

    state: RuntimeState
    cycle: RuntimeCycle
    facts: Sequence[Fact]
    evidence: Sequence[EvidenceSet]
    traces: Sequence[Trace]
