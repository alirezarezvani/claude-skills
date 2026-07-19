---
name: "cs-deep-research"
description: "/cs:deep-research <question> — Disciplined multi-source investigation for a high-stakes question. Reframes into falsifiable hypotheses, plans, fans out parallel search sub-agents, triangulates every thesis against >=3 independent sources, saves each source to its own file with verbatim quotes, runs an adversarial pass, and emits an auditable, reusable research folder with a refresh protocol. The heavyweight alternative to the fast research router."
argument-hint: "[the question or decision to research]"
---

# /cs:deep-research — Disciplined Meta-Research

**Command:** `/cs:deep-research <question>`

The `cs-deep-research` persona turns "research this" into an auditable, reusable investigation — the workflow to reach for when getting the answer *wrong* costs more than the tokens spent getting it right.

## When to Run

- A low-quality answer is expensive: strategy, business plan, report, or article groundwork.
- Comparing N institutions / products / methods / markets with defensible reasoning.
- Validating a hypothesis or an irreversible decision against external data.
- Meta-research: "understand how X works," "map the landscape of Y."

## When NOT to Run

- Quick fact-checks → answer directly.
- Structured 12-dimension competitor scoring → `competitive-teardown`.
- Fast topic overviews where decision risk is low → the **research router** (`/cs:research`).

## What You Get

1. **Reframe** — the question rewritten to the real decision + 2-4 falsifiable hypotheses.
2. **`plan.md`** — genre, sourcing strategy, opposition queries, risk register, stop-criteria.
3. **Parallel search** — sub-agents fanned out across channels; each source saved to `sources/NN_slug.md` with verbatim quotes + Credibility/Recency/Bias scores.
4. **Triangulated synthesis** — every thesis backed by >=3 independent, differently-typed sources (or flagged "insufficient evidence"), plus a mandatory adversarial pass.
5. **A reusable folder** — `sources.csv`, `findings/`, final report, and `refresh_targets.md` for delta-updates later.

## Trigger Phrases (auto-invoke without /cs:)

- "deep research on [topic]" / "do a deep dive on [topic]"
- "research this thoroughly / rigorously" / "high-stakes research"
- "compare [N options] and give me defensible reasoning"
- "validate this hypothesis with external data"

## Discipline

- **No fabricated citations** — empty fetch = empty claim.
- **Triangulation mandatory** — < 3 independent, differently-typed sources → "insufficient evidence," not fact.
- **Adversarial pass required** on medium/deep investigations.
- **Parallel sub-agents** — never serial in the search phase.
- **Persist to files** — the reuse value is the folder, not the transcript.

## Stop Conditions

- Report written + every thesis triangulated or flagged + `refresh_targets.md` emitted → done.
- On an `update <slug>` run: produce a delta in `diffs/` instead of replaying the whole investigation.

## Related

- Agent: [`cs-deep-research`](../agents/cs-deep-research.md)
- Skill: [`deep-research`](../skills/deep-research/SKILL.md)
- Siblings: `/cs:pulse` (recency), the research router, `litreview` / `dossier` / `patent`

---

**Version:** 1.0.0
