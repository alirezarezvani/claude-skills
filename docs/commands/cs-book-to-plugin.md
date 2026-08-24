---
title: "/cs-book-to-plugin — Slash Command for AI Coding Agents"
description: "/cs:book-to-plugin <compiled-skill-dir> [--domain <domain>] — wrap a compiled book skill in a claude-skills plugin package (manifest + cs-* agent +. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-book-to-plugin

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/book-to-skill/commands/cs-book-to-plugin.md">Source</a></span>
</div>


**Command:** `/cs:book-to-plugin <compiled-skill-dir> [--domain <domain>] [--rights <basis>]`

A folder in `~/.claude/skills/` is invisible to this repository: no manifest, no agent, no
command, no marketplace entry, so nothing else in the library can route to it. This command
closes that gap.

## What it emits

```
<domain>/<slug>/
├── .claude-plugin/plugin.json     manifest, ./skills/<slug>, provenance + rights metadata
├── README.md                      what the skill knows, where it came from, its limits
├── agents/cs-<slug>.md            persona that answers from the source and cites chapters
├── commands/cs-<slug>.md          /cs:<slug> [topic | framework | chNN]
└── skills/<slug>/                 the compiled skill, copied verbatim
```

…then prints the `.claude-plugin/marketplace.json` entry to register. It never edits
marketplace.json itself — registration is a repo-wide change and stays a human decision.

## Gates

| Gate | Behaviour |
|------|-----------|
| Source has no `SKILL.md` | Refuses. This is not a compiled book skill. |
| Source has validation errors | Refuses and lists them. A package built on a broken index stays broken. `--skip-validation` overrides, and is almost always the wrong call. |
| Destination already exists | Refuses without `--force`. |
| `--distribution shareable` without `--rights` | **Refuses.** Compiled notes from a copyrighted work are personal study notes; redistributing them needs a basis. |

Accepted rights bases: `public-domain`, `open-license`, `internal-docs`, `author-permission`.
Fair use is deliberately not one — it is a defence, not a licence, and not a script's call.
Without a basis the package emits as `--distribution local` and records
`source.cleared_for_distribution: false` in the manifest.

## Run

```bash
SKILL_ROOT=engineering/book-to-skill/skills/book-to-skill

# see exactly what would be written, first
python3 "$SKILL_ROOT/scripts/skill_plugin_emitter.py" \
    --skill-dir ~/.claude/skills/<slug> \
    --dest ./engineering --domain engineering \
    --source-note "<Full Title> by <Author>" \
    --dry-run

# write it
python3 "$SKILL_ROOT/scripts/skill_plugin_emitter.py" \
    --skill-dir ~/.claude/skills/<slug> \
    --dest ./engineering --domain engineering \
    --source-note "<Full Title> by <Author>"
```

## After emitting

1. Paste the printed entry into `.claude-plugin/marketplace.json` → `plugins`.
2. Re-derive the headline counters: `python3 scripts/derive_counters.py --check`, then update
   `README.md`, `CLAUDE.md` and the marketplace description to match.
3. Read the generated agent and command — they are scaffolds keyed to the source, and the
   voice is worth a pass by hand.
4. Open the PR against `dev`. Never `main`.

## Related

- `/cs:book-to-skill` — compile the source in the first place
- `/cs:plugin-audit` — 8-phase audit of the emitted package before merge
