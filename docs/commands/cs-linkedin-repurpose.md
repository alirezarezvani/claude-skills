---
title: "/cs-linkedin-repurpose — Slash Command for AI Coding Agents"
description: "/cs-linkedin-repurpose — Split an article, talk transcript, README, or write-up into standalone LinkedIn units, score each on whether it survives. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-linkedin-repurpose

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/marketing/linkedin/commands/cs-linkedin-repurpose.md">Source</a></span>
</div>


**Command:** `/cs-linkedin-repurpose [path to source]`

## When to run

- "Turn my talk into LinkedIn posts"
- "I wrote this article — what can I post from it?"
- You have a body of work and an empty content calendar

## What you get

1. **Scored standalone units** — length, dangling references, evidence, substance. A unit
   opening with "This meant that…" is disqualified regardless of its score, because it refers
   to something the reader never saw.
2. **A suggested format** per unit.
3. **Ledger-aware output** — anything already posted is skipped, with its date available on
   request.
4. **The named gap you have to fill** — the first-person sentence only you can write.

## Workflow

```bash
# Split and see what is available
python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-content/scripts/repurpose_splitter.py \
  --input talk.md --ledger .linkedin-ledger.json --output human

# After publishing unit 2, record it
python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-content/scripts/repurpose_splitter.py \
  --input talk.md --ledger .linkedin-ledger.json --record 2 --posted-on 2026-08-25

# Then lint the drafted post
python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-content/scripts/post_linter.py --input draft.md --output human
```

Commit the ledger alongside the source. It is project state, not a cache.

## Discipline

- **Every unit is source material, not a post.** Add what it cost, what you assumed, or what
  you would do differently. That sentence is the only genuinely new thing in a repurposed post.
- **Consent and confidentiality first** for post-mortems, customer notes, and anything with a
  named third party. The pattern is publishable; the customer is not.
- **Never publish identical text on two platforms the same day.**
- **One source should not carry a quarter.** When units start needing more setup than
  payload, the ledger is telling you to go do something new.

## Stop conditions

- Usable units identified and the first one drafted and linted clean → done.
- `NOT_SPLITTABLE` (exit 3) → this is one post, not a series. Say so and write the one post.
- All units already in the ledger → the source is mined out. Do not re-cut it.

## Related

- Skill: [`linkedin-content`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-content/SKILL.md)
- Reference: [`repurposing_discipline.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-content/references/repurposing_discipline.md)
