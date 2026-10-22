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
    "finance": "finance",
    "productivity": "productivity",
    "marketing": "marketing-top-level",
    "research": "research",
    "business-operations": "business-operations",
    "commercial": "commercial",
    "research-ops": "research-ops",
    "compliance-os": "compliance-os",
    "markdown-html": "markdown-html",
    "agent-launcher": "agent-launcher",
    "c-level-agents": "c-level-agents",
    "loop-library": "loop-library"
}


# Path components that never hold a real skill: fixtures, eval outputs, and
# vendored copies (c-level-agents/vendor/ re-exports skills listed elsewhere).
SKIP_PARTS = {".gemini", "assets", "eval-workspace", "evals", "vendor", "node_modules"}


def find_skills(repo_root: Path) -> List[Dict]:
    """
    Scan repository for all skills (SKILL.md files).

    Each skill directory is linked whole, so its scripts/ and references/ sit
    beside its SKILL.md. Gemini identifies a skill by its frontmatter name, so a
    dual-published skill (bundled + standalone copies with identical SKILL.md)
    is listed once, and commands or agents that share a skill's name are
    dropped rather than reported by Gemini as conflicts.
    """
    skills = []
    seen_names = set()
    fm_seen: Dict[str, bytes] = {}

    # 1. Find all SKILL.md files. Sorted, shortest path first, so the bundled
    # copy (<domain>/skills/<name>) wins over the standalone plugin copy and
    # repeated runs produce the same mirror.
    found = sorted(repo_root.rglob("SKILL.md"),
                   key=lambda p: (len(p.relative_to(repo_root).parts), str(p)))
    for skill_md in found:
        rel_parts = skill_md.relative_to(repo_root).parts
        if SKIP_PARTS.intersection(rel_parts):
            continue

        # Skip directories not in DOMAIN_MAP (e.g. gitignored local folders)
        top_level = rel_parts[0]
        if top_level not in DOMAIN_MAP:
            continue

        skill_dir = skill_md.parent
        fm_name = extract_frontmatter_field(skill_md, "name") or skill_dir.name
        body = skill_md.read_bytes()
        if fm_name in fm_seen:
            if fm_seen[fm_name] == body:
                continue  # dual-published copy of a skill already listed
            print(f"warning: two different skills are named '{fm_name}'; Gemini will load only one "
                  f"({skill_md.relative_to(repo_root)})", file=sys.stderr)
        fm_seen[fm_name] = body

        # For domain-level SKILL.md, name it after the domain
        if skill_dir.name in DOMAIN_MAP and skill_dir.parent == repo_root:
            skill_name = f"{skill_dir.name}-bundle"
        else:
            skill_name = skill_dir.name

        # Directory names must be unique even when frontmatter names differ.
        if skill_name in seen_names:
            candidate = f"{skill_dir.parent.name}-{skill_name}"
            n = 2
            base = candidate
            while candidate in seen_names:
                candidate = f"{base}-{n}"
                n += 1
            skill_name = candidate

        seen_names.add(skill_name)

        # Determine category based on top-level folder
        category = DOMAIN_MAP.get(top_level, "general")

        description = extract_skill_description(skill_md)

        # .gemini/skills/<name> -> ../../<skill dir>
        rel_dir = skill_dir.relative_to(repo_root)
        skills.append({
            "name": skill_name,
            "source": "../../" + str(rel_dir),
            "link": "dir",
            "category": category,
            "description": description or f"Skill from {rel_dir}"
        })

    # 2. Agents as Skills
    agents_path = repo_root / "agents"
    if agents_path.exists():
        for agent_file in agents_path.rglob("*.md"):
            # README/TEMPLATE are docs, not agents; mirroring them shipped frontmatter-less "skills" (#1001).
            if agent_file.name in {"CLAUDE.md", "README.md", "TEMPLATE.md"} or ".gemini" in agent_file.parts:
                continue
            
            agent_name = agent_file.stem
            agent_fm = extract_frontmatter_field(agent_file, "name") or agent_name
            if agent_fm in fm_seen:
                continue
            fm_seen[agent_fm] = b""
            if agent_name in seen_names:
                agent_name = f"agent-{agent_name}"
            seen_names.add(agent_name)
            
            description = extract_skill_description(agent_file)
            rel_path = agent_file.relative_to(repo_root)
            source_path = "../../../" + str(rel_path)
            
            skills.append({
                "name": agent_name,
                "source": source_path,
                "link": "file",
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
            if (extract_frontmatter_field(cmd_file, "name") or cmd_name) in fm_seen:
                continue  # a skill already answers to this name
            if cmd_name in seen_names:
                cmd_name = f"cmd-{cmd_name}"
            seen_names.add(cmd_name)
            
            description = extract_skill_description(cmd_file)
            rel_path = cmd_file.relative_to(repo_root)
            source_path = "../../../" + str(rel_path)
            
            skills.append({
                "name": cmd_name,
                "source": source_path,
                "link": "file",
                "category": "command",
                "description": description or "Custom slash command"
            })

    skills.sort(key=lambda s: (s["category"], s["name"]))
    return skills


def extract_frontmatter_field(path: Path, field: str) -> Optional[str]:
    """Return a single-line frontmatter value, unquoted, or None."""
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    if not content.startswith("---"):
        return None
    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return None
    for line in content[3:end_idx].split("\n"):
        if line.startswith(f"{field}:"):
            val = line[len(field) + 1:].strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            return val or None
    return None


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


def _is_generated(entry: Path) -> bool:
    """True for mirror entries this script made: a symlink, or a directory
    holding nothing but symlinks (the old one-file-per-skill layout)."""
    if entry.is_symlink():
        return True
    return entry.is_dir() and all(c.is_symlink() for c in entry.iterdir())


def _remove(entry: Path) -> None:
    if entry.is_symlink() or entry.is_file():
        entry.unlink()
    else:
        for c in entry.iterdir():
            c.unlink()
        entry.rmdir()


def create_symlinks(repo_root: Path, skills: List[Dict], dry_run: bool = False, verbose: bool = False) -> Dict:
    """
    Create .gemini/skills/<name> entries: a directory symlink for skills (so
    scripts/ and references/ resolve) and a SKILL.md file symlink for agents
    and commands. Generated entries that no longer map to a skill are removed.
    """
    gemini_skills_dir = repo_root / ".gemini" / "skills"
    created, updated, unchanged, removed, errors = [], [], [], [], []

    if not dry_run:
        gemini_skills_dir.mkdir(parents=True, exist_ok=True)

    wanted = {s["name"] for s in skills}
    if gemini_skills_dir.exists():
        for entry in sorted(gemini_skills_dir.iterdir()):
            if entry.name not in wanted and _is_generated(entry):
                if not dry_run:
                    _remove(entry)
                removed.append(entry.name)

    for skill in skills:
        skill_name = skill["name"]
        dest = gemini_skills_dir / skill_name
        target = skill["source"]
        try:
            if skill["link"] == "dir":
                if dest.is_symlink() and os.readlink(dest) == target:
                    unchanged.append(skill_name)
                    continue
                if dest.exists() or dest.is_symlink():
                    if not _is_generated(dest):
                        errors.append(f"{skill_name}: {dest} exists and was not generated by this script")
                        continue
                    if not dry_run:
                        _remove(dest)
                    updated.append(skill_name)
                else:
                    created.append(skill_name)
                if not dry_run:
                    dest.symlink_to(target, target_is_directory=True)
            else:
                link = dest / "SKILL.md"
                if link.is_symlink() and os.readlink(link) == target and not dest.is_symlink():
                    unchanged.append(skill_name)
                    continue
                if dest.is_symlink():
                    if not dry_run:
                        dest.unlink()
                if not dry_run:
                    dest.mkdir(exist_ok=True)
                    if link.is_symlink():
                        link.unlink()
                    link.symlink_to(target)
                (updated if link.exists() else created).append(skill_name)
        except OSError as e:
            errors.append(f"{skill_name}: {e}")

    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return {"created": created, "updated": updated, "unchanged": unchanged,
            "removed": removed, "errors": errors}


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
    print(f"Removed: {len(symlink_results['removed'])}")

    if symlink_results['errors']:
        print(f"Errors: {len(symlink_results['errors'])}")
        sys.exit(1)

if __name__ == "__main__":
    main()
