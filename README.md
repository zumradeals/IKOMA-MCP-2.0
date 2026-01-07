# IKOMA MCP 2.0

Référentiel de gouvernance et de conception pour IKOMA MCP 2.0.

## Structure du dépôt

- `docs/` : doctrine et actes (Loi du Moteur, RAE, documents conceptuels).
- `packages/` : paquets importables, dont le moteur conceptuel.
- `fixtures/` : exemples non-exécutifs (manifests, samples).

## Comment lire ce dépôt (90 secondes)

1. Commencer par `docs/LOI_DU_MOTEUR.md`.
2. Lire `docs/RAE_REFERENTIEL_APP_EXPORTABLE.md`.
3. Explorer le package `packages/ikoma_mcp/` pour les contrats et types.

Aucune logique d’exécution n’est incluse. Ce dépôt sépare strictement :

- la doctrine (racine + docs),
- le paquet (packages),
- la distribution (métadonnées de packaging uniquement).


