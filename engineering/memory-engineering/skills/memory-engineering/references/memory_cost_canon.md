# Memory Cost Canon — what remembering actually costs

> The Stanford lens: *what does remembering cost?*
>
> Every figure below is attributed and carries a confidence level. Where the
> popular summary of this research differs from the paper, the paper wins and
> the difference is called out.

---

## 1. The finding that reorders your priorities

**Construction, not retrieval, dominates the lifecycle cost of LLM-mediated
agent memory.**

> "For LLM-mediated agent memory systems, construction energy exceeds total
> query-phase energy across 300 queries."
> — Omri et al., *Agent Memory: Characterization and System Implications of
> Stateful Long-Horizon Workloads*, arXiv:2606.06448 (confidence: **high** —
> direct quote, measured with a phase-aware profiling harness)

This is uncomfortable because query latency is the number you watch: the user
feels it, your dashboard graphs it, your on-call pages on it. Construction is
invisible — it happens after the session, on a background worker, and nobody
has an SLO for it.

The practical consequence: **tuning retrieval on a write-heavy memory system is
optimizing the smaller half of the bill.**

## 2. Normalize by correct answers, never by accuracy alone

Accuracy hides cost. Two systems can report the same benchmark score while
differing by more than an order of magnitude in energy per useful result.

Measured spread across the ten evaluated systems:

| System | Energy per correct answer | Multiple vs baseline |
|---|---|---|
| BM25 (lexical baseline) | 4,145 J | 1× |
| A-Mem | ~115 kJ | ~28× |
| MIRIX | ~197 kJ | ~47× |

> "The spread across agent memory systems exceeds 47×."
> — Omri et al., arXiv:2606.06448 (confidence: **high**)

⚠️ **Correction to a widely-shared summary.** A popular thread describing this
paper states that *"two systems with identical accuracy split by 47 times."*
That is not what the paper reports. The 47× is the **spread across the ten
evaluated systems** (BM25 baseline vs. MIRIX), and A-Mem/MIRIX are described as
a "28–47× premium" — not a pair matched on accuracy. The directional lesson
survives intact and is still the right one: *quote quality and cost together,
always.* But do not cite the 47× as an accuracy-matched comparison.

## 3. The four paradigm families

The paper's taxonomy classifies systems along four axes — **construction,
storage, retrieval, and mutability** — yielding four families:

| Paradigm | Family | Evaluated systems |
|---|---|---|
| I | Long-context memory | `long_context` |
| II | Flat RAG memory | BM25, EmbedRAG |
| III | Structure-augmented RAG | GraphRAG, HippoRAG v2, Mem0, SimpleMem |
| IV | Agentic control flow | Letta, MIRIX, A-Mem |

(confidence: **high** — taxonomy and system list quoted directly)

**No family wins on all three of construction time, query latency, and
accuracy.** The paper is explicit that "no single system is therefore best on
all three axes." This is why `memory_architecture_picker.py` never returns a
"best" — it returns the family that fits your constraints and names the cost
that choice makes you pay.

## 4. Footprint grows monotonically, because nothing forgets

> "At 1M tokens, footprint varies by up to 9× across systems... None of the
> evaluated systems prune or forget by default, so footprint grows
> monotonically under default behavior."
> — Omri et al., arXiv:2606.06448 (confidence: **high**)

Two lessons, in order of importance:

1. **Forgetting is not a feature any of these systems gives you.** If you did
   not build it, you do not have it. This is the entire justification for
   `forgetting_policy_linter.py` treating a missing forgetting rule as a
   blocking failure rather than a warning.
2. **Judge growth slope, not baseline footprint.** A store that starts small
   with a steep slope bankrupts you later than one that starts large and flat —
   but it still bankrupts you, and it does so after you have built on it.

## 5. The ten system recommendations

Paraphrased from the paper (confidence: **high** on existence and substance,
**moderate** on exact wording):

1. Treat system selection as a systems-level decision, beyond accuracy.
2. Account for energy across the full agent lifecycle.
3. Treat construction as background throughput with admission control.
4. Exploit reuse across overlapping inputs.
5. Treat the minimum viable construction LLM as an algorithm-imposed cost floor.
6. Match the cost split to the workload's query arrival pattern.
7. Treat construction time as a hard feasibility constraint for inter-session
   workloads.
8. Make construction cadence system-aware.
9. Evaluate both baseline footprint and cost growth slope.
10. Treat worst-case latency as a selection criterion; LLM-bounded systems need
    caps.

Recommendations 3, 6, 9 and 10 are the ones this skill's tools enforce
mechanically.

## 6. Amortization: the question behind recommendation 4

A constructed record has to be read enough times to justify what it cost to
write. If your agent writes 400 records a day and serves 1,200 queries, each
record serves 3 queries on average — you are paying to remember things nobody
asks about.

`memory_cost_profiler.py` flags this below 10 queries per record. The floor is
a heuristic chosen for this skill, not a number from the paper (confidence:
**low** on the specific threshold, **high** on the principle).

The fix is usually *lazy construction*: build the memory record on second
access rather than eagerly at the end of every session.

---

## Sources

1. Omri, Y., Gan, Z., Broveak, Z., Geens, R., He, Z., Pentland, A., Verhelst,
   M., Weissman, T., Tambe, T. — *Agent Memory: Characterization and System
   Implications of Stateful Long-Horizon Workloads*, arXiv:2606.06448 (2026).
   <https://arxiv.org/abs/2606.06448> — the primary source for §1–§5.
2. MemoryAgentBench — the benchmark suite used for the characterization,
   evaluating accurate retrieval, test-time learning, long-range understanding,
   and selective forgetting.
3. Robertson, S. & Zaragoza, H. — *The Probabilistic Relevance Framework: BM25
   and Beyond* (2009). Establishes the lexical baseline that turns out to be
   the energy-efficiency floor in the Stanford run.
4. Kwon, W. et al. — *Efficient Memory Management for Large Language Model
   Serving with PagedAttention* (vLLM), SOSP 2023. The serving substrate the
   hardware findings sit on.
5. Chase, H. et al. — Mem0 / LangMem / Letta system documentation. Primary
   sources for the Paradigm III and IV systems named above.
6. Gao, Y. et al. — *Retrieval-Augmented Generation for Large Language Models:
   A Survey*, arXiv:2312.10997. Background for the Paradigm II family.
7. Anthropic — *Effective context engineering for AI agents* (2025).
   Practitioner framing of context as a finite, priced resource.

## Related tools in this skill

- `memory_cost_profiler.py` — §1, §2, §6
- `memory_architecture_picker.py` — §3
- `forgetting_policy_linter.py` — §4 (checks F1 and F8)
