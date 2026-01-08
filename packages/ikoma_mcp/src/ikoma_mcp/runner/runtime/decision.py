"""Décision du Runner Runtime (BUILD-6)."""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


class RunnerDecisionReason(str, Enum):
    """Motifs normalisés, traçables et non heuristiques."""

    INSUFFICIENT_PRIMARY_EVIDENCE = "preuve manquante"
    CRITICAL_DIVERGENCE = "incohérence critique"
    OUT_OF_AUTHORITY = "hors autorité"
    TRANSITION_ALLOWED = "transition autorisée"
    OBSERVED = "observation confirmée"


RunnerReasonRegistry = Mapping[RunnerDecisionReason, str]

RUNNER_REASON_REGISTRY: RunnerReasonRegistry = {
    RunnerDecisionReason.INSUFFICIENT_PRIMARY_EVIDENCE: "Aucune preuve primaire exploitable.",
    RunnerDecisionReason.CRITICAL_DIVERGENCE: "Divergence critique observée.",
    RunnerDecisionReason.OUT_OF_AUTHORITY: "Autorité insuffisante pour exprimer un ordre.",
    RunnerDecisionReason.TRANSITION_ALLOWED: "Transition autorisée par l'Acte III.",
    RunnerDecisionReason.OBSERVED: "Observation sans divergence critique.",
}


@dataclass(frozen=True)
class RunnerDecision:
    """Décision explicable du Runner Runtime."""

    summary: str
    reasons: Sequence[RunnerDecisionReason]
    acte_parent: str = "ACTE_IV"
