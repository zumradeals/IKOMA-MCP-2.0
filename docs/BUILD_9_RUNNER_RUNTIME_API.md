# BUILD-9 — Runner Runtime API (surface read-only)

## Décision

BUILD-9 est ouvert.
L'objectif est d'exposer une surface API read-only fournissant les rapports runtime existants
(moteur/runtime, runner, deployer, gateway) sans ajouter de règles, actions ou heuristiques.

## Périmètre autorisé (verrouillé)

### Ce qui est autorisé

- Ajouter une documentation et un contrat OpenAPI pour une API read-only.
- Exposer via HTTP des rapports JSON strictement dérivés des types/contracts existants.
- Mapper explicitement chaque endpoint vers Actes/Builds et types retournés.

### Ce qui est strictement interdit

- Toute UI.
- Toute exécution système (start/stop/fix/retry).
- Toute gouvernance, scoring, heuristique ou auto-confirmation.
- Toute mutation d'état.
- Toute boucle active/scheduler (API passive).

## Endpoints contractuels minimaux

| Endpoint | Type retourné | Build source | Acte |
| --- | --- | --- | --- |
| `GET /v1/runtime/status` | `RuntimeReport` | BUILD-5 runtime | ACTE IV (expression d'autorité) |
| `GET /v1/runner/cycle` | `RunnerRuntimeReport` | BUILD-6 runner runtime | ACTE IV (expression d'autorité) |
| `GET /v1/deployer/last` | `ExecutionResult` | BUILD-7 deployer runtime | ACTE III (DeployState) |
| `GET /v1/gateway/exposure` | `GatewayReport` | BUILD-8 gateway runtime | ACTE IV (expression d'autorité) |

## Invariants

- Toutes les réponses sont read-only et dérivées des contrats existants.
- Aucune décision nouvelle n'est produite.
- Aucune action système n'est déclenchée.
- Aucune mutation d'état n'est effectuée.
- L'API reste passive (aucune boucle, aucun scheduler).

## Contrat OpenAPI

Le contrat est maintenu dans `docs/BUILD_9_RUNNER_RUNTIME_API_OPENAPI.json`.
Il définit les schémas JSON correspondant aux rapports et types contracts existants.

## Non-objectifs explicites

- Fournir une UI ou un portail.
- Autoriser des commandes actives.
- Exécuter des ordres (déploiement, exposition, remédiation).
- Interpréter les rapports avec heuristique.

## Clause de clôture BUILD-9

BUILD-9 est clos lorsque :

- La documentation est complète (ce document).
- Un schéma OpenAPI est présent.
- Les imports sont stables.
- L'API read-only est disponible sans exécution réelle.
