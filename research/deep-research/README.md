# deep-research — Disciplined Meta-Research

> The heavyweight end of the research domain: an auditable, reusable, triangulated investigation — for when a wrong answer costs more than the tokens spent getting it right.

`deep-research` is the rigor-first alternative to the fast [`research` router](../research/). Where the router does keyword-classify → delegate → short brief for low-decision-risk questions, `deep-research` pays for rigor: falsifiable hypotheses, parallel sub-agent fan-out, source triangulation, a mandatory adversarial pass, and per-source files with verbatim quotes.

## The 9-phase pipeline

| # | Phase | What it does |
|---|-------|--------------|
| 1 | Reframe | Fix the underlying decision; state 2-4 falsifiable hypotheses |
| 2 | Genre & blocks | Pick report genre + building blocks |
| 3 | Plan | `plan.md`: scope, sourcing strategy, opposition queries, risk register, stop-criteria |
| 3.5 | Capability discovery | Audit available API keys/channels; map subtopics to sources |
| 4 | Search (parallel) | Fan out sub-agents → fetch & dedup → save each to `sources/NN.md` |
| 5 | Score & triangulate | Rate Credibility/Recency/Bias; require >=3 independent, differently-typed sources per thesis |
| 6 | Synthesize + adversarial | Assemble from blocks; 4 self-critique questions; steel-man counter-arguments |
| 6.5 | Verify | Lightweight citation check |
| 7 | Refresh targets | Emit `refresh_targets.md` for delta-updates |

## Core discipline

- **No fabricated citations** — empty fetch = empty claim; every assertion binds to a saved verbatim quote.
- **Triangulation mandatory** — a thesis with < 3 independent, differently-typed sources is "insufficient evidence," not fact.
- **Adversarial pass required** on medium/deep investigations.
- **Persist to files** — output is a reusable folder, not a chat wall.

## Use / don't use

**Use for:** strategy, comparing N options, hypothesis validation, mapping a field.
**Not for:** quick fact-checks (answer directly), 12-dimension competitor scoring (`competitive-teardown`), or fast low-risk overviews (the research router).

## What's in the box

- **Skill:** [`skills/deep-research/SKILL.md`](skills/deep-research/SKILL.md)
- **Agent:** [`agents/cs-deep-research.md`](agents/cs-deep-research.md)
- **Command:** [`commands/cs-deep-research.md`](commands/cs-deep-research.md) — `/cs:deep-research`
- **Reference:** [`skills/deep-research/references/full-catalog.md`](skills/deep-research/references/full-catalog.md) — pointer to the upstream source catalog

## Attribution

Methodology contributed by [@Socialpranker](https://github.com/Socialpranker) (PR #851). The continuously-maintained source catalog (29 channels, 460+ statistical sources, 39 validated APIs, 103 report blocks) lives upstream at [claude-deep-research](https://github.com/Socialpranker/claude-deep-research); the methodology here is self-contained. MIT.
