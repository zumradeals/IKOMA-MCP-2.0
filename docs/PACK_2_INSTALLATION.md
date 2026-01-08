# PACK-2 Installation (IKOMA MCP 2.0)

This document describes the PACK-2 installation scripts for IKOMA MCP 2.0. The scripts are **hors moteur** and only prepare the host environment. They do **not** execute governance logic, bind network ports, configure TLS, or run any runtime remediations.

## Prerequisites

- Ubuntu/Debian-like host with `systemd`
- Root access (all scripts must be run as root)
- Network access for `apt-get` and optional `git pull`

Minimal system dependencies installed by the scripts:

- `python3`
- `python3-venv`
- `python3-pip`
- `git`
- `ca-certificates`

## Installation

From the repository root:

```bash
sudo ./packaging/install.sh
```

What the installer does:

- Creates the `ikoma` system user and group (non-root).
- Sets up stable directories:
  - `/opt/ikoma/` (code + virtualenv)
  - `/etc/ikoma/` (env/config, root-owned, 600)
  - `/var/lib/ikoma/` (state)
  - `/var/log/ikoma/` (logs)
- Copies the repository into `/opt/ikoma/code` on first run.
- Creates a virtualenv at `/opt/ikoma/venv` and installs `packages/ikoma_mcp` in editable mode.
- Installs passive systemd unit files and env drop-ins.
- Creates environment files from templates if missing.

What the installer **does not** do:

- No TLS, reverse proxy, or domain configuration.
- No governance decisions or runtime actions.
- No database provisioning beyond directory creation.
- No Docker/Kubernetes orchestration.

## Upgrade

```bash
sudo ./packaging/upgrade.sh
```

Behavior:

- Performs `git pull --ff-only` if `/opt/ikoma/code` is a git repo.
- Reinstalls the package in the existing virtualenv.
- Reloads systemd and restarts any active IKOMA units.
- Preserves `/etc/ikoma/*.env`.

## Status

```bash
sudo ./packaging/status.sh
```

The status script is read-only and reports:

- Presence of directories
- Installed package version in the venv (if available)
- Systemd unit enable/active status

## Uninstall

```bash
sudo ./packaging/uninstall.sh
```

Optional purge to remove configs and state:

```bash
sudo ./packaging/uninstall.sh --purge
```

Behavior:

- Stops and disables IKOMA systemd units.
- Removes `/opt/ikoma/` (code + venv).
- By default preserves `/etc/ikoma`, `/var/lib/ikoma`, and `/var/log/ikoma`.
- With `--purge`, deletes those directories and removes the `ikoma` user/group.

## Manual Rollback (Basic)

If an upgrade causes issues:

1. `sudo systemctl stop ikoma-mcp.service`
2. `cd /opt/ikoma/code && git log --oneline` to identify a previous commit.
3. `sudo git -C /opt/ikoma/code reset --hard <commit>`
4. `sudo ./packaging/upgrade.sh`

## File Locations

- Installer scripts: `packaging/*.sh`
- Unit files: `packaging/systemd/*.service`
- Env templates: `packaging/templates/*.env.example`
- Operator docs: `docs/PACK_2_INSTALLATION.md`

## Hors Moteur Principles

These scripts only prepare the OS, Python environment, and systemd units. They do not change any governance logic or runtime behavior inside `packages/ikoma_mcp`.
