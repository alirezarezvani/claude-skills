#!/usr/bin/env bash
# Install claude-skills into OpenClaw's workspace skills directory
# Usage: ./scripts/openclaw-install.sh [--dry-run]

set -euo pipefail

SKILLS_DIR="${HOME}/.openclaw/workspace/skills"
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DRY_RUN=false

[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

# Find all SKILL.md files and install each skill
installed=0
skipped=0

while IFS= read -r skill_md; do
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  target="${SKILLS_DIR}/${skill_name}"

  if [[ -e "$target" ]]; then
    skipped=$((skipped + 1))
    continue
  fi

  if $DRY_RUN; then
    echo "  [dry-run] would install: $skill_name"
  else
    mkdir -p "$SKILLS_DIR"
    ln -sf "$skill_dir" "$target"
    echo "  ✅ installed: $skill_name"
  fi
  installed=$((installed + 1))
done < <(find "$REPO_DIR" -name "SKILL.md" -not -path "*/.git/*")

if $DRY_RUN; then
  echo ""
  echo "Dry run complete. Would install $installed skill(s). ($skipped already exist)"
else
  echo ""
  echo "Done. Installed $installed skill(s). ($skipped already existed)"
  echo "Restart OpenClaw (openclaw gateway restart) to pick up new skills."
fi
