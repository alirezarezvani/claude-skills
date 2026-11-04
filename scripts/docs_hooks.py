"""MkDocs hooks that keep the docs site in sync with the repository.

Registered in mkdocs.yml under `hooks:`. Everything a visitor reads as a number
or a list is computed here from the tree at build time, so the site cannot
drift from the repo:

- on_config: runs scripts/generate-docs.py (skill, agent and command pages),
  builds the Skills, Agents and Commands nav from what it generated, and fills
  counter tokens in site_description.
- on_page_markdown: fills tokens in hand-written pages ({{ count.skills }},
  {{ plugin_table }}, {{ whats_new }}) and points the edit button of generated
  pages at the source file they were rendered from.
- on_post_build: fills the same counter tokens in llms.txt / llms-full.txt.

Tokens are only expanded in hand-written pages (pages without `edit_source`),
so a skill whose own text contains `{{ ... }}` is never touched.
"""

import importlib.util
import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GITHUB = "https://github.com/alirezarezvani/claude-skills"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import derive_counters  # noqa: E402


def _load_generator():
    spec = importlib.util.spec_from_file_location("generate_docs", REPO_ROOT / "scripts" / "generate-docs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GEN = _load_generator()
TOKEN_RE = re.compile(r"\{\{\s*([a-z_]+(?:\.[a-z0-9_-]+)*)\s*\}\}")
_state = {}


def _latest_release():
    text = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", text, re.M)
    return m.group(1) if m else "unknown"


def _counters():
    d = derive_counters.derive(REPO_ROOT)
    values = {
        "count.skills": str(d["skills"]),
        "count.plugins": str(d["plugins_registered"]),
        "count.tools": str(d["python_tools"]),
        "count.references": str(d["references"]),
        "count.agents": str(d["agents"]),
        "count.commands": str(d["commands"]),
        "count.domains": str(d["domains"]),
        "count.version": _latest_release(),
    }
    for domain, n in derive_counters.derive_per_domain(REPO_ROOT).items():
        values[f"count.in.{domain}"] = str(n)
    per_domain = derive_counters.derive_per_domain(REPO_ROOT)
    bundles = [p for p in GEN.PLUGINS if "/" not in p["dir"] and per_domain.get(p["dir"], 0) > 1]
    values["count.bundles"] = str(len(bundles))
    values["count.standalone"] = str(len(GEN.PLUGINS) - len(bundles))
    for harness in ("hermes", "vibe"):
        mirror = REPO_ROOT / f".{harness}" / "skills" / "claude-skills"
        values[f"count.{harness}"] = str(sum(1 for _ in mirror.glob("*/*/SKILL.md")))
    for harness in ("codex", "gemini"):
        index = REPO_ROOT / f".{harness}" / "skills-index.json"
        values[f"count.{harness}"] = str(json.loads(index.read_text(encoding="utf-8"))["total_skills"])
    return values


def _plugin_table():
    rows = ["| Plugin | Category | What it does | Install |", "|---|---|---|---|"]
    for p in sorted(GEN.PLUGINS, key=lambda p: (p.get("category", ""), p["name"])):
        desc = re.sub(r"\s+", " ", p.get("description", "")).replace("|", "\\|")
        if len(desc) > 160:
            desc = desc[:157].rsplit(" ", 1)[0] + "..."
        rows.append(
            f"| [`{p['name']}`]({GITHUB}/tree/main/{p['dir']}) | {p.get('category', '')} | {desc} "
            f"| `/plugin install {p['name']}@{GEN.MARKETPLACE_NAME}` |")
    return "\n".join(rows)


def _whats_new(limit=5):
    """The last `limit` released CHANGELOG sections, headings demoted one level."""
    text = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(?=## \[\d+\.\d+\.\d+\])", text)
    releases = [p for p in parts if re.match(r"## \[\d", p)][:limit]
    out = []
    for rel in releases:
        rel = re.sub(r"(?m)^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", rel.strip())
        rel = re.sub(r"\(#(\d+)\)", lambda m: f"([#{m.group(1)}]({GITHUB}/pull/{m.group(1)}))", rel)
        out.append(rel)
    out.append(f"\nOlder releases: [CHANGELOG.md]({GITHUB}/blob/main/CHANGELOG.md).")
    return "\n\n".join(out)


def _expand(text):
    values = _state["values"]

    def sub(m):
        key = m.group(1)
        if key in values:
            return values[key]
        if key == "plugin_table":
            return _plugin_table()
        if key == "whats_new":
            return _whats_new()
        return m.group(0)

    return TOKEN_RE.sub(sub, text)


def on_config(config, **kwargs):
    _state["values"] = _counters()
    result = GEN.main()
    generated = GEN.build_nav(result)
    nav = config.get("nav") or []
    for i, entry in enumerate(nav):
        if isinstance(entry, dict):
            (key, value), = entry.items()
            if key in generated:
                # Hand-written entries after the Overview stub (e.g. Personas under
                # Agents) stay, placed right after the generated Overview.
                extra = [e for e in (value if isinstance(value, list) else [])
                         if not (isinstance(e, dict) and "Overview" in e)]
                gen = generated[key]
                nav[i] = {key: gen[:1] + extra + gen[1:]}
    config["nav"] = nav
    if config.get("site_description"):
        config["site_description"] = _expand(config["site_description"])
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    source = page.meta.get("edit_source")
    if source:
        page.edit_url = f"{GITHUB}/edit/dev/{source}"
        return markdown
    for key in ("title", "description"):
        if isinstance(page.meta.get(key), str):
            page.meta[key] = _expand(page.meta[key])
    return _expand(markdown)


def on_post_build(config, **kwargs):
    site = Path(config["site_dir"])
    for name in ("llms.txt", "llms-full.txt"):
        path = site / name
        if path.exists():
            path.write_text(_expand(path.read_text(encoding="utf-8")), encoding="utf-8")
