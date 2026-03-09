#!/bin/bash
#
# Gemini CLI Installation Script for Claude Skills Library
#
# Sets up the workspace for Gemini CLI by generating symlinks and an index.
#
# Usage:
#   ./scripts/gemini-install.sh [--dry-run]
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
GEMINI_SYNC_SCRIPT="$SCRIPT_DIR/sync-gemini-skills.py"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Banner
echo ""
echo "========================================"
echo "  Claude Skills - Gemini CLI Setup"
echo "========================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required for this setup."
    exit 1
fi

# Run the sync script
print_info "Synchronizing skills for Gemini CLI..."
python3 "$GEMINI_SYNC_SCRIPT" "$@"

# Post-installation instructions
echo ""
print_success "Gemini CLI setup complete!"
echo ""
echo "How to use these skills in Gemini CLI:"
echo "--------------------------------------"
echo "1. Activate any skill by name:"
echo "   > activate_skill(name=\"senior-architect\")"
echo ""
echo "2. Activate an agent persona:"
echo "   > activate_skill(name=\"cs-engineering-lead\")"
echo ""
echo "3. Run a custom command:"
echo "   > activate_skill(name=\"tdd\")"
echo ""
echo "The skills are indexed in .gemini/skills/ for discovery."
echo "Each skill folder contains its own SKILL.md instructions."
echo ""
print_info "Read GEMINI.md in the root for more details."
echo ""
