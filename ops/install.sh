#!/usr/bin/env bash
set -euo pipefail

# IKOMA MCP 2.0 - Zero-Touch Installation Script
# Target: Ubuntu 22.04 VPS

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd -- "${SCRIPT_DIR}/.." && pwd)

IKOMA_USER="ikoma"
IKOMA_GROUP="ikoma"
BASE_DIR="/opt/ikoma"
CODE_DIR="${BASE_DIR}/code"
VENV_DIR="${BASE_DIR}/venv"
ETC_DIR="/etc/ikoma"
LIB_DIR="/var/lib/ikoma"
LOG_DIR="/var/log/ikoma"

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

ensure_user_group() {
  if ! getent group "${IKOMA_GROUP}" >/dev/null; then
    log "Creating group ${IKOMA_GROUP}"
    groupadd --system "${IKOMA_GROUP}"
  fi

  if ! id -u "${IKOMA_USER}" >/dev/null 2>&1; then
    log "Creating user ${IKOMA_USER}"
    useradd --system --gid "${IKOMA_GROUP}" --home-dir "${BASE_DIR}" --shell /usr/sbin/nologin "${IKOMA_USER}"
  fi
}

ensure_dirs() {
  log "Ensuring directories"
  install -d -m 750 -o "${IKOMA_USER}" -g "${IKOMA_GROUP}" "${BASE_DIR}" "${LIB_DIR}" "${LOG_DIR}"
  install -d -m 750 -o root -g "${IKOMA_GROUP}" "${ETC_DIR}"
  
  # Deployer orders tree
  install -d -m 770 -o "${IKOMA_USER}" -g "${IKOMA_GROUP}" "${LIB_DIR}/orders"
  install -d -m 770 -o "${IKOMA_USER}" -g "${IKOMA_GROUP}" "${LIB_DIR}/orders/inbox"
  install -d -m 770 -o "${IKOMA_USER}" -g "${IKOMA_GROUP}" "${LIB_DIR}/orders/consumed"
  install -d -m 770 -o "${IKOMA_USER}" -g "${IKOMA_GROUP}" "${LIB_DIR}/orders/rejected"
}

install_packages() {
  log "Installing system dependencies"
  apt-get update -y
  apt-get install -y python3 python3-venv python3-pip git ca-certificates curl net-tools
}

install_code() {
  if [[ -d "${CODE_DIR}" ]]; then
    log "Updating code at ${CODE_DIR}"
    rm -rf "${CODE_DIR}"
  fi

  log "Installing code to ${CODE_DIR}"
  cp -a "${REPO_ROOT}/." "${CODE_DIR}/"
  chown -R "${IKOMA_USER}:${IKOMA_GROUP}" "${CODE_DIR}"
  
  # Git safety
  sudo -u "${IKOMA_USER}" git config --global --add safe.directory "${CODE_DIR}"
}

install_venv() {
  log "Creating virtual environment at ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
  "${VENV_DIR}/bin/pip" install --upgrade pip
  "${VENV_DIR}/bin/pip" install -e "${CODE_DIR}/packages/ikoma_mcp"
}

install_config() {
  log "Installing environment files"
  for template in runner deployer gateway; do
    local env_file="${ETC_DIR}/${template}.env"
    if [[ ! -f "${env_file}" ]]; then
      install -m 640 -o root -g "${IKOMA_GROUP}" "${CODE_DIR}/packaging/templates/${template}.env.example" "${env_file}"
    fi
  done
}

install_systemd() {
  log "Installing systemd units"
  local systemd_dir="/etc/systemd/system"
  for unit in ikoma-mcp-runner.service ikoma-mcp-deployer.service ikoma-mcp-gateway.service ikoma-mcp.service; do
    cp "${CODE_DIR}/packaging/systemd/${unit}" "${systemd_dir}/${unit}"
    sed -i "s|/opt/ikoma|${BASE_DIR}|g" "${systemd_dir}/${unit}"
    sed -i "s|/etc/ikoma|${ETC_DIR}|g" "${systemd_dir}/${unit}"
  done
  systemctl daemon-reload
  systemctl enable ikoma-mcp-runner ikoma-mcp-deployer ikoma-mcp-gateway ikoma-mcp
  systemctl restart ikoma-mcp-runner ikoma-mcp-deployer ikoma-mcp-gateway ikoma-mcp
}

health_check() {
  log "Running health checks"
  sleep 5
  
  local endpoints=(
    "http://127.0.0.1:9000/health"
    "http://127.0.0.1:9000/v1/runner/cycle"
    "http://127.0.0.1:9000/v1/deployer/last"
  )
  
  for ep in "${endpoints[@]}"; do
    log "Checking ${ep}..."
    if curl -s -f "${ep}" > /dev/null; then
      log "OK: ${ep}"
    else
      log "FAIL: ${ep}"
      return 1
    fi
  done
}

main() {
  require_root
  log "Starting IKOMA MCP 2.0 Final Installation"
  install_packages
  ensure_user_group
  ensure_dirs
  install_code
  install_venv
  install_config
  install_systemd
  health_check
  log "Installation Successful"
}

main "$@"
