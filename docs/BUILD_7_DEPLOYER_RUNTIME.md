# BUILD-7 — Deployer Runtime (contrats + exécution minimale)

## Principe cardinal

Le Deployer exécute, puis se tait.
Il ne valide rien, ne corrige rien, ne "sait" pas si c’est bien ou mal.

## Périmètre autorisé (verrouillé)

### Ce qui est autorisé

- Définir les interfaces runtime du Deployer.
- Définir un ExecutionContext (fourni par Runner).
- Implémenter une exécution minimale explicite :
  - action demandée,
  - résultat brut,
  - statut observable.
- Produire : Facts, Traces, ExecutionResult.
- Marquer l’ordre comme consommé (sans interprétation).

### Ce qui est interdit

- Toute décision conditionnelle ("si", "peut-être", "retry").
- Toute reclassification d’état.
- Toute correction automatique.
- Toute lecture d’intention métier.
- Toute interaction avec Gateway.
- Toute boucle active, cron, watcher.

## Livrables attendus (minimaux)

1. Contrats Deployer Runtime
   - `deployer/runtime/contracts.py`
   - `ExecutionRequest`
   - `ExecutionContext`
   - `ExecutionResult`
   - `ExecutionStatus` (APPLIED | FAILED | UNKNOWN)

2. Exécution minimale
   - `deployer/runtime/execute.py`
   - fonction pure autant que possible
   - exécute une instruction explicite
   - retourne un ExecutionResult
   - n’émet aucune décision

3. Traces

- timestamp début / fin
- identité de l’ordre
- action tentée
- résultat brut
- erreur brute (si présente)

## Mapping ACTE III

Résultat → État de déploiement :

- succès observable → APPLIED
- échec observable → FAILED
- absence de preuve → UNKNOWN

⚠️ Aucun passage direct vers UP/DOWN applicatif

## Non-objectifs explicites

- Pas de rollback
- Pas de retry
- Pas de health
- Pas de préflight
- Pas de compensation
- Pas de logique conditionnelle

## Séquence de travail recommandée (disciplinée)

1. Créer les types/contrats.
2. Implémenter l’exécution minimale.
3. Générer les traces.
4. Rédiger la doc de clôture BUILD-7.

## Tests (optionnel, minimal)

- Import / instanciation uniquement (pas d’intégration).

## Clause de clôture BUILD-7

BUILD-7 sera clos lorsque :

- le Deployer peut exécuter un ordre sans réfléchir,
- le résultat est observable et traçable,
- aucune logique de gouvernance n’existe dans le code.
