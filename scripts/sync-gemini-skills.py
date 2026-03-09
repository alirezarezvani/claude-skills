#!/usr/bin/env python3
"""
Sync Gemini Skills - Generate symlinks and index for Gemini CLI compatibility.

This script scans the entire repository for SKILL.md files and creates:
1. Symlinks in .gemini/skills/ directory
2. skills-index.json manifest for tooling

Usage:
    python scripts/sync-gemini-skills.py [--dry-run] [--verbose]
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


# Domain mapping for categories based on top-level folder
DOMAIN_MAP = {
    "marketing-skill": "marketing",
    "engineering-team": "engineering",
    "engineering": "engineering-advanced",
    "product-team": "product",
    "c-level-advisor": "c-level",
    "project-management": "project-management",
    "ra-qm-team": "ra-qm",
    "business-growth": "business-growth",
    "finance": "finance"
}


def find_skills(repo_root: Path) -> List[Dict]:
    """
    Scan repository for all skills (SKILL.md files).
    """
    skills = []
    seen_names = set()

    # 1. Find all SKILL.md files recursively
    for skill_md in repo_root.rglob("SKILL.md"):
        # Skip internal .gemini directory
        if ".gemini" in skill_md.parts:
            continue
        
        # Skip evaluation workspaces, assets, and gitignored directories
        if "eval-workspace" in skill_md.parts or "assets" in skill_md.parts or "evals" in skill_md.parts:
            if "sample-skill" not in skill_md.parts: # Keep sample if it's for testing
                continue

        # Skip directories not in DOMAIN_MAP (e.g. gitignored local folders)
        top_level = skill_md.relative_to(repo_root).parts[0]
        if top_level not in DOMAIN_MAP and top_level not in ("agents", "commands"):
            continue

        skill_dir = skill_md.parent
        
        # Determine skill name
        if skill_dir == repo_root:
            continue # Root SKILL.md (unlikely)
            
        # For domain-level SKILL.md, name it after the domain
        if skill_dir.name in DOMAIN_MAP:
            skill_name = f"{skill_dir.name}-bundle"
        else:
            skill_name = skill_dir.name

        # Handle duplicates by appending parent name
        if skill_name in seen_names:
            skill_name = f"{skill_dir.parent.name}-{skill_name}"
        
        seen_names.add(skill_name)
        
        # Determine category based on top-level folder
        category = "general"
        for folder, cat in DOMAIN_MAP.items():
            if folder in skill_md.parts:
                category = cat
                break

        description = extract_skill_description(skill_md)
        
        # Calculate relative path (3 levels up from .gemini/skills/{name}/SKILL.md)
        rel_path = skill_md.relative_to(repo_root)
        source_path = "../../../" + str(rel_path)

        skills.append({
            "name": skill_name,
            "source": source_path,
            "category": category,
            "description": description or f"Skill from {rel_path.parent}"
        })

    # 2. Agents as Skills
    agents_path = repo_root / "agents"
    if agents_path.exists():
        for agent_file in agents_path.rglob("*.md"):
            if agent_file.name == "CLAUDE.md" or ".gemini" in agent_file.parts:
                continue
            
            agent_name = agent_file.stem
            if agent_name in seen_names:
                agent_name = f"agent-{agent_name}"
            seen_names.add(agent_name)
            
            description = extract_skill_description(agent_file)
            rel_path = agent_file.relative_to(repo_root)
            source_path = "../../../" + str(rel_path)
            
            skills.append({
                "name": agent_name,
                "source": source_path,
                "category": "agent",
                "description": description or f"Agent from {agent_file.parent.name}"
            })

    # 3. Commands as Skills
    commands_path = repo_root / "commands"
    if commands_path.exists():
        for cmd_file in commands_path.glob("*.md"):
            if cmd_file.name == ".gitkeep":
                continue
            
            cmd_name = cmd_file.stem
            if cmd_name in seen_names:
                cmd_name = f"cmd-{cmd_name}"
            seen_names.add(cmd_name)
            
            description = extract_skill_description(cmd_file)
            rel_path = cmd_file.relative_to(repo_root)
            source_path = "../../../" + str(rel_path)
            
            skills.append({
                "name": cmd_name,
                "source": source_path,
                "category": "command",
                "description": description or "Custom slash command"
            })

    skills.sort(key=lambda s: (s["category"], s["name"]))
    return skills


def extract_skill_description(skill_md_path: Path) -> Optional[str]:
    """
    Extract description from YAML frontmatter.
    """
    try:
        content = skill_md_path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return None
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return None
        frontmatter = content[3:end_idx]
        for line in frontmatter.split("\n"):
            line = line.strip()
            if line.startswith("description:"):
                desc = line[len("description:"):].strip()
                if (desc.startswith('"') and desc.endswith('"')) or (desc.startswith("'") and desc.endswith("'")):
                    desc = desc[1:-1]
                return desc
        return None
    except Exception:
        return None


def create_symlinks(repo_root: Path, skills: List[Dict], dry_run: bool = False, verbose: bool = False) -> Dict:
    """
    Create symlinks in .gemini/skills/ directory.
    """
    gemini_skills_dir = repo_root / ".gemini" / "skills"
    
    # Optional: Clean existing skills to remove stale ones
    # if not dry_run and gemini_skills_dir.exists():
    #     import shutil
    #     shutil.rmtree(gemini_skills_dir)

    created, updated, unchanged, errors = [], [], [], []

    if not dry_run:
        gemini_skills_dir.mkdir(parents=True, exist_ok=True)

    for skill in skills:
        skill_name = skill["name"]
        skill_dest_dir = gemini_skills_dir / skill_name
        
        if not dry_run:
            skill_dest_dir.mkdir(exist_ok=True)
            
        symlink_path = skill_dest_dir / "SKILL.md"
        target = skill["source"]

        try:
            if symlink_path.is_symlink():
                current_target = os.readlink(symlink_path)
                if current_target == target:
                    unchanged.append(skill_name)
                else:
                    if not dry_run:
                        symlink_path.unlink()
                        symlink_path.symlink_to(target)
                    updated.append(skill_name)
            elif symlink_path.exists():
                errors.append(f"{skill_name}: path exists but is not a symlink")
            else:
                if not dry_run:
                    symlink_path.symlink_to(target)
                created.append(skill_name)
        except Exception as e:
            errors.append(f"{skill_name}: {str(e)}")

    return {"created": created, "updated": updated, "unchanged": unchanged, "errors": errors}


def generate_skills_index(repo_root: Path, skills: List[Dict], dry_run: bool = False) -> Dict:
    """
    Generate .gemini/skills-index.json manifest.
    """
    categories = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "description": f"{cat.capitalize()} resources"}
        categories[cat]["count"] += 1

    index = {
        "version": "1.0.0",
        "name": "gemini-cli-skills",
        "total_skills": len(skills),
        "skills": [{"name": s["name"], "category": s["category"], "description": s["description"]} for s in skills],
        "categories": categories
    }

    if not dry_run:
        index_path = repo_root / ".gemini" / "skills-index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    return index


def main():
    parser = argparse.ArgumentParser(description="Sync Gemini skills")
    parser.add_argument("--dry-run", "-n", action="store_true")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    skills = find_skills(repo_root)
    
    if not skills:
        print("No skills found.")
        sys.exit(1)

    symlink_results = create_symlinks(repo_root, skills, args.dry_run, args.verbose)
    generate_skills_index(repo_root, skills, args.dry_run)

    print(f"Total items synced for Gemini CLI: {len(skills)}")
    print(f"Created: {len(symlink_results['created'])}")
    print(f"Updated: {len(symlink_results['updated'])}")
    print(f"Unchanged: {len(symlink_results['unchanged'])}")

    if symlink_results['errors']:
        print(f"Errors: {len(symlink_results['errors'])}")

if __name__ == "__main__":
    main()
