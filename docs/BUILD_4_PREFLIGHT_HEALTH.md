BUILD-4 — Preflight & Health (contractuel)

## Ouverture

BUILD-4 — Preflight & Health (implémentation contractuelle)

Décision : BUILD-4 est ouvert, strictement en implémentation contractuelle.
Aucune exécution, aucune action système, aucune heuristique.

## Périmètre autorisé (verrouillé)

### Ce qui est autorisé

- Définir les interfaces et types du Preflight et du Health.
- Implémenter des contrats read-only produisant :
  - des Facts,
  - de l'Evidence (primaire/secondaire),
  - des Traces.
- Mapper explicitement les sorties vers Ordre / Refus / Silence (ACTE IV) sans arbitrage autonome.
- Décrire les invariants (préconditions strictes, non-auto-confirmation).

### Ce qui est interdit

- Toute exécution (start/stop, fix, retry).
- Toute auto-validation (health ≠ confirmation).
- Tout scoring, seuil adaptatif, ou heuristique.
- Toute mutation d'état du moteur ou des apps.
- Tout worker, cron, watcher actif.

## Livrables attendus (minimaux)

### Contrats

- `packages/ikoma_mcp/src/ikoma_mcp/runner/preflight/contracts.py`
  - `PreflightCheck` (input : contexte, output : `PreflightReport`)
  - `PreflightReport` (facts + evidence + trace)
- `packages/ikoma_mcp/src/ikoma_mcp/runner/health/contracts.py`
  - `HealthProbe` (read-only)
  - `HealthReport` (non auto-confirmant)

### Mapping ACTE IV

- Table/enum liant `PreflightReport` → Ordre / Refus / Silence.
- Règle explicite : preuve manquante ⇒ rapport bloquant (statut `insufficient_evidence`) et aucun ordre émis par défaut.

## Invariants contractuels

- Preflight = vérification de conditions, basée uniquement sur les évidences BUILD-2B.
- Health = observation d'état, jamais une validation.
- Silence = absence d'évidence suffisante, sans interprétation.
- Refus = condition explicitement non satisfaite, traçable.
- Aucun Preflight ne peut produire AVAILABLE ou READY par lui-même.

## Acte → Artefacts

- Acte III (États & Transitions) → `packages/ikoma_mcp/src/ikoma_mcp/runner/health/contracts.py`
- Acte IV (Ordres / Refus / Silence) → `packages/ikoma_mcp/src/ikoma_mcp/runner/preflight/contracts.py`
- BUILD-2B (Observabilité read-only) → `packages/ikoma_mcp/src/ikoma_mcp/core/evidence/`

## Non-objectifs verrouillés

- Pas d'exécution.
- Pas d'auto-remédiation.
- Pas de décision.
- Pas de pipeline CI.
- Pas de tests au-delà d'import/instanciation.

## Clôture (draft)

### Conditions de blocage

- Rapport `insufficient_evidence` = bloquant, sans ordre par défaut.

### Cas d'absence d'observable

- Absence d'évidence suffisante ⇒ silence contractuel, sans interprétation.

### Règles d'irréversibilité locale (sans mécanisme)

- Aucune transition d'état n'est déclenchée par BUILD-4.

## Clôture explicite

BUILD-4 est clos :
- absence totale d'exécution confirmée,
- non-objectifs verrouillés listés ci-dessus,
- toute action future nécessitera un nouvel ordre explicite.
