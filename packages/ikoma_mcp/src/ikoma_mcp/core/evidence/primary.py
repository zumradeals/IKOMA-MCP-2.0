"""Contrat pour une évidence primaire."""

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidencePrimary:
    """Évidence prioritaire, observable et répétable."""

    description: str
