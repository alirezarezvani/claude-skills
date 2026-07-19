#!/usr/bin/env bash
# Claude Code plugin runner — thin wrapper over the shared runner so all
# platform plugins share one engine launcher.
#
# In this vendored copy, sleep.sh/run-sleep.sh/install-cron.sh live together
# in <plugin-root>/scripts/, and the engine package lives at
# <plugin-root>/skillopt_sleep/ (i.e. engineering/skillopt-sleep/ in
# alirezarezvani/claude-skills). After marketplace install the plugin is
# isolated in a cache directory, but that same relative layout is preserved,
# so the repo-relative path still resolves. We try four locations:
#   1. Co-located run-sleep.sh (bundled copy — works in marketplace cache)
#   2. Repo-relative ../../run-sleep.sh (dev checkout; harmless no-op here
#      since (1) always resolves first for this vendored layout)
#   3. CLAUDE_PLUGIN_ROOT/../run-sleep.sh (plugin env variable; also a no-op
#      here for the same reason)
#   4. SKILLOPT_SLEEP_REPO/scripts/run-sleep.sh (explicit env, pointed at
#      this plugin's root — the escape hatch if (1)-(3) somehow all miss)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SHARED=""
if [ -f "$HERE/run-sleep.sh" ]; then
  SHARED="$HERE/run-sleep.sh"
elif [ -f "$(cd "$HERE/../.." 2>/dev/null && pwd)/run-sleep.sh" ]; then
  SHARED="$(cd "$HERE/../.." && pwd)/run-sleep.sh"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -f "$(cd "$CLAUDE_PLUGIN_ROOT/.." 2>/dev/null && pwd)/run-sleep.sh" ]; then
  SHARED="$(cd "$CLAUDE_PLUGIN_ROOT/.." && pwd)/run-sleep.sh"
elif [ -n "${SKILLOPT_SLEEP_REPO:-}" ] && [ -f "$SKILLOPT_SLEEP_REPO/scripts/run-sleep.sh" ]; then
  SHARED="$SKILLOPT_SLEEP_REPO/scripts/run-sleep.sh"
fi

if [ -z "$SHARED" ]; then
  echo "[sleep] ERROR: cannot locate run-sleep.sh." >&2
  echo "[sleep] Set SKILLOPT_SLEEP_REPO to the SkillOpt repo root, or pip install skillopt." >&2
  exit 1
fi
exec bash "$SHARED" "$@"
