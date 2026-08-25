# Designing the gates — why these thresholds, and what they cost

The tiers are easy. The gates are the whole design. This file states what each
threshold is *for*, what it lets through, and what it wrongly blocks — because a
gate whose failure modes are undocumented will be "fixed" by the first person
who hits one.

---

## 1. The asymmetry that sets every threshold

**Confidence: high** — this is a decision, not a measurement, and it is the
premise everything else follows from.

The two error directions are not equally expensive:

| Error | Cost |
|---|---|
| **Under-promote** a true claim | the user restates it once; the restatement is itself an observation, so the system self-corrects |
| **Over-promote** a false claim | it is injected into *every* future session, silently steering work, until a human notices and hunts down where it came from |

Under-promotion is self-healing. Over-promotion is not. Every threshold is
therefore tuned toward refusing, and every ambiguous case resolves to "stay
where you are."

## 2. Why 3 sessions, and why days matter separately

**Confidence: high on the reasoning; the specific numbers are judgement, not
measurement.**

Three *sessions* filters the single-conversation artifact: a claim restated
three times inside one debugging session is one belief, expressed three times.
Session count alone does not fix this, because sessions can be minutes apart.

The **≥ 2 distinct calendar days** requirement is the part doing the real work.
It comes from the spacing effect (see `tiered_memory_canon.md` §5) and applies
to *every* path except `verified`. Note the implementation detail worth
preserving: because `first_seen` and `last_seen` **bound every observation**,
comparing their dates is *equivalent to* "≥ 2 distinct calendar days" — not a
proxy for it. Anyone tempted to store a full date set to be "more correct"
should know they would be storing data that cannot change the answer.

**What this wrongly blocks:** a genuine one-day-only fact — a decision made and
acted on in a single sitting, never mentioned again. It stays at L1 and is
recalled on relevance, which is the correct place for it. It is not lost; it is
just not promoted to always-loaded.

## 3. The confidence fast paths

| Confidence | Sessions needed | Day rule |
|---|---|---|
| `observed` | 3 | applies |
| `stated` | 2 | **still applies** |
| `verified` | 1 | **exempt** |

**Confidence: high on the design, and this table exists because the exemption is
the most likely thing to be implemented wrong.** `stated` is a shortcut on
*volume*, not on *time* — a user saying a thing outright twice is stronger
evidence than the system inferring it three times, but saying it twice in one
hour is still one conversation.

`verified` is the only day-exempt path, and it is exempt because its evidence is
categorically different: a claim is `verified` when a deterministic check
confirmed it (a command exited zero, a file contained what was claimed). That
is not testimony that needs corroboration over time — it is a measurement.

## 4. Redaction blocks promotion — a *durability-independent* barrier

**Confidence: high. This is the security-critical rule in the design.**

The recurrence gates answer "is this durable?" They do not answer "is this safe
to commit?" Those are different questions, and a secret restated across five
sessions and three days passes every durability gate with room to spare.

So `redacted: true` is a **hard block**, independent of all evidence. The
reasoning:

1. The flag firing means the redaction pass **altered the claim** — positive
   evidence the source text contained something sensitive.
2. Redaction is **lexical**. Finding one secret is not proof of finding every
   secret in the same sentence.
3. L2 and L3 are **committed to git**. The blast radius of being wrong is
   permanent and public.

A human reviews it at `adopt`. There is no volume of evidence that substitutes
for that review.

## 5. Contradiction blocks promotion, and detection is a filter

**Confidence: high on the mechanism; explicitly limited on coverage.**

Two deterministic rules — explicit negation, and same-subject value swap — run
at merge time over atoms sharing a project. On a fire, the **older** atom is
marked contested; the newer is not auto-blessed. Both freeze.

Three things about this are worth stating plainly, because each has been
implemented wrong somewhere:

- **The newer atom carries no flag.** So the "no contradiction open" check
  cannot be a field read on both sides — it is a **reverse join**: blocked if
  your own `contested` is set *or* your id appears in anyone's `contested_by`. A
  mirrored field would be the same fact stored twice with nothing able to say
  which copy is right.
- **Detection cannot reach the global tier.** A global atom carries no project,
  so it is in no group the detector forms. This is structural, not a missing
  loop.
- **The rules will miss semantic contradictions.** "Always squash-merge" vs
  "keep merge commits" needs meaning, not string shape. Both promote; the
  conflict surfaces one tier later, tagged, for a human. **Detection is a
  filter, never a guarantee** — the human gate is what actually holds.

## 6. Caps, and the two different things a cap can mean

**Confidence: high.**

| Tier | Cap | On overflow |
|---|---|---|
| L1 | 500 | evict oldest by `last_seen` — it is the recoverable tier |
| L2 | 60 / project | **demote** to L1 — recoverable, not destroyed |
| L3 | 30 | **refuse inflow** — never auto-demote |

The L3 rule is the subtle one. "Never auto-demoted" is a promise to the user
that a stable persona line will not silently disappear. Honouring it means the
cap must block *entry*, not force *exit*. A full L3 is a signal for a human to
prune, not a licence for the system to.

## 7. What would falsify this design

**Confidence: this section is the honest one.** The gates are asserted, not
validated. The specific ways to find out they are wrong:

- **Recall is too low to matter.** If a two-week trial yields a handful of
  atoms and none reach L2, rule-based extraction is not viable and the honest
  response is to delete the folder — not to loosen the gates until something
  passes.
- **Precision is worse than claimed.** If atoms that reach L2 are frequently
  things the user would not have written down, the markers are catching
  conversational filler.
- **The store is never read.** If `--why` is never run and staged promotions are
  adopted without review, the human gate is theatre and the security argument
  above collapses.

## Sources

1. O'Neil, O'Neil & Weikum, *The LRU-K Page Replacement Algorithm*, SIGMOD 1993
   — promotion on the K-th reference.
2. Megiddo & Modha, *ARC: A Self-Tuning, Low Overhead Replacement Cache*,
   FAST 2003 — separating recency from frequency.
3. Cepeda et al., *Distributed practice in verbal recall tasks: A review and
   quantitative synthesis*, Psychological Bulletin, 2006 — the spacing effect.
4. Park et al., *Generative Agents* (arXiv:2304.03442) — reflection as
   promotion, and importance scoring as its gate.
5. Packer et al., *MemGPT* (arXiv:2310.08560) — context as a cache with an
   eviction policy.
6. TencentDB-Agent-Memory —
   <https://github.com/TencentCloud/TencentDB-Agent-Memory> — the tier ladder
   this design rebuilds natively.
7. This repo's `engineering/skillopt-sleep` — the staging discipline
   ("propose, never apply") reused here rather than reinvented.
