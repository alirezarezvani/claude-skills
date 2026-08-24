---
title: "/cs-forgetting-audit — Slash Command for AI Coding Agents"
description: "Run only the blocking forgetting gate on a memory design or store — what leaves, and on what rule.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-forgetting-audit

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/memory-engineering/commands/cs-forgetting-audit.md">Source</a></span>
</div>


The short pass. Skip the cost and architecture work; answer one question about
`$ARGUMENTS`:

> **What leaves this store, and on what rule?**

## Run

If given a policy JSON:

```bash
python skills/memory-engineering/scripts/forgetting_policy_linter.py --policy <policy.json>
```

If given a directory, first show what is actually accumulating, then gate:

```bash
python skills/memory-engineering/scripts/memory_density_auditor.py --dir <path>
python skills/memory-engineering/scripts/forgetting_policy_linter.py --policy <policy.json>
```

If no policy file exists, that is the answer — nothing leaves the store. Show
what `--sample-failing` blocks, then help write one from
`skills/memory-engineering/assets/forgetting_policy_template.md`.

## The two blocking checks

- **F1 — an explicit forgetting rule** (TTL, capacity bound with a stated
  eviction order, or relevance decay). None of the memory systems in the
  Stanford evaluation prunes or forgets by default: if it was not built, it does
  not exist.
- **F4 — contradictions surfaced, never auto-merged.** `newest_wins`,
  `auto_merge`, `overwrite` and `last_write_wins` all fail. Two memories that
  disagree may both have been true in different contexts, and silently resolving
  them destroys the only evidence the conflict existed.

The other six checks (dedup, consolidation, scope, audit trail, rollback,
growth-slope monitoring) degrade the verdict to CONDITIONAL rather than failing
it.

## Report

1. **Verdict** — PASS (0) / CONDITIONAL (2) / **FAIL (4)**
2. **Every failing check** with its ID, why it matters, and its fix
3. **The one thing to fix first** — F1 or F4 if either failed; otherwise the
   highest-leverage warning

## Do not

- Do not soften a FAIL into a suggestion. Retrofitting forgetting onto a full
  store is a data migration with a judgment call attached to every record —
  which is exactly why it never happens.
- Do not accept "we will add pruning later." Later is the failure mode.
- Do not propose auto-resolution for contradictions, in any form.
