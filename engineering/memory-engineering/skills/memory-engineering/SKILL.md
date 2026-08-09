---
name: memory-engineering
description: Use when designing, reviewing, or paying for an agent memory system — adding memory to an agent, choosing between long-context / RAG / graph / agentic memory, auditing what a CLAUDE.md or memory directory actually holds, deciding what to keep and what to expire, or when a memory store keeps growing and nobody has said what leaves it. Prices the write path, picks which cost to pay, classifies records as facts / skills / logs, and refuses a design that has no forgetting policy.
argument-hint: "[optional: path to a memory dir, design spec JSON, or a question]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Four-lens synthesis (Stanford / Microsoft / Anthropic / Nvidia) + 4 deterministic stdlib scripts, with a blocking forgetting gate"
  distinct_from: "llm-wiki (maintains one specific markdown vault; this audits and prices any memory system); skillopt-sleep (runs a nightly consolidation loop; this decides whether that loop's output is worth keeping); agent-harness (bounds a task loop; this bounds a store)"
---

# Memory Engineering — engineer the forgetting, not just the remembering

> **Portability:** 4 stdlib scripts, no APIs/LLM calls/network. They measure and gate; you decide.

## What this does

Anyone can give an agent memory: vector store, pipe in the history, retrieve
top-k. That works until the history outgrows the context window, the write path
costs more than every query it serves, and the store fills with stale state
nobody removes. Memory is not a bucket — it is a system with a metabolism.

**The shift:** a storer optimizes what a system remembers; a memory engineer
optimizes what it forgets. The problem was never that an agent forgets — it is
that it never forgets *on purpose*.

## The four lenses

| Lens | Question | The finding that hurts |
|---|---|---|
| **Stanford** | What does remembering cost? | Construction energy exceeds total query energy across 300 queries. The tuned half is the smaller half. |
| **Microsoft** | What is worth keeping? | More raw memory can make an agent *worse*. Keep facts and skills; drop the events. |
| **Anthropic** | Who controls what it keeps? | A wrong memory does not fail once — it persists into every future session that reads it. |
| **Nvidia** | Where does it hit hardware? | It is all KV cache in HBM. Construction is prefill-heavy and stalls the query a user is waiting on. |

## Workflow

```bash
# 1 - Price it first. Never quote a quality number without a cost number.
python scripts/memory_cost_profiler.py --print-sample-spec > workload.json
python scripts/memory_cost_profiler.py --spec workload.json
# 2 - Pick which cost to pay. No "best" verdict; on a tie it asks, exit 2.
python scripts/memory_architecture_picker.py --constraints workload.json
# 3 - Audit what the store actually holds (skip if greenfield).
python scripts/memory_density_auditor.py --dir ~/.claude/memory
# 4 - Gate on forgetting. Exit 4 is a stop, not a suggestion.
python scripts/forgetting_policy_linter.py --policy design.json
# 5 - No command. Prove each pass by hand before scheduling it.
```

Step 1 reports the construction/query split, **cost per correct answer**, and
amortization — if construction dominates, cut construction tokens *before*
touching retrieval. Step 2 names the cost the winning family makes you pay.
Step 3 classifies records FACT / SKILL / LOG / PROSE (`LOG-HEAVY` = archiving
events; `PROSE-HEAVY` = docs, not memory).

Step 4 is the gate: **F1** (explicit forgetting rule) and **F4** (contradictions
surfaced, never auto-merged) are blocking. Retrofitting forgetting onto two
years of records is a migration nobody does; auto-merging disagreeing memories
destroys the evidence the conflict existed.

Step 5 has no script — prove each pass by hand, then automate. Run it once
against real history and ask whether it changed a decision. If not, scheduling
it only makes noise. Ship order: `forgetting_policy_design.md` §7.

## Hard rules

1. **Never quote accuracy without cost per correct answer.**
2. **Never return a "best" memory system** — name the cost the choice makes you pay.
3. **Never auto-merge contradictions.** The system surfaces; the human decides.
4. **Never call a design done without a forgetting rule.** No evaluated system provides one by default.
5. **Never schedule a pass not yet run by hand.**
6. **Report findings as findings.** A non-zero exit is a result to surface, not an error to swallow.
7. **Attribute every number** with its confidence level. Vendor customer figures are testimonials, not benchmarks.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/memory_cost_profiler.py` | Construction vs query split, cost per correct answer, amortization, co-location warning | 0 · 2 finding · 3 bad input |
| `scripts/memory_architecture_picker.py` | Scores 4 families, disqualifies, names the cost, refuses to pick on a tie | 0 · 2 ambiguous · 3 bad input · 4 none viable |
| `scripts/memory_density_auditor.py` | FACT/SKILL/LOG/PROSE, duplicates, staleness, density (`--dir` or `--jsonl`) | 0 dense · 2 finding · 3 bad input |
| `scripts/forgetting_policy_linter.py` | The gate: 8 checks, F1 and F4 blocking | 0 PASS · 2 CONDITIONAL · 4 FAIL |

All support `--output json` and `--sample` (no input file needed).

## References and assets

- [`references/memory_cost_canon.md`](references/memory_cost_canon.md) — construction dominance, energy per correct answer, the four families, ten recommendations (7 sources)
- [`references/what_to_keep.md`](references/what_to_keep.md) — PlugMem and MEMENTO: facts over logs, density over volume (7 sources)
- [`references/memory_control_and_governance.md`](references/memory_control_and_governance.md) — memory as files, scope/audit/rollback, poisoning, reading vendor numbers (7 sources)
- [`references/forgetting_policy_design.md`](references/forgetting_policy_design.md) — forgetting mechanisms, contradiction discipline, KV cache, ship order (7 sources)
- [`assets/memory_engineer_worksheet.md`](assets/memory_engineer_worksheet.md) — seven forcing questions with recommended answers + citations; walk one at a time
- [`assets/memory_design_spec.example.json`](assets/memory_design_spec.example.json) — one file covering every script's input
- [`assets/forgetting_policy_template.md`](assets/forgetting_policy_template.md) — fillable policy covering F1–F8

## Provenance

Framing from *"How to be a Memory Engineer"* by [@N01ennn](https://x.com/N01ennn/status/2083971749079581120); every
number is cited to a primary source instead, and two paraphrases are corrected — `memory_cost_canon.md` §2, `memory_control_and_governance.md` §4.
