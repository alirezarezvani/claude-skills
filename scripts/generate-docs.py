#!/usr/bin/env python3
"""Generate MkDocs documentation pages from SKILL.md files, agents, and commands."""

import os
import re
import shutil

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
}

# Skills to skip (nested assets, samples, etc.)
SKIP_PATTERNS = [
    "assets/sample-skill",
    "medium-content-pro 2",  # duplicate with space
]


def find_skill_files():
    """Walk the repo and find all SKILL.md files, grouped by domain."""
    skills = {}
    for root, dirs, files in os.walk(REPO_ROOT):
        if "SKILL.md" not in files:
            continue
        rel_path = os.path.relpath(root, REPO_ROOT)
        if any(skip in rel_path for skip in SKIP_PATTERNS):
            continue
        # Determine domain
        parts = rel_path.split(os.sep)
        domain_key = parts[0]
        if domain_key not in DOMAINS:
            continue
        skill_name = parts[-1]  # last directory component
        skill_path = os.path.join(root, "SKILL.md")
        # Determine nesting (e.g., playwright-pro/skills/generate)
        is_sub_skill = len(parts) > 2
        parent = parts[1] if len(parts) > 2 else None

        if domain_key not in skills:
            skills[domain_key] = []
        skills[domain_key].append({
            "name": skill_name,
            "path": skill_path,
            "rel_path": rel_path,
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


def extract_description_from_frontmatter(filepath):
    """Extract the description field from YAML frontmatter."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.match(r"^---\n(.*?)---\n", content, re.DOTALL)
        if match:
            fm = match.group(1)
            desc_match = re.search(r'description:\s*["\']?(.*?)["\']?\s*$', fm, re.MULTILINE)
            if desc_match:
                return desc_match.group(1).strip()
    except Exception:
        pass
    return None


def slugify(name):
    """Convert a skill name to a URL-friendly slug."""
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


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


def rewrite_relative_links(content, source_rel_path):
    """Rewrite relative markdown links (../../, ../) to absolute GitHub URLs.

    Agent and command source files use relative paths like ../../product-team/SKILL.md
    which break when rendered in the docs site. Convert them to GitHub source links.
    """
    source_dir = os.path.dirname(source_rel_path)

    def resolve_link(match):
        text = match.group(1)
        rel_target = match.group(2)
        # Only rewrite relative paths that go up (../)
        if not rel_target.startswith("../"):
            return match.group(0)
        # Resolve against source directory
        resolved = os.path.normpath(os.path.join(source_dir, rel_target))
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

    content = re.sub(r"\[([^\]]+)\]\((\.\.[^\)]+)\)", resolve_link, content)

    # Also rewrite backtick code references like `../../product-team/foo/SKILL.md`
    # Convert to clickable GitHub links
    def resolve_backtick(match):
        rel_target = match.group(1)
        if not rel_target.startswith("../"):
            return match.group(0)
        resolved = os.path.normpath(os.path.join(source_dir, rel_target))
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
    # Clean title of markdown artifacts
    title = re.sub(r"[*_`]", "", title)

    domain_name, _, domain_icon, plugin_name = DOMAINS[domain_key]
    description = f"{title} - Claude Code skill from the {domain_name} domain."
    subtitle = extract_subtitle(skill_md_path) or ""
    # Clean subtitle of markdown artifacts for the intro
    subtitle_clean = re.sub(r"[*_`\[\]]", "", subtitle)

    # Build the page with design system
    page = f'''---
title: "{title}"
description: "{description}"
---

# {title}

<div class="page-meta" markdown>
<span class="meta-badge">{domain_icon} {domain_name}</span>
<span class="meta-badge">:material-identifier: `{skill["name"]}`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/{skill["rel_path"]}/SKILL.md">Source</a></span>
</div>

'''
    # Add install banner
    page += f'''<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install {plugin_name}</code>
</div>

'''

    content_clean = strip_content(content)
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


def main():
    skills_by_domain = find_skill_files()

    # Create docs/skills/ directories
    for domain_key in skills_by_domain:
        os.makedirs(os.path.join(DOCS_DIR, "skills", domain_key), exist_ok=True)

    total = 0
    # Generate individual skill pages
    for domain_key, skills in skills_by_domain.items():
        top_level = [s for s in skills if not s["is_sub_skill"]]
        sub_skills = [s for s in skills if s["is_sub_skill"]]

        for skill in top_level:
            slug = slugify(skill["name"])
            page_content = generate_skill_page(skill, domain_key)
            page_path = os.path.join(DOCS_DIR, "skills", domain_key, f"{slug}.md")
            with open(page_path, "w", encoding="utf-8") as f:
                f.write(page_content)
            total += 1

            # Generate sub-skill pages
            children = [s for s in sub_skills if s["parent"] == skill["name"]]
            for child in children:
                child_slug = slugify(child["name"])
                child_content = generate_skill_page(child, domain_key)
                child_path = os.path.join(DOCS_DIR, "skills", domain_key, f"{slug}-{child_slug}.md")
                with open(child_path, "w", encoding="utf-8") as f:
                    f.write(child_content)
                total += 1

    # Generate domain index pages
    sorted_domains = sorted(skills_by_domain.items(), key=lambda x: DOMAINS[x[0]][1])
    for domain_key, skills in sorted_domains:
        domain_name, _, domain_icon, plugin_name = DOMAINS[domain_key]
        top_level = sorted([s for s in skills if not s["is_sub_skill"]], key=lambda s: s["name"])
        sub_skills = [s for s in skills if s["is_sub_skill"]]
        skill_count = len(skills)

        # Build grid cards for skills
        cards = ""
        for skill in top_level:
            slug = slugify(skill["name"])
            title = extract_title(skill["path"]) or prettify(skill["name"])
            title = re.sub(r"[*_`]", "", title)
            subtitle = extract_subtitle(skill["path"]) or f"`{skill['name']}`"
            subtitle = re.sub(r"[*_`\[\]]", "", subtitle)
            # Truncate long subtitles
            if len(subtitle) > 120:
                subtitle = subtitle[:117] + "..."
            children = sorted([s for s in sub_skills if s["parent"] == skill["name"]], key=lambda s: s["name"])
            sub_count = len(children)
            sub_text = f" + {sub_count} sub-skills" if sub_count > 0 else ""

            cards += f"""
-   **[{title}]({slug}.md)**{sub_text}

    ---

    {subtitle}
"""

        index_content = f'''---
title: "{domain_name} Skills"
description: "All {skill_count} {domain_name} skills for Claude Code, Codex CLI, Gemini CLI, and OpenClaw."
---

<div class="domain-header" markdown>

# {domain_icon} {domain_name}

<p class="domain-count">{skill_count} skills in this domain</p>

</div>

<div class="install-banner" markdown>
<span class="install-label">Install all:</span> <code>claude /plugin install {plugin_name}</code>
</div>

<div class="grid cards" markdown>
{cards}
</div>
'''

        index_path = os.path.join(DOCS_DIR, "skills", domain_key, "index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)

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
                rel = os.path.relpath(agent_path, REPO_ROOT)
                title = extract_title(agent_path) or prettify(agent_name)
                title = re.sub(r"[*_`]", "", title)

                with open(agent_path, "r", encoding="utf-8") as f:
                    content = f.read()

                content_clean = strip_content(content)
                content_clean = rewrite_relative_links(content_clean, rel)

                page = f'''---
title: "{title}"
description: "{title} - Claude Code agent for {domain_label}."
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
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(page)
                agent_count += 1
                agent_entries.append((title, slug, domain_label, domain_icon))

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
title: "Agents"
description: "All {agent_count} Claude Code agents — multi-skill orchestrators across domains."
---

<div class="domain-header" markdown>

# :material-robot: Agents

<p class="domain-count">{agent_count} agents that orchestrate skills across domains</p>

</div>

<div class="grid cards" markdown>
{agent_cards}
</div>
'''
        with open(os.path.join(agents_docs_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(idx)

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
            rel = os.path.relpath(cmd_path, REPO_ROOT)
            title = extract_title(cmd_path) or prettify(cmd_name)
            title = re.sub(r"[*_`]", "", title)

            with open(cmd_path, "r", encoding="utf-8") as f:
                content = f.read()

            content_clean = strip_content(content)
            content_clean = rewrite_relative_links(content_clean, rel)

            page = f'''---
title: "/{cmd_name}"
description: "/{cmd_name} — Claude Code slash command."
---

# /{cmd_name}

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/{rel}">Source</a></span>
</div>

{content_clean}'''
            slug = slugify(cmd_name)
            out_path = os.path.join(commands_docs_dir, f"{slug}.md")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            cmd_count += 1
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
title: "Commands"
description: "All {cmd_count} slash commands for quick access to common operations."
---

<div class="domain-header" markdown>

# :material-console: Slash Commands

<p class="domain-count">{cmd_count} commands for quick access to common operations</p>

</div>

<div class="grid cards" markdown>
{cmd_cards}
</div>
'''
        with open(os.path.join(commands_docs_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(idx)

    # Print summary
    print(f"Generated {total} skill pages across {len(skills_by_domain)} domains.")
    print(f"Generated {agent_count} agent pages.")
    print(f"Generated {cmd_count} command pages.")
    print(f"Total: {total + agent_count + cmd_count} pages.")


if __name__ == "__main__":
    main()
