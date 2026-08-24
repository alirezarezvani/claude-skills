# What To Keep — facts and skills, not logs

> The Microsoft lens: *what is worth keeping?*
>
> Every figure is attributed with a confidence level.

---

## 1. More memory can make an agent worse

The uncomfortable premise of Microsoft Research's **PlugMem**: giving an agent
more raw memory does not monotonically help it. History piles up, retrieval
drowns in near-misses, and the agent burns attention wading through transcripts
for the one line that mattered.

> PlugMem "distinguishes between remembering events, knowing facts, and knowing
> how to perform tasks, with effective decisions relying on the facts and skills
> extracted from those events."
> — Microsoft Research, *PlugMem: A Task-Agnostic Plugin Memory Module for LLM
> Agents* (confidence: **high**)

The structure borrowed here is the classic memory taxonomy from cognitive
psychology — Tulving's split between **episodic** memory (what happened) and
**semantic** memory (what is true), with **procedural** memory (how to do it) as
the third leg. Humans do not replay episodes to make decisions; we act on the
semantic and procedural residue we distilled from them.

**The engineering translation:** your write path's job is *extraction*, not
*archival*. If your memory system stores what happened, you built a log with a
vector index on it.

## 2. Density is the metric, not volume

> PlugMem "enables agents to achieve better results while using significantly
> fewer memory tokens, with efficiency measured by the utility of the
> information delivered relative to the context consumed," reporting "consistent
> gains over generic retrieval and task-specific memory designs across three
> benchmarks while consuming less of the agent's context window."
> — Microsoft Research (confidence: **high** on the directional claim;
> **moderate** on magnitude, as per-benchmark numbers vary)

So the metric to optimize is:

```
decision-relevant information delivered
───────────────────────────────────────
     tokens of context it costs
```

Not "how many records did we store." `memory_density_auditor.py` approximates
the numerator by counting FACT and SKILL records, and the denominator by
estimated tokens.

⚠️ **A note on a related claim.** A widely-shared summary states PlugMem "cuts
context by up to 100×." Microsoft's own materials describe consistent gains at
lower context cost without foregrounding that multiple. Treat any specific
compression multiple as **low confidence** unless you read it in the paper's
results table for your own workload shape.

## 3. Memento — the model manages its own context

Microsoft's **MEMENTO** pushes context management inside the model rather than
bolting orchestration around it. The model learns to segment its reasoning into
blocks, compress each block into a dense "memento" summary, drop the full block
from context, and reason forward attending only to the mementos.

Measured results (confidence: **high** — reported in the paper):

| Metric | Result |
|---|---|
| Memento size target | 15–25% of original block tokens |
| Peak KV cache | ~2.5× reduction (paper reports 2–3× peak memory) |
| Throughput (vLLM) | ~1.75× improvement |
| Training data | OpenMementos — 228K reasoning traces |

Two things a memory engineer should take from it:

**First, this is a learned skill, not an orchestration layer.** It comes from
ordinary fine-tuning on segmented traces. You cannot get it by wrapping a model
in a summarizer loop.

**Second — and this is the subtle one — forgetting is not deletion.**

> "Information from each reasoning block is carried both by the memento text
> and by corresponding KV states, which retain implicit information from the
> original block — removing this channel drops accuracy by 15 percentage points
> on AIME24."
> — *MEMENTO: Teaching LLMs to Manage Their Own Context*, arXiv:2604.09852
> (confidence: **high**)

A shadow of the erased reasoning survives in the KV states. Rebuilding context
from the summary text *alone* costs 15 points. The lesson generalizes beyond
Memento: **a summary is not equivalent to what it summarizes**, and any
architecture that assumes "we distilled it, so we can drop the original" should
measure that assumption rather than trust it.

## 4. The three record types, and how to tell them apart

`memory_density_auditor.py` classifies every record into one of four buckets.
The classification is lexical and deliberately conservative.

| Type | What it is | Signal | Keep? |
|---|---|---|---|
| **FACT** | A declarative truth about the world | `X is Y`, `key: value`, versions, owners, endpoints | Yes — this is semantic memory |
| **SKILL** | A procedure or a rule | numbered steps, `always/never`, `to X, do Y` | Yes — this is procedural memory |
| **LOG** | A record of an event | speaker turns, timestamps, first-person past tense | Extract from it, then drop it |
| **PROSE** | Narrative with no signal either way | none of the above | Distill or move to docs |

**Why PROSE exists as a category.** An earlier version of this classifier
labeled every signal-less block as LOG, which fired the log-heavy finding on any
prose-shaped documentation store — a false positive severe enough to make the
tool untrustworthy. Narrative documentation is neither an event log nor a
retrievable fact; it deserves its own verdict and its own fix (distill it, or
move it out of the memory store).

**Why LOG wins ties.** Mistaking an event for knowledge is the costly direction
of error. A false LOG label costs you a review; a false FACT label puts a
transcript into the retrieval path forever.

## 5. What this means for your write path

Ordered by leverage:

1. **Extract at write time, not read time.** The whole point of paying for
   construction is that the thinking already happened when the query arrives.
2. **Store the conclusion with its provenance, not the conversation.** "Billing
   is owned by the payments team (source: 2026-03 handover doc)" beats the
   thread where that was worked out.
3. **Write the fact so it can go stale detectably.** "Postgres 14 as of
   2026-03" beats "currently on Postgres." Time-relative wording rots silently;
   `memory_density_auditor.py` flags it as `VOLATILE_WORDING`.
4. **Prefer one dense record to five thin ones.** Consolidation is check F3 in
   the forgetting linter for exactly this reason.

---

## Sources

1. Microsoft Research — *PlugMem: A Task-Agnostic Plugin Memory Module for LLM
   Agents*.
   <https://www.microsoft.com/en-us/research/publication/plugmem-a-task-agnostic-plugin-memory-module-for-llm-agents/>
2. Microsoft Research Blog — *From raw interaction to reusable knowledge:
   rethinking memory for AI agents*.
   <https://www.microsoft.com/en-us/research/blog/from-raw-interaction-to-reusable-knowledge-rethinking-memory-for-ai-agents/>
3. Kontonis, V. et al. — *MEMENTO: Teaching LLMs to Manage Their Own Context*,
   arXiv:2604.09852. <https://arxiv.org/abs/2604.09852>
4. `microsoft/OpenMementos` — the 228K-trace public dataset released with
   MEMENTO. <https://huggingface.co/datasets/microsoft/OpenMementos>
5. Tulving, E. — *Episodic and Semantic Memory* (1972), and *Elements of
   Episodic Memory* (1983). The episodic/semantic distinction PlugMem borrows.
6. Anderson, J. R. — *ACT-R* and the declarative/procedural memory split.
   Source of the fact-versus-skill distinction used in the classifier.
7. Anthropic — *Effective context engineering for AI agents* (2025). The
   context-as-finite-budget framing behind the density metric.

## Related tools in this skill

- `memory_density_auditor.py` — §2, §4
- `forgetting_policy_linter.py` — §5 (checks F2 dedup, F3 consolidation)
