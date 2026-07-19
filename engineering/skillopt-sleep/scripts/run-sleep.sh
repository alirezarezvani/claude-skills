#!/usr/bin/env bash
# SkillOpt-Sleep shared runner — used by all platform plugins (Claude Code,
# Codex, Copilot). Resolves the repo root (which contains the skillopt_sleep
# package), picks a Python >= 3.10, and execs the engine CLI.
#
# Usage: run-sleep.sh <run|dry-run|status|adopt|harvest|...> [args...]
set -euo pipefail

# In this vendored copy this script lives at
# <plugin-root>/scripts/run-sleep.sh (engineering/skillopt-sleep/scripts/ in
# alirezarezvani/claude-skills), so the plugin root (which holds
# skillopt_sleep/) is one level up — that's what the first branch below
# checks. CLAUDE_PLUGIN_ROOT (set by Claude Code when it invokes a plugin
# script) points directly at that same plugin root in this layout, so
# skillopt_sleep/ sits directly inside it, not two levels up as it would in
# upstream's <repo>/plugins/claude-code/ layout — both are checked so this
# script stays portable if it's ever reused in that shape again.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "$SCRIPT_DIR/../skillopt_sleep" ]; then
  REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -d "$CLAUDE_PLUGIN_ROOT/skillopt_sleep" ]; then
  REPO_ROOT="$CLAUDE_PLUGIN_ROOT"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -d "$CLAUDE_PLUGIN_ROOT/../../skillopt_sleep" ]; then
  REPO_ROOT="$(cd "$CLAUDE_PLUGIN_ROOT/../.." && pwd)"
elif [ -n "${SKILLOPT_SLEEP_REPO:-}" ] && [ -d "$SKILLOPT_SLEEP_REPO/skillopt_sleep" ]; then
  REPO_ROOT="$SKILLOPT_SLEEP_REPO"
else
  # last resort: search upward from CWD
  d="$PWD"
  while [ "$d" != "/" ]; do
    [ -d "$d/skillopt_sleep" ] && { REPO_ROOT="$d"; break; }
    d="$(dirname "$d")"
  done
fi
if [ -z "${REPO_ROOT:-}" ]; then
  echo "[sleep] ERROR: could not locate the skillopt_sleep package. Set SKILLOPT_SLEEP_REPO to the repo root." >&2
  exit 1
fi

PY=""
# Allow explicit Python override (useful on macOS with old system Python).
if [ -n "${SKILLOPT_SLEEP_PYTHON:-}" ]; then
  PY="$SKILLOPT_SLEEP_PYTHON"
else
  for cand in python3.12 python3.11 python3.10 python3; do
    if command -v "$cand" >/dev/null 2>&1; then
      ver="$("$cand" -c 'import sys; print("%d%d" % sys.version_info[:2])' 2>/dev/null || echo 0)"
      if [ "${ver:-0}" -ge 310 ]; then PY="$cand"; break; fi
    fi
  done
fi
if [ -z "$PY" ]; then
  echo "[sleep] ERROR: need Python >= 3.10 (found none)." >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then set -- status; fi
cd "$REPO_ROOT"
exec "$PY" -m skillopt_sleep "$@"
