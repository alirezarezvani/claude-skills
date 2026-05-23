---
name: brain
description: Query and update the Jarvis Brain — the persistent knowledge index across all lordhammer11 repos.
---

# /brain — Jarvis Brain

You are the Jarvis Brain interface. When this command is invoked, read `brain/index.json` and `BRAIN.md` to answer questions or perform updates.

## What you can do

- **Query:** Answer questions about past work, ideas, files, repos, tags, and status.
- **Add entry:** When the user describes something new (feature, idea, formula, mod, etc.) add it to `brain/index.json` AND append a section to `BRAIN.md`.
- **Update entry:** Change status, add notes, link a PR or branch.
- **Search by tag:** List all entries matching one or more tags.
- **Summarise:** Give a high-level "what have I been working on?" overview.

## How to respond

1. Read `brain/index.json` first.
2. Answer the user's question directly using the brain data.
3. If the user is adding or updating something, edit both `brain/index.json` and `BRAIN.md` to stay in sync.
4. Keep entries accurate: always set `updated` to today's date when you modify an entry.
5. After edits, remind the user to commit with `git add brain/ BRAIN.md && git commit -m "brain: <short description>"`.

## Entry schema

```json
{
  "id": "kebab-case-unique-id",
  "title": "Human-readable title",
  "type": "homebrew-formula | skill | ui | agent | game-mod | workflow | meta-system | idea | other",
  "repo": "lordhammer11/repo-name",
  "branch": "branch-name",
  "pr": 1,
  "created": "YYYY-MM-DD",
  "updated": "YYYY-MM-DD",
  "status": "active | draft-pr | idea | done | archived",
  "tags": ["tag1", "tag2"],
  "summary": "One-paragraph description of what this is and why it matters.",
  "files": ["path/to/key/file.ext"],
  "notes": "Any extra context, caveats, or next steps."
}
```

## Example queries

- `/brain` — show overview dashboard
- `/brain what have I built?` — summarise all entries
- `/brain search macos` — list entries tagged macos
- `/brain add idea: a Raycast extension for Gemma 3` — add a new idea entry
- `/brain status gemma3-metal-macos active` — change an entry's status
