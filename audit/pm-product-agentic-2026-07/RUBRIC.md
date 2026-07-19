# Agentic-Readiness Rubric (AR v1) — as applied to product-team + project-management

Audit date: 2026-07-03 · Branch: `claude/pm-audit-agentic-loops-jxurlq`

This audit applies the **same AR v1 rubric** established by the engineering agentic audit
([../engineering-agentic-2026-07/RUBRIC.md](../engineering-agentic-2026-07/RUBRIC.md)) —
six dimensions scored 0–2, answering: **can an agent pick this skill up with a goal and
drive it to a verified close?**

| # | Dimension | 2 means |
|---|---|---|
| AR1 | Goal intake | Forcing questions / intake tool / refuses vague input (exit-code gate) |
| AR2 | Task decomposition | Explicit planning step or tool whose output the workflow consumes |
| AR3 | Deterministic execution | Exact runnable CLIs; output consumed by a named next step |
| AR4 | Verification | Machine-checkable gate the workflow REQUIRES before proceeding |
| AR5 | Loop discipline | Iteration caps, stop conditions, escalation thresholds |
| AR6 | Close-out | Definition of done + state persistence or handoff artifact |

Classes: **HARNESS-READY** (total ≥ 9 AND AR4 ≥ 1 AND AR5 ≥ 1) · **LOOP-CAPABLE** (6–8,
or ≥ 9 failing the AR4/AR5 gate) · **TOOL-ONLY** (3–5) · **PROSE-ONLY** (0–2).

Baseline reference: the June 2026 quality audit of these domains lives at
[../newgen-2026-06/product-pm.md](../newgen-2026-06/product-pm.md); this audit scores the
new agentic dimension and ships the domain harness layer that the scores motivated.

Executable enforcement: the regenerated domain manifests
(`engineering/agent-harness/skills/agent-harness/assets/harnesses/{product-team,project-management}.json`)
record per-skill `agentic_signals`; the two new domain orchestrators (`product-skills`,
`pm-skills`) enforce AR1 (routers with exit-code gates), AR4 (delivery gate / OST linter),
and AR5/AR6 (harness budgets + close refusal) at run time.
