#!/usr/bin/env python3
"""Generate MkDocs documentation pages from SKILL.md files, agents, and commands."""

import os
import re
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

# Domain mapping: directory prefix -> (section name, sort order)
DOMAINS = {
    "engineering-team": ("Engineering - Core", 1),
    "engineering": ("Engineering - POWERFUL", 2),
    "product-team": ("Product", 3),
    "marketing-skill": ("Marketing", 4),
    "project-management": ("Project Management", 5),
    "c-level-advisor": ("C-Level Advisory", 6),
    "ra-qm-team": ("Regulatory & Quality", 7),
    "business-growth": ("Business & Growth", 8),
    "finance": ("Finance", 9),
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


def slugify(name):
    """Convert a skill name to a URL-friendly slug."""
    return re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")


def prettify(name):
    """Convert kebab-case to Title Case."""
    return name.replace("-", " ").title()


def generate_skill_page(skill, domain_key):
    """Generate a docs page for a single skill."""
    skill_md_path = skill["path"]
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title or generate one
    title = extract_title(skill_md_path) or prettify(skill["name"])
    # Clean title of markdown artifacts
    title = re.sub(r"[*_`]", "", title)

    domain_name = DOMAINS[domain_key][0]
    description = f"{title} - Claude Code skill from the {domain_name} domain."

    # Build the page with SEO frontmatter
    page = f"""---
title: "{title}"
description: "{description}"
---

# {title}

**Domain:** {domain_name} | **Skill:** `{skill["name"]}` | **Source:** [`{skill["rel_path"]}/SKILL.md`](https://github.com/alirezarezvani/claude-skills/tree/main/{skill["rel_path"]}/SKILL.md)

---

"""
    # Strip frontmatter from original content and skip the first H1 (we already added it)
    content = re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL)
    # Remove the first H1 if it exists (avoid duplicate)
    content = re.sub(r"^#\s+.+\n", "", content, count=1)
    page += content

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
        domain_name = DOMAINS[domain_key][0]
        top_level = sorted([s for s in skills if not s["is_sub_skill"]], key=lambda s: s["name"])
        sub_skills = [s for s in skills if s["is_sub_skill"]]

        index_content = f"""---
title: "{domain_name} Skills"
description: "All {domain_name} skills for Claude Code, OpenAI Codex, and OpenClaw."
---

# {domain_name} Skills

{len(skills)} skills in this domain.

| Skill | Description |
|-------|-------------|
"""
        for skill in top_level:
            slug = slugify(skill["name"])
            title = extract_title(skill["path"]) or prettify(skill["name"])
            title = re.sub(r"[*_`]", "", title)
            index_content += f"| [{title}]({slug}.md) | `{skill['name']}` |\n"

            children = sorted([s for s in sub_skills if s["parent"] == skill["name"]], key=lambda s: s["name"])
            for child in children:
                child_slug = slugify(child["name"])
                child_title = extract_title(child["path"]) or prettify(child["name"])
                child_title = re.sub(r"[*_`]", "", child_title)
                index_content += f"| &nbsp;&nbsp;[{child_title}]({slug}-{child_slug}.md) | `{child['name']}` (sub-skill of `{skill['name']}`) |\n"

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
        "business-growth": "Business & Growth",
        "c-level": "C-Level Advisory",
        "engineering-team": "Engineering - Core",
        "engineering": "Engineering - POWERFUL",
        "finance": "Finance",
        "marketing": "Marketing",
        "product": "Product",
        "project-management": "Project Management",
        "ra-qm-team": "Regulatory & Quality",
    }

    if os.path.isdir(agents_dir):
        for domain_folder in sorted(os.listdir(agents_dir)):
            domain_path = os.path.join(agents_dir, domain_folder)
            if not os.path.isdir(domain_path):
                continue
            domain_label = AGENT_DOMAINS.get(domain_folder, prettify(domain_folder))
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

                content_clean = re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL)
                content_clean = re.sub(r"^#\s+.+\n", "", content_clean, count=1)

                page = f"""---
title: "{title}"
description: "{title} - Claude Code agent for {domain_label}."
---

# {title}

**Type:** Agent | **Domain:** {domain_label} | **Source:** [`{rel}`](https://github.com/alirezarezvani/claude-skills/tree/main/{rel})

---

{content_clean}"""
                slug = slugify(agent_name)
                out_path = os.path.join(agents_docs_dir, f"{slug}.md")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(page)
                agent_count += 1
                agent_entries.append((title, slug, domain_label))

    # Generate agents index
    if agent_entries:
        idx = f"""---
title: "Agents"
description: "All {agent_count} Claude Code agents — multi-skill orchestrators across domains."
---

# Agents

{agent_count} agents that orchestrate skills across domains.

| Agent | Domain |
|-------|--------|
"""
        for title, slug, domain in agent_entries:
            idx += f"| [{title}]({slug}.md) | {domain} |\n"
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

            content_clean = re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL)
            content_clean = re.sub(r"^#\s+.+\n", "", content_clean, count=1)

            page = f"""---
title: "/{cmd_name}"
description: "/{cmd_name} — Claude Code slash command."
---

# /{cmd_name}

**Type:** Slash Command | **Source:** [`{rel}`](https://github.com/alirezarezvani/claude-skills/tree/main/{rel})

---

{content_clean}"""
            slug = slugify(cmd_name)
            out_path = os.path.join(commands_docs_dir, f"{slug}.md")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(page)
            cmd_count += 1
            desc = extract_subtitle(cmd_path) or title
            cmd_entries.append((cmd_name, slug, title, desc))

    # Generate commands index
    if cmd_entries:
        idx = f"""---
title: "Commands"
description: "All {cmd_count} slash commands for quick access to common operations."
---

# Slash Commands

{cmd_count} commands for quick access to common operations.

| Command | Description |
|---------|-------------|
"""
        for name, slug, title, desc in cmd_entries:
            idx += f"| [`/{name}`]({slug}.md) | {desc} |\n"
        with open(os.path.join(commands_docs_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write(idx)

    # Print summary
    print(f"Generated {total} skill pages across {len(skills_by_domain)} domains.")
    print(f"Generated {agent_count} agent pages.")
    print(f"Generated {cmd_count} command pages.")
    print(f"Total: {total + agent_count + cmd_count} pages.")


if __name__ == "__main__":
    main()
