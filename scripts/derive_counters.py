#!/usr/bin/env python3
"""derive_counters.py — single source of truth for repository headline counters.

Walks the canonical tree (excluding sync copies, docs site, audit workspace,
and VCS/CI internals) and derives the headline numbers that README.md,
CLAUDE.md, and .claude-plugin/marketplace.json claim:

  skills              count of SKILL.md files
  plugins_on_disk     count of **/.claude-plugin/plugin.json manifests
  plugins_registered  entries in .claude-plugin/marketplace.json `plugins` array
  python_tools        .py files in the canonical tree, excluding repo-root scripts/
                      (i.e. automation tools shipped inside skill/plugin folders)
  references          .md files under any references/ directory
  agents              .md files under any agents/ directory (excl. CLAUDE.md/README.md)
  commands            .md files under any commands/ directory (excl. CLAUDE.md/README.md)
  domains             top-level folders containing at least one SKILL.md

Modes:
  (default)   print a human-readable table
  --json      print the derived counters as JSON
  --check     exit 1 listing mismatches if the headline counters claimed in
              README.md, root CLAUDE.md ("Current Scope" line), and
              marketplace.json metadata.description disagree with derived
              values. Also validates the README "Skills Overview" per-domain
              table: every domain row's count must equal the SKILL.md count in
              its linked folder, and every on-disk domain must have a row. CI gate G3.

Stdlib only. No writes ever.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Top-level directories excluded from the canonical tree.
EXCLUDED_TOP_LEVEL = {
    ".git",
    ".codex",
    ".codex-plugin",
    ".gemini",
    ".hermes",
    ".vibe",
    "docs",
    "audit",
    "node_modules",
    ".github",
    ".claude",
}

DOC_FILENAMES = {"CLAUDE.md", "README.md"}


def canonical_walk(root: Path):
    """Yield every file in the canonical tree (excluded top-level dirs pruned)."""
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = sorted(current.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if current == root and entry.name in EXCLUDED_TOP_LEVEL:
                    continue
                stack.append(entry)
            elif entry.is_file():
                yield entry


def derive(root: Path) -> dict:
    counters = {
        "skills": 0,
        "plugins_on_disk": 0,
        "plugins_registered": 0,
        "python_tools": 0,
        "references": 0,
        "agents": 0,
        "commands": 0,
        "domains": 0,
    }
    domains = set()

    for path in canonical_walk(root):
        rel = path.relative_to(root)
        parts = rel.parts
        name = path.name

        if name == "SKILL.md":
            counters["skills"] += 1
            if len(parts) > 1:
                domains.add(parts[0])
        elif name == "plugin.json" and path.parent.name == ".claude-plugin":
            counters["plugins_on_disk"] += 1
        elif path.suffix == ".py":
            # Skill/plugin automation tools: every .py except repo-root scripts/.
            if parts[0] != "scripts":
                counters["python_tools"] += 1
        elif path.suffix == ".md":
            if "references" in parts[:-1]:
                counters["references"] += 1
            elif "agents" in parts[:-1] and name not in DOC_FILENAMES:
                counters["agents"] += 1
            elif "commands" in parts[:-1] and name not in DOC_FILENAMES:
                counters["commands"] += 1

    counters["domains"] = len(domains)
    counters["_domain_list"] = sorted(domains)

    marketplace = root / ".claude-plugin" / "marketplace.json"
    if marketplace.is_file():
        try:
            data = json.loads(marketplace.read_text(encoding="utf-8"))
            counters["plugins_registered"] = len(data.get("plugins", []))
        except (json.JSONDecodeError, OSError):
            counters["plugins_registered"] = -1

    return counters


# ---------------------------------------------------------------------------
# --check: parse the standardized claim patterns in the three headline files.
#
# Standardized claim patterns (keep docs in lockstep with these):
#   "<N> production-ready skills" (or "production-ready Claude Code skills")
#   "skills across <D> domains"
#   "<T> Python automation tools" or "<T> Python tools"
#   "<R> reference guides"
#   "<P> marketplace plugins"
# ---------------------------------------------------------------------------

CLAIM_PATTERNS = {
    "skills": re.compile(r"(\d+)\s+production-ready (?:Claude Code )?skills"),
    "domains": re.compile(r"skills across\s+(\d+)\s+domains"),
    "python_tools": re.compile(r"(\d+)\s+Python (?:automation )?tools"),
    "references": re.compile(r"(\d+)\s+reference guides"),
    "plugins_registered": re.compile(r"(\d+)\s+marketplace plugins"),
}


def extract_claims(text: str) -> dict:
    """Return {counter_name: first claimed int} for every pattern found in text."""
    claims = {}
    for key, pattern in CLAIM_PATTERNS.items():
        match = pattern.search(text)
        if match:
            claims[key] = int(match.group(1))
    return claims


# ---------------------------------------------------------------------------
# Per-domain table validation: the README "Skills Overview" table has one row
# per domain, each ending in a `[<folder>/](<folder>/)` link. Every row's count
# must equal the SKILL.md count in its folder, and every on-disk domain must
# have a row. This catches per-domain drift that the headline aggregates miss.
# ---------------------------------------------------------------------------

DOMAIN_ROW_RE = re.compile(r"^\|\s*\*\*")
DOMAIN_LINK_RE = re.compile(r"\]\(([^)]+?)/?\)")


def derive_per_domain(root: Path) -> dict:
    """Return {top_level_domain: SKILL.md count}."""
    counts = {}
    for path in canonical_walk(root):
        if path.name == "SKILL.md":
            rel = path.relative_to(root)
            if len(rel.parts) > 1:
                counts[rel.parts[0]] = counts.get(rel.parts[0], 0) + 1
    return counts


def parse_domain_table(root: Path, readme_text: str) -> dict:
    """Parse README domain rows -> {domain_folder: claimed_count}.

    Only rows whose trailing link resolves to a real top-level directory are
    treated as domain rows, so other bold-first-cell tables (install matrices,
    the skills-vs-agents table) are ignored.
    """
    table = {}
    for line in readme_text.splitlines():
        if not DOMAIN_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        count = next((int(c) for c in cells[1:] if c.isdigit()), None)
        link = DOMAIN_LINK_RE.search(cells[-1])
        if count is None or not link:
            continue
        folder = link.group(1).strip().rstrip("/").split("/")[0]
        if folder and (root / folder).is_dir():
            table[folder] = count
    return table


def check_domain_table(root: Path) -> list:
    """Return mismatch strings between README domain rows and on-disk SKILL.md counts."""
    readme = root / "README.md"
    if not readme.is_file():
        return []
    per_domain = derive_per_domain(root)
    table = parse_domain_table(root, readme.read_text(encoding="utf-8"))
    problems = []
    for folder, claimed in sorted(table.items()):
        actual = per_domain.get(folder, 0)
        if claimed != actual:
            problems.append(
                f"README domain table: '{folder}' row claims {claimed}, disk has {actual} skills"
            )
    for domain, actual in sorted(per_domain.items()):
        if domain not in table:
            problems.append(
                f"README domain table: domain '{domain}' ({actual} skills) has no row"
            )
    return problems


# README shields.io badges of the form ![Skills](.../Skills-355-brightgreen...).
# Validated separately from prose CLAIM_PATTERNS: badges are a fixed
# `<Label>-<count>-<color>` shape, so a per-label regex is exact and cannot
# over-match surrounding prose. Covers the counters that ship as badges.
BADGE_PATTERNS = {
    "skills": re.compile(r"Skills-(\d+)-"),
    "agents": re.compile(r"Agents-(\d+)-"),
    "commands": re.compile(r"Commands-(\d+)-"),
}


def check_readme_badges(root: Path, derived: dict) -> list:
    """Return mismatch strings between README shield badges and derived counts."""
    readme = root / "README.md"
    if not readme.is_file():
        return []
    text = readme.read_text(encoding="utf-8")
    out = []
    for key, pattern in BADGE_PATTERNS.items():
        match = pattern.search(text)
        if not match:
            # Fail loudly rather than skip: a renamed/removed badge would
            # otherwise silently drop out of the gate (mirrors run_check's
            # "no recognizable counter claims found" precedent).
            out.append(
                f"README badge: '{key}' badge not found "
                f"(expected a '{key.capitalize()}-<n>-' shield)"
            )
        elif int(match.group(1)) != derived[key]:
            out.append(
                f"README badge: '{key}' badge claims {match.group(1)}, "
                f"derived {key}={derived[key]}"
            )
    return out


def run_check(root: Path, derived: dict) -> int:
    sources = []

    readme = root / "README.md"
    if readme.is_file():
        sources.append(("README.md", readme.read_text(encoding="utf-8")))

    claude_md = root / "CLAUDE.md"
    if claude_md.is_file():
        text = claude_md.read_text(encoding="utf-8")
        # Restrict to the "Current Scope" line so history sections don't trip the gate.
        scope_lines = [ln for ln in text.splitlines() if ln.startswith("**Current Scope:**")]
        sources.append(("CLAUDE.md (Current Scope line)", "\n".join(scope_lines)))

    marketplace = root / ".claude-plugin" / "marketplace.json"
    if marketplace.is_file():
        try:
            data = json.loads(marketplace.read_text(encoding="utf-8"))
            desc = data.get("metadata", {}).get("description", "")
            sources.append(("marketplace.json metadata.description", desc))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"FAIL: cannot parse marketplace.json: {exc}")
            return 1

    mismatches = []
    for label, text in sources:
        claims = extract_claims(text)
        if not claims:
            mismatches.append(f"{label}: no recognizable counter claims found")
            continue
        for key, claimed in claims.items():
            actual = derived[key]
            if claimed != actual:
                mismatches.append(
                    f"{label}: claims {key}={claimed}, derived {key}={actual}"
                )

    mismatches.extend(check_domain_table(root))
    mismatches.extend(check_readme_badges(root, derived))

    if mismatches:
        print("COUNTER CHECK FAILED — headline claims disagree with derived values:")
        for line in mismatches:
            print(f"  - {line}")
        print("\nRun `python3 scripts/derive_counters.py` for the ground-truth table.")
        return 1

    print("Counter check passed: README.md, CLAUDE.md, marketplace.json match derived values.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Derive repository headline counters from the canonical tree."
    )
    parser.add_argument("--json", action="store_true", help="emit counters as JSON")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if README.md / CLAUDE.md / marketplace.json claims drift from derived values",
    )
    args = parser.parse_args()

    derived = derive(REPO_ROOT)
    domain_list = derived.pop("_domain_list")

    if args.json:
        out = dict(derived)
        out["domain_list"] = domain_list
        print(json.dumps(out, indent=2))
    else:
        width = max(len(k) for k in derived)
        print("Derived repository counters (canonical tree)")
        print("-" * 46)
        for key, value in derived.items():
            print(f"{key.ljust(width)}  {value}")
        print("-" * 46)
        print("domains: " + ", ".join(domain_list))

    if args.check:
        derived["_domain_list"] = domain_list
        return run_check(REPO_ROOT, derived)
    return 0


if __name__ == "__main__":
    sys.exit(main())
