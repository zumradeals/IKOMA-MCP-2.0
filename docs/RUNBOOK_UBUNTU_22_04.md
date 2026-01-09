# IKOMA MCP 2.0 - Runbook Ubuntu 22.04

Ce document guide l'installation et la maintenance de l'infrastructure IKOMA MCP 2.0 sur Ubuntu 22.04.

## Installation Standard

```bash
sudo ./packaging/install.sh
```

## Gestion des Environnements

Les fichiers de configuration se trouvent dans `/etc/ikoma/` :
- `runner.env`
- `deployer.env`
- `gateway.env`

**Permissions :** 640 (root:ikoma). Seul root et l'utilisateur du service peuvent les lire.

## Gestion de Git (Dubious Ownership)

Si vous rencontrez des erreurs de "dubious ownership", utilisez l'une des méthodes suivantes :

### Méthode A (Recommandée - Automatisée)
Le script d'installation configure automatiquement le répertoire comme sûr pour l'utilisateur `ikoma`.

### Méthode B (Manuelle - Ciblée)
```bash
sudo -u ikoma git config --global --add safe.directory /opt/ikoma/code
```

### Méthode C (Interdite)
Ne jamais utiliser `git config --global --add safe.directory '*'` en production.

## Vérification de la Santé

```bash
# Vérifier les services
systemctl status ikoma-mcp-*

# Vérifier le chargement des envfiles
systemctl show ikoma-mcp-runner | grep EnvironmentFile

# Tester l'accès aux fichiers .env
sudo -u ikoma cat /etc/ikoma/runner.env
```
