# BUILD-6 — Deployer (exécution minimale, obéissante)

## Ouverture
BUILD-6 matérialise le Deployer comme exécuteur strict : il applique des Ordres explicitement formés, sans décision, et retourne un résultat observable + traçable.

## Mapping ACTE → Artefacts
- **ACTE I (types)** → Fact/Trace/Decision/State existants.
- **ACTE II (autorité & evidence)** → `validate_order_contract` refuse si preuve primaire manquante.
- **ACTE III (états & transitions)** → `DeployOutcome` et transitions déclaratives.
- **ACTE IV (ordre/refus/silence)** → consommation d’ordre + traces.

## Artefacts créés
- `packages/ikoma_mcp/src/ikoma_mcp/deployer/config.py`
- `packages/ikoma_mcp/src/ikoma_mcp/deployer/result.py`
- `packages/ikoma_mcp/src/ikoma_mcp/deployer/runtime.py`
- `packages/ikoma_mcp/src/ikoma_mcp/deployer/__init__.py`
- `packages/ikoma_mcp/tests/test_deployer_runtime.py`

## Non-objectifs (verrouillés)
- Aucune exécution système par défaut (DRY_RUN seulement).
- Aucune gestion réseau / gateway.
- Aucun wiring Runner → Deployer.
- Aucun accès secrets, aucun stockage de secrets.
- Aucun rollback, aucune stratégie, aucune optimisation.
- Aucun auto-heal.

## Critères d’acceptation
- **Importable** : le module deployer runtime s’importe sans side-effects.
- **Déterministe** : mêmes inputs → mêmes outputs (hors timestamps).
- **Traçable** : chaque `apply()` produit au moins 1 Trace et 2 Facts minimaux.
- **Sûr** : DRY_RUN par défaut, aucune exécution système.
- **Tests unitaires** : passent localement (sans intégration).

## Clôture
BUILD-6 est clos quand le Deployer peut appliquer un ordre en mode DRY_RUN et retourner un résultat observable + traces/facts, sans action système réelle.
