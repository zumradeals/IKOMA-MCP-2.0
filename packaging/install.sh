#!/usr/bin/env bash
set -euo pipefail

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
LOG_FILE="${LOG_DIR}/packaging-install.log"

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

ensure_command() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    die "Missing required command: ${cmd}"
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
}

setup_logging() {
  touch "${LOG_FILE}"
  chmod 640 "${LOG_FILE}"
  exec > >(tee -a "${LOG_FILE}") 2>&1
}

install_packages() {
  log "Installing system dependencies"
  ensure_command apt-get
  apt-get update -y
  apt-get install -y python3 python3-venv python3-pip git ca-certificates
}

install_code() {
  if [[ -d "${CODE_DIR}" ]]; then
    log "Code directory already exists at ${CODE_DIR}; skipping copy"
    return
  fi

  log "Installing code to ${CODE_DIR}"
  if git -C "${REPO_ROOT}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git clone "${REPO_ROOT}" "${CODE_DIR}"
  else
    mkdir -p "${CODE_DIR}"
    cp -a "${REPO_ROOT}/." "${CODE_DIR}/"
  fi

  chown -R "${IKOMA_USER}:${IKOMA_GROUP}" "${CODE_DIR}"
}

install_venv() {
  if [[ ! -d "${VENV_DIR}" ]]; then
    log "Creating virtual environment at ${VENV_DIR}"
    python3 -m venv "${VENV_DIR}"
  fi

  log "Installing Python package"
  "${VENV_DIR}/bin/pip" install --upgrade pip
  "${VENV_DIR}/bin/pip" install -e "${CODE_DIR}/packages/ikoma_mcp"
}

install_templates() {
  log "Installing environment templates"
  for template in runner deployer gateway; do
    local env_file="${ETC_DIR}/${template}.env"
    if [[ ! -f "${env_file}" ]]; then
      install -m 600 -o root -g root "${SCRIPT_DIR}/templates/${template}.env.example" "${env_file}"
      log "Created ${env_file}"
    else
      log "Env file exists: ${env_file}"
    fi
  done
}

install_systemd_units() {
  log "Installing systemd unit files"
  for unit in ikoma-mcp-runner.service ikoma-mcp-deployer.service ikoma-mcp-gateway.service ikoma-mcp.service; do
    install -m 644 -o root -g root "${SCRIPT_DIR}/systemd/${unit}" "/etc/systemd/system/${unit}"
  done

  for svc in ikoma-mcp-runner ikoma-mcp-deployer ikoma-mcp-gateway; do
    rm -rf "/etc/systemd/system/${svc}.service.d"
  done

  systemctl daemon-reload
}

enable_services() {
  local enable_now="$1"
  local services=(ikoma-mcp-runner ikoma-mcp-deployer ikoma-mcp-gateway ikoma-mcp)
  if [[ "${enable_now}" == "true" ]]; then
    log "Enabling and starting services"
    systemctl enable --now "${services[@]/%/.service}"
  else
    log "Enabling services without starting (--no-start)"
    systemctl enable "${services[@]/%/.service}"
  fi
}

main() {
  require_root
  local start_services="true"
  for arg in "$@"; do
    case "${arg}" in
      --no-start)
        start_services="false"
        ;;
      *)
        die "Unknown argument: ${arg}"
        ;;
    esac
  done
  install -d -m 750 -o root -g root "${LOG_DIR}"
  setup_logging
  log "Starting IKOMA MCP 2.0 PACK-2 installation"
  install_packages
  ensure_user_group
  ensure_dirs
  install_code
  install_venv
  install_templates
  install_systemd_units
  enable_services "${start_services}"
  log "Installation complete"
  log "Installed code at ${CODE_DIR}"
  log "Virtualenv at ${VENV_DIR}"
  log "Config directory at ${ETC_DIR}"
  log "State directory at ${LIB_DIR}"
  log "Log directory at ${LOG_DIR}"
}

main "$@"
