#!/usr/bin/env bash
# Usage:
#   ./scripts/install.sh --tool <name> [--target <dir>] [--force] [--help]
#
# Installs converted skills into the appropriate location.
# --target overrides the default install path.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TOOL=""
TARGET=""
FORCE=false

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok() {
  echo -e "${GREEN}[OK]${NC} $*"
}

warn() {
  echo -e "${YELLOW}[!!]${NC} $*"
}

err() {
  echo -e "${RED}[ERR]${NC} $*" >&2
}

usage() {
  cat <<'USAGE'
Usage:
  ./scripts/install.sh --tool <name> [--target <dir>] [--force] [--help]

Tools:
  antigravity, cursor, aider, kilocode, windsurf, opencode, augment

Examples:
  ./scripts/install.sh --tool cursor --target /path/to/project
  ./scripts/install.sh --tool antigravity
  ./scripts/install.sh --tool aider --force
USAGE
}

is_valid_tool() {
  case "$1" in
    antigravity|cursor|aider|kilocode|windsurf|opencode|augment) return 0 ;;
    *) return 1 ;;
  esac
}

confirm_overwrite() {
  local prompt="$1"

  if $FORCE; then
    return 0
  fi

  printf "%s [y/N]: " "$prompt"
  read -r reply
  case "$reply" in
    y|Y|yes|YES) return 0 ;;
    *) return 1 ;;
  esac
}

safe_copy_dir_contents() {
  local src_dir="$1"
  local dst_dir="$2"

  mkdir -p "$dst_dir"
  cp -R "${src_dir}/." "$dst_dir/"
}

install_antigravity() {
  local src_root="${REPO_ROOT}/integrations/antigravity"
  local dst_root

  if [[ -n "$TARGET" ]]; then
    dst_root="$TARGET"
  else
    dst_root="${HOME}/.gemini/antigravity/skills"
  fi

  if [[ ! -d "$src_root" ]]; then
    err "Missing source directory: $src_root"
    err "Run ./scripts/convert.sh --tool antigravity first."
    exit 1
  fi

  mkdir -p "$dst_root"

  local count=0
  local skill_dir
  for skill_dir in "$src_root"/*; do
    if [[ ! -d "$skill_dir" ]]; then
      continue
    fi
    if [[ "$(basename "$skill_dir")" == "README.md" ]]; then
      continue
    fi

    local skill_name
    skill_name="$(basename "$skill_dir")"
    local dst_skill="${dst_root}/${skill_name}"

    if [[ -e "$dst_skill" ]]; then
      if ! confirm_overwrite "Overwrite existing ${dst_skill}?"; then
        warn "Skipped ${dst_skill}"
        continue
      fi
      rm -rf "$dst_skill"
    fi

    cp -R "$skill_dir" "$dst_skill"
    count=$((count + 1))
  done

  ok "Installed ${count} skill directories to ${dst_root}"
}

install_flat_rules_tool() {
  local tool="$1"
  local subdir="$2"
  local ext="$3"

  local src_dir="${REPO_ROOT}/integrations/${tool}/rules"
  local base_target="${TARGET:-$PWD}"
  local dst_dir="${base_target}/${subdir}"

  if [[ ! -d "$src_dir" ]]; then
    err "Missing source directory: $src_dir"
    err "Run ./scripts/convert.sh --tool ${tool} first."
    exit 1
  fi

  if [[ -d "$dst_dir" ]] && [[ "$(find "$dst_dir" -maxdepth 1 -type f -name "*${ext}" | wc -l | tr -d ' ')" -gt 0 ]]; then
    if ! confirm_overwrite "${dst_dir} already contains ${ext} files. Overwrite contents?"; then
      warn "Install cancelled for ${tool}"
      return
    fi
    rm -rf "$dst_dir"
  fi

  mkdir -p "$dst_dir"
  cp -R "${src_dir}/." "$dst_dir/"

  local count
  count="$(find "$dst_dir" -maxdepth 1 -type f -name "*${ext}" | wc -l | tr -d ' ')"
  ok "Installed ${count} files to ${dst_dir}"
}

install_aider() {
  local src_file="${REPO_ROOT}/integrations/aider/CONVENTIONS.md"
  local base_target="${TARGET:-$PWD}"
  local dst_file="${base_target}/CONVENTIONS.md"

  if [[ ! -f "$src_file" ]]; then
    err "Missing source file: $src_file"
    err "Run ./scripts/convert.sh --tool aider first."
    exit 1
  fi

  mkdir -p "$base_target"

  if [[ -f "$dst_file" ]]; then
    if ! confirm_overwrite "Overwrite existing ${dst_file}?"; then
      warn "Skipped ${dst_file}"
      return
    fi
  fi

  cp "$src_file" "$dst_file"
  ok "Installed ${dst_file}"
}

install_skill_bundle_tool() {
  local tool="$1"
  local src_dir="${REPO_ROOT}/integrations/${tool}/skills"
  local base_target="${TARGET:-$PWD}"
  local dst_dir="${base_target}/.${tool}/skills"

  if [[ ! -d "$src_dir" ]]; then
    err "Missing source directory: $src_dir"
    err "Run ./scripts/convert.sh --tool ${tool} first."
    exit 1
  fi

  if [[ -d "$dst_dir" ]] && [[ "$(find "$dst_dir" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')" -gt 0 ]]; then
    if ! confirm_overwrite "${dst_dir} already contains skills. Overwrite contents?"; then
      warn "Install cancelled for ${tool}"
      return
    fi
    rm -rf "$dst_dir"
  fi

  mkdir -p "$dst_dir"
  cp -R "${src_dir}/." "$dst_dir/"

  local count
  count="$(find "$dst_dir" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  ok "Installed ${count} skill directories to ${dst_dir}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      TOOL="${2:-}"
      shift 2
      ;;
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      err "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$TOOL" ]]; then
  err "--tool is required"
  usage
  exit 1
fi

if ! is_valid_tool "$TOOL"; then
  err "Invalid --tool value: ${TOOL}"
  usage
  exit 1
fi

case "$TOOL" in
  antigravity)
    install_antigravity
    ;;
  cursor)
    install_flat_rules_tool "cursor" ".cursor/rules" ".mdc"
    ;;
  aider)
    install_aider
    ;;
  kilocode)
    install_flat_rules_tool "kilocode" ".kilocode/rules" ".md"
    ;;
  windsurf)
    install_skill_bundle_tool "windsurf"
    ;;
  opencode)
    install_skill_bundle_tool "opencode"
    ;;
  augment)
    install_flat_rules_tool "augment" ".augment/rules" ".md"
    ;;
  *)
    err "Unhandled tool: ${TOOL}"
    exit 1
    ;;
esac

ok "Installation complete for ${TOOL}"
