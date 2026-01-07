# BUILD-8 — Gateway Contractuel (Read-Only Exposure)

## Ouverture
BUILD-8 matérialise le Gateway comme surface d'exposition strictement read-only : un snapshot
observable sans ouverture réseau, sans action ni exécution, et sans heuristique. Le Gateway
ne décide pas et ne déclenche aucune opération.

## ACTE → Artefacts
- **ACTE I (faits/trace/decision)** → snapshots exposés et vues dérivées des états.
- **ACTE II (contrat)** → contrats d'exposition read-only et protocoles Gateway.
- **ACTE III (transition)** → UNKNOWN sans preuve primaire dans les vues.
- **ACTE IV (autorité)** → exposition sans ordre, sans exécution, sans écriture persistante.

## Artefacts créés
- `packages/ikoma_mcp/src/ikoma_mcp/gateway/interfaces.py`
- `packages/ikoma_mcp/src/ikoma_mcp/gateway/exposure.py`
- `packages/ikoma_mcp/src/ikoma_mcp/gateway/views.py`
- `packages/ikoma_mcp/tests/test_gateway_exposure.py`
- `docs/BUILD_8_GATEWAY_EXPOSURE.md`

## Invariants testables
- **Read-only** : snapshots et exposition sont immuables.
- **UNKNOWN sans preuve primaire** : absence d'évidence primaire → état UNKNOWN.
- **Pas d'import runtime** : pas d'import depuis `deployer/runtime`.

## Non-objectifs (verrouillés)
- Aucune ouverture de port ou endpoint réseau.
- Aucun HTTP, aucune authentification.
- Aucune exécution (pas d'ordres, pas de runtime).
- Aucune écriture persistante.
- Aucune heuristique ou auto-justification.

## Clôture
BUILD-8 est clos lorsque le Gateway expose uniquement des snapshots read-only,
les vues dérivées respectent la preuve primaire (UNKNOWN sans preuve), et
les tests garantissent l'absence d'action et d'import runtime.
