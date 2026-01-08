#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

BASE_DIR="/opt/ikoma"
CODE_DIR="${BASE_DIR}/code"
VENV_DIR="${BASE_DIR}/venv"
LOG_DIR="/var/log/ikoma"
LOG_FILE="${LOG_DIR}/packaging-upgrade.log"

log() {
  printf '[%s] %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*"
}

die() {
  log "ERROR: $*"
  exit 1
}

require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    die "This script must be run as root."
  fi
}

setup_logging() {
  install -d -m 750 -o root -g root "${LOG_DIR}"
  touch "${LOG_FILE}"
  chmod 640 "${LOG_FILE}"
  exec > >(tee -a "${LOG_FILE}") 2>&1
}

update_code() {
  if [[ -d "${CODE_DIR}/.git" ]]; then
    log "Updating code via git pull"
    git -C "${CODE_DIR}" pull --ff-only
  else
    log "No git repository found at ${CODE_DIR}; skipping git pull"
  fi
}

upgrade_package() {
  if [[ ! -d "${VENV_DIR}" ]]; then
    die "Virtualenv not found at ${VENV_DIR}. Run install.sh first."
  fi
  log "Upgrading Python package"
  "${VENV_DIR}/bin/pip" install --upgrade pip
  "${VENV_DIR}/bin/pip" install -e "${CODE_DIR}/packages/ikoma_mcp"
}

reload_services() {
  log "Reloading systemd units"
  systemctl daemon-reload
  for svc in ikoma-mcp-runner ikoma-mcp-deployer ikoma-mcp-gateway ikoma-mcp; do
    if systemctl is-active --quiet "${svc}.service"; then
      systemctl try-restart "${svc}.service" || true
    fi
  done
}

main() {
  require_root
  setup_logging
  log "Starting IKOMA MCP 2.0 PACK-2 upgrade"
  update_code
  upgrade_package
  reload_services
  log "Upgrade complete"
}

main "$@"
