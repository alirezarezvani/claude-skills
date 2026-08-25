#!/usr/bin/env python3
"""skill_plugin_emitter.py — wrap a generated book skill in a claude-skills plugin.

The upstream converter stops at a bare skill folder in a personal skills home
(`~/.claude/skills/<slug>/`). That folder is invisible to this repository: it
has no plugin manifest, no `cs-*` agent, no `/cs:*` command, and no marketplace
entry, so nothing else in the library can route to it.

This tool closes that gap. Point it at a generated book skill and it emits the
plugin package this repo's conventions require:

    <domain>/<slug>/
    ├── .claude-plugin/plugin.json     manifest, spec fields only (no `source`)
    ├── .claude-plugin/authoring-notes.json   provenance the manifest may not carry
    ├── README.md                      what the skill knows and where it came from
    ├── agents/cs-<slug>.md            persona that answers from the book
    ├── commands/cs-<slug>.md          /cs:<slug> entry point
    └── skills/<slug>/                 the generated skill, copied verbatim

and prints the marketplace.json entry to paste into `.claude-plugin/`. It never
edits marketplace.json itself — registration is a repo-wide change and stays a
human decision.

Rights gate: a book skill built from a copyrighted work is personal study
notes. `--distribution shareable` therefore refuses to emit unless `--rights`
names a basis that permits redistribution. `--distribution local` (the default)
emits with a notice and records `source.cleared_for_distribution: false`
in `authoring-notes.json`. Provenance never goes in `plugin.json`: Claude Code
rejects the whole manifest on any unrecognized key (issue #954).

Exit codes:
    0  package emitted (or --dry-run / --sample completed)
    1  refused: rights gate, existing destination, or unusable source skill
    2  bad invocation

Usage:
    python3 skill_plugin_emitter.py --skill-dir ~/.claude/skills/meadows-systems \\
        --dest ./engineering --domain engineering
    python3 skill_plugin_emitter.py --skill-dir ./ddia --dest ./engineering \\
        --distribution shareable --rights public-domain
    python3 skill_plugin_emitter.py --sample
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_skill_validator import (  # noqa: E402
    ScanError,
    parse_frontmatter,
    scalar_value,
    validate,
)

# Bases that permit redistributing a derived knowledge base. "fair-use" is
# deliberately absent: it is a defence, not a licence, and it is not this
# script's call to make.
RIGHTS_BASES = {
    "public-domain": "the source work is in the public domain",
    "open-license": "the source work carries a licence permitting derivative distribution",
    "internal-docs": "the source is the organisation's own documentation",
    "author-permission": "the rights holder gave written permission",
}
DEFAULT_DOMAIN = "engineering"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class EmitError(RuntimeError):
    """The plugin package could not be emitted."""


def _scalar(frontmatter: str, key: str) -> str:
    return scalar_value(frontmatter, key) or ""


def read_skill_identity(skill_dir: Path) -> dict:
    """Pull slug, description, title and chapter count out of the generated skill."""
    master = skill_dir / "SKILL.md"
    if not master.is_file():
        raise EmitError(f"{skill_dir} has no SKILL.md — this is not a generated book skill")
    text = master.read_text(encoding="utf-8-sig")
    frontmatter, body = parse_frontmatter(text)
    if frontmatter is None:
        raise EmitError("SKILL.md has no YAML frontmatter; run book_skill_validator.py first")

    heading = next((line[2:].strip() for line in body.splitlines() if line.startswith("# ")), "")
    chapters = sorted((skill_dir / "chapters").glob("*.md")) if (skill_dir / "chapters").is_dir() else []
    return {
        "slug": _scalar(frontmatter, "name") or skill_dir.name,
        "description": _scalar(frontmatter, "description"),
        "title": heading or skill_dir.name,
        "chapters": len(chapters),
    }


def _assert_replaceable(package_root: Path, dest_root: Path, skill_dir: Path) -> None:
    """Refuse to recursively delete anything that is not a plugin package we own.

    ``--force`` reaches a ``shutil.rmtree``, so every assumption behind that call
    is checked here rather than trusted: the target must be a real directory (not
    a symlink pointing elsewhere), must live directly under the resolved
    destination, must not contain the source skill being copied from, and must
    look like a plugin package rather than an arbitrary folder that happens to
    share the slug's name.
    """
    if package_root.is_symlink():
        raise EmitError(f"{package_root} is a symbolic link — refusing to replace it")
    if not package_root.is_dir():
        raise EmitError(f"{package_root} exists and is not a directory — refusing to replace it")

    resolved = package_root.resolve()
    if resolved.parent != dest_root:
        raise EmitError(f"{package_root} resolves outside {dest_root} — refusing to replace it")
    if resolved == dest_root or resolved.parent == resolved:
        raise EmitError("refusing to replace a filesystem root or the destination itself")

    source = skill_dir.resolve()
    if resolved == source or resolved in source.parents:
        raise EmitError(
            f"{package_root} contains the source skill being copied from — refusing to "
            f"delete the input"
        )

    manifest = resolved / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        raise EmitError(
            f"{package_root} exists but has no .claude-plugin/plugin.json, so it is not a "
            f"plugin package this tool created. Move it aside by hand rather than passing "
            f"--force."
        )


def _assert_no_symlinks(skill_dir: Path) -> None:
    """Refuse to package a source tree containing any symbolic link.

    The validator checks the files it knows about — SKILL.md, the three
    supporting files, chapters/*.md — but `shutil.copytree` defaults to
    `symlinks=False`, which follows a link *anywhere else* in the tree (an
    `assets/` entry, an arbitrary subdirectory) and bakes the target's real
    content into the emitted package. That package can then go out as
    `--distribution shareable`, so a link pointing at something outside the
    skill becomes part of a published artifact.

    Refusing beats `copytree(symlinks=True)`: preserving the link would ship a
    package whose contents depend on the emitting machine's filesystem. This
    check runs even under `--skip-validation`, which otherwise disables the
    file-level symlink checks entirely.
    """
    offenders = [p for p in sorted(skill_dir.rglob("*")) if p.is_symlink()]
    if offenders:
        listed = "\n".join(f"  {p.relative_to(skill_dir).as_posix()} -> {os.readlink(p)}"
                           for p in offenders[:10])
        more = f"\n  ... and {len(offenders) - 10} more" if len(offenders) > 10 else ""
        raise EmitError(
            f"source skill contains {len(offenders)} symbolic link(s); packaging would copy "
            f"the target's content into a distributable package:\n{listed}{more}\n"
            "Replace them with real files, or point --skill-dir at a tree without links."
        )


def _plugin_manifest(identity: dict, *, domain: str, author: str, author_url: str,
                     repository: str) -> dict:
    # Spec fields ONLY. Claude Code's manifest validator rejects the whole
    # plugin.json on any unrecognized key (issue #954), and the repo's own gate
    # (scripts/check_plugin_json.py) hard-fails a manifest carrying `source` or
    # `attribution`. Provenance therefore goes to the sidecar file the validator
    # never reads — see _authoring_notes below.
    return {
        "name": identity["slug"],
        "description": identity["description"],
        "version": "1.0.0",
        "author": {"name": author, "url": author_url},
        "homepage": f"{repository}/tree/main/{domain}/{identity['slug']}",
        "repository": repository,
        # Covers this package's scaffolding — manifest, agent, command, README —
        # NOT the compiled notes under skills/, whose terms follow the source
        # document. Stated in `source.license_scope` too, so a tool reading only
        # the manifest sees the distinction that README.md makes in prose.
        "license": "MIT",
        "skills": [f"./skills/{identity['slug']}"],
    }


def _authoring_notes(identity: dict, *, distribution: str, rights: str | None,
                     source_note: str) -> dict:
    """Provenance for `.claude-plugin/authoring-notes.json`.

    The repo's schema allows exactly two keys here, `source` and `attribution`;
    a generated skill's provenance is a `source` block. This file is authoring
    metadata that Claude Code's manifest validator never reads, which is
    precisely why the fields live here rather than in plugin.json.
    """
    source = {
        "spec": "generated by engineering/book-to-skill",
        "build_pattern": "book-to-skill conversion: extract -> analyze -> chapter files "
                         "+ glossary + patterns + cheatsheet -> master SKILL.md",
        "distinct_from": "not a hand-authored skill; every claim traces to the source "
                         "document named below",
        "source_document": source_note or identity["title"],
        "chapters": identity["chapters"],
        "distribution": distribution,
        "license_scope": (
            "plugin.json's top-level `license` covers this package's scaffolding only. "
            "The compiled notes under skills/ are derived from the source document and "
            "carry that work's terms; see source.rights_basis."
        ),
    }
    if rights:
        source["rights_basis"] = rights
        source["rights_note"] = RIGHTS_BASES[rights]
    if distribution == "local":
        # A local package is study notes from a work the user owns. The flag is
        # advisory metadata, not enforcement — it exists so a later publish step
        # (or a reviewer) can see the package was never cleared for sharing.
        source["cleared_for_distribution"] = False
    return {"source": source}


def _agent_markdown(identity: dict, domain: str, source_note: str) -> str:
    slug = identity["slug"]
    return f"""---
name: cs-{slug}
description: Answers from the knowledge base compiled from {source_note or identity['title']}. \
Loads the master frameworks first and reads a single chapter file on demand rather than the \
whole source. Refuses to answer beyond what the source covers.
skills: {domain}/{slug}/skills/{slug}
domain: {domain}
model: opus
tools: [Read, Grep, Glob]
---

# {identity['title']} — Knowledge Agent

## Voice

**Opening:** "Which framework or chapter are you reaching for?"
**Forcing question:** "Is this something the source actually covers, or are you asking me to
extrapolate past it?"
**Closing:** "That is the author's formulation, from ch<N>. Anything past it is my inference, not theirs."

## Purpose

Applies the frameworks compiled from **{source_note or identity['title']}** ({identity['chapters']} chapters
indexed) while the user works. Answers with the author's exact naming, then cites the chapter.

## How it navigates

1. Read `skills/{slug}/SKILL.md` — Core Frameworks and both indexes.
2. Match the question against the Topic Index; read **only** the chapter files it points to.
3. Reach for `glossary.md` for a term, `patterns.md` for a technique, `cheatsheet.md` for a decision.
4. Never load every chapter — that is the cost this skill exists to avoid.

## Hard rules

- **Cite the chapter.** Every framework claim names the chapter it came from.
- **Do not extrapolate silently.** If the source does not cover it, say so before answering from
  general knowledge, and label which is which.
- **Preserve exact naming.** The author's term is the interface; a paraphrase breaks lookup.
- **Do not reproduce the source at length.** These are structured notes, not a copy of the work.
"""


def _command_markdown(identity: dict, domain: str, source_note: str) -> str:
    slug = identity["slug"]
    return f"""---
name: "cs-{slug}"
description: "/cs:{slug} [topic | framework | chNN] — query the knowledge base compiled from \
{source_note or identity['title']}. Use when applying its frameworks while working, looking up a \
term, or reading one chapter's summary."
---

# /cs:{slug} — {identity['title']}

**Command:** `/cs:{slug} [topic | framework name | chNN]`

## When to run

- Applying a framework from this source to work in progress
- Looking up the author's exact formulation of a term
- Reading one chapter's compiled summary without opening the source
- Checking whether the source covers a question at all

## What it does

1. Loads `{domain}/{slug}/skills/{slug}/SKILL.md` — Core Frameworks plus the Chapter and Topic indexes.
2. **No argument** → reports the core frameworks and the chapter index.
3. **A topic or framework name** → resolves it through the Topic Index and reads only the
   matching chapter file.
4. **`chNN`** → reads that chapter's summary directly.
5. Answers with the author's naming and cites the chapter.

## Boundary

This command answers from **one source** ({identity['chapters']} chapters indexed). Anything it does not
cover gets said out loud rather than filled in — and hands-on work in your codebase belongs to the
engineering skills, not here.
"""


def _readme_markdown(identity: dict, *, domain: str, distribution: str, rights: str | None,
                     source_note: str) -> str:
    slug = identity["slug"]
    rights_line = (
        f"**Rights basis:** `{rights}` — {RIGHTS_BASES[rights]}."
        if rights else
        "**Rights basis:** not declared. This package is local study notes from a work the "
        "operator owns; it is not cleared for redistribution."
    )
    return f"""# {identity['title']}

Knowledge-base plugin compiled from **{source_note or identity['title']}** by
[`engineering/book-to-skill`](../book-to-skill/). {identity['chapters']} chapters indexed.

## What is in here

| File | Contents |
|------|----------|
| `skills/{slug}/SKILL.md` | Core frameworks, chapter index, topic index (resident, under 4k tokens) |
| `skills/{slug}/chapters/` | One summary per chapter — loaded on demand, never all at once |
| `skills/{slug}/glossary.md` | Every significant term, alphabetized, with its chapter |
| `skills/{slug}/patterns.md` | Techniques and design patterns with trade-offs |
| `skills/{slug}/cheatsheet.md` | Decision rules, thresholds and trade-off matrices |

## Use

```
/cs:{slug}                    # core frameworks + chapter index
/cs:{slug} <topic>            # resolve via topic index, read one chapter
/cs:{slug} ch05               # read one chapter summary
```

Or invoke the `cs-{slug}` agent for a working session anchored to this source.

## Provenance and limits

Generated, not hand-authored: every claim traces to the source document. It carries that source's
blind spots, and it is a set of structured notes — not a copy of the work and not a substitute for
reading it.

{rights_line}

Distribution: `{distribution}`. Regenerate or extend with
`python3 {domain}/book-to-skill/skills/book-to-skill/scripts/extract_document.py`, then re-run
`book_skill_validator.py` before loading the result.
"""


def _marketplace_entry(identity: dict, domain: str, author: str) -> dict:
    """The entry to paste into marketplace.json.

    `author` is threaded through rather than hardcoded: this snippet exists to
    stop hand-editing mistakes, so printing a different name than the manifest
    it accompanies would defeat its own purpose for anyone but the default.
    """
    return {
        "name": identity["slug"],
        "source": f"./{domain}/{identity['slug']}",
        "description": identity["description"],
        "version": "1.0.0",
        "author": {"name": author},
        "keywords": ["knowledge-base", "book-to-skill", domain],
        "category": domain,
    }


def emit(*, skill_dir: Path, dest_root: Path, domain: str, author: str, author_url: str,
         repository: str,
         distribution: str, rights: str | None, source_note: str, slug_override: str | None,
         force: bool, dry_run: bool, skip_validation: bool) -> dict:
    skill_dir = skill_dir.expanduser().resolve()
    identity = read_skill_identity(skill_dir)
    if slug_override:
        identity["slug"] = slug_override
    if not SLUG_RE.fullmatch(identity["slug"]):
        raise EmitError(f"'{identity['slug']}' is not a valid slug (lowercase, digits, single hyphens)")
    if not identity["description"]:
        raise EmitError("SKILL.md frontmatter has no description — the plugin manifest requires one")

    if distribution == "shareable" and not rights:
        raise EmitError(
            "refusing to emit a shareable package without --rights.\n"
            "A skill compiled from a copyrighted work is personal study notes; redistributing it "
            "needs a basis.\n"
            "Choose one of: " + ", ".join(sorted(RIGHTS_BASES)) + "\n"
            "Or emit with --distribution local (the default) to keep it on this machine."
        )

    # Unconditional: --skip-validation waives content findings, never the
    # guarantee that packaging copies only what is actually in the source tree.
    _assert_no_symlinks(skill_dir)

    if not skip_validation:
        try:
            findings = validate(skill_dir)
        except ScanError as exc:
            raise EmitError(f"source skill could not be validated: {exc}") from exc
        errors = [f for f in findings if f.severity == "error"]
        if errors:
            summary = "\n".join(f"  {f.path}:{f.line} ({f.rule_id}) {f.message}" for f in errors)
            raise EmitError(
                f"source skill has {len(errors)} validation error(s); fix them before wrapping "
                f"it in a plugin:\n{summary}\n"
                "(--skip-validation overrides this, but a package built on a broken index stays broken.)"
            )

    resolved_dest = dest_root.expanduser().resolve()
    package_root = resolved_dest / identity["slug"]
    if package_root.exists() and not force:
        raise EmitError(f"{package_root} already exists — pass --force to replace it")
    if package_root.exists():
        _assert_replaceable(package_root, resolved_dest, skill_dir)

    manifest = _plugin_manifest(identity, domain=domain, author=author, author_url=author_url,
                                repository=repository)
    notes = _authoring_notes(identity, distribution=distribution, rights=rights,
                             source_note=source_note)
    files = {
        ".claude-plugin/plugin.json": json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        ".claude-plugin/authoring-notes.json": json.dumps(notes, indent=2, ensure_ascii=False) + "\n",
        "README.md": _readme_markdown(identity, domain=domain, distribution=distribution,
                                      rights=rights, source_note=source_note),
        f"agents/cs-{identity['slug']}.md": _agent_markdown(identity, domain, source_note),
        f"commands/cs-{identity['slug']}.md": _command_markdown(identity, domain, source_note),
    }

    result = {
        "slug": identity["slug"],
        "title": identity["title"],
        "chapters": identity["chapters"],
        "package_root": str(package_root),
        "files": sorted(files) + [f"skills/{identity['slug']}/ (copied from {skill_dir})"],
        "distribution": distribution,
        "rights_basis": rights,
        "dry_run": dry_run,
        "marketplace_entry": _marketplace_entry(identity, domain, author),
    }
    if dry_run:
        return result

    if package_root.exists():
        shutil.rmtree(package_root)
    for relative, text in files.items():
        target = package_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    # symlinks=True is redundant after _assert_no_symlinks, and kept so a future
    # edit that loosens that check cannot silently reintroduce dereferencing. It
    # also bounds the check-then-act window: a link planted between the walk and
    # this copy is copied *as a link*, so no target content is read.
    copied = package_root / "skills" / identity["slug"]
    shutil.copytree(skill_dir, copied, symlinks=True)

    # Close the window properly: re-walk what actually landed. A concurrent
    # writer with access to skill_dir could have planted a link after
    # _assert_no_symlinks ran, and a distributable package must not carry one.
    planted = [p for p in sorted(copied.rglob("*")) if p.is_symlink()]
    if planted:
        shutil.rmtree(package_root)
        listed = "\n".join(f"  {p.relative_to(copied).as_posix()}" for p in planted[:10])
        raise EmitError(
            f"symbolic link(s) appeared in the source tree while it was being copied — "
            f"the package has been removed rather than shipped:\n{listed}\n"
            "Something else is writing to the source directory; re-run once it is quiet."
        )
    return result


SAMPLE_SKILL = {
    "SKILL.md": """---
name: sample-systems-thinking
description: "Knowledge base from \\"A Sample Systems Primer\\" by A. Author. Use when applying
  the author's leverage-point frameworks, studying the book, or referencing its concepts."
---

# A Sample Systems Primer

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-stocks-and-flows.md) | Stocks and Flows | Stock-Flow Model |

## Topic Index

- **Stock-Flow Model** → ch01
""",
    "chapters/ch01-stocks-and-flows.md": "# Chapter 1: Stocks and Flows\n\n## Core Idea\n"
                                         "A stock is what accumulates; a flow is what changes it.\n",
    "glossary.md": "**Stock** — an accumulation measured at a point in time (Ch 1)\n",
    "patterns.md": "## Stock-Flow Model\n**When to use**: modelling accumulation.\n",
    "cheatsheet.md": "| Situation | Do | Because |\n|---|---|---|\n| Stock falling | Raise inflow | Flows set direction |\n",
}


def run_sample(as_json: bool) -> int:
    """Emit a package from a built-in sample skill into a temp folder, then discard it."""
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "sample-systems-thinking"
        (source / "chapters").mkdir(parents=True)
        for relative, text in SAMPLE_SKILL.items():
            (source / relative).write_text(text, encoding="utf-8")
        result = emit(
            skill_dir=source, dest_root=Path(tmp) / "out", domain=DEFAULT_DOMAIN,
            author="Alireza Rezvani", author_url="https://alirezarezvani.com",
            repository="https://github.com/alirezarezvani/claude-skills",
            distribution="local", rights=None, source_note="A Sample Systems Primer",
            slug_override=None, force=False, dry_run=False, skip_validation=False,
        )
        emitted = sorted(
            p.relative_to(Path(tmp) / "out").as_posix()
            for p in (Path(tmp) / "out").rglob("*") if p.is_file()
        )
        result["files"] = emitted
        return _report(result, as_json)


def _report(result: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    verb = "Would emit" if result["dry_run"] else "Emitted"
    print(f"{verb} plugin package: {result['package_root']}")
    print(f"  source   : {result['title']} ({result['chapters']} chapters)")
    print(f"  slug     : {result['slug']}")
    print(f"  sharing  : {result['distribution']}"
          + (f" (rights: {result['rights_basis']})" if result["rights_basis"] else " — not cleared for redistribution"))
    print("  files    :")
    for relative in result["files"]:
        print(f"    {relative}")
    print("\nRegister it by adding this entry to .claude-plugin/marketplace.json `plugins`:\n")
    print(json.dumps(result["marketplace_entry"], indent=2, ensure_ascii=False))
    print("\n(This tool never edits marketplace.json — registration is a repo-wide change.)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skill_plugin_emitter.py",
        description="Wrap a generated book skill in a claude-skills plugin package.",
    )
    parser.add_argument("--skill-dir", help="generated book skill folder (contains SKILL.md)")
    parser.add_argument("--dest", help="domain folder to emit into, e.g. ./engineering")
    parser.add_argument("--domain", default=DEFAULT_DOMAIN,
                        help=f"domain name used in paths and metadata (default: {DEFAULT_DOMAIN})")
    parser.add_argument("--slug", help="override the plugin slug (default: the skill's name)")
    parser.add_argument("--source-note", default="",
                        help="how to name the source document in generated prose")
    parser.add_argument("--author", default="Alireza Rezvani", help="plugin manifest author")
    parser.add_argument("--author-url", default="https://alirezarezvani.com",
                        help="author URL (required by the repo plugin.json schema)")
    parser.add_argument("--repository", default="https://github.com/alirezarezvani/claude-skills",
                        help="repository URL for the manifest")
    parser.add_argument("--distribution", choices=("local", "shareable"), default="local",
                        help="local keeps the package private (default); shareable requires --rights")
    parser.add_argument("--rights", choices=sorted(RIGHTS_BASES),
                        help="basis on which the compiled notes may be redistributed")
    parser.add_argument("--force", action="store_true", help="replace an existing destination")
    parser.add_argument("--dry-run", action="store_true", help="report without writing anything")
    parser.add_argument("--skip-validation", action="store_true",
                        help="emit even if the source skill has validation errors")
    parser.add_argument("--output", choices=("text", "json"), default="text")
    parser.add_argument("--sample", action="store_true",
                        help="emit a package from a built-in sample skill into a temp folder")
    args = parser.parse_args(argv)

    if args.sample:
        return run_sample(args.output == "json")
    if not args.skill_dir or not args.dest:
        parser.print_usage(sys.stderr)
        print("ERROR: --skill-dir and --dest are both required (or use --sample).", file=sys.stderr)
        return 2

    try:
        result = emit(
            skill_dir=Path(args.skill_dir), dest_root=Path(args.dest), domain=args.domain,
            author=args.author, author_url=args.author_url, repository=args.repository,
            distribution=args.distribution,
            rights=args.rights, source_note=args.source_note, slug_override=args.slug,
            force=args.force, dry_run=args.dry_run, skip_validation=args.skip_validation,
        )
    except EmitError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    return _report(result, args.output == "json")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `tool | head` closes the pipe while this is still writing. Exit quietly
        # instead of dumping a traceback: redirect stdout to devnull first so the
        # interpreter's shutdown flush cannot re-raise. 141 = 128 + SIGPIPE.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(141)
