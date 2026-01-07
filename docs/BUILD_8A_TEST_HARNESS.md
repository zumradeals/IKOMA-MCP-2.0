# BUILD-8A — Stabiliser l’exécution des tests (Module import)

## Why
Les tests doivent pouvoir importer `ikoma_mcp` sans imposer `PYTHONPATH=packages/ikoma_mcp/src`.

## Scope
- Ajouter une configuration pytest racine qui injecte `packages/ikoma_mcp/src` dans le
  `pythonpath`.
- Garantir que `pytest -q packages/ikoma_mcp/tests/test_gateway_exposure.py` fonctionne
  depuis la racine.

## Non-objectives
- Modifier les contrats Gateway/Deployer/Runner.
- Changer la structure des packages ou l’installation.
- Exécuter des tests hors de `pytest`.
