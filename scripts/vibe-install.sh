#!/bin/bash
#
# Mistral Vibe Installation Script for Claude Skills Library
#
# Syncs all skills into ~/.vibe/skills/claude-skills/ for discovery by
# Mistral Vibe (https://github.com/mistralai/mistral-vibe). Uses the
# agentskills.io SKILL.md standard — no format conversion needed.
#
# Usage:
#   ./scripts/vibe-install.sh [--dry-run] [--verbose] [--domain engineering] [--copy]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
VIBE_SYNC_SCRIPT="$SCRIPT_DIR/sync-vibe-skills.py"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

echo ""
echo "========================================"
echo "  Claude Skills - Mistral Vibe Setup"
echo "========================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required for this setup."
    exit 1
fi

print_info "Synchronizing skills for Mistral Vibe..."
python3 "$VIBE_SYNC_SCRIPT" "$@"

echo ""
print_success "Mistral Vibe setup complete!"
echo ""
echo "How to use these skills in Mistral Vibe:"
echo "----------------------------------------"
echo "1. List available skills inside Vibe:"
echo "   > /skills"
echo ""
echo "2. Invoke a skill by name:"
echo "   > /senior-architect"
echo ""
echo "3. Or describe a task — Vibe will auto-load matching skills via the"
echo "   description field in each SKILL.md frontmatter."
echo ""
echo "Skills install to ~/.vibe/skills/claude-skills/ as symlinks back to"
echo "this repo (or copies, if you passed --copy)."
echo ""
print_info "Docs: https://docs.mistral.ai/mistral-vibe/agents-skills"
echo ""
