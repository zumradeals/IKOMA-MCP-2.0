⚖️ LOI DU MOTEUR
IKOMA MCP 2.0 — Système souverain d’orchestration applicative
Préambule — Nature du Moteur

IKOMA MCP 2.0 n’est pas une application.
IKOMA MCP 2.0 n’est pas un produit livrable.
IKOMA MCP 2.0 n’est pas généré pour un client final.

IKOMA MCP 2.0 est :

un MOTEUR SYSTÈME,
destiné à faire exister, contrôler et gouverner
d’autres entités logicielles.

Il appartient à la même catégorie que :

un OS minimal,

un orchestrateur,

un daemon racine,

une autorité d’état.

Il ne se déploie pas,
il est installé.

Article 1 — Séparation ontologique absolue

Le moteur IKOMA MCP est ontologiquement distinct de toute application qu’il gère.

En conséquence :

MCP ne suit pas les règles imposées aux applications IKOMA.

MCP n’obéit pas au PROMPT IKOMA — Application.

MCP ne peut pas être décrit comme un “service client”.

MCP ne dépend d’aucun framework applicatif généré par IA.

👉 Ce qu’il contrôle ne peut pas le contrôler.

Article 2 — Principe de non-récursion

Le moteur :

ne se déploie pas lui-même,

ne se met pas à jour via lui-même,

ne s’orchestre pas lui-même,

ne lit jamais ses propres manifests comme vérité.

Toute tentative de :

“MCP qui lit un ikoma.release pour lui-même”

“MCP généré par le même prompt que ses apps”

est formellement interdite.

Article 3 — Vérité terrain > Déclaration

IKOMA MCP 2.0 ne croit aucune déclaration sans vérification.

La source de vérité est toujours l’état réel du système :

process en cours,

ports réellement ouverts,

containers réellement actifs,

bases réellement accessibles,

fichiers réellement présents.

Toute divergence entre :

l’état déclaré

et l’état observé

est traitée comme une erreur critique, jamais comme une exception silencieuse.

Article 4 — Traçabilité native obligatoire

Toute action du moteur génère :

un événement horodaté,

une cause explicite,

une conséquence mesurable.

Aucun “magique”, aucun “automatique”, aucun “on suppose”.

MCP est explicable a posteriori.
Sinon, il n’existe pas.

Article 5 — Neutralité applicative

Le moteur :

ne connaît pas React,

ne connaît pas Vite,

ne connaît pas Supabase en tant que produit,

ne connaît que des contrats.

Il ne manipule que :

 des ports,

 des process,

 des repos,

 des manifests,

 des états (UP / DOWN / FAILED / UNKNOWN).

Les technologies sont des détails injectés, jamais des dépendances structurelles.

Article 6 — Installation ≠ Déploiement

IKOMA MCP 2.0 :

est installé une seule fois sur un serveur,

persiste indépendamment des applications,

survit aux crashs des apps,

survit aux suppressions de containers.

Les applications sont éphémères.
Le moteur est persistant.

Article 7 — Autorité hiérarchique

La hiérarchie est immuable :

IKOMA MCP (MOTEUR)
 ├── Runner (interface d’observation et de commande)
 ├── Deployer (exécutant contrôlé)
 ├── Gateway (exposition réseau)
 └── Applications (entités gouvernées)


Une application :

ne peut pas modifier MCP,

ne peut pas modifier Runner,

ne peut pas modifier Gateway.

Article 8 — Responsabilité explicite des composants

Chaque composant a un rôle non négociable :

Runner : voir, décider, enregistrer

Deployer : exécuter, rien de plus

Gateway : exposer, jamais décider

Toute confusion de responsabilité est un bug conceptuel, pas un bug technique.

Article 9 — Refus du “ça marche”

Un comportement est considéré valide uniquement si :

il est traçable,

reproductible,

explicable,

durable.

Un système qui “marche mais qu’on ne comprend pas”
est officiellement déclaré instable.

Article 10 — Primauté de la conception

Aucune ligne de code du moteur ne doit être produite tant que :

la loi n’est pas comprise,

les frontières ne sont pas écrites,

les responsabilités ne sont pas figées.

Le moteur préfère ne pas exister
plutôt qu’exister de travers.

Clause finale — Non-retour

Toute version future de IKOMA MCP :

devra respecter cette loi,

devra être compatible avec elle,

ou devra explicitement la révoquer.

Sans loi, MCP n’est qu’un outil.
Avec cette loi, MCP devient une infrastructure souveraine.
