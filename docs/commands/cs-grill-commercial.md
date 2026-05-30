---
title: "/cs-grill-commercial — Slash Command for AI Coding Agents"
description: "Matt Pocock-style docs-anchored grilling for a Commercial plan, deal, pricing decision, or forecast. Walks the user's plan against the SaaS pricing. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-grill-commercial

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/commercial/commands/cs-grill-commercial.md">Source</a></span>
</div>


Apply Matt Pocock's `grill-with-docs` discipline to this Commercial plan / problem:

**$ARGUMENTS**

## Five rules (preserved from Matt Pocock, MIT)

1. **One question per turn.** Never bundle.
2. **Recommend an answer with each question.**
3. **Explore the workspace before asking** — check for deal records, pricing comps, RFP docs, MSA redlines.
4. **Walk depth-first.**
5. **Track dependencies** — pricing → packaging → deal → forecast.

## The Commercial decision tree (depth-first)

### Branch 1 — Which lane?

- PRICING / DEAL / PARTNERSHIP / CHANNEL_ECON / POLICY / RFP / FORECAST

### Branch 2 — The forcing question per lane

**PRICING:** "Is your customer paying for outcomes, seats, or usage?"
Recommended: outcomes (value-based) if you can measure them; usage if marginal cost is variable; seats only if usage is roughly flat per user.
Canon: Ramanujam 2016 *Monetizing Innovation* (the 9-mistake list). Anti-pattern: seat-based on a usage-variable product caps TAM at ~20% of WTP.

**DEAL:** "What's the gross margin at full discount, AND what does next quarter's pipeline look like at the same terms?"
Recommended: model both. Refuse to approve until reps can articulate the precedent risk.
Canon: Skok (For Entrepreneurs — discount math), Tunguz benchmarks. Anti-pattern: one 40% precedent reshapes 3 quarters of pipeline.

**PARTNERSHIP:** "Does the partner have independent demand, or are they reselling our pipeline?"
Recommended: insist on independent-demand evidence (named accounts the partner sourced, not co-sold).
Canon: Forrester channel research. Anti-pattern: channel-led deals from your own pipeline cost more than direct.

**CHANNEL_ECON:** "What's your fully-loaded cost-to-serve direct vs partner?"
Recommended: model both with allocated overhead.
Canon: Bessemer State of the Cloud channel benchmarks.

**POLICY:** "Is your current discount matrix backed by data, or by precedent?"
Recommended: data — discount band vs. win rate vs. NRR.
Canon: OpenView discount studies.

**RFP:** "Do you have proof points for each requirement, or are you writing aspirational claims?"
Recommended: proof points only. Refuse to invent claims.
Canon: APMP (Association of Proposal Management Professionals).

**FORECAST:** "Are you using stage-conversion from the last 4 quarters, or the last 12?"
Recommended: last 4, weighted toward most recent.
Canon: Skok, OpenView. Anti-pattern: 12-month equal-weight hides recent slowdown.

### Branch 3 — Reversibility check

"If this commercial decision lands and we want to roll it back in 90 days, what does it cost?"
Hard-to-reverse + surprising + real trade-off → ADR per Matt's grill-with-docs criteria.

### Branch 4 — Approval chain

"Who is the human approver on the output?"
Recommended: named role + named person, not "the team".

### Branch 5 — Now invoke the sub-skill

Only after branches 1-4 are locked, invoke `/cs:commercial` with the synthesized inquiry.

## Output format per turn

```
Q[i]/[total]: [precise question]
Recommended: [answer + canon-cited rationale]

(Confirm, or override?)
```

## Stop conditions

- All branches resolved → invoke `/cs:commercial <synthesized>`
- User says "stop grilling, just run it" → invoke with whatever's resolved, flag unresolved branches in digest
- User abandons → no sub-skill, save partial grill to `commercial-grill-{timestamp}.md`

## Distinct from

- `engineering/grill-me` (Matt Pocock) — generic
- `engineering/grill-with-docs` (Matt Pocock) — codebase + ADR-anchored for engineering. This is **Commercial-domain grilling** against the SaaS pricing canon.
- `/cs:commercial` — **executes** routing. This **interrogates** first.
