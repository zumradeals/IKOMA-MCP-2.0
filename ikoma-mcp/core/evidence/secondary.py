"""Contrat pour une évidence secondaire."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceSecondary:
    """Évidence contextuelle, jamais suffisante seule."""

    description: str
