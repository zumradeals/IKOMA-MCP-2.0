# BUILD-5 — Runtime Runner minimal

## Déclaration d’ouverture

BUILD-5 est ouvert pour matérialiser un Runner minimal conforme aux Actes I–IV et BUILD-0..4.

## Déclaration de clôture

BUILD-5 est clos dès qu’un Runner local peut produire un ledger append-only sans aucune action
système ni dépendance web.

## ACTE → Artefacts

- ACTE I–III → `packages/ikoma_mcp/src/ikoma_mcp/runner/runtime.py`
- ACTE IV → `packages/ikoma_mcp/src/ikoma_mcp/runner/emit.py`
- Ledger append-only → `packages/ikoma_mcp/src/ikoma_mcp/runner/ledger.py`
- Configuration → `packages/ikoma_mcp/src/ikoma_mcp/runner/config.py`

## Non-objectifs (verrouillés)

- Aucune exécution système (Deployer/Gateway interdits).
- Aucune heuristique ni auto-confirmation.
- Aucune action réseau ou dépendance web.
- Aucune intégration système.
