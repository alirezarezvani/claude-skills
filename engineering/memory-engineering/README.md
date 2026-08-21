# memory-engineering

> Your agent's problem was never that it forgets. It's that it never forgets
> **on purpose**.

A storer optimizes what a system remembers. A memory engineer optimizes what it
forgets. This plugin makes that shift executable: four deterministic stdlib
scripts that price the write path, choose which cost to pay, audit what a store
actually holds, and **refuse a design with no forgetting policy**.

## Why this exists

Everyone building agent memory optimizes retrieval. Almost nobody engineers
what it costs to build, what is worth keeping, who can delete it, and where it
lands on the hardware. Stanford's systems characterization of ten memory systems
found the gap concretely:

- **Construction energy exceeds total query-phase energy across 300 queries** —
  the bill is paid on the write path you never watch.
- Energy per correct answer **spreads more than 47×** across systems (BM25 at
  4,145 J; MIRIX at ~197 kJ).
- At 1M tokens, footprint varies **up to 9×** — and **"none of the evaluated
  systems prune or forget by default."**

If you did not build forgetting, you do not have it.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install memory-engineering
```

## Use

```bash
/cs:memory-engineering ~/.claude/memory      # full four-lens pass
/cs:forgetting-audit design.json             # just the blocking gate
```

Or run the scripts directly — each has `--help`, `--sample`, and `--output json`:

```bash
cd skills/memory-engineering

python scripts/memory_cost_profiler.py --sample
python scripts/memory_architecture_picker.py --sample
python scripts/memory_density_auditor.py --dir ~/.claude/memory
python scripts/forgetting_policy_linter.py --sample-failing
```

## The four scripts

| Script | Lens | What it does | Exit codes |
|---|---|---|---|
| `memory_cost_profiler.py` | Stanford — *what does it cost?* | Splits construction vs query spend, computes **cost per correct answer**, flags under-amortized writes and construction co-located with live queries | 0 · 2 finding · 3 bad input |
| `memory_architecture_picker.py` | Stanford — *which cost to pay?* | Scores long-context / flat RAG / structure-augmented RAG / agentic against constraints, disqualifies on hard limits, **names the cost you're choosing**, refuses to pick on a tie | 0 · 2 ambiguous · 3 bad input · 4 none viable |
| `memory_density_auditor.py` | Microsoft — *what's worth keeping?* | Classifies records **FACT / SKILL / LOG / PROSE**, finds near-duplicates, flags stale and time-relative wording, scores knowledge density. Runs on a real directory or JSONL | 0 dense · 2 finding · 3 bad input |
| `forgetting_policy_linter.py` | Anthropic + the gate | 8 checks; **F1** (explicit forgetting rule) and **F4** (contradictions surfaced, never auto-merged) are **blocking** | 0 PASS · 2 CONDITIONAL · **4 FAIL** |

Stdlib only. No network, no LLM calls, no dependencies.

## The gate

```
$ python scripts/forgetting_policy_linter.py --sample-failing

VERDICT: FAIL  (0/8 checks pass)
This design does not forget on purpose. F1 failed. F4 failed.

  FAIL  F1  explicit forgetting rule [BLOCKING]
        No TTL, no capacity bound, no decay. The store only grows.
  FAIL  F4  contradictions surfaced, never auto-merged [BLOCKING]
        Contradiction policy is 'newest_wins', which resolves conflicts silently.
```

**F4 is blocking on purpose.** Two memories that disagree may both have been
true in different contexts — "deploys go through Jenkins" and "deploys go
through GitHub Actions" is not a contradiction to resolve, it is a migration to
record. Auto-merging destroys the only evidence the conflict existed.

## Evidence discipline

The four-lens framing synthesizes *"How to be a Memory Engineer, from the
perspective of Stanford, Microsoft, Anthropic and Nvidia"* by
[@N01ennn](https://x.com/N01ennn/status/2083971749079581120).

**Every quantitative claim is cited to the primary source, not to that
article,** and each carries an explicit confidence level. Two of the article's
paraphrases are corrected in the references:

- The **47×** energy figure is the spread across ten evaluated systems, not
  "two systems with identical accuracy" (`memory_cost_canon.md` §2).
- The **97%** first-pass-error reduction is Rakuten's named, vendor-published
  customer testimonial — not a controlled study or a general property of
  building memory this way (`memory_control_and_governance.md` §4).

## Not this plugin

| You want | Use |
|---|---|
| Build and maintain one markdown knowledge vault | `llm-wiki` |
| A nightly self-improvement loop over transcripts | `skillopt-sleep` |
| Bound an agent's *task loop* | `agent-harness` |
| Price inference generally | `llm-cost-optimizer` |

This bounds a **store**, not a loop and not a vault.

## Primary sources

- Omri, Y. et al. — *Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads*, [arXiv:2606.06448](https://arxiv.org/abs/2606.06448)
- Microsoft Research — [*PlugMem: A Task-Agnostic Plugin Memory Module for LLM Agents*](https://www.microsoft.com/en-us/research/publication/plugmem-a-task-agnostic-plugin-memory-module-for-llm-agents/)
- Kontonis, V. et al. — *MEMENTO: Teaching LLMs to Manage Their Own Context*, [arXiv:2604.09852](https://arxiv.org/abs/2604.09852)
- Anthropic — [*Built-in memory for Claude Managed Agents*](https://claude.com/blog/claude-managed-agents-memory)

Full citation lists (7 sources each) are in
[`skills/memory-engineering/references/`](skills/memory-engineering/references/).

## License

MIT.
