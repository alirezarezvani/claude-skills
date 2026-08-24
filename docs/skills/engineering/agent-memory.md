---
title: "Agent Memory — promotion is earned, not asserted — Agent Skill for Codex & OpenClaw"
description: "Use when a project's CLAUDE.md has grown past what anyone reads and you want the agent to learn durable facts from its own sessions instead — or when. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Agent Memory — promotion is earned, not asserted

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `agent-memory`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/agent-memory/skills/agent-memory/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> **Portability:** stdlib only. No database, no embeddings, no network, no LLM calls.

## The problem

A project's `CLAUDE.md` is a memory system with one tier and no eviction: every
durable fact and every passing preference land in the same always-loaded file,
until the important lines are diluted by the incidental ones. Facts learned
mid-session vanish at teardown unless someone writes them down.

**The fix is not more storage — it is a promotion ladder.** A claim earns its
way toward always-loaded context by recurring; a human confirms the last step.

## The four tiers

Tiers are distinguished by **injection policy**, not storage format.

| Tier | Holds | Injected | Committed |
|---|---|---|---|
| **L0** | raw session transcripts | never | no (already on disk) |
| **L1** | candidate atoms | on relevance, at prompt time | no (gitignored) |
| **L2** | this project's context | every session start | yes, after adopt |
| **L3** | stable cross-project persona | always | yes, after adopt |

## The gates

Nothing moves up because it sounded important. It moves up because it recurred.

- **L0 → L1** — an explicit marker fires (a directive, a correction, a stated
  preference, a named lesson, a reproducible failure). Rule-based, high
  precision, deliberately low recall.
- **L1 → L2** — ≥ 3 distinct sessions spanning ≥ 2 distinct calendar days. A
  claim stated outright needs 2 sessions; the distinct-day rule still applies. A
  verified claim promotes on one observation and is the only day-exempt path.
- **L2 → L3** — held in ≥ 2 distinct projects, aged ≥ 30 days, uncontested.

**Two gates refuse rather than guess.** A claim whose text was altered by
redaction never promotes on evidence alone — the flag firing is evidence the
source was sensitive, and a lexical filter finding one secret is not proof it
found all of them. A claim with an open contradiction is frozen at L1 until a
human resolves it; the incumbent is never silently overwritten.

## Use it

```bash
# what is remembered, and what is blocking the next promotion
python3 scripts/memory_inspect.py --tier L1

# where did this line come from — sessions, days, transcript, quoted source
python3 scripts/memory_inspect.py --why "PR base branch is dev"

# every claim with an open contradiction, both directions of the join
python3 scripts/memory_inspect.py --contested

# dry-run the promotion pass; writes nothing
python3 scripts/memory_promote.py
```

Three hooks run the loop unattended: `SessionStart` injects L2 + L3,
`UserPromptSubmit` recalls relevant L1 atoms, `SessionEnd` captures and stages.
Each is disabled independently with `AGENT_MEMORY_SESSIONSTART=0`,
`AGENT_MEMORY_USERPROMPTSUBMIT=0`, `AGENT_MEMORY_SESSIONEND=0`. Every hook fails
open: a broken memory system costs you memory, never a session.

## Hard rules

1. **Redact before writing.** Every atom passes the filter before it reaches
   disk. Anything altered is quarantined from promotion.
2. **Propose, never apply.** Promotions land in `.memory/staged/`. Only an
   explicit `/cs:memory adopt` touches a `CLAUDE.md`, and it backs both up first.
3. **Cite, don't invent.** Every atom carries a back-pointer to the transcript
   line that produced it. `--why` resolving to *ambiguous* prints nothing rather
   than guess: a wrong citation is worse than a missing one.
4. **Never surface a contested claim as fact.** It is still injected — hiding
   the conflict is worse — but always tagged.
5. **The committed tiers carry no paths.** Promotion strips the back-pointer
   prefix, which embeds an OS username.

## Forcing questions

Walk these one at a time before trusting the store.

1. Which line in your `CLAUDE.md` did you last actually read before acting?
2. Would you rather the agent forget a true thing, or remember a false one?
3. When two remembered rules disagree, who decides — and when?
4. What would make you delete `.memory/` entirely?

Rationale, open decisions, field schema: [[`agent-memory/DESIGN.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/agent-memory/DESIGN.md)](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/agent-memory/DESIGN.md).
