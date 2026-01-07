"""Contrat de vérification d'autorité."""

from typing import Protocol

from .levels import AuthorityLevel


class AuthorityCheck(Protocol):
    """Contrat pour valider un niveau d'autorité."""

    def has_authority(self, level: AuthorityLevel) -> bool:
        """Retourne True si le niveau d'autorité est reconnu."""
        ...
