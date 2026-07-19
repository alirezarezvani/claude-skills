# Agentic-Readiness Rubric (AR v1)

Audit date: 2026-07-03 · Branch: `claude/engineering-audit-agentic-loops-hv9x9m`

The June 2026 audit ([../newgen-2026-06/RUBRIC.md](../newgen-2026-06/RUBRIC.md)) asked
"does this skill earn its context window?" This follow-up asks the next question:
**can an agent pick this skill up with a goal and drive it to a verified close?** — the
gather-context → take-action → verify-work → repeat loop the 2024–2026 harness canon
converged on (see [research-digest.md](research-digest.md)).

## The six dimensions (0–2 each, total 0–12)

| # | Dimension | 0 | 1 | 2 |
|---|---|---|---|---|
| AR1 | **Goal intake** | Accepts any input silently | Asks context questions | Forcing questions / intake tool / refuses vague input (exit-code gate) |
| AR2 | **Task decomposition** | No plan step | Prose phases | Explicit planning step or tool whose output the workflow consumes |
| AR3 | **Deterministic execution** | No wired tools | Tools named, CLIs incomplete | Exact runnable CLIs; output consumed by a named next step |
| AR4 | **Verification** | None | Checklist prose | Machine-checkable gate (exit codes, JSON assertions) the workflow REQUIRES before proceeding |
| AR5 | **Loop discipline** | No retry/stop rules | "Re-run until clean" without a cap | Iteration caps, stop conditions, escalation thresholds |
| AR6 | **Close-out** | Work just ends | Informal done statement | Definition of done + state persistence or handoff artifact |

## Classes

| Class | Criteria | Meaning |
|---|---|---|
| **HARNESS-READY** | total ≥ 9 AND AR4 ≥ 1 AND AR5 ≥ 1 | An agent can run this skill inside a bounded loop today |
| **LOOP-CAPABLE** | total 6–8 (or ≥9 failing an AR4/AR5 gate) | One or two targeted additions from harness-ready |
| **TOOL-ONLY** | total 3–5 | Good tools, no loop spine |
| **PROSE-ONLY** | total 0–2 | Knowledge dump; needs structural rebuild |

The AR4/AR5 gate is deliberate: a skill with perfect intake and tools but no verification
gate or stop condition is *more* dangerous in an autonomous loop, not less — it runs
confidently and forever.

## Executable enforcement

The rubric is now mechanized: `engineering/agent-harness/skills/agent-harness/scripts/harness_manifest_builder.py`
records per-skill `agentic_signals` (static evidence for AR1/AR4/AR5/AR6) in every domain
manifest, and `loop_controller.py` enforces AR4/AR5/AR6 at run time regardless of the
skill's own discipline. Improvement PRs should move skills up this ladder; the manifests
make regressions diffable.
