#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/opt/ikoma"
CODE_DIR="${BASE_DIR}/code"
VENV_DIR="${BASE_DIR}/venv"
ETC_DIR="/etc/ikoma"
LIB_DIR="/var/lib/ikoma"
LOG_DIR="/var/log/ikoma"

log() {
  printf '[%s] %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$*"
}

check_path() {
  local label="$1"
  local path="$2"
  if [[ -e "${path}" ]]; then
    log "OK: ${label} at ${path}"
  else
    log "MISSING: ${label} at ${path}"
  fi
}

check_service() {
  local svc="$1"
  if systemctl list-unit-files "${svc}.service" >/dev/null 2>&1; then
    if systemctl is-active --quiet "${svc}.service"; then
      log "SERVICE: ${svc} is active"
    else
      log "SERVICE: ${svc} is inactive"
    fi
    if systemctl is-enabled --quiet "${svc}.service"; then
      log "SERVICE: ${svc} is enabled"
    else
      log "SERVICE: ${svc} is disabled"
    fi
  else
    log "SERVICE: ${svc} unit not installed"
  fi
}

check_version() {
  if [[ -x "${VENV_DIR}/bin/python" ]]; then
    local version
    version=$("${VENV_DIR}/bin/python" -c "import importlib.metadata as m; print(m.version('ikoma_mcp'))" 2>/dev/null || true)
    if [[ -n "${version}" ]]; then
      log "PACKAGE: ikoma_mcp version ${version}"
    else
      log "PACKAGE: ikoma_mcp not installed in venv"
    fi
  else
    log "PACKAGE: venv python not found"
  fi
}

main() {
  log "IKOMA MCP 2.0 PACK-2 status"
  check_path "Base directory" "${BASE_DIR}"
  check_path "Code directory" "${CODE_DIR}"
  check_path "Virtualenv" "${VENV_DIR}"
  check_path "Config directory" "${ETC_DIR}"
  check_path "State directory" "${LIB_DIR}"
  check_path "Log directory" "${LOG_DIR}"
  check_version
  check_service "ikoma-mcp-runner"
  check_service "ikoma-mcp-deployer"
  check_service "ikoma-mcp-gateway"
  check_service "ikoma-mcp"
  log "Status complete"
}

main "$@"
