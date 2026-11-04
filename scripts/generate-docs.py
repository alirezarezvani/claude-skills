#!/usr/bin/env python3
"""Generate MkDocs documentation pages from SKILL.md files, agents, and commands."""

import argparse
import json
import os
import re
import shutil
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

# Domain mapping: directory prefix -> (section name, sort order, icon, plugin_name)
DOMAINS = {
    "engineering-team": ("Engineering - Core", 1, ":material-code-braces:", "engineering-skills"),
    "engineering": ("Engineering - POWERFUL", 2, ":material-rocket-launch:", "engineering-advanced-skills"),
    "product-team": ("Product", 3, ":material-lightbulb-outline:", "product-skills"),
    "marketing-skill": ("Marketing", 4, ":material-bullhorn-outline:", "marketing-skills"),
    "project-management": ("Project Management", 5, ":material-clipboard-check-outline:", "pm-skills"),
    "c-level-advisor": ("C-Level Advisory", 6, ":material-account-tie:", "c-level-skills"),
    "ra-qm-team": ("Regulatory & Quality", 7, ":material-shield-check-outline:", "ra-qm-skills"),
    "business-growth": ("Business & Growth", 8, ":material-trending-up:", "business-growth-skills"),
    "finance": ("Finance", 9, ":material-calculator-variant:", "finance-skills"),
    "productivity": ("Productivity", 10, ":material-lightning-bolt-outline:", "productivity-skills"),
    "marketing": ("Marketing (Top-Level)", 11, ":material-web:", "marketing-top-level-skills"),
    "research": ("Research", 12, ":material-magnify:", "research-skills"),
    "business-operations": ("Business Operations", 13, ":material-cog-outline:", "business-operations-skills"),
    "commercial": ("Commercial", 14, ":material-handshake-outline:", "commercial-skills"),
    "research-ops": ("Research Operations", 15, ":material-flask-outline:", "research-ops-skills"),
    "compliance-os": ("Compliance OS", 16, ":material-shield-lock-outline:", "compliance-os"),
    "markdown-html": ("Markdown to HTML", 17, ":material-language-html5:", "markdown-html-skills"),
    "agent-launcher": ("Agent Launcher", 18, ":material-rocket-launch-outline:", "agent-launcher-skills"),
    "c-level-agents": ("C-Level Agents", 19, ":material-account-group-outline:", "c-level-agents"),
    "loop-library": ("Loop Library", 20, ":material-repeat:", "loop-library"),
}

# Skills to skip (nested assets, samples, etc.)
SKIP_PATTERNS = [
    "assets/sample-skill",
    "medium-content-pro 2",  # duplicate with space
]


def find_skill_files():
    """Walk the repo and find all SKILL.md files, grouped by domain.

    Dedupes the dual-publish pattern: when a skill has both a bundled mirror
    at <domain>/skills/<name>/SKILL.md AND a standalone wrapper at
    <domain>/<name>/skills/<name>/SKILL.md, the standalone wrapper is skipped
    (the bundled location is canonical for docs). The two are kept in sync by
    scripts/sync_skill_bundles.py; rendering both creates duplicate pages.
    """
    # First pass: collect all SKILL.md paths grouped by domain.
    raw = {}
    for root, dirs, files in os.walk(REPO_ROOT):
        if "SKILL.md" not in files:
            continue
        rel_path = os.path.relpath(root, REPO_ROOT).replace(os.sep, "/")
        if any(skip in rel_path for skip in SKIP_PATTERNS):
            continue
        parts = rel_path.split("/")
        domain_key = parts[0]
        if domain_key not in DOMAINS:
            continue
        raw.setdefault(domain_key, []).append((parts, root))

    # Second pass: build the bundled-name set per domain, then skip
    # standalone wrappers that mirror those bundled skills.
    skills = {}
    for domain_key, entries in raw.items():
        bundled_names = {
            parts[2]
            for parts, _ in entries
            if len(parts) == 3 and parts[1] == "skills"
        }
        for parts, root in entries:
            # Detect the dual-publish standalone wrapper:
            # <domain>/<name>/skills/<same-name>/SKILL.md (4 parts) where
            # the same <name> already exists in the bundled set.
            is_dual_publish_mirror = (
                len(parts) == 4
                and parts[2] == "skills"
                and parts[1] == parts[3]
                and parts[1] in bundled_names
            )
            if is_dual_publish_mirror:
                continue

            skill_name = parts[-1]
            skill_path = os.path.join(root, "SKILL.md")
            if len(parts) >= 3 and parts[1] == "skills":
                is_sub_skill = False
                parent = None
            else:
                is_sub_skill = len(parts) > 2
                parent = parts[1] if len(parts) > 2 else None

            skills.setdefault(domain_key, []).append({
                "name": skill_name,
                "path": skill_path,
                "rel_path": os.path.relpath(root, REPO_ROOT).replace(os.sep, "/"),
                "is_sub_skill": is_sub_skill,
                "parent": parent,
            })
    return skills


def extract_title(filepath):
    """Extract the first H1 heading from a SKILL.md file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip YAML frontmatter
                if line == "---":
                    in_frontmatter = True
                    for line2 in f:
                        if line2.strip() == "---":
                            break
                    continue
                if line.startswith("# "):
                    return line[2:].strip()
    except Exception:
        pass
    return None


def extract_subtitle(filepath):
    """Extract the first non-empty line after the first H1 heading."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            found_h1 = False
            in_frontmatter = False
            for line in f:
                stripped = line.strip()
                if stripped == "---" and not in_frontmatter:
                    in_frontmatter = True
                    for line2 in f:
                        if line2.strip() == "---":
                            break
                    continue
                if stripped.startswith("# ") and not found_h1:
                    found_h1 = True
                    continue
                if found_h1 and stripped and not stripped.startswith("#"):
                    return stripped
    except Exception:
        pass
    return None


def card_summary(filepath, limit=120):
    """One-line card text: the frontmatter description's first sentence, else the
    first line after the H1. Markdown quote/emphasis markers are stripped."""
    text = extract_description_from_frontmatter(filepath) or extract_subtitle(filepath) or ""
    text = re.sub(r"^>\s*", "", text.strip())
    text = re.sub(r"[*_`\[\]]", "", text)
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    if m and len(m.group(1)) >= 40:
        text = m.group(1)
    if len(text) > limit:
        text = text[:limit - 3].rsplit(" ", 1)[0] + "..."
    return text


def extract_description_from_frontmatter(filepath):
    """Extract the description field from YAML frontmatter.

    Handles single-line, quoted, and multi-line (| or >) YAML descriptions.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.match(r"^---\n(.*?)---\n", content, re.DOTALL)
        if not match:
            return None
        fm = match.group(1)

        # Try quoted single-line: description: "text" or description: 'text'
        m = re.search(r'description:\s*"([^"]+)"', fm)
        if m:
            return m.group(1).strip()
        m = re.search(r"description:\s*'([^']+)'", fm)
        if m:
            return m.group(1).strip()

        # Try multi-line block scalar: description: | or description: >
        m = re.search(r"description:\s*[|>]-?\s*\n((?:[ \t]+.+\n?)+)", fm)
        if m:
            lines = m.group(1).strip().splitlines()
            text = " ".join(line.strip() for line in lines)
            return text

        # Try unquoted single-line: description: text
        m = re.search(r"description:\s+([^\n\"'][^\n]+)", fm)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return None


def slugify(name):
    """Convert a skill name to a URL-friendly slug."""
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


# SEO keyword mapping: domain_key -> differentiating keywords for <title> tags
# site_name already carries "Claude Code Skills" on every page,
# so per-page suffixes emphasize complementary terms: agent skill, Codex, OpenClaw, domain
DOMAIN_SEO_SUFFIX = {
    "engineering-team": "Agent Skill & Codex Plugin",
    "engineering": "Agent Skill for Codex & OpenClaw",
    "product-team": "Agent Skill for Product Teams",
    "marketing-skill": "Agent Skill for Marketing",
    "project-management": "Agent Skill for PM",
    "c-level-advisor": "Agent Skill for Executives",
    "ra-qm-team": "Agent Skill for Compliance",
    "business-growth": "Agent Skill for Growth",
    "finance": "Agent Skill for Finance",
    "productivity": "Agent Skill for Personal Productivity",
    "marketing": "Agent Skill for Landing Pages",
    "research": "Agent Skill for Research Workflows",
    "markdown-html": "Agent Skill for HTML Output",
    "agent-launcher": "Agent Skill for Claude Managed Agents",
}

# Domain-specific description context for pages without frontmatter descriptions
DOMAIN_SEO_CONTEXT = {
    "engineering-team": "engineering agent skill and Claude Code plugin for code generation, DevOps, architecture, and testing",
    "engineering": "advanced agent-native skill and Claude Code plugin for AI agent design, infrastructure, and automation",
    "product-team": "product management agent skill and Claude Code plugin for PRDs, discovery, analytics, and roadmaps",
    "marketing-skill": "marketing agent skill and Claude Code plugin for content, SEO, CRO, and growth",
    "project-management": "project management agent skill and Claude Code plugin for sprints, Jira, and Confluence",
    "c-level-advisor": "executive advisory agent skill and Claude Code plugin for strategic decisions and board meetings",
    "ra-qm-team": "regulatory and quality management agent skill for ISO 13485, MDR, FDA, and GDPR compliance",
    "business-growth": "business growth agent skill and Claude Code plugin for customer success, sales, and revenue ops",
    "finance": "finance agent skill and Claude Code plugin for DCF valuation, budgeting, and SaaS metrics",
    "productivity": "personal productivity agent skill and Claude Code plugin for brain-dump capture, email triage, and reflection",
    "marketing": "landing-page generator agent skill and Claude Code plugin for single-file HTML output with 4 design styles",
    "research": "research orchestrator agent skill and Claude Code plugin for hybrid routing across pulse, litreview, grants, dossier, patent, syllabus, and notebooklm specialists",
    "business-operations": "business operations agent skill and Claude Code plugin for process mapping, vendor management, capacity planning, and internal comms",
    "commercial": "commercial agent skill and Claude Code plugin for pricing strategy, deal desk, partnerships, and RFP response",
    "research-ops": "enterprise research operations agent skill and Claude Code plugin for clinical study design, R&D finance, market sizing, and product research",
    "compliance-os": "compliance readiness agent skill and Claude Code plugin for ISO 13485, ISO 27001, SOC 2, GDPR, FDA QSR, and EU AI Act audit prep",
    "markdown-html": "markdown-to-interactive-HTML converter agent skill and Claude Code plugin for single-file documents, code reviews, and slide decks",
    "agent-launcher": "Claude Managed Agent launcher agent skill and Claude Code plugin for session-goal-driven interview, BYOK launch, bounded grade-iterate loops, and cron scheduled deployments",
}


def prettify(name):
    """Convert kebab-case to Title Case."""
    return name.replace("-", " ").title()


def strip_content(content):
    """Strip frontmatter and first H1 from content, handling edge cases."""
    # Strip YAML frontmatter
    content = re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL)
    # Strip leading whitespace
    content = content.lstrip()
    # Remove the first H1 if it exists (avoid duplicate)
    content = re.sub(r"^#\s+.+\n", "", content, count=1)
    # Remove leading hr after title
    content = re.sub(r"^\s*---\s*\n", "", content)
    return content


GITHUB_BASE = "https://github.com/alirezarezvani/claude-skills/tree/main"
GITHUB_EDIT_BASE = "https://github.com/alirezarezvani/claude-skills/edit/dev"
START_HERE_PATH = os.path.join(REPO_ROOT, "scripts", "docs_start_here.json")
MARKETPLACE_PATH = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")


def load_marketplace():
    """Return (marketplace_name, [plugin dicts with a normalized 'dir'])."""
    with open(MARKETPLACE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    plugins = []
    for p in data.get("plugins", []):
        src = p.get("source")
        if not isinstance(src, str):
            continue
        plugins.append({**p, "dir": src[2:].rstrip("/") if src.startswith("./") else src.rstrip("/")})
    return data["name"], plugins


MARKETPLACE_NAME, PLUGINS = load_marketplace()
with open(START_HERE_PATH, encoding="utf-8") as _f:
    START_HERE = {k: v for k, v in json.load(_f).items() if not k.startswith("_")}
PLUGIN_NAMES = {p["name"] for p in PLUGINS}


def resolve_plugins(skill_rel_path, skill_name):
    """Find the plugin(s) that ship a skill.

    Returns (primary, bundle): primary is the most specific plugin to install
    (a standalone plugin named after the skill when one exists), bundle is a
    larger plugin that also contains it, or None. Both are names that exist in
    marketplace.json, so every install line on the site is runnable.
    """
    domain = skill_rel_path.split("/")[0]
    # Plugins whose directory contains the skill, most specific first.
    containing = sorted(
        (p for p in PLUGINS
         if skill_rel_path == p["dir"] or skill_rel_path.startswith(p["dir"] + "/")),
        key=lambda p: len(p["dir"]), reverse=True)
    # Dual-published skill: the docs page renders the bundled copy, but a
    # standalone plugin at <domain>/<name> also ships it.
    standalone = next((p for p in PLUGINS if p["dir"] == f"{domain}/{skill_name}"), None)
    primary = standalone or (containing[0] if containing else None)
    bundle = next((p for p in containing if primary is None or p["name"] != primary["name"]), None)
    if bundle is not None and primary is not None and len(bundle["dir"]) >= len(primary["dir"]):
        bundle = None
    return (primary["name"] if primary else None, bundle["name"] if bundle else None)


def install_banner(primary, bundle, label="Install"):
    """HTML banner with a runnable install command (inside Claude Code)."""
    if primary is None:
        return ('<div class="install-banner" markdown>\n'
                '<span class="install-label">Install:</span> not packaged as a plugin; '
                'copy the skill folder or see [Getting Started](../../getting-started.md).\n'
                '</div>\n\n')
    extra = ""
    if bundle:
        extra = f' <span class="install-alt">also in <code>{bundle}</code></span>'
    return ('<div class="install-banner" markdown>\n'
            f'<span class="install-label">{label}:</span> '
            f'<code>/plugin install {primary}@{MARKETPLACE_NAME}</code>{extra}\n'
            '</div>\n\n')


def _resolve_vendor(source_rel_dir, vendor_rel):
    """Map ${CLAUDE_PLUGIN_ROOT}/vendor/<x> to the real repo path behind the symlink."""
    d = source_rel_dir
    while d and d != ".":
        candidate = os.path.join(REPO_ROOT, d, vendor_rel)
        if os.path.exists(candidate):
            return os.path.relpath(os.path.realpath(candidate), os.path.realpath(REPO_ROOT)).replace(os.sep, "/")
        d = os.path.dirname(d)
    return None


def rewrite_remaining_links(content, source_rel_dir):
    """Last pass: any relative link that still points outside docs/ goes to GitHub.

    SKILL.md files link to chapters/, scorers/, glossary.md, vendored
    ${CLAUDE_PLUGIN_ROOT}/vendor/<path> files and similar. None of those are
    docs pages, so on the site they 404 (and fail `mkdocs build --strict`).
    """
    def fix(match):
        text, target = match.group(1), match.group(2)
        if target.startswith(("#", "http://", "https://", "mailto:", "/")):
            return match.group(0)
        path, _, anchor = target.partition("#")
        if path.startswith("${CLAUDE_PLUGIN_ROOT}/vendor/"):
            repo_path = _resolve_vendor(source_rel_dir, path[len("${CLAUDE_PLUGIN_ROOT}/"):])
            if repo_path is None:
                return match.group(0)
        elif path.startswith("${CLAUDE_PLUGIN_ROOT}/"):
            return f"[{text}]({GITHUB_BASE}/{source_rel_dir})"
        else:
            repo_path = os.path.normpath(os.path.join(source_rel_dir, path)).replace(os.sep, "/")
        if repo_path.startswith("..") or not os.path.exists(os.path.join(REPO_ROOT, repo_path)):
            return match.group(0)
        return f"[{text}]({GITHUB_BASE}/{repo_path}{'#' + anchor if anchor else ''})"

    return re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", fix, content)


def rewrite_skill_internal_links(content, skill_rel_path):
    """Rewrite skill-internal relative links to GitHub source URLs.

    SKILL.md files contain links like references/foo.md, scripts/bar.py,
    assets/template.md, README.md — these exist in the repo but not in docs/.
    Convert them to absolute GitHub URLs.
    """
    # Patterns that are skill-internal (not other docs pages)
    internal_prefixes = ("references/", "scripts/", "assets/", "templates/", "tools/")

    def resolve_internal(match):
        text = match.group(1)
        target = match.group(2)
        # Skip anchors, absolute URLs, and links to other docs pages
        if target.startswith(("#", "http://", "https://", "mailto:")):
            return match.group(0)
        # Rewrite skill-internal links
        if (target.startswith(internal_prefixes) or target == "README.md"
                or target.endswith((".py", ".json", ".yaml", ".yml", ".sh"))):
            github_url = f"{GITHUB_BASE}/{skill_rel_path}/{target}"
            return f"[{text}]({github_url})"
        # Explicit ./ links and ALL-CAPS companion files (CONTEXT-FORMAT.md,
        # ADR-FORMAT.md, REFERENCE.md) are skill-folder siblings, not docs pages.
        bare = target[2:] if target.startswith("./") else target
        stem = bare.split("/")[0].split("#")[0].rsplit(".", 1)[0]
        if target.startswith("./") or (bare.endswith(".md") and "/" not in bare
                                       and stem and stem == stem.upper()):
            github_url = f"{GITHUB_BASE}/{skill_rel_path}/{bare}"
            return f"[{text}]({github_url})"
        return match.group(0)

    content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", resolve_internal, content)
    return content


def rewrite_relative_links(content, source_rel_path):
    """Rewrite relative markdown links (../../, ../) to absolute GitHub URLs.

    Agent and command source files use relative paths like ../../product-team/SKILL.md
    which break when rendered in the docs site. Convert them to GitHub source links.
    """
    source_dir = os.path.dirname(source_rel_path)

    def resolve_link(match):
        text = match.group(1)
        rel_target = match.group(2)
        # Repo-root-relative links (e.g. engineering/grill-me/agents/cs-foo.md or
        # marketing-skill/skills/aeo/SKILL.md) exist in the repo but not in docs/ —
        # rewrite them to GitHub source URLs.
        if (not rel_target.startswith(("../", "#", "http://", "https://", "mailto:"))
                and "/" in rel_target
                and os.path.exists(os.path.join(REPO_ROOT, rel_target.split("#")[0]))):
            return f"[{text}]({GITHUB_BASE}/{rel_target})"
        # Only rewrite relative paths that go up (../)
        if not rel_target.startswith("../"):
            return match.group(0)
        # Resolve against source directory
        resolved = os.path.normpath(os.path.join(source_dir, rel_target)).replace(os.sep, "/")
        # Keep links to sibling .md files in the same docs directory
        # e.g. agents/product/cs-foo.md linking to cs-bar.md (same-level agent docs)
        # These resolve to agents/product/cs-bar.md — only keep if they're
        # a docs page we generate (agent .md that isn't CLAUDE.md)
        if (resolved.startswith("agents/") and resolved.count("/") == 1
                and resolved.endswith(".md") and "CLAUDE" not in resolved):
            # This is a sibling agent doc link — rewrite to flat docs slug
            sibling = os.path.basename(resolved).replace(".md", "") + ".md"
            return f"[{text}]({sibling})"
        return f"[{text}]({GITHUB_BASE}/{resolved})"

    content = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", resolve_link, content)

    # Also rewrite backtick code references like `../../product-team/foo/SKILL.md`
    # Convert to clickable GitHub links
    def resolve_backtick(match):
        rel_target = match.group(1)
        if not rel_target.startswith("../"):
            return match.group(0)
        resolved = os.path.normpath(os.path.join(source_dir, rel_target)).replace(os.sep, "/")
        # Make the path a clickable link to the GitHub source
        # Show parent/filename for context (e.g., product-analytics/SKILL.md)
        parts = resolved.split("/")
        display = "/".join(parts[-2:]) if len(parts) >= 2 else resolved
        return f"[`{display}`]({GITHUB_BASE}/{resolved})"

    content = re.sub(r"`(\.\./[^`]+)`", resolve_backtick, content)

    return content


def generate_skill_page(skill, domain_key):
    """Generate a docs page for a single skill."""
    skill_md_path = skill["path"]
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title or generate one
    title = extract_title(skill_md_path) or prettify(skill["name"])
    # Clean title of markdown artifacts and strip domain labels
    title = re.sub(r"[*_`]", "", title)
    title = re.sub(r"\s*[-—]\s*(POWERFUL|Core|Advanced)\s*$", "", title, flags=re.IGNORECASE)

    domain_name, _, domain_icon, plugin_name = DOMAINS[domain_key]
    seo_suffix = DOMAIN_SEO_SUFFIX.get(domain_key, "Claude Code Plugin & Agent Skill")
    seo_title = f"{title} — {seo_suffix}"

    fm_desc = extract_description_from_frontmatter(skill_md_path)
    desc_platforms = "Claude Code, Codex CLI, Gemini CLI, OpenClaw"
    if fm_desc:
        # Strip quotes and clean
        clean = fm_desc.strip("'\"").replace('"', "'")
        # Check if platform keywords already present
        has_platform = any(k in clean.lower() for k in ["claude code", "codex", "gemini"])
        if len(clean) > 150:
            # Truncate at last word boundary before 150 chars
            truncated = clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
            description = f"{truncated}." if has_platform else f"{truncated}. Agent skill for {desc_platforms}."
        else:
            desc_text = clean.rstrip(".")
            description = f"{desc_text}." if has_platform else f"{desc_text}. Agent skill for {desc_platforms}."
    else:
        seo_ctx = DOMAIN_SEO_CONTEXT.get(domain_key, f"agent skill for {domain_name}")
        description = f"{title} — {seo_ctx}. Works with {desc_platforms}."
    subtitle = extract_subtitle(skill_md_path) or ""
    # Clean subtitle of markdown artifacts for the intro
    subtitle_clean = re.sub(r"[*_`\[\]]", "", subtitle)

    # Build the page with design system
    page = f'''---
title: "{seo_title}"
description: "{description}"
edit_source: "{skill["rel_path"]}/SKILL.md"
search:
  boost: 2
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">{domain_icon} {domain_name}</span>
<span class="meta-badge">:material-identifier: `{skill["name"]}`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/{skill["rel_path"]}/SKILL.md">Source</a></span>
</div>

'''
    # Add install banner (real plugin names from marketplace.json)
    page += install_banner(*resolve_plugins(skill["rel_path"], skill["name"]))

    content_clean = strip_content(content)
    content_clean = rewrite_skill_internal_links(content_clean, skill["rel_path"])
    content_clean = rewrite_relative_links(content_clean, os.path.join(skill["rel_path"], "SKILL.md"))
    content_clean = rewrite_remaining_links(content_clean, skill["rel_path"])
    page += content_clean

    return page


def generate_nav_entry(skills_by_domain):
    """Generate the nav section for mkdocs.yml."""
    nav_lines = []
    sorted_domains = sorted(skills_by_domain.items(), key=lambda x: DOMAINS[x[0]][1])

    for domain_key, skills in sorted_domains:
        domain_name = DOMAINS[domain_key][0]
        # Group sub-skills under their parent
        top_level = [s for s in skills if not s["is_sub_skill"]]
        sub_skills = [s for s in skills if s["is_sub_skill"]]
        top_level.sort(key=lambda s: s["name"])

        nav_lines.append(f"    - {domain_name}:")
        for skill in top_level:
            slug = slugify(skill["name"])
            page_path = f"skills/{domain_key}/{slug}.md"
            title = extract_title(skill["path"]) or prettify(skill["name"])
            title = re.sub(r"[*_`]", "", title)
            nav_lines.append(f"      - \"{title}\": {page_path}")

            # Add sub-skills under parent
            children = [s for s in sub_skills if s["parent"] == skill["name"]]
            children.sort(key=lambda s: s["name"])
            for child in children:
                child_slug = slugify(child["name"])
                child_path = f"skills/{domain_key}/{slug}-{child_slug}.md"
                child_title = extract_title(child["path"]) or prettify(child["name"])
                child_title = re.sub(r"[*_`]", "", child_title)
                nav_lines.append(f"        - \"{child_title}\": {child_path}")

    return "\n".join(nav_lines)


NAV_RECORDS = {}


def write_if_changed(path, content):
    """Write only when content differs, so `mkdocs serve` does not loop on its own output."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            if f.read() == content:
                return
    except FileNotFoundError:
        pass
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def skill_title(skill):
    title = extract_title(skill["path"]) or prettify(skill["name"])
    title = re.sub(r"[*_`]", "", title)
    return re.sub(r"\s*[-—]\s*(POWERFUL|Core|Advanced)\s*$", "", title, flags=re.IGNORECASE)


def record_nav(domain_key, filename, skill, group):
    """Remember a generated skill page so the docs hook can build the nav."""
    NAV_RECORDS.setdefault(domain_key, []).append({
        "path": f"skills/{domain_key}/{filename}",
        "title": skill_title(skill),
        "group": group,
        "skill": skill,
    })


NAV_LABELS_PATH = os.path.join(REPO_ROOT, "scripts", "docs_nav_labels.json")


def nav_label(path, title, labels):
    """Curated short label if one exists, else the page H1 without its subtitle."""
    return labels.get(path) or re.split(r"\s+[—–]\s+", title, maxsplit=1)[0].strip()


def build_nav(result):
    """Nav subtrees for the Skills, Agents and Commands tabs (mkdocs nav format).

    Every generated page appears exactly once, so nothing is reachable only by
    search. Labels come from scripts/docs_nav_labels.json when curated there.
    """
    with open(NAV_LABELS_PATH, "r", encoding="utf-8") as f:
        labels = json.load(f)
    skills_nav = [{"Overview": "skills/index.md"}]
    for domain_key in sorted(NAV_RECORDS, key=lambda d: DOMAINS[d][1]):
        items = [{"Overview": f"skills/{domain_key}/index.md"}]
        groups = {}
        for rec in sorted(NAV_RECORDS[domain_key], key=lambda r: ((r["group"] or r["title"]).lower(), r["group"] is None or r["title"] != r["group"], r["title"].lower())):
            if rec["group"]:
                if rec["group"] not in groups:
                    groups[rec["group"]] = []
                    items.append({nav_label("", rec["group"], {}): groups[rec["group"]]})
                groups[rec["group"]].append({nav_label(rec["path"], rec["title"], labels): rec["path"]})
            else:
                items.append({nav_label(rec["path"], rec["title"], labels): rec["path"]})
        skills_nav.append({DOMAINS[domain_key][0]: items})

    by_domain = {}
    for title, slug, domain_label, _icon in result["agents"]:
        path = f"agents/{slug}.md"
        by_domain.setdefault(domain_label, []).append({nav_label(path, title, labels): path})
    agents_nav = [{"Overview": "agents/index.md"}]
    for label in sorted(by_domain):
        agents_nav.append({label: sorted(by_domain[label], key=lambda d: next(iter(d)).lower())})

    commands_nav = [{"Overview": "commands/index.md"}]
    commands_nav += [{f"/{name}": f"commands/{slug}.md"} for name, slug, _t, _d in sorted(result["commands"])]
    return {"Skills": skills_nav, "Agents": agents_nav, "Commands": commands_nav}


def parse_args(argv=None):
    """Parse CLI arguments BEFORE any filesystem access.

    `--help` must be side-effect-free: argparse prints usage and exits 0
    without ever touching docs/. Default (no-arg) behavior is unchanged —
    the full docs/ tree is regenerated.
    """
    parser = argparse.ArgumentParser(
        description="Generate MkDocs documentation pages from SKILL.md files, "
                    "agents, and commands. Running with no arguments rewrites "
                    "the docs/ tree.")
    return parser.parse_args(argv)


def main():
    NAV_RECORDS.clear()
    skills_by_domain = find_skill_files()

    # Create docs/skills/ directories
    for domain_key in skills_by_domain:
        os.makedirs(os.path.join(DOCS_DIR, "skills", domain_key), exist_ok=True)

    total = 0
    # Generate individual skill pages
    for domain_key, skills in skills_by_domain.items():
        top_level = [s for s in skills if not s["is_sub_skill"]]
        sub_skills = [s for s in skills if s["is_sub_skill"]]
        top_level_names = {s["name"] for s in top_level}

        for skill in top_level:
            slug = slugify(skill["name"])
            page_content = generate_skill_page(skill, domain_key)
            page_path = os.path.join(DOCS_DIR, "skills", domain_key, f"{slug}.md")
            write_if_changed(page_path, page_content)
            total += 1

            # Generate sub-skill pages
            children = [s for s in sub_skills if s["parent"] == skill["name"]]
            group = skill_title(skill) if children else None
            record_nav(domain_key, f"{slug}.md", skill, group)
            for child in children:
                child_slug = slugify(child["name"])
                child_content = generate_skill_page(child, domain_key)
                child_path = os.path.join(DOCS_DIR, "skills", domain_key, f"{slug}-{child_slug}.md")
                write_if_changed(child_path, child_content)
                total += 1
                record_nav(domain_key, f"{slug}-{child_slug}.md", child, group)

        # Render orphan sub-skills (sub-skills whose parent is a plugin folder,
        # not a top-level skill at <domain>/skills/<name>/). Without this,
        # standalone-only plugins like executive-mentor, agenthub, autoresearch-agent,
        # playwright-pro, self-improving-agent, c-level-agents, and llm-wiki have
        # their sub-skills silently dropped (~79 pages missing from the docs site).
        orphan_sub_skills = [s for s in sub_skills if s["parent"] not in top_level_names]
        # Group by plugin parent
        by_parent = {}
        for s in orphan_sub_skills:
            by_parent.setdefault(s["parent"], []).append(s)
        for parent, children in by_parent.items():
            parent_slug = slugify(parent)
            # If a child has the same name as parent, it's the plugin's index skill;
            # render as <parent>.md (preserves existing URLs like executive-mentor.md).
            index_sub = next((s for s in children if s["name"] == parent), None)
            group = (skill_title(index_sub) if index_sub else prettify(parent)) if len(children) > 1 else None
            if index_sub:
                page_content = generate_skill_page(index_sub, domain_key)
                page_path = os.path.join(DOCS_DIR, "skills", domain_key, f"{parent_slug}.md")
                write_if_changed(page_path, page_content)
                total += 1
                record_nav(domain_key, f"{parent_slug}.md", index_sub, group)
            # Render non-index children as <parent>-<child>.md
            # (preserves existing URLs like executive-mentor-challenge.md).
            for child in children:
                if child["name"] == parent:
                    continue
                child_slug = slugify(child["name"])
                child_content = generate_skill_page(child, domain_key)
                child_path = os.path.join(DOCS_DIR, "skills", domain_key, f"{parent_slug}-{child_slug}.md")
                write_if_changed(child_path, child_content)
                total += 1
                record_nav(domain_key, f"{parent_slug}-{child_slug}.md", child, group)

    # Generate domain index pages
    sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))
    import derive_counters
    from pathlib import Path
    DERIVED_PER_DOMAIN = derive_counters.derive_per_domain(Path(REPO_ROOT))
    sorted_domains = sorted(skills_by_domain.items(), key=lambda x: DOMAINS[x[0]][1])
    for domain_key, skills in sorted_domains:
        domain_name, _, domain_icon, plugin_name = DOMAINS[domain_key]
        # Same number the homepage shows (scripts/derive_counters.py), so a
        # domain never claims a different count on two pages.
        skill_count = DERIVED_PER_DOMAIN.get(domain_key, len(skills))

        # One card per page group: a plugin with sub-skills gets one card (its
        # index page) with a sub-skill count; every ungrouped page gets its own.
        records = NAV_RECORDS.get(domain_key, [])
        entries, seen_groups = [], {}
        for rec in records:
            if rec["group"] is None:
                entries.append({**rec, "subs": 0})
            elif rec["group"] not in seen_groups:
                seen_groups[rec["group"]] = len(entries)
                entries.append({**rec, "subs": 0})
            else:
                entries[seen_groups[rec["group"]]]["subs"] += 1
        entries.sort(key=lambda e: e["title"].lower())

        def card(entry):
            slug = os.path.basename(entry["path"])
            title = re.sub(r"[*_`]", "", extract_title(entry["skill"]["path"]) or entry["title"])
            subtitle = card_summary(entry["skill"]["path"]) or f"`{entry['skill']['name']}`"
            sub_text = f" + {entry['subs']} sub-skills" if entry["subs"] else ""
            return f"""
-   **[{title}]({slug})**{sub_text}

    ---

    {subtitle}
"""

        cards = "".join(card(e) for e in entries)
        by_slug = {os.path.basename(e["path"])[:-3]: e for e in entries}
        picks = [by_slug[p] for p in START_HERE.get(domain_key, []) if p in by_slug]
        start_here = ""
        if picks and len(entries) > 3:
            start_here = ('\n## Start here\n\n<div class="grid cards start-here" markdown>\n'
                          + "".join(card(p) for p in picks) + "\n</div>\n\n## All skills\n")

        domain_plugin = next((p["name"] for p in PLUGINS if p["dir"] == domain_key), None)
        domain_install = install_banner(domain_plugin, None, "Install all") if domain_plugin else ""
        domain_seo_ctx = DOMAIN_SEO_CONTEXT.get(domain_key, f"agent skills for {domain_name}")
        index_content = f'''---
title: "{domain_name} Skills — Agent Skills & Codex Plugins"
description: "{skill_count} {domain_name.lower()} skills — {domain_seo_ctx}. Works with Claude Code, Codex CLI, Gemini CLI, and OpenClaw."
---

<div class="domain-header" markdown>

# {domain_icon} {domain_name}

<p class="domain-count">{skill_count} skills in this domain</p>

</div>

{domain_install}
{start_here}
<div class="grid cards" markdown>
{cards}
</div>
'''

        index_path = os.path.join(DOCS_DIR, "skills", domain_key, "index.md")
        write_if_changed(index_path, index_content)

    # Generate agent pages
    agents_dir = os.path.join(REPO_ROOT, "agents")
    agents_docs_dir = os.path.join(DOCS_DIR, "agents")
    os.makedirs(agents_docs_dir, exist_ok=True)
    agent_count = 0
    agent_entries = []

    # Agent domain mapping for display
    AGENT_DOMAINS = {
        "business-growth": ("Business & Growth", ":material-trending-up:"),
        "c-level": ("C-Level Advisory", ":material-account-tie:"),
        "engineering-team": ("Engineering - Core", ":material-code-braces:"),
        "engineering": ("Engineering - POWERFUL", ":material-rocket-launch:"),
        "finance": ("Finance", ":material-calculator-variant:"),
        "marketing": ("Marketing", ":material-bullhorn-outline:"),
        "product": ("Product", ":material-lightbulb-outline:"),
        "project-management": ("Project Management", ":material-clipboard-check-outline:"),
        "ra-qm-team": ("Regulatory & Quality", ":material-shield-check-outline:"),
        "markdown-html": ("Markdown to HTML", ":material-language-html5:"),
        "agent-launcher": ("Agent Launcher", ":material-rocket-launch-outline:"),
    }

    if os.path.isdir(agents_dir):
        for domain_folder in sorted(os.listdir(agents_dir)):
            domain_path = os.path.join(agents_dir, domain_folder)
            if not os.path.isdir(domain_path):
                continue
            domain_info = AGENT_DOMAINS.get(domain_folder, (prettify(domain_folder), ":material-account:"))
            domain_label, domain_icon = domain_info
            for agent_file in sorted(os.listdir(domain_path)):
                if not agent_file.endswith(".md"):
                    continue
                agent_name = agent_file.replace(".md", "")
                agent_path = os.path.join(domain_path, agent_file)
                rel = os.path.relpath(agent_path, REPO_ROOT).replace(os.sep, "/")
                title = extract_title(agent_path) or prettify(agent_name)
                title = re.sub(r"[*_`]", "", title)
                # If H1 is a raw slug (cs-foo-bar), prettify it
                if re.match(r"^cs-[a-z-]+$", title):
                    title = prettify(title.removeprefix("cs-"))

                with open(agent_path, "r", encoding="utf-8") as f:
                    content = f.read()

                content_clean = strip_content(content)
                content_clean = rewrite_relative_links(content_clean, rel)
                content_clean = rewrite_remaining_links(content_clean, os.path.dirname(rel))

                agent_seo_title = f"{title} — AI Coding Agent & Codex Skill"
                agent_fm_desc = extract_description_from_frontmatter(agent_path)
                if agent_fm_desc:
                    agent_clean = agent_fm_desc.strip("'\"").replace('"', "'")
                    if len(agent_clean) > 150:
                        agent_clean = agent_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                    agent_desc = f"{agent_clean}. Agent-native orchestrator for Claude Code, Codex, Gemini CLI."
                else:
                    agent_desc = f"{title} — agent-native AI orchestrator for {domain_label}. Works with Claude Code, Codex CLI, Gemini CLI, and OpenClaw."

                page = f'''---
title: "{agent_seo_title}"
description: "{agent_desc}"
edit_source: "{rel}"
search:
  boost: 0.5
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Agent</span>
<span class="meta-badge">{domain_icon} {domain_label}</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/{rel}">Source</a></span>
</div>

{content_clean}'''
                slug = slugify(agent_name)
                out_path = os.path.join(agents_docs_dir, f"{slug}.md")
                write_if_changed(out_path, page)
                agent_count += 1
                agent_entries.append((title, slug, domain_label, domain_icon))

    # Pass 2: walk plugin-internal agents/ folders.
    # Plugins like c-level-agents, executive-mentor, agenthub, llm-wiki,
    # self-improving-agent bundle agents alongside their skills at
    # <domain>/<plugin>/agents/*.md. These weren't previously discovered;
    # nav entries in mkdocs.yml that point to them would 404.
    SKILL_TO_AGENT_DOMAIN = {
        "c-level-advisor": "c-level",
        "engineering": "engineering",
        "engineering-team": "engineering-team",
        "marketing-skill": "marketing",
        "product-team": "product",
        "project-management": "project-management",
        "ra-qm-team": "ra-qm-team",
        "business-growth": "business-growth",
        "finance": "finance",
        "business-operations": "business-operations",
        "commercial": "commercial",
        "research-ops": "research-ops",
        "compliance-os": "compliance-os",
        "markdown-html": "markdown-html",
        "agent-launcher": "agent-launcher",
    }
    seen_slugs = {entry[1] for entry in agent_entries}
    for skill_domain in DOMAINS:
        skill_domain_path = os.path.join(REPO_ROOT, skill_domain)
        if not os.path.isdir(skill_domain_path):
            continue
        # Pass 2a: <domain>/agents/<agent>.md (v2.8.0 pattern — business-operations, commercial)
        domain_agents = os.path.join(skill_domain_path, "agents")
        candidate_dirs = []
        if os.path.isdir(domain_agents):
            candidate_dirs.append(domain_agents)
        # Pass 2b: <domain>/<plugin>/agents/<agent>.md (legacy pattern — c-level-agents, agenthub, etc.)
        for plugin_name in sorted(os.listdir(skill_domain_path)):
            plugin_agents_dir = os.path.join(skill_domain_path, plugin_name, "agents")
            if os.path.isdir(plugin_agents_dir):
                candidate_dirs.append(plugin_agents_dir)
        for plugin_agents_dir in candidate_dirs:
            agent_domain_key = SKILL_TO_AGENT_DOMAIN.get(skill_domain, skill_domain)
            domain_info = AGENT_DOMAINS.get(agent_domain_key, (prettify(agent_domain_key), ":material-account:"))
            domain_label, domain_icon = domain_info
            for agent_file in sorted(os.listdir(plugin_agents_dir)):
                if not agent_file.endswith(".md"):
                    continue
                agent_name = agent_file.replace(".md", "")
                slug = slugify(agent_name)
                if slug in seen_slugs:
                    continue
                agent_path = os.path.join(plugin_agents_dir, agent_file)
                rel = os.path.relpath(agent_path, REPO_ROOT).replace(os.sep, "/")
                title = extract_title(agent_path) or prettify(agent_name)
                title = re.sub(r"[*_`]", "", title)
                if re.match(r"^cs-[a-z-]+$", title):
                    title = prettify(title.removeprefix("cs-"))

                with open(agent_path, "r", encoding="utf-8") as f:
                    content = f.read()

                content_clean = strip_content(content)
                content_clean = rewrite_relative_links(content_clean, rel)
                content_clean = rewrite_remaining_links(content_clean, os.path.dirname(rel))

                agent_seo_title = f"{title} — AI Coding Agent & Codex Skill"
                agent_fm_desc = extract_description_from_frontmatter(agent_path)
                if agent_fm_desc:
                    agent_clean = agent_fm_desc.strip("'\"").replace('"', "'")
                    if len(agent_clean) > 150:
                        agent_clean = agent_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                    agent_desc = f"{agent_clean}. Agent-native orchestrator for Claude Code, Codex, Gemini CLI."
                else:
                    agent_desc = f"{title} — agent-native AI orchestrator for {domain_label}. Works with Claude Code, Codex CLI, Gemini CLI, and OpenClaw."

                page = f'''---
title: "{agent_seo_title}"
description: "{agent_desc}"
edit_source: "{rel}"
search:
  boost: 0.5
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Agent</span>
<span class="meta-badge">{domain_icon} {domain_label}</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/{rel}">Source</a></span>
</div>

{content_clean}'''
                out_path = os.path.join(agents_docs_dir, f"{slug}.md")
                write_if_changed(out_path, page)
                agent_count += 1
                agent_entries.append((title, slug, domain_label, domain_icon))
                seen_slugs.add(slug)

    # Generate agents index
    if agent_entries:
        agent_cards = ""
        for title, slug, domain, icon in agent_entries:
            agent_cards += f"""
-   {icon}{{ .lg .middle }} **[{title}]({slug}.md)**

    ---

    {domain}
"""

        idx = f'''---
title: "AI Coding Agents — Agent-Native Orchestrators & Codex Skills"
description: "{agent_count} agent-native orchestrators for Claude Code, Codex CLI, and Gemini CLI — multi-skill AI agents across engineering, product, marketing, and more."
---

<div class="domain-header" markdown>

# :material-robot: Agents

<p class="domain-count">{agent_count} agents that orchestrate skills across domains</p>

</div>

<div class="grid cards" markdown>
{agent_cards}
</div>
'''
        write_if_changed(os.path.join(agents_docs_dir, "index.md"), idx)

    # Generate command pages
    commands_dir = os.path.join(REPO_ROOT, "commands")
    commands_docs_dir = os.path.join(DOCS_DIR, "commands")
    os.makedirs(commands_docs_dir, exist_ok=True)
    cmd_count = 0
    cmd_entries = []

    if os.path.isdir(commands_dir):
        for cmd_file in sorted(os.listdir(commands_dir)):
            if not cmd_file.endswith(".md") or cmd_file == "CLAUDE.md":
                continue
            cmd_name = cmd_file.replace(".md", "")
            cmd_path = os.path.join(commands_dir, cmd_file)
            rel = os.path.relpath(cmd_path, REPO_ROOT).replace(os.sep, "/")
            title = extract_title(cmd_path) or prettify(cmd_name)
            title = re.sub(r"[*_`]", "", title)

            with open(cmd_path, "r", encoding="utf-8") as f:
                content = f.read()

            content_clean = strip_content(content)
            content_clean = rewrite_relative_links(content_clean, rel)
            content_clean = rewrite_remaining_links(content_clean, os.path.dirname(rel))

            cmd_fm_desc = extract_description_from_frontmatter(cmd_path)
            if cmd_fm_desc:
                cmd_clean = cmd_fm_desc.strip("'\"").replace('"', "'")
                if len(cmd_clean) > 150:
                    cmd_clean = cmd_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                cmd_desc = f"{cmd_clean}. Slash command for Claude Code, Codex CLI, Gemini CLI."
            else:
                cmd_desc = f"/{cmd_name} — slash command for Claude Code, Codex CLI, and Gemini CLI. Run directly in your AI coding agent."

            page = f'''---
title: "/{cmd_name} — Slash Command for AI Coding Agents"
description: "{cmd_desc}"
edit_source: "{rel}"
search:
  boost: 0.5
---

# /{cmd_name}

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/{rel}">Source</a></span>
</div>

{content_clean}'''
            slug = slugify(cmd_name)
            out_path = os.path.join(commands_docs_dir, f"{slug}.md")
            write_if_changed(out_path, page)
            cmd_count += 1
            desc = extract_subtitle(cmd_path) or title
            cmd_entries.append((cmd_name, slug, title, desc))

    # Pass 2: domain-level and skill-internal commands/ folders.
    # Patterns:
    #   <domain>/commands/<cmd>.md         — v2.8.0 (business-operations, commercial)
    #   <domain>/<skill>/commands/<cmd>.md — v2.7.0 (productivity, research, marketing top-level)
    seen_cmd_slugs = {entry[1] for entry in cmd_entries}
    extra_cmd_dirs = []
    for skill_domain in DOMAINS:
        skill_domain_path = os.path.join(REPO_ROOT, skill_domain)
        if not os.path.isdir(skill_domain_path):
            continue
        # v2.8.0 pattern: <domain>/commands/
        domain_cmds = os.path.join(skill_domain_path, "commands")
        if os.path.isdir(domain_cmds):
            extra_cmd_dirs.append(domain_cmds)
        # v2.7.0 pattern: <domain>/<skill>/commands/
        for entry in sorted(os.listdir(skill_domain_path)):
            if entry in {"skills", "agents", "commands", ".claude-plugin", ".codex-plugin"}:
                continue
            skill_cmds = os.path.join(skill_domain_path, entry, "commands")
            if os.path.isdir(skill_cmds):
                extra_cmd_dirs.append(skill_cmds)

    for cmd_dir in extra_cmd_dirs:
        for cmd_file in sorted(os.listdir(cmd_dir)):
            if not cmd_file.endswith(".md") or cmd_file == "CLAUDE.md":
                continue
            cmd_name = cmd_file.replace(".md", "")
            slug = slugify(cmd_name)
            if slug in seen_cmd_slugs:
                continue
            cmd_path = os.path.join(cmd_dir, cmd_file)
            rel = os.path.relpath(cmd_path, REPO_ROOT).replace(os.sep, "/")
            title = extract_title(cmd_path) or prettify(cmd_name)
            title = re.sub(r"[*_`]", "", title)

            with open(cmd_path, "r", encoding="utf-8") as f:
                content = f.read()

            content_clean = strip_content(content)
            content_clean = rewrite_relative_links(content_clean, rel)
            content_clean = rewrite_remaining_links(content_clean, os.path.dirname(rel))

            cmd_fm_desc = extract_description_from_frontmatter(cmd_path)
            if cmd_fm_desc:
                cmd_clean = cmd_fm_desc.strip("'\"").replace('"', "'")
                if len(cmd_clean) > 150:
                    cmd_clean = cmd_clean[:150].rsplit(" ", 1)[0].rstrip(".,;:—-")
                cmd_desc = f"{cmd_clean}. Slash command for Claude Code, Codex CLI, Gemini CLI."
            else:
                cmd_desc = f"/{cmd_name} — slash command for Claude Code, Codex CLI, and Gemini CLI. Run directly in your AI coding agent."

            page = f'''---
title: "/{cmd_name} — Slash Command for AI Coding Agents"
description: "{cmd_desc}"
edit_source: "{rel}"
search:
  boost: 0.5
---

# /{cmd_name}

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/{rel}">Source</a></span>
</div>

{content_clean}'''
            out_path = os.path.join(commands_docs_dir, f"{slug}.md")
            write_if_changed(out_path, page)
            cmd_count += 1
            seen_cmd_slugs.add(slug)
            desc = extract_subtitle(cmd_path) or title
            cmd_entries.append((cmd_name, slug, title, desc))

    # Generate commands index
    if cmd_entries:
        cmd_cards = ""
        for name, slug, title, desc in cmd_entries:
            desc_clean = re.sub(r"[*_`\[\]]", "", desc)
            if len(desc_clean) > 120:
                desc_clean = desc_clean[:117] + "..."
            cmd_cards += f"""
-   :material-console:{{ .lg .middle }} **[`/{name}`]({slug}.md)**

    ---

    {desc_clean}
"""

        idx = f'''---
title: "Slash Commands — AI Coding Agent Commands & Codex Shortcuts"
description: "{cmd_count} slash commands for Claude Code, Codex CLI, and Gemini CLI — sprint planning, tech debt analysis, PRDs, OKRs, and more."
---

<div class="domain-header" markdown>

# :material-console: Slash Commands

<p class="domain-count">{cmd_count} commands for quick access to common operations</p>

</div>

<div class="grid cards" markdown>
{cmd_cards}
</div>
'''
        write_if_changed(os.path.join(commands_docs_dir, "index.md"), idx)

    # Print summary
    print(f"Generated {total} skill pages across {len(skills_by_domain)} domains.")
    print(f"Generated {agent_count} agent pages.")
    print(f"Generated {cmd_count} command pages.")
    print(f"Total: {total + agent_count + cmd_count} pages.")
    return {"agents": agent_entries, "commands": cmd_entries, "skill_pages": total}


if __name__ == "__main__":
    parse_args()
    main()
