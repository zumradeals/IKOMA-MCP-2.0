#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

IKOMA_USER="ikoma"
IKOMA_GROUP="ikoma"
BASE_DIR="/opt/ikoma"
ETC_DIR="/etc/ikoma"
LIB_DIR="/var/lib/ikoma"
LOG_DIR="/var/log/ikoma"
LOG_FILE="${LOG_DIR}/packaging-uninstall.log"

PURGE=false

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

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --purge)
        PURGE=true
        shift
        ;;
      -h|--help)
        cat <<EOF_HELP
Usage: $0 [--purge]

--purge   Remove /etc/ikoma, /var/lib/ikoma, and /var/log/ikoma in addition to code/venv.
EOF_HELP
        exit 0
        ;;
      *)
        die "Unknown argument: $1"
        ;;
    esac
  done
}

stop_services() {
  log "Stopping services"
  for svc in ikoma-mcp-runner ikoma-mcp-deployer ikoma-mcp-gateway ikoma-mcp; do
    if systemctl list-unit-files "${svc}.service" >/dev/null 2>&1; then
      systemctl stop "${svc}.service" || true
      systemctl disable "${svc}.service" || true
    fi
  done
}

remove_systemd_units() {
  log "Removing systemd unit files"
  for unit in ikoma-mcp-runner.service ikoma-mcp-deployer.service ikoma-mcp-gateway.service ikoma-mcp.service; do
    rm -f "/etc/systemd/system/${unit}"
  done
  rm -rf /etc/systemd/system/ikoma-mcp-runner.service.d
  rm -rf /etc/systemd/system/ikoma-mcp-deployer.service.d
  rm -rf /etc/systemd/system/ikoma-mcp-gateway.service.d
  systemctl daemon-reload
}

remove_runtime() {
  log "Removing runtime directories"
  rm -rf "${BASE_DIR}"
}

purge_state() {
  if [[ "${PURGE}" == "true" ]]; then
    log "Purging configuration and state"
    rm -rf "${ETC_DIR}" "${LIB_DIR}" "${LOG_DIR}"
  else
    log "Preserving ${ETC_DIR}, ${LIB_DIR}, and ${LOG_DIR} (use --purge to remove)"
  fi
}

remove_user_group() {
  if [[ "${PURGE}" == "true" ]]; then
    if id -u "${IKOMA_USER}" >/dev/null 2>&1; then
      log "Removing user ${IKOMA_USER}"
      userdel "${IKOMA_USER}" || true
    fi
    if getent group "${IKOMA_GROUP}" >/dev/null 2>&1; then
      log "Removing group ${IKOMA_GROUP}"
      groupdel "${IKOMA_GROUP}" || true
    fi
  fi
}

main() {
  require_root
  parse_args "$@"
  setup_logging
  log "Starting IKOMA MCP 2.0 PACK-2 uninstall"
  stop_services
  remove_systemd_units
  remove_runtime
  purge_state
  remove_user_group
  log "Uninstall complete"
}

main "$@"
