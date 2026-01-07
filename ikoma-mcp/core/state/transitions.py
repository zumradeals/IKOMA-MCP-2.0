"""Table déclarative des transitions autorisées et interdites."""

from typing import Mapping, Tuple

from .app import AppState
from .deploy import DeployState
from .engine import EngineState
from .integration import IntegrationState

EngineTransition = Tuple[EngineState, EngineState]
AppTransition = Tuple[AppState, AppState]
DeployTransition = Tuple[DeployState, DeployState]
IntegrationTransition = Tuple[IntegrationState, IntegrationState]

ALLOWED_ENGINE_TRANSITIONS: Mapping[EngineTransition, str] = {
    (EngineState.UNKNOWN, EngineState.UP): "preuve primaire obtenue",
    (EngineState.UNKNOWN, EngineState.DEGRADED): "preuve primaire obtenue",
    (EngineState.UP, EngineState.DEGRADED): "variation d'observabilité",
    (EngineState.DEGRADED, EngineState.UP): "variation d'observabilité",
    (EngineState.UP, EngineState.FAILED): "divergence critique prouvée",
    (EngineState.DEGRADED, EngineState.FAILED): "divergence critique prouvée",
}

ALLOWED_APP_TRANSITIONS: Mapping[AppTransition, str] = {
    (AppState.UNKNOWN, AppState.DOWN): "preuve primaire obtenue",
    (AppState.UNKNOWN, AppState.UP): "preuve primaire obtenue",
    (AppState.DOWN, AppState.UP): "exécution observée",
    (AppState.UP, AppState.DOWN): "arrêt observé",
    (AppState.UP, AppState.FAILED): "divergence critique",
    (AppState.DOWN, AppState.FAILED): "divergence critique",
}

ALLOWED_DEPLOY_TRANSITIONS: Mapping[DeployTransition, str] = {
    (DeployState.UNKNOWN, DeployState.APPLIED): "preuve issue de l'exécution",
    (DeployState.UNKNOWN, DeployState.REJECTED): "refus par gouvernance",
    (DeployState.UNKNOWN, DeployState.FAILED): "exécution invalide",
}

ALLOWED_INTEGRATION_TRANSITIONS: Mapping[IntegrationTransition, str] = {
    (IntegrationState.UNKNOWN, IntegrationState.AVAILABLE): "preuve primaire obtenue",
    (IntegrationState.UNKNOWN, IntegrationState.UNAVAILABLE): "preuve primaire obtenue",
    (IntegrationState.UNKNOWN, IntegrationState.UNSTABLE): "preuve primaire obtenue",
    (IntegrationState.AVAILABLE, IntegrationState.UNSTABLE): "variation observée",
    (IntegrationState.UNSTABLE, IntegrationState.AVAILABLE): "variation observée",
    (IntegrationState.UNSTABLE, IntegrationState.UNAVAILABLE): "dégradation observée",
}
