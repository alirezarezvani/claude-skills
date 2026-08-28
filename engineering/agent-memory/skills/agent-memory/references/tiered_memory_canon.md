# Tiered agent memory — the canon, and what this skill takes from it

Every claim below carries a confidence level. Where a source is paraphrased
rather than quoted, that is stated. Where a figure comes from a vendor rather
than a controlled study, that is stated too — following the `andreessen`
precedent in this repo.

---

## 1. The idea: tiers are an *injection policy*, not a storage format

**Confidence: high** (this is the load-bearing design claim, and it is
architectural rather than empirical).

The reflex when adding memory to an agent is to pick a store — vector DB, graph,
JSONL — and treat tiering as an implementation detail of that store. That gets
the dependency backwards. What actually distinguishes a tier is **when its
contents enter the context window**:

| Tier | Injection policy | Consequence |
|---|---|---|
| L0 | never | may be arbitrarily large |
| L1 | on lexical relevance, per prompt | must be cheap to scan and cheap to be wrong about |
| L2 | once per session, project-scoped | must be small and must be right |
| L3 | always | must be *very* small and must be nearly certain |

Because the constraint tightens monotonically as you climb, the interesting
engineering is not storage — it is the **gate between tiers**. A design that
specifies four stores but not four gates has specified nothing.

## 2. TencentDB-Agent-Memory — the source of the framing

**Confidence: moderate on specifics, high on the framing.** The framing
(hierarchical memory with promotion between levels, backed by a database) is
clearly the project's organising idea. Specific API surface and defaults change;
read the repository rather than trusting a summary of it.

- Source: <https://github.com/TencentCloud/TencentDB-Agent-Memory>

What this skill **took**: the tier ladder, and the principle that a memory
system's value is in what it refuses to promote.

What it **rejected**, and why:

1. **The database.** A managed DB is a deployment dependency this repo's skills
   cannot carry (root `CLAUDE.md`: stdlib only, self-contained packages). One
   append-oriented JSONL file per project is enough for a store capped at 500
   candidate atoms.
2. **A proxy layer between the agent and the model.** Claude Code already has
   the interception points — `SessionStart`, `UserPromptSubmit`, `SessionEnd`.
   Adding a proxy to obtain hooks a platform already provides buys nothing and
   costs a failure mode on the critical path.
3. **LLM-based extraction.** Root `CLAUDE.md` forbids LLM calls in skill
   scripts. This is not merely compliance: an extractor that calls a model
   cannot run in an async teardown hook on a latency budget, and its output is
   not reproducible from the transcript, which breaks "cite, don't invent."

## 3. MemGPT / Letta — memory as an OS paging problem

**Confidence: high on the core analogy, moderate on current implementation
details** (the project has been renamed and substantially rewritten).

Packer et al., *MemGPT: Towards LLMs as Operating Systems* (arXiv:2310.08560),
frames finite context as physical memory and everything else as disk, with the
model itself issuing paging calls. The durable contribution is the framing: a
context window is a **cache**, and every cache needs an eviction policy someone
chose on purpose.

- <https://arxiv.org/abs/2310.08560>
- <https://github.com/letta-ai/letta>

**Divergence, deliberate:** MemGPT lets the *model* decide what to page in.
This skill does not. Model-driven promotion means a confident wrong statement
promotes itself; recurrence across sessions cannot be produced by confidence.

## 4. Generative Agents — reflection, and the cost it implies

**Confidence: high** (widely replicated; the architecture is described in
detail in the paper).

Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*
(arXiv:2304.03442), pairs a raw observation stream with periodic **reflection**
that synthesizes higher-level statements — a promotion ladder in all but name,
retrieving on recency, importance, and relevance.

- <https://arxiv.org/abs/2304.03442>

**Divergence:** reflection there is an LLM call scoring importance. Here
importance is not scored at all — it is *observed*, as recurrence. That is a
strictly weaker signal, and the trade is deliberate: it is deterministic,
auditable, and free.

## 5. Spaced repetition — why recurrence is the right durability signal

**Confidence: high on the effect, moderate on transferring it to agents.** The
spacing effect is one of the most replicated findings in learning research
(Ebbinghaus, *Über das Gedächtnis*, 1885; and the modern review literature,
e.g. Cepeda et al., *Distributed practice in verbal recall tasks*,
*Psychological Bulletin*, 2006). Repetition **distributed across time** produces
durable retention where massed repetition does not.

The transfer to an agent's memory is an **analogy, not a result**. It is why the
L1 → L2 gate requires ≥ 2 distinct calendar days and not merely ≥ 3 sightings:
three sightings in one hour is one conversation restating itself, which is
exactly the massed-practice case the literature says does not indicate
durability.

## 6. Cache promotion policies — the closest true prior art

**Confidence: high.** LRU-K (O'Neil, O'Neil & Weikum, SIGMOD 1993) promotes a
page on its **K-th** reference rather than its first, specifically to stop a
single scan from evicting a genuinely hot working set. ARC (Megiddo & Modha,
FAST 2003) maintains recency and frequency lists separately for the same reason.

- O'Neil et al., *The LRU-K Page Replacement Algorithm* (SIGMOD 1993)
- Megiddo & Modha, *ARC: A Self-Tuning, Low Overhead Replacement Cache* (FAST 2003)

The L1 → L2 gate is LRU-K with K = 3 and a wall-clock spread requirement. This
is the most honest description of what the gate is.

## 7. Anthropic on context engineering

**Confidence: moderate.** Anthropic's engineering writing on context management
and long-running agents consistently makes one point relevant here: context is a
scarce, curated resource, and what you *leave out* is a design decision. See
<https://www.anthropic.com/engineering> for current material.

This is the reason L3 is capped at 30 atoms. A persona tier with no cap is not a
persona — it is a second `CLAUDE.md`, which is the problem this skill exists to
address.

---

## What follows from all of this

1. **Do not let the model promote its own claims.** Every system above that
   works uses an external signal (time, frequency, human) for durability.
2. **Cap every tier.** Uncapped memory is the failure mode, not the feature.
3. **Recurrence is weak but cheap and honest.** It under-promotes. Under-
   promotion costs a re-statement; over-promotion costs a wrong instruction in
   every future session.
