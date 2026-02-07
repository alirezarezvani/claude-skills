#!/usr/bin/env python3
"""
Sync Codex Skills - Generate symlinks and index for OpenAI Codex compatibility.

This script scans all domain folders for SKILL.md files and creates:
1. Symlinks in .codex/skills/ directory
2. skills-index.json manifest for tooling

Usage:
    python scripts/sync-codex-skills.py [--dry-run] [--verbose]
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


# Skill domain configuration
SKILL_DOMAINS = {
    "marketing-skill": {
        "category": "marketing",
        "description": "Marketing, content, and demand generation skills"
    },
    "engineering-team": {
        "category": "engineering",
        "description": "Software engineering and technical skills"
    },
    "product-team": {
        "category": "product",
        "description": "Product management and design skills"
    },
    "c-level-advisor": {
        "category": "c-level",
        "description": "Executive leadership and advisory skills"
    },
    "project-management": {
        "category": "project-management",
        "description": "Project management and Atlassian skills"
    },
    "ra-qm-team": {
        "category": "ra-qm",
        "description": "Regulatory affairs and quality management skills"
    },
    "business-growth": {
        "category": "business-growth",
        "description": "Customer success, sales engineering, and revenue operations skills"
    },
    "finance": {
        "category": "finance",
        "description": "Financial analysis, valuation, and forecasting skills"
    }
}


def find_skills(repo_root: Path) -> List[Dict]:
    """
    Scan repository for all skills (folders containing SKILL.md).

    Returns list of skill dictionaries with metadata.
    """
    skills = []

    for domain_dir, domain_info in SKILL_DOMAINS.items():
        domain_path = repo_root / domain_dir

        if not domain_path.exists():
            continue

        # Find all subdirectories with SKILL.md
        for skill_path in domain_path.iterdir():
            if not skill_path.is_dir():
                continue

            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue

            # Extract skill name and description from SKILL.md
            skill_name = skill_path.name
            description = extract_skill_description(skill_md)

            # Calculate relative path from .codex/skills/ to skill folder
            relative_path = f"../../{domain_dir}/{skill_name}"

            skills.append({
                "name": skill_name,
                "source": relative_path,
                "source_absolute": str(skill_path.relative_to(repo_root)),
                "category": domain_info["category"],
                "description": description or f"Skill from {domain_dir}"
            })

    # Sort by category then name for consistent output
    skills.sort(key=lambda s: (s["category"], s["name"]))

    return skills


def extract_skill_description(skill_md_path: Path) -> Optional[str]:
    """
    Extract description from SKILL.md YAML frontmatter.

    Looks for:
    ---
    name: ...
    description: ...
    ---
    """
    try:
        content = skill_md_path.read_text(encoding="utf-8")

        # Check for YAML frontmatter
        if not content.startswith("---"):
            return None

        # Find end of frontmatter
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return None

        frontmatter = content[3:end_idx]

        # Simple extraction without YAML parser dependency
        for line in frontmatter.split("\n"):
            line = line.strip()
            if line.startswith("description:"):
                desc = line[len("description:"):].strip()
                # Remove quotes if present
                if desc.startswith('"') and desc.endswith('"'):
                    desc = desc[1:-1]
                elif desc.startswith("'") and desc.endswith("'"):
                    desc = desc[1:-1]
                return desc

        return None

    except Exception:
        return None


def create_symlinks(repo_root: Path, skills: List[Dict], dry_run: bool = False, verbose: bool = False) -> Dict:
    """
    Create symlinks in .codex/skills/ directory.

    Returns summary of operations.
    """
    codex_skills_dir = repo_root / ".codex" / "skills"

    created = []
    updated = []
    unchanged = []
    errors = []

    if not dry_run:
        codex_skills_dir.mkdir(parents=True, exist_ok=True)

    for skill in skills:
        symlink_path = codex_skills_dir / skill["name"]
        target = skill["source"]

        try:
            if symlink_path.is_symlink():
                current_target = os.readlink(symlink_path)
                if current_target == target:
                    unchanged.append(skill["name"])
                    if verbose:
                        print(f"  [UNCHANGED] {skill['name']} -> {target}")
                else:
                    if not dry_run:
                        symlink_path.unlink()
                        symlink_path.symlink_to(target)
                    updated.append(skill["name"])
                    if verbose:
                        print(f"  [UPDATED] {skill['name']} -> {target} (was: {current_target})")
            elif symlink_path.exists():
                errors.append(f"{skill['name']}: path exists but is not a symlink")
                if verbose:
                    print(f"  [ERROR] {skill['name']}: path exists but is not a symlink")
            else:
                if not dry_run:
                    symlink_path.symlink_to(target)
                created.append(skill["name"])
                if verbose:
                    print(f"  [CREATED] {skill['name']} -> {target}")

        except Exception as e:
            errors.append(f"{skill['name']}: {str(e)}")
            if verbose:
                print(f"  [ERROR] {skill['name']}: {str(e)}")

    return {
        "created": created,
        "updated": updated,
        "unchanged": unchanged,
        "errors": errors
    }


def generate_skills_index(repo_root: Path, skills: List[Dict], dry_run: bool = False) -> Dict:
    """
    Generate .codex/skills-index.json manifest.

    Returns the index data.
    """
    # Calculate category counts
    categories = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            # Find domain info
            for domain_dir, domain_info in SKILL_DOMAINS.items():
                if domain_info["category"] == cat:
                    categories[cat] = {
                        "count": 0,
                        "source": f"../../{domain_dir}",
                        "description": domain_info["description"]
                    }
                    break
        if cat in categories:
            categories[cat]["count"] += 1

    # Build index
    index = {
        "version": "1.0.0",
        "name": "claude-code-skills",
        "description": "Production-ready skill packages for AI agents - Marketing, Engineering, Product, C-Level, PM, and RA/QM",
        "repository": "https://github.com/alirezarezvani/claude-skills",
        "total_skills": len(skills),
        "skills": [
            {
                "name": s["name"],
                "source": s["source"],
                "category": s["category"],
                "description": s["description"]
            }
            for s in skills
        ],
        "categories": categories
    }

    if not dry_run:
        index_path = repo_root / ".codex" / "skills-index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    return index


def validate_symlinks(repo_root: Path, skills: List[Dict]) -> List[str]:
    """
    Validate that all symlinks resolve to valid SKILL.md files.

    Returns list of broken symlinks.
    """
    broken = []
    codex_skills_dir = repo_root / ".codex" / "skills"

    for skill in skills:
        symlink_path = codex_skills_dir / skill["name"]

        if not symlink_path.exists():
            broken.append(f"{skill['name']}: symlink does not exist")
            continue

        skill_md = symlink_path / "SKILL.md"
        if not skill_md.exists():
            broken.append(f"{skill['name']}: SKILL.md not found through symlink")

    return broken


def main():
    parser = argparse.ArgumentParser(
        description="Sync Codex skills symlinks and generate index"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate symlinks after sync"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Find repository root (where this script lives in scripts/)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    if args.verbose and not args.json:
        print(f"Repository root: {repo_root}")
        print(f"Scanning for skills...")

    # Find all skills
    skills = find_skills(repo_root)

    if not skills:
        if args.json:
            print(json.dumps({"error": "No skills found"}, indent=2))
        else:
            print("No skills found in repository")
        sys.exit(1)

    if args.verbose and not args.json:
        print(f"Found {len(skills)} skills across {len(set(s['category'] for s in skills))} categories")
        print()

    # Create symlinks
    if not args.json:
        mode = "[DRY RUN] " if args.dry_run else ""
        print(f"{mode}Creating symlinks in .codex/skills/...")

    symlink_results = create_symlinks(repo_root, skills, args.dry_run, args.verbose)

    # Generate index
    if not args.json:
        print(f"{mode}Generating .codex/skills-index.json...")

    index = generate_skills_index(repo_root, skills, args.dry_run)

    # Validate if requested
    validation_errors = []
    if args.validate and not args.dry_run:
        if not args.json:
            print("Validating symlinks...")
        validation_errors = validate_symlinks(repo_root, skills)

    # Output results
    if args.json:
        output = {
            "dry_run": args.dry_run,
            "total_skills": len(skills),
            "symlinks": symlink_results,
            "index_generated": not args.dry_run,
            "validation_errors": validation_errors if args.validate else None
        }
        print(json.dumps(output, indent=2))
    else:
        print()
        print("=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"Total skills: {len(skills)}")
        print(f"Symlinks created: {len(symlink_results['created'])}")
        print(f"Symlinks updated: {len(symlink_results['updated'])}")
        print(f"Symlinks unchanged: {len(symlink_results['unchanged'])}")

        if symlink_results['errors']:
            print(f"Errors: {len(symlink_results['errors'])}")
            for err in symlink_results['errors']:
                print(f"  - {err}")

        if validation_errors:
            print(f"Validation errors: {len(validation_errors)}")
            for err in validation_errors:
                print(f"  - {err}")

        print()
        print("Categories:")
        for cat, info in index["categories"].items():
            print(f"  {cat}: {info['count']} skills")

        if args.dry_run:
            print()
            print("No changes made (dry run mode)")
        else:
            print()
            print(f"Index written to: .codex/skills-index.json")
            print(f"Symlinks created in: .codex/skills/")

    # Exit with error if there were issues
    if symlink_results['errors'] or validation_errors:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
