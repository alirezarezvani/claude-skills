# Master report — Engineering agentic-loop audit + agent-harness framework

**Audited:** 2026-07-03 · **Branch:** `claude/engineering-audit-agentic-loops-hv9x9m` ·
**Scope:** both engineering domain folders — `engineering/` (63 skills) and
`engineering-team/` (52 skills incl. sub-skills) — re-audited against the June 2026 baseline
AND scored on a new **agentic-readiness** rubric. Plus: a new `engineering/agent-harness`
skill that turns any of the repo's 18 domains into a bounded, self-verifying agent loop.

**Method:** (1) read the June `audit/newgen-2026-06/` reports; (2) two parallel deep-dive
agents re-read every SKILL.md, re-ran the June "Verify" criteria, and smoke-tested ~90
scripts; (3) one research agent web-verified the 2025–2026 agent-harness canon
([research-digest.md](research-digest.md)); (4) one explorer mapped the repo's existing
loop infrastructure so the new skill reuses rather than duplicates it.

---

## 1. The two questions

June asked: **does each skill earn its context window?** (trigger quality, wiring,
freshness). That audit drove a wave of fixes — REWRITEs, a phantom-path sweep, orphan-script
wiring, a 100-line ceiling.

This audit asks the next question: **can an agent pick a skill up with a goal and drive it
to a verified close?** — the gather→act→verify→repeat loop the harness literature converged
on. The rubric ([RUBRIC.md](RUBRIC.md)) scores six dimensions 0–2: goal intake (AR1), task
decomposition (AR2), deterministic execution (AR3), verification (AR4), loop discipline
(AR5), close-out (AR6).

---

## 2. Combined scorecard (115 skills across both folders)

| Class | engineering/ | engineering-team/ | Total | Meaning |
|---|---|---|---|---|
| **HARNESS-READY** (≥9, AR4≥1, AR5≥1) | 22 | 4 | **26** | An agent can loop this today |
| **LOOP-CAPABLE** (6–8) | 23 | 16 | **39** | One or two additions away |
| **TOOL-ONLY** (3–5) | 16 | 27 | **43** | Good tools, no loop spine |
| **PROSE-ONLY** (0–2) | 2 | 5 | **7** | Needs structural rebuild |

**Delta vs June** (35 non-KEEP verdicts across both folders): RESOLVED 16 ·
PARTIALLY-RESOLVED 10 · STILL-OPEN 9. The June wave landed most of its wiring and
correctness fixes; what remains is structural (deferred merges/dedupes) and the *new*
dimension this audit adds.

---

## 3. The single biggest finding: AR5 (loop discipline) is the repo-wide gap

The June wiring epidemic is largely cured — AR3 (deterministic execution) is now the median
strength. But **loop discipline is the weakest dimension in both folders.** Skills describe
"re-run until clean" with no iteration cap, or have no stop condition at all. Only the
v2.4+/Pocock/orchestrator generation (agenthub, autoresearch, chaos-engineering,
grill-with-docs, workflow-builder, playwright-pro/fix, the upgraded senior-* trio) carries
caps and escalation thresholds.

**Why it matters most for autonomous work:** a skill with great intake and tools but no
verification gate or stop condition is *more* dangerous in a loop, not less — it runs
confidently and forever, and (per the reward-hacking literature) may learn to game its own
checks. That is exactly why the AR class gate requires AR4≥1 **and** AR5≥1 before a skill
counts as harness-ready regardless of total score.

**Cheapest high-leverage fix:** a one-sentence loop-cap pattern —
*"max N fix-rerun cycles, then escalate to a human"* — ported across the ~15 skills sitting
at 7–8 points would roughly double the HARNESS-READY count. The pattern already exists
in-house (playwright-pro/fix, spec-driven-workflow, focused-fix's 3-strike rule).

Second gap: **AR1 (goal intake).** Most tool-rich skills accept any input silently. The
decision-engine "refuse without required inputs" pattern from the upgraded senior-* trio and
grill-me is the cheapest fix to propagate.

---

## 4. What this PR ships: the agent-harness framework

Rather than hand-fix 100 skills, this PR builds the **thin unifying layer** the explorer
found missing — each existing loop primitive (agenthub, autoresearch, tc-tracker,
workflow-builder, the fork-orchestrators) ships its own state dir, state machine, and eval
contract, with nothing that lets an agent pick up an arbitrary goal for an arbitrary domain
and drive it to a verified close. `engineering/agent-harness` is that layer:

- **`harness_manifest_builder.py`** scans a domain folder → a `manifest.v1` JSON inventory
  (every skill, its tools, the exact `--help`/`--sample` checks that prove each tool works,
  and static `agentic_signals` mapping to AR1/AR4/AR5/AR6). **18 domain manifests are
  committed** under the skill's `assets/harnesses/` — the whole repo, machine-readable.
- **`goal_compiler.py`** turns a goal + manifest into a `plan.v1` task plan (deterministic
  keyword scoring, no LLM call). **Refuses vague goals (exit 3)** with forcing questions and
  **refuses no-match (exit 4)** with nearest candidates — the harness never runs on fuzz.
- **`loop_controller.py`** is the JSON-backed state machine: `init → next → record →
  verify → close`. It **runs verification checks itself via subprocess** (no verification
  theater), **caps attempts and iterations** (escalates instead of looping forever), and
  **refuses to close** while any task is unverified and unwaived (exit 4, no force flag).

Plus `harness-runner` agent (stateless one-task-per-invocation executor), `/cs:harness`
command, a JSON schema, and 3 references citing the canon. Every design decision traces to a
source: verifier's law, SWE-agent's write-time feedback, Ralph fresh-context iteration,
Cognition's serialize-writers rule, Anthropic's long-running-agents harness, and this repo's
own tc-tracker / autoresearch locked-evaluator / loop-library stop-state taxonomy.

**Reuse, not reinvention.** The harness routes to agenthub for N-agent tournaments, to
autoresearch for metric optimization, and adopts tc-tracker's atomic-write + handoff schema
and autoresearch's "never modify the evaluator" invariant. See the reuse map in the skill's
`references/domain_harness_design.md`.

---

## 5. Per-domain reports

- [engineering.md](engineering.md) — 63 skills, full delta + AR table + 10 exemplars.
- [engineering-team.md](engineering-team.md) — 52 skills, delta + AR table + the two-
  generation role-skill split + 1 new P1 (senior-data-engineer CLI mismatch).
- [improvement-fields.md](improvement-fields.md) — the eight fields where investment moves
  the most skills, ordered by leverage (the "what to improve, per field" rollup).
- [research-digest.md](research-digest.md) — the web-verified harness canon.
- [RUBRIC.md](RUBRIC.md) — the AR scoring rubric.

---

## 6. Recommended follow-up PRs (in leverage order)

1. **Loop-cap sweep** — one-sentence stop-condition + iteration cap across the ~15
   LOOP-CAPABLE skills at 7–8 points. Cheapest path to ~doubling HARNESS-READY. Use each
   domain report's "Top improvement" column as the work list.
2. **Intake sweep** — port the decision-engine "refuse on missing required input" pattern to
   the tool-rich TOOL-ONLY skills (AR1 0→2).
3. **Bind the gates** — make described validators *required* (exit-code gate before
   proceeding) in llm-wiki, karpathy-coder, docker-development, helm-chart-builder.
4. **New defects** — wire ship-gate's orphaned scanner + fix its 84→89 table; fix
   senior-data-engineer's documented CLI; strip senior-ml-engineer's 2024 pricing; fix
   claude-coach's 3 June defects; document workflow-builder's by-design `--sample` exit 1.
5. **Deferred structural verdicts** — dedupe the 4 dual-published pairs; merge/retire the
   database trio; register named-persona-adversarial-review in the indexes.
6. **CI gate** — add a manifest-drift check (`harness_manifest_builder.py --all
   --no-timestamp` + `git diff --exit-code`) so the harness manifests stay true to the tree,
   mirroring `derive_counters.py --check`.

Every item above has an executable acceptance criterion in the per-domain reports — the same
"definition of done" discipline the June audit established.
