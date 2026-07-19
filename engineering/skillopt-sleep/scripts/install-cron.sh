#!/usr/bin/env bash
# Print (does NOT install) a crontab line that runs SkillOpt-Sleep nightly.
# The user copies the line into `crontab -e` if they want it.
set -euo pipefail

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
RUNNER="$PLUGIN_ROOT/scripts/sleep.sh"
PROJECT="${1:-$(pwd)}"
BACKEND="${2:-mock}"

# 3:17am local — deliberately off the :00 mark so many users don't all hit the
# API at once (and we leave room for jitter).
MIN=17
HOUR=3

cat <<EOF
# ── SkillOpt-Sleep nightly cycle ────────────────────────────────────────────
# Review past sessions, replay tasks, stage validated memory/skill updates.
# Runs at ${HOUR}:$(printf '%02d' $MIN) local every day. Output goes to the project's
# .skillopt-sleep/ dir; nothing live is changed until you run '/skillopt-sleep adopt'
# (unless you pass --auto-adopt below).
#
# Copy the next line into 'crontab -e':
${MIN} ${HOUR} * * *  "${RUNNER}" run --project "${PROJECT}" --scope invoked --backend "${BACKEND}" >> "${PROJECT}/.skillopt-sleep/cron.log" 2>&1
#
# For fully-autonomous adoption (power users), append: --auto-adopt
# To spend real API budget for genuine lift, set BACKEND=anthropic above.
# ────────────────────────────────────────────────────────────────────────────
EOF
