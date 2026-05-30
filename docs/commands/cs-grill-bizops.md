---
title: "/cs-grill-bizops — Slash Command for AI Coding Agents"
description: "Matt Pocock-style docs-anchored grilling for a BizOps plan or design. Walks the user's plan against the BizOps canon (Lean, Theory of Constraints. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-grill-bizops

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/business-operations/commands/cs-grill-bizops.md">Source</a></span>
</div>


Apply Matt Pocock's `grill-with-docs` discipline to this BizOps plan / problem:

**$ARGUMENTS**

## Five rules (preserved from Matt Pocock, MIT)

1. **One question per turn.** Never bundle.
2. **Recommend an answer with each question.** Defaulting to "what do you think?" is lazy.
3. **Explore the workspace before asking.** If `Glob`/`Read`/`Grep` resolves it, do that first.
4. **Walk the decision tree depth-first.** Finish a branch before opening another.
5. **Track dependencies.** Resolve A before B if B depends on A.

## The BizOps decision tree (depth-first)

Walk these branches in order. Skip a branch only if the workspace already resolves it.

### Branch 1 — Which lane?

- PROCESS / VENDOR / CAPACITY / COMMS / KNOWLEDGE / PROCUREMENT
- Canon source: this skill's signal table + `references/` per lane

### Branch 2 — Measurement state

For PROCESS: "Do you have measured cycle times per stage, or estimates?" — Recommended: insist on measured for top-3 longest stages. Anti-pattern (Goldratt 1984): map estimates → optimize wrong constraint.

For VENDOR: "Tier-1 threshold — spend or operational dependency?" — Recommended: operational dependency. Anti-pattern (Target/HVAC breach, Verkada): spend-only tiering misses critical low-spend vendors.

For CAPACITY: "Plan for utilization or throughput?" — Recommended: throughput (Little's Law). Anti-pattern (DORA): planning for utilization > 80% destroys throughput.

For COMMS: "Push or pull comms?" — Recommended: depends on change magnitude. ADKAR model (Hiatt 2006): high-uncertainty change needs push + 7+ touchpoints.

For KNOWLEDGE: "SOP or runbook?" — Recommended: SOP if humans, runbook if 50% automated. Atlassian/Google SRE distinction.

For PROCUREMENT: "Spend or supplier consolidation goal?" — Recommended: consolidation if Pareto says top-20% suppliers = 80% spend. Else spend categorization.

### Branch 3 — Owner + accountability

"Who owns this when the recommendation lands?" — Recommended: named human, not a team. Anti-pattern: 'the ops team owns it' = no one owns it.

### Branch 4 — Reversibility

"Is this decision reversible in < 30 days at < $X cost?" If no, propose an ADR (per Matt's grill-with-docs ADR criteria: hard to reverse + surprising-without-context + real trade-off).

### Branch 5 — Now invoke the sub-skill

Only after branches 1-4 are resolved, invoke `/cs:bizops` to route to the right sub-skill.

## Output format per turn

```
Q[i]/[total resolved branches]: [precise question]
Recommended: [answer + 1-sentence canon-cited rationale]

(Confirm, or override?)
```

## Stop conditions

- All branches resolved → invoke `/cs:bizops <synthesized inquiry>`
- User says "stop grilling, just run it" → invoke `/cs:bizops` with whatever's resolved, flag the unresolved branches in the digest
- User abandons → no sub-skill invocation, save the partial grill to `bizops-grill-{timestamp}.md`

## Distinct from

- `engineering/grill-me` (Matt Pocock) — generic plan grilling, no domain canon
- `engineering/grill-with-docs` (Matt Pocock) — codebase + ADR-anchored grilling for engineering. This is **BizOps-domain grilling**.
- `/cs:bizops` — that **executes** the routing. This **interrogates** before executing.
