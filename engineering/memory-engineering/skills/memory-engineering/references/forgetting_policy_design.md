# Forgetting Policy Design — and where memory hits the hardware

> The keystone, plus the Nvidia lens: *how do you forget on purpose, and where
> does all of it land on the GPU?*

---

## 1. Why forgetting must be designed before the store grows

The single most consequential finding for anyone shipping agent memory:

> "None of the evaluated systems prune or forget by default, so footprint grows
> monotonically under default behavior."
> — Omri et al., arXiv:2606.06448 (confidence: **high**)

Read that as an engineering instruction: **if you did not build forgetting, you
do not have it.** Not from your vector database, not from your memory
framework, not from your agent SDK.

And the cost of retrofitting is asymmetric. Adding a forgetting policy to an
empty store is a config decision. Adding one to a store with two years of
accumulated records is a data-migration project with a judgment call attached to
every record — which is why it never happens, and why the store keeps growing.

**Slope beats baseline.** The paper's recommendation 9 is to evaluate both
baseline footprint *and* cost growth slope. A store that starts at 2 GB and
grows 1%/month is healthier than one starting at 200 MB and growing 40%/month.
Agentic systems (Paradigm IV) compound worst, because the store itself becomes
input to the next construction pass.

## 2. The four forgetting mechanisms

Pick at least one. They compose.

| Mechanism | Rule | Best when | Failure mode |
|---|---|---|---|
| **TTL** | Expire after N days | Facts with a natural shelf life (prices, staffing, config) | Deletes a still-true fact nobody restated |
| **Capacity bound** | Cap records/bytes, evict by policy | Hard budget, predictable cost | Eviction order becomes the real policy — LRU evicts rare-but-critical facts |
| **Relevance decay** | Score decays unless retrieved; expire below threshold | Retrieval frequency correlates with value | Self-reinforcing: never-retrieved-because-never-surfaced records die |
| **Consolidation** | Merge N related records into one denser record | Many thin records on one topic | Lossy merges destroy the distinctions that mattered |

**On eviction order.** If you use a capacity bound, the eviction policy *is*
your forgetting policy — "LRU" is a real design decision, not a default. Recency
is a poor proxy for value in memory systems: the fact you look up once a year is
often the one you cannot reconstruct.

## 3. Never auto-merge contradictions

This is check **F4** in the linter, and it is blocking.

When two stored memories disagree, the tempting resolutions are all wrong:

- **`newest_wins`** — assumes recency implies correctness. Often it means the
  newest session was confused.
- **`auto_merge`** — produces a record that says something neither source said.
- **`overwrite` / `last_write_wins`** — the storage layer's default, chosen by
  nobody, silently destroying the evidence that a conflict existed.

**Two memories that disagree may both have been true in different contexts.**
"Deploys go through Jenkins" and "deploys go through GitHub Actions" are not a
contradiction to resolve — they are a migration to record, and the interesting
information is *when it changed and why*.

The rule: **the system surfaces, the human decides.** Surface both versions with
their sources and timestamps. A contradiction is a signal that your model of the
world is out of date, which is exactly the signal you do not want auto-resolved.

## 4. Where all of this lands on the hardware

Strip away the algorithms and every memory decision becomes a GPU decision.

**Keeping full history in context is quadratic, not merely slow.** Attention
cost grows with the square of sequence length, so doubling retained history
roughly quadruples the attention work.

**Prefix caching saves you within a session and collapses across sessions.**
The KV cache that makes turn 40 cheap in one conversation does not carry to
tomorrow's conversation. Inter-session memory is precisely the case where the
cache does not help — which is why "just keep it in context" degrades from a
cost problem into a feasibility problem at session boundaries.

**The scarce resource is KV cache in high-bandwidth memory.** A memory engineer
should be able to state their system in these units: HBM bandwidth, GPU
utilization, tokens/second, and KV slots freed. Under every clever retrieval
scheme, the real currency is cache.

MEMENTO makes the connection concrete: compressing reasoning blocks into
summaries cut peak KV cache ~2.5× and improved vLLM throughput ~1.75×
(arXiv:2604.09852, confidence: **high**). Forgetting *is* a throughput
optimization.

## 5. Construction is a background job

Construction is almost pure prefill — long reads in, short writes out — so it
behaves like a background indexing job, not like a user request.

**Co-locate it with live queries and a large write will stall the scheduler
exactly when a user query arrives.** Prefill saturates the GPU; a query that
lands behind a big construction batch waits for it.

The controls, per the paper's recommendations 3, 6, 8 and 10:

1. **Rate-limit** construction with admission control.
2. **Batch** writes rather than constructing per-session inline.
3. **Defer** construction off the latency-sensitive path entirely.
4. **Cap** LLM-bounded retrieval loops — worst-case latency is a selection
   criterion, and agentic systems have no natural bound without one.

`memory_cost_profiler.py` flags `CONSTRUCTION_COLOCATED` for exactly this.

## 6. Prove each pass by hand before you schedule it

Before automating any memory pass — extraction, consolidation, contradiction
detection, expiry — run it once, by hand, against your real history.

Ask of the output: **did this change a decision?** If yes, it earns a schedule.
If no, scheduling it just generates noise you will learn to ignore.

**A memory system run against three notes will hallucinate connections that are
not there.** Sparse input produces confident spurious structure, and the
experience of being wrong early trains you to distrust the system permanently.
Let the store fill with real material first.

## 7. Ship order

The sequence matters, because each step's output is the next step's input:

1. **Build the write path first** — storing facts and skills, not logs — and let
   it fill for a few weeks so there is real material to work with.
2. **Add contradiction detection by hand**, a few times. Schedule it only if the
   collisions surprise you.
3. **Add the forgetting and maintenance policy before volume climbs.** This is
   the step that is easy now and impossible later.
4. **Tune the hardware layer last**, once volume is real: batch construction,
   cap retrieval, watch the KV cache.

Do not schedule everything on day one. Get one manual run reliable, wrap it,
then automate it.

## 8. The eight checks

What `forgetting_policy_linter.py` enforces:

| ID | Check | Blocking |
|---|---|---|
| F1 | Explicit forgetting rule (TTL, capacity, or decay) | **Yes** |
| F2 | Dedup at write time | No |
| F3 | Consolidation / compaction | No |
| F4 | Contradictions surfaced, never auto-merged | **Yes** |
| F5 | Read scope and write scope both named | No |
| F6 | Audit trail (timestamp + source attribution) | No |
| F7 | Rollback and delete path | No |
| F8 | Growth-slope monitoring | No |

F1 and F2–F8 come from the Stanford recommendations and the Anthropic control
surface. F4 is blocking because it is the one failure that silently destroys
information rather than merely accumulating it.

---

## Sources

1. Omri, Y. et al. — *Agent Memory: Characterization and System Implications of
   Stateful Long-Horizon Workloads*, arXiv:2606.06448.
   <https://arxiv.org/abs/2606.06448> — §1, §5, §8.
2. Kontonis, V. et al. — *MEMENTO: Teaching LLMs to Manage Their Own Context*,
   arXiv:2604.09852. <https://arxiv.org/abs/2604.09852> — §4.
3. Kwon, W. et al. — *Efficient Memory Management for Large Language Model
   Serving with PagedAttention* (vLLM), SOSP 2023. KV cache paging and prefix
   reuse mechanics behind §4.
4. Dao, T. et al. — *FlashAttention* (2022) and *FlashAttention-2* (2023). The
   quadratic-attention cost structure referenced in §4.
5. Ebbinghaus, H. — *Über das Gedächtnis* (1885), and Bjork, R. A. & Bjork,
   E. L. — *A New Theory of Disuse* (1992). The retrieval-strength/decay model
   behind relevance decay in §2.
6. Anthropic — *Built-in memory for Claude Managed Agents*.
   <https://claude.com/blog/claude-managed-agents-memory> — §8 controls F5–F7.
7. Denning, P. J. — *The Working Set Model for Program Behavior* (1968), and the
   LRU/LFU cache-eviction literature. Prior art for §2's eviction-order warning.

## Related tools in this skill

- `forgetting_policy_linter.py` — §2, §3, §8
- `memory_cost_profiler.py` — §5
