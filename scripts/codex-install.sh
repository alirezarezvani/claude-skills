#!/bin/bash
#
# Codex Installation Script for Claude Skills Library
#
# Installs skills from this repository to your local Codex skills directory.
# Follows symlinks to copy actual skill contents.
#
# Usage:
#   ./scripts/codex-install.sh [--all | --category <name> | --skill <name>]
#
# Options:
#   --all             Install all skills (default)
#   --category <name> Install skills from a specific category
#   --skill <name>    Install a single skill by name
#   --list            List available skills and categories
#   --dry-run         Show what would be installed without making changes
#   --help            Show this help message
#
# Examples:
#   ./scripts/codex-install.sh                    # Install all skills
#   ./scripts/codex-install.sh --category marketing
#   ./scripts/codex-install.sh --skill content-creator
#   ./scripts/codex-install.sh --list
#

set -e

# Configuration
CODEX_SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
CODEX_SKILLS_SRC="$REPO_ROOT/.codex/skills"
CODEX_INDEX="$REPO_ROOT/.codex/skills-index.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show help
show_help() {
    head -35 "$0" | tail -30
    exit 0
}

# Check prerequisites
check_prerequisites() {
    if [[ ! -d "$CODEX_SKILLS_SRC" ]]; then
        print_error "Codex skills directory not found: $CODEX_SKILLS_SRC"
        print_info "Run 'python scripts/sync-codex-skills.py' first to generate symlinks."
        exit 1
    fi

    if [[ ! -f "$CODEX_INDEX" ]]; then
        print_warning "skills-index.json not found. Some features may be limited."
    fi
}

# List available skills
list_skills() {
    print_info "Available skills in $CODEX_SKILLS_SRC:"
    echo ""

    if [[ -f "$CODEX_INDEX" ]] && command -v python3 &> /dev/null; then
        # Use Python to parse JSON and display nicely
        python3 << 'EOF'
import json
import sys

try:
    with open('$CODEX_INDEX'.replace('$CODEX_INDEX', '''$CODEX_INDEX'''), 'r') as f:
        index = json.load(f)

    print("Categories:")
    print("-" * 50)
    for cat, info in index.get('categories', {}).items():
        print(f"  {cat}: {info['count']} skills")

    print()
    print("Skills by category:")
    print("-" * 50)

    current_cat = None
    for skill in index.get('skills', []):
        if skill['category'] != current_cat:
            current_cat = skill['category']
            print(f"\n  [{current_cat}]")
        print(f"    - {skill['name']}: {skill['description'][:60]}...")

except Exception as e:
    print(f"Error parsing index: {e}")
    sys.exit(1)
EOF
    else
        # Fallback to simple listing
        for skill in "$CODEX_SKILLS_SRC"/*; do
            if [[ -L "$skill" ]] && [[ -e "$skill/SKILL.md" ]]; then
                echo "  - $(basename "$skill")"
            fi
        done
    fi

    exit 0
}

# Install a single skill
install_skill() {
    local skill_name="$1"
    local dry_run="$2"
    local skill_src="$CODEX_SKILLS_SRC/$skill_name"
    local skill_dest="$CODEX_SKILLS_DIR/$skill_name"

    # Check if skill exists
    if [[ ! -e "$skill_src" ]]; then
        print_error "Skill not found: $skill_name"
        return 1
    fi

    # Check if it's a valid skill (has SKILL.md)
    if [[ ! -e "$skill_src/SKILL.md" ]]; then
        print_error "Invalid skill (no SKILL.md): $skill_name"
        return 1
    fi

    if [[ "$dry_run" == "true" ]]; then
        print_info "[DRY RUN] Would install: $skill_name -> $skill_dest"
        return 0
    fi

    # Create destination directory
    mkdir -p "$CODEX_SKILLS_DIR"

    # Remove existing installation
    if [[ -e "$skill_dest" ]]; then
        print_info "Updating existing skill: $skill_name"
        rm -rf "$skill_dest"
    fi

    # Copy skill (following symlinks with -L)
    cp -rL "$skill_src" "$skill_dest"

    print_success "Installed: $skill_name"
    return 0
}

# Install skills by category
install_category() {
    local category="$1"
    local dry_run="$2"
    local installed=0
    local failed=0

    if [[ ! -f "$CODEX_INDEX" ]]; then
        print_error "skills-index.json required for category installation"
        exit 1
    fi

    print_info "Installing skills from category: $category"

    # Get skills for this category from index
    local skills
    skills=$(python3 -c "
import json
with open('$CODEX_INDEX', 'r') as f:
    index = json.load(f)
for skill in index.get('skills', []):
    if skill['category'] == '$category':
        print(skill['name'])
")

    if [[ -z "$skills" ]]; then
        print_error "No skills found for category: $category"
        exit 1
    fi

    while IFS= read -r skill; do
        if install_skill "$skill" "$dry_run"; then
            ((installed++))
        else
            ((failed++))
        fi
    done <<< "$skills"

    echo ""
    print_info "Category '$category' complete: $installed installed, $failed failed"
}

# Install all skills
install_all() {
    local dry_run="$1"
    local installed=0
    local failed=0

    print_info "Installing all skills to: $CODEX_SKILLS_DIR"
    echo ""

    for skill in "$CODEX_SKILLS_SRC"/*; do
        if [[ -L "$skill" ]] || [[ -d "$skill" ]]; then
            local skill_name
            skill_name=$(basename "$skill")

            if install_skill "$skill_name" "$dry_run"; then
                ((installed++))
            else
                ((failed++))
            fi
        fi
    done

    echo ""
    print_info "Installation complete: $installed installed, $failed failed"

    if [[ "$dry_run" != "true" ]]; then
        echo ""
        print_success "Skills installed to: $CODEX_SKILLS_DIR"
        print_info "Verify with: ls $CODEX_SKILLS_DIR"
    fi
}

# Main
main() {
    local mode="all"
    local target=""
    local dry_run="false"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                mode="all"
                shift
                ;;
            --category)
                mode="category"
                target="$2"
                shift 2
                ;;
            --skill)
                mode="skill"
                target="$2"
                shift 2
                ;;
            --list)
                mode="list"
                shift
                ;;
            --dry-run)
                dry_run="true"
                shift
                ;;
            --help|-h)
                show_help
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                ;;
        esac
    done

    # Banner
    echo ""
    echo "========================================"
    echo "  Claude Skills - Codex Installer"
    echo "========================================"
    echo ""

    check_prerequisites

    case $mode in
        list)
            list_skills
            ;;
        skill)
            if [[ -z "$target" ]]; then
                print_error "Skill name required"
                exit 1
            fi
            install_skill "$target" "$dry_run"
            ;;
        category)
            if [[ -z "$target" ]]; then
                print_error "Category name required"
                exit 1
            fi
            install_category "$target" "$dry_run"
            ;;
        all)
            install_all "$dry_run"
            ;;
    esac
}

main "$@"
