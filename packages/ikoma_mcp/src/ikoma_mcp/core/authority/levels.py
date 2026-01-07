"""Niveaux d'autorité définis par l'Acte II."""

from enum import Enum


class AuthorityLevel(str, Enum):
    """Niveaux d'autorité non négociables."""

    ONTOLOGICAL = "MCP"
    OPERATIONAL = "Runner"
    EXECUTIVE = "Deployer"
    EXPOSURE = "Gateway"
