# IKOMA MCP 2.0 - Audit Fix Evidence Log

Ce document contient les preuves d'exécution et de validation des corrections d'infrastructure.

## Checkpoint 0: Plan de Correction

### Plan d'action (10 lignes max)
1. Créer la branche `fix/infra-production-ready`.
2. Remplacer les wildcards `EnvironmentFile` par des chemins explicites dans les unités Systemd.
3. Corriger les permissions des fichiers `.env` (640, root:ikoma) dans `install.sh`.
4. Résoudre le problème de "dubious ownership" Git en assurant la cohérence de l'ownership sur `/opt/ikoma/code`.
5. Réduire les hardcodes dans les scripts de packaging via des variables de base.
6. Valider chaque étape par des commandes de preuve.
7. Mettre à jour le Runbook Ubuntu 22.04.
8. Effectuer une installation complète de test pour la certification finale.

### Fichiers Systemd concernés
- `packaging/systemd/ikoma-mcp-runner.service`
- `packaging/systemd/ikoma-mcp-deployer.service`
- `packaging/systemd/ikoma-mcp-gateway.service`

### Scripts Packaging concernés
- `packaging/install.sh`
- `packaging/upgrade.sh` (si applicable)

### Stratégie Git recommandée
**Méthode A (Recommandée)** : Assurer un ownership cohérent sur `/opt/ikoma/code` pour l'utilisateur du service (`ikoma`). Le script d'installation doit effectuer un `chown -R ikoma:ikoma` après le clone/copie, et les opérations Git ultérieures doivent être effectuées par cet utilisateur ou via une configuration `safe.directory` spécifique si nécessaire.
## Checkpoint 1: Systemd
```bash
systemctl show ikoma-mcp-runner | grep EnvironmentFile
EnvironmentFiles=/etc/ikoma/runner.env (ignore_errors=no)
```
## Checkpoint 2: Permissions .env
```bash
## Checkpoint 2: Permissions .env
```bash
-rw-r----- 1 root ikoma 117 Jan  9 04:43 /etc/ikoma/deployer.env
-rw-r----- 1 root ikoma 116 Jan  9 04:43 /etc/ikoma/gateway.env
-rw-r----- 1 root ikoma 115 Jan  9 04:43 /etc/ikoma/runner.env
# IKOMA MCP Runner environment
```
## Checkpoint 3: Git Dubious Ownership
```bash
On branch fix/infra-production-ready
Your branch is up to date with 'origin/fix/infra-production-ready'.
```
## Checkpoint 4: Portabilité
```bash
BASE_DIR="/opt/ikoma"
ETC_DIR="/etc/ikoma"
```
## Checkpoint 5: Re-Certification
```bash
active
EnvironmentFiles=/etc/ikoma/runner.env (ignore_errors=no)
# IKOMA MCP Runner environment
On branch fix/infra-production-ready
```
## Checkpoint 5: Re-Certification (Suite)
```bash
{"status": "ok", "service": "gateway", "version": "0.1.0"}
```
### VERDICT FINAL: CERTIFICATION IKOMA MCP 2.0: OK
