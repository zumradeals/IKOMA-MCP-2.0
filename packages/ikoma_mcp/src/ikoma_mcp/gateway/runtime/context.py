"""Contexte d'exposition du Gateway Runtime (BUILD-8)."""

from dataclasses import dataclass
from typing import Sequence

from ...core.types.fact import Fact
from ...core.types.trace import Trace
from .state import GatewayExposureState


@dataclass(frozen=True)
class GatewayContext:
    """Contexte read-only fourni au Gateway Runtime."""

    target: str
    exposure_state: GatewayExposureState
    proof_present: bool
    facts: Sequence[Fact]
    traces: Sequence[Trace]
