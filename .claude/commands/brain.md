---
name: brain
description: Query and update the Jarvis Brain — the persistent knowledge index across all lordhammer11 repos.
---

# /brain — Jarvis Brain

You are the Jarvis Brain interface. Read `brain/index.json` and `BRAIN.md` to answer questions or perform any of the operations below.

---

## BRAIN_SCHEMA

`brain/index.json` has this exact shape:

```json
{
  "meta": {
    "version": "string",
    "owner": "string",
    "description": "string",
    "last_updated": "ISO-8601 datetime",
    "repos": ["owner/repo", "..."]
  },
  "entries": [
    {
      "id": "kebab-case-unique-id",
      "title": "Human-readable title",
      "type": "homebrew-formula | skill | ui | agent | game-mod | workflow | meta-system | idea | other",
      "repo": "owner/repo-name",
      "branch": "branch-name-or-main",
      "pr": 1,
      "created": "YYYY-MM-DD",
      "updated": "YYYY-MM-DD",
      "status": "active | draft-pr | open-pr | idea | done | archived",
      "tags": ["tag1", "tag2"],
      "summary": "One-paragraph description of what this is and why it matters.",
      "files": ["path/to/key/file.ext"],
      "notes": "Extra context, caveats, or next steps."
    }
  ],
  "ideas": [
    {
      "id": "idea-kebab-id",
      "title": "Idea title",
      "status": "idea",
      "created": "YYYY-MM-DD",
      "tags": ["tag1", "tag2"],
      "description": "What it is and why it's interesting."
    }
  ]
}
```

**Field rules:**
| Field | Required | Notes |
|-------|----------|-------|
| `id` | Yes | Unique, kebab-case, stable — never change after creation |
| `type` | Yes | Use `idea` only in `entries` if it graduated from `ideas` array |
| `pr` | No | `null` if no PR exists |
| `status` | Yes | `archived` = keep for history; `done` = shipped and closed |
| `tags` | Yes | 2–10 lowercase tags, no spaces |
| `files` | No | Key files only, not exhaustive |
| `notes` | No | Omit or leave `""` if nothing to add |

---

## WORKFLOW

### (a) Query

1. Read `brain/index.json`.
2. Answer the question directly. For overviews, render a table like `BRAIN.md`.
3. If data is missing or stale, say so and suggest running `brain_update.py`.

### (b) Add Entry

1. Read `brain/index.json`.
2. Generate a new `id` (kebab-case, unique, descriptive).
3. Set `created` and `updated` to today's date (`YYYY-MM-DD`).
4. Append the new object to `entries` (or `ideas` if it's a raw idea).
5. Update `meta.last_updated` to current ISO-8601 datetime.
6. Write `brain/index.json`.
7. Regenerate `BRAIN.md` by running the logical equivalent of `brain_update.py --rebuild-md`, or manually append the new entry's section.
8. Tell the user: `git add brain/ BRAIN.md && git commit -m "brain: add <id>"`.

### (c) Update Status

1. Read `brain/index.json`.
2. Find the entry by `id` (exact match) or by title keyword.
3. Set `status` to the new value. Set `updated` to today.
4. If a PR number is provided, set `pr` too.
5. Write `brain/index.json`.
6. Regenerate or patch the matching section in `BRAIN.md`.
7. Tell the user to commit.

### (d) Add Idea

1. Read `brain/index.json`.
2. Append to the `ideas` array (not `entries`).
3. Generate `id` as `idea-<kebab-title>`.
4. Set `status: "idea"`, `created` to today.
5. Write `brain/index.json`.
6. Append the idea to the **Ideas (Backlog)** table in `BRAIN.md`.
7. Tell the user to commit.

### (e) Search by Tag

1. Read `brain/index.json`.
2. Filter `entries` where `tags` array contains all requested tags (AND logic by default; use OR if the user says "any of").
3. Also check `ideas` array.
4. Return a formatted table: `id | title | status | repo | tags`.
5. Offer to show full details for any entry.

---

## EXAMPLE INVOCATIONS

| Invocation | What happens |
|------------|--------------|
| `/brain` | Show overview dashboard (active work table + stats) |
| `/brain what have I built?` | Summarise all entries grouped by type |
| `/brain search macos` | List entries tagged `macos` |
| `/brain search macos metal` | Entries tagged both `macos` AND `metal` |
| `/brain add idea: Raycast extension for Gemma 3` | Append to `ideas` array |
| `/brain status gemma3-metal-macos active` | Change entry status to `active` |
| `/brain status apex-agent done pr 7` | Set status `done` and `pr: 7` |
| `/brain add entry: new ollama workflow for Claude Code` | Full new entry, prompts for details |
| `/brain notes gemma3-metal-macos Metal perf is 2× faster on M3` | Append to `notes` field |
| `/brain archive apex-agent` | Set status to `archived`, set `updated` today |
| `/brain what's in draft?` | List all entries where status contains `pr` |
| `/brain show ideas` | Dump the `ideas` array as a formatted list |
| `/brain promote idea-gemma3-swift-ui` | Move from `ideas` to `entries`, prompt for missing fields |
| `/brain stats` | Print the Stats table from `BRAIN.md` |

---

## TIPS

**Keeping the brain accurate**
- Run `python3 scripts/brain_update.py --token $GITHUB_TOKEN` after shipping PRs — it auto-updates statuses.
- When you finish a feature locally, run `/brain status <id> done` before closing the branch.
- After every `/brain` add or update, commit immediately so the brain doesn't drift from git history.

**Archive vs Delete**
| Situation | Action |
|-----------|--------|
| Work is done and shipped | `status: "done"` |
| Experiment abandoned, might revisit | `status: "archived"` |
| Duplicate entry or added by mistake | Delete the object from JSON; remove from BRAIN.md |
| Old idea that's no longer relevant | Remove from `ideas` array entirely |

Never use `archived` as a substitute for `done` — they mean different things for the stats.

**Tagging effectively**
- Use the technology name: `gemma3`, `ollama`, `swift`, `homebrew`.
- Use the platform: `macos`, `linux`, `ios`, `web`.
- Use the role: `ui`, `agent`, `cli`, `api`, `formula`.
- Keep tags lowercase with no spaces — use hyphens if needed (`open-source`).
- 3–6 tags is the sweet spot; more than 10 dilutes filtering usefulness.
- Prefer existing tags over inventing new ones — run `/brain search <tag>` first to check.

---

## RELATED FILES

| File | Purpose |
|------|---------|
| `brain/index.json` | Source of truth — the full machine-readable brain |
| `brain/entries/` | (Reserved) per-entry markdown files for rich detail |
| `brain/timeline.md` | Chronological view of all entries, newest first |
| `brain/README.md` | Human onboarding guide for the brain system |
| `BRAIN.md` | Human-readable dashboard auto-generated from index.json |
| `.claude/commands/brain.md` | This file — the `/brain` slash command |
| `scripts/brain_update.py` | CLI sync script: updates statuses from GitHub + rebuilds BRAIN.md |
| `.github/workflows/brain-sync.yml` | GitHub Actions: runs brain_update.py daily at 06:00 UTC |

---

## HOW TO RESPOND

1. Always read `brain/index.json` before answering — never guess the data.
2. Be direct: answer the question first, then offer follow-up actions.
3. When editing files, write the full updated content — don't leave partial states.
4. Always bump `updated` (on changed entries) and `meta.last_updated` when writing.
5. End every write operation with the exact git command the user should run.
