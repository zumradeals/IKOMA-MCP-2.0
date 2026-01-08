# BUILD-8 — Gateway Runtime (contrats + exposition contrôlée)

## Décision

BUILD-8 est ouvert.
Le Gateway Runtime expose ou n’expose pas, sans gouvernance ni logique applicative.

## Périmètre autorisé (verrouillé)

### Ce qui est autorisé

- Définir des contrats Gateway Runtime :
  - Contexte d’exposition (GatewayContext)
  - Demande d’exposition (GatewayRequest)
  - Rapport d’exposition (GatewayReport)
- Implémenter des fonctions pures et passives :
  - production de rapports d’exposition,
  - génération de faits + traces,
  - mapping état → exposition observée.
- Mapper explicitement les sorties vers Ordre / Refus / Silence (ACTE IV).
- Définir les états d’exposition (sans exécution réseau) : OPEN, CLOSED, UNKNOWN.

### Ce qui est strictement interdit

- Toute gouvernance (aucune décision).
- Toute observation système directe (ports, réseau, firewall).
- Toute ouverture réelle de port, socket, proxy, route.
- Tout retry, auto-correction ou heuristique.
- Toute logique applicative.
- Toute mutation du moteur.

## États Gateway

- OPEN
- CLOSED
- UNKNOWN

## Mapping ACTE IV (explicite)

- Exposition confirmée + ordre valide → Order consommé.
- Preuve manquante → Silence.
- Incohérence / ordre invalide → Refus traçable.

⚠️ Aucun cas ne doit produire une décision implicite.

## Invariants

- Gateway n’est pas une source de vérité.
- Gateway ne confirme jamais seul.
- Gateway ne produit que des rapports, jamais des actions.
- Toute exposition est déclarative et traçable.
- Absence de preuve ⇒ UNKNOWN, jamais OPEN par défaut.

## Non-objectifs explicites

- Pas d’exposition réelle.
- Pas de proxy, reverse-proxy, firewall, DNS.
- Pas de supervision réseau.
- Pas de dépendance OS ou plateforme.
- Pas de tests d’intégration système.

## Séquence de travail (obligatoire)

1. Créer les types et enums Gateway.
2. Implémenter des builders de rapports purs.
3. Ajouter le mapping ACTE IV (ordre / refus / silence).
4. Ajouter les traces associées.
5. Rédiger la documentation de clôture BUILD-8.

## Tests

Aucun test d’exécution.
Tests autorisés : instanciation, import, mapping logique, traçabilité.

## Clause de clôture

BUILD-8 est clos lorsque :

- Les contrats Gateway existent,
- Les états d’exposition sont définis,
- Le mapping ACTE IV est explicite,
- Aucun mécanisme réseau n’est implémenté,
- La séparation Runner / Deployer / Gateway est intacte.

Aucune suite n’est autorisée sans validation explicite de l’Orchestrateur.
