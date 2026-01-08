"""Temps logique et cycle du runtime passif."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class RuntimeClock:
    """Horloge logique: tick, instant, cycle."""

    tick: int
    instant: int
    cycle: int


@dataclass(frozen=True)
class RuntimeCycle:
    """Cycle logique read-only du runtime."""

    clock: RuntimeClock
    opened_at: datetime
    closed_at: Optional[datetime] = None
