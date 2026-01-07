# BUILD-1 — Squelette du Moteur

## Déclaration d’ouverture

BUILD-1 est ouvert pour documenter un squelette strictement contractuel aligné sur les Actes I–IV.

## Déclaration de clôture

BUILD-1 est clos : les modules/contrats existent déjà et aucun comportement n’est ajouté.

## ACTE → Artefacts (contractuels)

### ACTE I — Carte ontologique
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/fact.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/state.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/decision.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/trace.py`

### ACTE II — Autorité & Évidence
- `packages/ikoma_mcp/src/ikoma_mcp/core/authority/levels.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/authority/check.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/evidence/primary.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/evidence/secondary.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/evidence/set.py`

### ACTE III — États & Transitions
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/engine.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/app.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/deploy.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/integration.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/transitions.py`

### ACTE IV — Ordres, Refus, Silences
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/order.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/refusal.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/silence.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/registry.py`

## Non-objectifs (verrouillés)

- Pas d’observabilité.
- Pas de preflight.
- Pas d’exécution.
- Pas de gateway réseau.
- Pas d’heuristique.
