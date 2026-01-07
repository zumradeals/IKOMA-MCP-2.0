# BUILD-0 — Table ACTE → Artefacts

## A) Artefacts normatifs (docs/)

| ACTE | Artefacts normatifs | Statut |
| --- | --- | --- |
| ACTE I — Carte ontologique | `docs/ACTE_I_CARTE_ONTOLOGIQUE.md` (obligatoire) | À créer |
|  | `docs/LOI_DU_MOTEUR.md` (référence croisée) | Présent |
| ACTE II — Autorité & Évidence (RAE) | `docs/ACTE_II_RAE_AUTORITE_EVIDENCE.md` (obligatoire) | À créer |
|  | `docs/RAE_REFERENTIEL_APP_EXPORTABLE.md` (annexe) | Présent |
| ACTE III — États & Transitions | `docs/ACTE_III_ETATS_TRANSITIONS.md` (obligatoire) | À créer |
| ACTE IV — Ordres, Refus, Silences | `docs/ACTE_IV_ORDRES_REFUS_SILENCES.md` (obligatoire) | À créer |

## B) Artefacts de contrat (packages/)

### ACTE I → Types fondamentaux
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/fact.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/state.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/decision.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/types/trace.py`

### ACTE II → Autorité & Évidence
- `packages/ikoma_mcp/src/ikoma_mcp/core/authority/levels.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/authority/check.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/evidence/primary.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/evidence/secondary.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/evidence/set.py`

### ACTE III → États & Transitions
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/engine.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/app.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/deploy.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/integration.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/state/transitions.py`

### ACTE IV → Ordres / Refus / Silences
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/order.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/refusal.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/silence.py`
- `packages/ikoma_mcp/src/ikoma_mcp/core/orders/registry.py`

### Frontières (Acte I + Loi) → Interfaces des composants
- `packages/ikoma_mcp/src/ikoma_mcp/mcp/interfaces.py`
- `packages/ikoma_mcp/src/ikoma_mcp/runner/interfaces.py`
- `packages/ikoma_mcp/src/ikoma_mcp/deployer/interfaces.py`
- `packages/ikoma_mcp/src/ikoma_mcp/gateway/interfaces.py`

## C) Artefacts interdits (BUILD-0/1/2A)

- Aucun appel système (`ps`, `ss`, `docker`) dans `packages/`.
- Aucun client DB / réseau actif.
- Aucun executor.
- Aucun deploy réel.
- Aucun daemon/CLI.

## Règle de traçabilité

Tout nouvel artefact doit déclarer son ACTE parent.
