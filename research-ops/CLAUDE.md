# Research Operations — Domain Guide

This file provides domain-specific guidance for skills in `research-ops/`.

## Purpose

The Research Operations domain ships skills that help **R&D leads, clinical study teams, R&D finance/controllers, market-research analysts, and product-research / ResearchOps teams** plan, fund, scope, and synthesize research across enterprise workstreams. This is the **enterprise / cross-functional counterpart** to the academic `research/` domain (litreview, grants, patent, syllabus, pulse, dossier, notebooklm).

It is **not regulatory submission** (`ra-qm-team`), **not corporate financial close/valuation** (`finance/financial-analysis`), **not funding discovery** (`research/grants`), **not persona/journey/live-experiment design** (`product-team`), and **not campaign analytics** (`marketing-skill`).

## Skills (v2.9.0)

| Skill | Purpose | `context: fork`? |
|---|---|---|
| `research-ops-skills` | Domain orchestrator — routes to 4 sub-skills | YES |
| `clinical-research` | Study design: protocol synopsis + endpoint selection + sample-size/power + phase-gating | NO |
| `research-finance` | R&D program budgeting + burn/runway + F&A rate modeling + capitalize-vs-expense routing | NO |
| `market-research` | TAM/SAM/SOM (both methods) + survey/sampling design + segmentation + CI synthesis | NO |
| `product-research` | Study design + saturation/sample method + insight repository synthesis | NO |

## Hard rules (domain-specific)

1. **clinical-research: outputs are study-design RECOMMENDATIONS signed by a named clinician/biostatistician/regulatory owner.** Power/sample-size is an ESTIMATE with stated assumptions — never presented as clinical fact. Every tool prints an "ESTIMATE — confirm with a biostatistician" banner.
2. **research-finance: every budget output surfaces its assumptions block.** Capitalize-vs-expense routes to a NAMED finance owner and never auto-decides accounting treatment.
3. **market-research: TAM/SAM/SOM always shows method (top-down AND bottoms-up) + assumptions.** Never a single unsourced number.
4. **product-research: never fabricates user insight.** Sample-size/saturation guidance is method-based and surfaces confidence; single-source claims are flagged as anecdotes, not insights.
5. **Stdlib-only Python.** Deterministic logic, no LLM calls in scripts.
6. **Industry tuning** via `--profile` on every scoring tool.
7. **Matt Pocock grill discipline** — `/cs:grill-research-ops` interrogates the plan against the research canon (ICH E9, IAS 38, Cochran, Nielsen, Kotler) before any sub-skill runs.
8. **Onboarding-first + customization-in-use.** Each sub-skill ships `scripts/onboard.py` (its own question set) + `scripts/config_loader.py`. Answers persist to `~/.config/research-ops/<skill>.json` (global) or `./.research-ops/<skill>.json` (project) and are consumed by every tool (CLI flags override; `RESEARCH_OPS_NO_CONFIG=1` bypasses). Customization must change behavior, not sit as decoration.
9. **Autoresearch is opt-in + isolated.** Each sub-skill ships `scripts/ar_evaluator.py` — a per-skill, locked ground-truth bridge to `engineering/autoresearch-agent`. A loop is invoked ONLY on explicit user request and only edits the skill's input file, never the evaluator. No cross-skill coupling.

## Build pattern

Path-B contract per skill: SKILL.md + 3 stdlib scoring scripts + 3 references (each citing 5-7 sources) + 1 asset template, **plus** 3 integration scripts — `onboard.py` (questionnaire), `config_loader.py` (customization loader, project→global→defaults precedence), and `ar_evaluator.py` (isolated autoresearch bridge). SKILL.md includes a "Forcing-question library" section (cited-canon grilling, one question at a time) and the "Onboarding & customization" + "Optimize with autoresearch (opt-in)" sections.

## Agent + command pattern

- `cs-research-ops-orchestrator` — evidence-first R&D operations lead. Voice: "What decision does this research drive, and what's your confidence — show me the method and the assumptions before the number."
- `/cs:research-ops <inquiry>` — top-level router
- `/cs:grill-research-ops <plan>` — Matt-style grilling first
- `/cs:clinical-research`, `/cs:research-finance`, `/cs:market-research`, `/cs:product-research` — direct per-skill invocation

## Anti-patterns (domain-level)

- ❌ Skills that overlap `ra-qm-team` (regulatory/QM submission) — clinical-research designs the **study**, not the submission
- ❌ Skills that overlap `finance/financial-analysis` (close/valuation) — research-finance manages **R&D program spend**
- ❌ Skills that overlap `research/grants` (funding discovery) — research-finance manages **money already won**
- ❌ Skills that overlap `product-team` (persona/journey/live experiments) — product-research is **method + repository discipline**
- ❌ Skills that overlap `marketing-skill` (campaign analytics) — market-research is **upstream methodology**
- ❌ A market size stated as a single unsourced number
- ❌ A clinical power/endpoint output presented as fact rather than an estimate with a named owner
- ❌ A product insight asserted from a single participant

## References

- Master plan: `documentation/implementation/research-ops-expansion-plan.md`
- Matt Pocock derivation: `engineering/grill-with-docs`
- Academic counterpart: `research/` (litreview, grants, patent)
- Regulatory complement: `ra-qm-team`
- Corporate-finance complement: `finance/financial-analysis`
- Product complement: `product-team`
