# PACK-2 Installation Scripts

This folder contains the PACK-2 installation assets for IKOMA MCP 2.0. The scripts are strictly **hors moteur** and do not introduce any governance logic.

## Contents

- `install.sh`: Idempotent installer.
- `upgrade.sh`: Pull + reinstall while preserving `/etc/ikoma/*.env`.
- `uninstall.sh`: Clean removal with optional `--purge`.
- `status.sh`: Read-only health/status checks.
- `systemd/`: Unit files for passive services.
- `templates/`: Environment file templates for `/etc/ikoma/`.

## Directory Convention

- `/opt/ikoma/`: code + virtualenv + runtime
- `/etc/ikoma/`: configuration/env (root-owned, 600)
- `/var/lib/ikoma/`: persistent state
- `/var/log/ikoma/`: logs

## Services

Systemd units are passive `oneshot` services that only import the Python package to validate availability.
No runtime governance or network services are started by these units.

## Quickstart

```bash
sudo ./packaging/install.sh
sudo ./packaging/status.sh
```

## Notes

- No TLS, no reverse proxy, no DNS configuration.
- Secrets must be stored only in `/etc/ikoma/*.env` with strict permissions.
