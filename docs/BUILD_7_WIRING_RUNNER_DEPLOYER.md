# BUILD-7 — Wiring Runner ↔ Deployer (câblage contrôlé)

## Ouverture
BUILD-7 est ouvert pour câbler le Runner et le Deployer sans exécution système, en conservant
un flux strict et testable : Order/Silence → ApplyResult → Ledger.

## ACTE → Artefacts
- **ACTE I (faits/trace/decision)** → traces et facts du wiring + `LedgerEntry`.
- **ACTE II (contrat)** → refus traçables si contrat d’ordre non respecté.
- **ACTE III (transition)** → résultat d’application (APPLIED/REJECTED/FAILED).
- **ACTE IV (autorité)** → ordre/ refus / silence comme expressions explicites.

## Artefacts créés
- `packages/ikoma_mcp/src/ikoma_mcp/link/__init__.py`
- `packages/ikoma_mcp/src/ikoma_mcp/link/wiring.py`
- `packages/ikoma_mcp/tests/test_link_wiring.py`
- `docs/BUILD_7_WIRING_RUNNER_DEPLOYER.md`

## Invariants testables
- **Silence explicite** : absence d’ordre → Silence + Trace `link.silence`.
- **Refus sur ordre consommé** : ordre déjà consommé → Refusal + Trace `link.refusal`.
- **Application valide** : ordre valide → ApplyResult APPLIED + LedgerEntry avec traces Deployer + Link.
- **Rejet contractuel** : ordre invalide → Refusal traçable + erreurs remontées.
- **Ledger strict** : chaque cycle produit un `LedgerEntry` déterministe (hors timestamps).

## Non-objectifs (verrouillés)
- Aucune exécution système (pas de docker/systemd/ports/fs/network).
- Aucune décision dans le Deployer.
- Aucune gouvernance dans le Deployer/Gateway.
- Aucune auto-confirmation ni heuristique.
- Aucun IO en dehors du ledger in-memory (pas d’append réel dans les tests).

## Clôture
BUILD-7 est clos lorsque le câblage Runner ↔ Deployer produit des cycles purs, traçables et
testés, avec ledger, refus, silence et résultats d’application vérifiables.
