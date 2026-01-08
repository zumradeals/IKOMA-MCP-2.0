# BUILD-5 — Runtime passif (contractuel)

## Ouverture

BUILD-5 est ouvert pour définir le Runtime passif d’IKOMA MCP, sans droit d’action.
Le Runtime existe, observe, traite et trace, mais ne modifie rien.

## Ce que le Runtime fait

- Initialise son état en `UNKNOWN` puis expose un cycle logique read-only.
- Reçoit des Facts et construit un `EvidenceSet`.
- Exécute Preflight et Health en lecture seule.
- Applique le mapping ACTE IV pour exprimer un Ordre / Refus / Silence.
- Trace toute décision ou non-décision (silence explicite).

## Ce que le Runtime refuse de faire

- Exécuter un ordre ou déclencher une action système.
- Jouer un rôle de scheduler, daemon, orchestrateur ou correcteur.
- Déduire des décisions hors des règles existantes.
- Introduire un backend, une base, ou une dépendance système.

## Ce qui reste impossible tant que BUILD-6 n’est pas ouvert

- Toute exécution d’ordres (start/stop/reload/install).
- Toute orchestration de déploiement ou intégration système.
- Toute remédiation, auto-réparation, auto-validation.

## Périmètre autorisé (verrouillé)

### Cycle de Runtime

- Initialisation du moteur (état `UNKNOWN`).
- Boucle passive de réception des observables.
- Passage par Preflight / Health (read-only).
- Production de Reports, Traces, Ordres / Refus / Silences (ACTE IV).

### Temporalité

- Gestion du temps logique : tick, instant, cycle.
- Règle stricte : aucun cycle ne déclenche une action par lui-même.

### Persistance minimale

- Registres de traces.
- États connus / inconnus.
- Ordres consommés ou refusés.
- Aucun backend imposé.

### Interfaces Runtime

- Entrée : Facts / Evidence.
- Sortie : Reports / Orders / Traces.
- Aucune dépendance système.

### Silence Runtime

- Silence implémenté comme état explicite.
- Silence traçable.
- Silence ≠ erreur.

## Runtime Flow (documenté)

1. Réception Facts
2. Construction EvidenceSet
3. Preflight (read-only)
4. Health (read-only)
5. Mapping ACTE IV
6. Production Ordre / Refus / Silence
7. Trace finale

## États Runtime

- INIT
- RUNNING (passif)
- DEGRADED (observabilité partielle)
- BLOCKED (absence de preuve)
- FAILED (incohérence critique)
- STOPPED (arrêt externe, non décidé)

## Non-objectifs à lister explicitement

- Installation
- Distribution
- Déploiement
- Configuration serveur
- Sécurité système
- Performance
- Scalabilité
- Haute disponibilité

## Rappel explicite

> Le Runtime existe sans agir.

## Clause de clôture obligatoire

> BUILD-5 est clos.
> Le moteur est vivant, conscient de son état, mais sans droit d’action.
> Aucune mutation du réel n’est autorisée à ce stade.
> Toute suite nécessite validation explicite de l’Orchestrateur.
