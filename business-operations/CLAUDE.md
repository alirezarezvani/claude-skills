# Business Operations — Domain Guide

This file provides domain-specific guidance for skills in `business-operations/`.

## Purpose

The Business Operations domain ships skills that help **internal operators** (BizOps lead, COO direct reports, vendor management office, IT ops) run the company day-to-day. This is **not strategy** (that's `c-level-advisor/`) and **not external sales** (that's `business-growth/`).

## Skills (v2.8.0 complete)

| Skill | Job-to-be-done | `context: fork`? |
|---|---|---|
| `business-operations-skills` | Domain orchestrator — routes inquiries to the 6 sub-skills | YES |
| `process-mapper` | BPMN-style process docs + bottleneck + cycle-time (Lean / TOC canon) | YES |
| `vendor-management` | Vendor scoring + SLA + third-party risk (NIST SP 800-161 / ISO 27036) | YES |
| `capacity-planner` | Erlang-C queueing math for ops teams (NOT engineering capacity) | NO |
| `internal-comms` | ADKAR + Kotter 8-step change comms (NOT marketing) | NO |
| `knowledge-ops` | SOPs + runbooks with 5W2H validation + KB hygiene (NOT personal PKM) | YES |
| `procurement-optimizer` | UNSPSC-aligned spend categorization + supplier consolidation | NO |

## Build pattern

Path-B 11-file contract per skill (Matt Pocock-derived discipline preserved):

```
skill/
├── SKILL.md                  # YAML frontmatter + workflow + forcing-question library
├── scripts/                  # 3 stdlib-only Python CLI tools
├── references/               # 3 ref docs, ≥ 7 cited sources each
└── assets/                   # ≥ 1 user-customizable template
```

## Hard rules

1. **Stdlib-only Python** — no `requests`, `pandas`, `numpy`. Just `argparse`, `json`, `sys`, `pathlib`, `statistics`, `dataclasses`, `enum`, `datetime`, `math`, `re`, `collections`.
2. **Deterministic logic** — no LLM calls in scripts. Same input → same output. Erlang-C math implemented in log-space to avoid factorial overflow.
3. **Industry tuning** — every scoring tool exposes `--profile {saas,services,manufacturing,healthcare,…}` for threshold calibration.
4. **Matt Pocock grill discipline** — orchestrator routes via one-question-per-turn with a recommended answer + canon citation. Never bundles. Never auto-routes silently after a question. Every SKILL.md ships a "Forcing-question library" section with 5-7 cited canon-anchored questions.
5. **Output is recommendation, not approval** — `vendor-management` never says "replace this vendor"; `procurement-optimizer` never auto-consolidates suppliers; the human always decides.

## Agent + command pattern

- `cs-bizops-orchestrator` — the persona agent. Voice: "Where does the work spend most of its time waiting?" (Theory of Constraints anchor).
- `/cs:bizops <inquiry>` — top-level router.
- `/cs:grill-bizops <plan>` — Matt-style docs-anchored grilling **before** routing.
- `/cs:process-map`, `/cs:vendor-review`, `/cs:capacity-plan`, `/cs:internal-comms`, `/cs:knowledge-ops`, `/cs:procurement` — direct per-skill invocation.

## Anti-patterns (domain-level)

- ❌ Skills that overlap `business-growth/*` (external sales motion) — BizOps is **internal**
- ❌ Skills that overlap `c-level-advisor/coo-advisor` — that's strategic; BizOps is tactical
- ❌ "Process improvement consultant" generic skills — every skill must answer a SPECIFIC question (e.g., "where's the bottleneck?", "is this vendor delivering?", "are we sized to peak demand?", not "how can we improve operations?")
- ❌ Tools without `--profile` tuning — every score must be industry-tunable
- ❌ Bundled questions in the orchestrator — Matt's rule: one at a time, with a recommended answer
- ❌ Engineering-specific framing in capacity-planner — that's vpe-advisor's lane

## References

- Master plan: `documentation/implementation/bizops-commercial-expansion-plan.md`
- Matt Pocock derivation: `engineering/grill-me`, `engineering/grill-with-docs`
- Strategic complement: `c-level-advisor/coo-advisor`
