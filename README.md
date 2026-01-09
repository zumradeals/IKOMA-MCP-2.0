# IKOMA MCP 2.0

Référentiel de gouvernance et de conception pour IKOMA MCP 2.0.

## VPS vierge → IKOMA MCP prêt

Pour installer IKOMA MCP 2.0 sur un VPS Ubuntu 22.04 vierge :

```bash
git clone https://github.com/zumradeals/IKOMA-MCP-2.0.git
cd IKOMA-MCP-2.0
sudo ./ops/install.sh
```

Cette commande installe l'utilisateur `ikoma`, l'environnement virtuel Python, les services systemd et configure le système d'ordres fichiers.

## Ordres fichiers (JSON)

Les ordres déposés dans `/var/lib/ikoma/orders/inbox/` doivent respecter ce schéma :

- `identifier` (string, requis)
- `scope` (string, requis)
- `created_at` (string ISO-8601, optionnel, défaut = maintenant UTC)
- `acte_parent` (string, optionnel, défaut = `ACTE_IV`)
- `metadata` (objet, optionnel, défaut = `{}`) avec :
  - `action` : `deploy.up`, `deploy.down`, `deploy.restart`
  - `target` : composant cible (ex: `gateway`)
  - `release_ref` : référence de release (ex: `v1.0.0`)

Exemple d'ordre :

```json
{
  "identifier": "order-2024-0001",
  "scope": "production",
  "created_at": "2024-01-01T00:00:00Z",
  "acte_parent": "ACTE_IV",
  "metadata": {
    "action": "deploy.up",
    "target": "gateway",
    "release_ref": "v1.0.0"
  }
}
```

Les répertoires d'ordres sont créés par `ops/install.sh`, ainsi qu'un exemple dans
`/var/lib/ikoma/orders/example_order.json`.

## Structure du dépôt

- `docs/` : doctrine et actes (Loi du Moteur, RAE, documents conceptuels).
- `packages/` : paquets importables, dont le moteur conceptuel.
- `fixtures/` : exemples non-exécutifs (manifests, samples).
- `ops/` : scripts d'exploitation et d'installation.

## Comment lire ce dépôt (90 secondes)

1. Commencer par `docs/LOI_DU_MOTEUR.md`.
2. Lire `docs/RAE_REFERENTIEL_APP_EXPORTABLE.md`.
3. Explorer le package `packages/ikoma_mcp/` pour les contrats et types.

Aucune logique d’exécution n’est incluse. Ce dépôt sépare strictement :

- la doctrine (racine + docs),
- le paquet (packages),
- la distribution (métadonnées de packaging uniquement).

## Build ledger

- BUILD-0 = clos (`docs/BUILD_0_ACTE_ARTEFACTS_TABLE.md`)
- BUILD-1 = clos (`docs/BUILD_1_SKELETON_DU_MOTEUR.md`)
- BUILD-2B = clos (observabilité read-only)
- BUILD-3 = clos (Acte IV contractuel)
- BUILD-4 = Preflight and Execution Contracts (Acte IV)
