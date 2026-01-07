"""Décision: acte du Runner conforme à la loi MCP."""

from dataclasses import dataclass
from typing import Sequence

from .fact import Fact


@dataclass(frozen=True)
class Decision:
    """Décision traçable, justifiée par des faits."""

    summary: str
    facts: Sequence[Fact]
