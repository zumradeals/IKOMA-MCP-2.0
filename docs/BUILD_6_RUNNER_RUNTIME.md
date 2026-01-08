# BUILD-6 — Runner Runtime (passif, opérationnel)

## Ouverture

BUILD-6 est ouvert pour donner vie au Runner Runtime en mode passif/opérationnel :
observe → classe → trace → émet Ordre/Refus/Silence, sans exécution.

## Périmètre autorisé (verrouillé)

### Autorisé

- Définir les types/contracts du Runner Runtime.
- Implémenter un cycle Runner pur (sans effets de bord).
- Appliquer les tables États/Transitions (Acte III) + Autorité/Évidence (Acte II).
- Produire : décision explicable, trace horodatée, ordre/refus/silence (Acte IV), report complet.
- Définir un registre des motifs explicables (raison normalisée).

### Interdit

- Toute action système : start/stop/restart, fix, retry, apply.
- Tout appel direct au Deployer ou à la Gateway.
- Tout watcher/cron/daemon actif (pas de boucle infinie).
- Toute heuristique/scoring adaptatif.
- Toute auto-confirmation de santé.

## Livrables attendus (minimaux)

- `packages/ikoma_mcp/src/ikoma_mcp/runner/runtime/contracts.py`
- `packages/ikoma_mcp/src/ikoma_mcp/runner/runtime/decision.py`
- `packages/ikoma_mcp/src/ikoma_mcp/runner/runtime/runner_cycle.py`

## Mapping Actes

- Acte II → autorité et preuves (input explicite).
- Acte III → transitions autorisées (tables de transitions).
- Acte IV → expression Ordre/Refus/Silence sans exécution.

## Règles de mapping (Acte IV)

- Preuve primaire insuffisante ⇒ Refus ou Silence (selon contrat explicite).
- Divergence critique observée ⇒ jamais Silence.
- Toute sortie est traçable et référence l’Acte.

## Tests (optionnel, minimal)

- Imports + instanciation des types (pas d’intégration, pas de runtime actif).

## Clôture BUILD-6 (condition)

Le Runner Runtime peut produire un report complet (decision + trace + ordre/refus/silence)
sans exécuter et sans dépendre d’un environnement système.
