---
title: "/cs-memory-engineering — Slash Command for AI Coding Agents"
description: "Price, choose, audit and gate an agent memory system — the full four-lens memory-engineering pass.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-memory-engineering

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/memory-engineering/commands/cs-memory-engineering.md">Source</a></span>
</div>


Run the memory-engineering pass on `$ARGUMENTS`.

Load `engineering/memory-engineering/skills/memory-engineering/SKILL.md` and
follow it. Report every script's exit code as a finding — a non-zero exit is a
result to surface, never an error to swallow.

## Pre-flight

Establish these before running anything. If the user cannot answer 1 or 2,
that gap **is** the first finding — say so rather than guessing:

1. **Does a memory system exist yet, or is this a design?** Design → steps 1, 2, 4. Existing store → steps 1, 3, 4.
2. **What leaves the store today?** If the answer is "nothing", skip to step 4; the gate result is the headline.
3. **Is this actually a memory question?** Maintaining one markdown vault → `llm-wiki`. Nightly consolidation loop → `skillopt-sleep`. Bounding a task loop → `agent-harness`.

## Pass

**1. Price the write path**

```bash
python skills/memory-engineering/scripts/memory_cost_profiler.py --spec <workload.json>
```

Lead the report with the construction/query split and **cost per correct
answer**. Never present accuracy on its own.

**2. Choose which cost to pay**

```bash
python skills/memory-engineering/scripts/memory_architecture_picker.py --constraints <workload.json>
```

If it exits 2 (`AMBIGUOUS`), **stop and put the printed tie-breaking question to
the user.** Do not pick for them — the tie is real, not a tooling limitation.

**3. Audit the real store** (skip if this is a greenfield design)

```bash
python skills/memory-engineering/scripts/memory_density_auditor.py --dir <path>
```

Report the FACT/SKILL/LOG/PROSE split. Users are routinely wrong about how much
of their store is transcripts.

**4. Gate on forgetting** — blocking

```bash
python skills/memory-engineering/scripts/forgetting_policy_linter.py --policy <design.json>
```

Exit 4 is a **stop**. Name the failing check (F1 or F4) and its fix. Do not
present a FAIL alongside a recommendation to proceed.

## Output

Report in this order — cost before quality, always:

1. **Verdict** — one line, leading with the blocking result if there is one
2. **Cost** — construction/query split, cost per correct answer, amortization
3. **Architecture** — the family, and the cost it makes them pay
4. **What the store holds** — the FACT/SKILL/LOG/PROSE split, duplicates, staleness
5. **Forgetting gate** — PASS / CONDITIONAL / FAIL with the named failing checks
6. **Next step** — exactly one, sequenced per the ship order

Attribute every number to its source with a confidence level. Vendor customer
figures are testimonials, not benchmarks — label them as such.

For a structured walkthrough, hand the user
`skills/memory-engineering/assets/memory_engineer_worksheet.md` (the seven forcing questions) and walk
them **one at a time**.
