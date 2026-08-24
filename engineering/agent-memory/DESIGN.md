# agent-memory — design spec (NOT YET IMPLEMENTED)

> **Editing this file? Run the checker first — nothing in CI will.**
> ```sh
> python3 skills/agent-memory/scripts/validate_examples.py
> ```
> It ties this doc, `assets/memory_schema.json`, and the fixtures together
> (§10.1). Drift between those three was the dominant defect class during this
> spec's review, and the checker is the only thing that catches it.

**Status:** design stage. No `SKILL.md`, no `plugin.json`, no Python. This folder
holds a specification and two contract files (`hooks/hooks.json`,
`assets/memory_schema.json`) so the shape can be reviewed before anything is
built. Repo counters are intentionally untouched — `scripts/derive_counters.py`
counts skills by `SKILL.md`, and this folder deliberately has none.

**Where this file lives is an open maintainer decision**, not a settled
convention — `engineering/` here, versus `audit/` or the gitignored
`documentation/`. The full comparison is in [§11](#11-where-this-file-should-live),
at the end, so it does not stand between a reader and the spec.

**Origin:** an inspection of
[TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory)
(MIT, © 2026 Tencent, v2.0.0). This spec **borrows two design ideas** from that
project — the L0→L3 memory tiering and the ownership/visibility model — and
**rejects its integration mechanism**. No Tencent code is vendored. See
[§8 Rejected](#8-rejected-memoryproxy) for why.

---

## 1. The problem

Claude Code memory today is flat. `CLAUDE.md` has exactly one injection policy:
**always inject, in full, every session**. That single policy is the cause of
three failure modes this repo already sees at 360+ skills:

1. **Bloat** — root `CLAUDE.md` in this repo is **88 KB** (`wc -c` → 90,312
   bytes, measured at this branch's base) of release notes, loaded
   into every session regardless of whether the task touches `markdown-html/` or
   `ra-qm-team/`. It read 85,875 bytes when this spec was first written and
   grew **4,437 bytes while this PR was open** — the §1 thesis demonstrating
   itself on the file it is about.
2. **Staleness** — nothing expires. A v2.7.0 note sits at the same priority as a
   v2.11.2 one.
3. **False permanence** — a fact stated once in one session, if written down,
   becomes indistinguishable from a fact that has held across fifty sessions.

Tiering fixes this by splitting memory on **durability** and giving each tier its
own retrieval policy.

---

## 2. Overlap analysis — what already exists

This is the section that decides whether the plugin should be built at all.
Verified by reading the code, not the docs.

### 2.1 `engineering/skillopt-sleep/` — substantial overlap

Already implemented, stdlib-only:

| Capability | Where | Verdict |
|---|---|---|
| Walks `~/.claude/projects/*/*.jsonl` → `SessionDigest` | `harvest.py:259-289` | **This is the L0 reader.** Already done. |
| Writes into `CLAUDE.md` inside a protected marker block | `memory.py` (`LEARNED_START`/`LEARNED_END`) | Reusable pattern for L2/L3 writes. |
| Held-out validation gate before adoption | `gate.py`, `consolidate.py:87` | Different purpose — see below. |
| Secret redaction across every persisted artifact | `redact_secrets()` | **Must be reused.** Non-negotiable. |
| `SessionEnd` hook, async | `hooks/hooks.json` | Same trigger point L0 capture needs. |
| Staging + explicit `adopt` with backup | `staging.py` | Correct human-gate model; copy it. |

**What it does not have — and this is the entire delta:**

- **No tiers.** Every learned line lands in one flat `LEARNED` block. There is no
  L1/L2/L3 separation and therefore no per-tier injection policy — the exact
  problem in §1.
- **No recall.** There is no `UserPromptSubmit` hook. Nothing retrieves a
  relevant fact *during* a session; consolidation is strictly offline/nightly.
- **No durability gate.** `gate.py` asks *"does this edit score better on replayed
  tasks?"* — a **quality** gate. Tiering needs a **recurrence** gate: *"has this
  held across N independent sessions?"* These are orthogonal; a claim can be
  high-quality and still be a one-off.
- **No project/global scoping.** No notion of "true in `claude-skills`" vs "true
  everywhere."

### 2.2 `productivity/handoff/` — adjacent, complementary

Has the `SessionStart` + `SessionEnd` hook pair this spec needs
(`hooks/hooks.json`), plus a 17-pattern redaction linter. Handoff is
**single-hop**: session *n* → session *n+1*, one file, user-authored, discarded
after. Memory is **many-hop and cumulative**. Different lifetimes; no conflict.
Reuse the hook wiring pattern and the redaction linter's pattern list.

### 2.3 `engineering/llm-wiki/` — different axis

Wiki is *curated external knowledge* the user deliberately ingests. Memory is
*observed operational fact* the agent passively accumulates. Overlap is only at
L2. Keep separate; L2 may cite a wiki page, never duplicate it.

### 2.4 `engineering-team/self-improving-agent/` — narrow

`PostToolUse` on `Bash` for error capture only. A useful **additional L1 source**
(failed commands are high-signal facts), not a competing system.

### 2.5 `engineering/memory-engineering/` — different layer, shared gate

Merged to dev via #947, after this spec's first draft — added here so §2 reflects
the tree this folder would actually land in.

`memory-engineering` is an **advisory/audit toolkit**: it prices, picks, and
audits *other* memory systems (`memory_cost_profiler.py`,
`memory_architecture_picker.py`, `memory_density_auditor.py`,
`forgetting_policy_linter.py`). It designs memory systems; it does not run one.
`agent-memory` would **be** a runtime memory system for Claude Code. Different
layer — neither supersedes the other, and its SKILL.md claim that the repo's
nearest neighbours "all bound something else" stays true only while this fence
holds.

Three concrete touchpoints, adopted as constraints on this spec:

1. **Namespace fence:** `agent-memory` (runtime layer) vs `memory-engineering`
   (advisory layer). Both SKILL.md descriptions must cross-reference the other
   with this exact distinction when agent-memory ships.
2. **The forgetting policy is expressible in F1–F8 form.** §5.1's eviction and
   contradiction rules will be written so
   `memory-engineering/scripts/forgetting_policy_linter.py` can lint them:
   F1 (an explicit forgetting rule — the ≤500/≤60/≤30 caps + recurrence decay)
   and F4 (contradictions surfaced, never auto-merged — §5.1 already mandates
   this) are the blocking checks, and this spec must pass them, not re-derive
   its own variants.
3. **Cost discipline:** before implementation, `memory_cost_profiler.py`'s
   construction-vs-query split is the framework for the §7 latency/cost budget
   — the measured 23.2 ms scan cost belongs in its cost-per-correct-answer
   terms, not as a bare number.

### 2.6 Conclusion

> **Build as a separate, self-contained plugin. Do not extend `skillopt-sleep`.**

Two reasons:

1. `skillopt-sleep` is a **vendored** copy of `microsoft/SkillOpt` carrying 23
   documented deviations that must be re-applied on every re-vendor (root
   `CLAUDE.md`). Adding a tiering subsystem inside it would make re-vendoring
   impractical.
2. Root `CLAUDE.md` anti-pattern: *"Creating dependencies between skills (keep
   each self-contained)."*

**Therefore: `agent-memory` MUST NOT `import skillopt_sleep`.** It re-implements
the ~40 lines of jsonl transcript walking independently. This duplication is
deliberate and is the cheaper side of the trade.

---

## 3. Tier schema

Four tiers. The distinguishing property is the **injection policy**, not the
storage format.

| Tier | Holds | Storage | Written by | Injection policy | TTL |
|---|---|---|---|---|---|
| **L0** | Raw session transcripts | `~/.claude/projects/*/*.jsonl` (pre-existing, read-only) | Claude Code itself | **Never injected.** Queried on demand only. | Claude Code's own retention |
| **L1** | Atomic facts — one claim each | `.memory/atoms.jsonl` (project-local, gitignored) | `SessionEnd` extraction | Retrieved by relevance at `UserPromptSubmit`, capped | 90 days, refreshed on re-observation |
| **L2** | Project-scoped context | `CLAUDE.md` marker block (committed) | Promotion from L1 | Injected at `SessionStart`, **current project only** | Until demoted |
| **L3** | Stable cross-project persona | `~/.claude/CLAUDE.md` marker block | Promotion from L2 | Always in context. Hard cap. | Until demoted |

### 3.1 L1 atom record

**13 fields are unconditionally required** — `id`, `claim`, `scope`, `kind`,
`first_seen`, `last_seen`, `observations`, `sessions`, `source`, `first_source`,
`confidence`, `tier`, `redacted`. An atom missing provenance is discarded, not
stored.

**`redacted` is required on purpose**, unlike the other later-stage fields: §6
rule 1 makes redaction non-negotiable **before any write**, so every atom that
exists on disk has already been through the pass and knows its answer. Leaving
it optional would make an atom that skipped redaction entirely schema-*valid* —
exactly the state the rule forbids. Requiring it turns "redaction ran" into
something `memory_promote.py` can **check** rather than trust.

The rest are conditional or optional, and an extractor **must not** emit them
unconditionally: `project` is required when `scope: "project"` and *forbidden*
when `scope: "global"` (§3.1's conditional); `promoted_from_projects` is required
only at `tier: "L3"` (§4.1.1); `contested`, `contested_by` and `promoted_at` are
set by later stages — contradiction handling (§4.2) and promotion respectively —
not at extraction time. The example below shows `project` because it is a
project-scoped atom, not because that field is universally mandatory.

```json
{
  "id": "atm_961f033d",
  "claim": "PR base branch is dev, never main",
  "scope": "project",
  "project": "claude-skills",
  "kind": "constraint",
  "first_seen": "2026-07-02T09:11:04Z",
  "last_seen": "2026-07-02T09:11:04Z",
  "observations": 1,
  "sessions": ["01SESSIONAAAA11112222333"],
  "source": "~/.claude/projects/-home-user-claude-skills/01SESSIONAAAA11112222333.jsonl#L77",
  "first_source": "~/.claude/projects/-home-user-claude-skills/01SESSIONAAAA11112222333.jsonl#L77",
  "confidence": "observed",
  "tier": "L1",
  "redacted": false
}
```

- `kind` ∈ `constraint` · `preference` · `fact` · `decision` · `failure`
- `sessions` is a **set** — this is what makes the promotion gate countable.
  Re-stating a claim twice in one session does not increment durability.
- `source` / `first_source` are back-pointers into L0. Any promoted claim must be
  traceable to a transcript line, or it cannot be promoted — the anti-fabrication
  rule. **Both are kept deliberately:** `source` is overwritten on every merge, so
  after N observations it points only at the latest sighting; `first_source` is
  written once and never overwritten, preserving the evidence that originally
  justified the claim. A single field would lose exactly the record an auditor
  asking "why does the agent believe this?" needs.

- `confidence` ∈ `observed` (agent inferred it) · `stated` (user said it
  directly) · `verified` (a check confirmed it). `stated` and `verified` promote
  faster — see §4.

#### 3.1.1 Back-pointer format is tier-dependent — and must be

| Tier | Format | Why |
|---|---|---|
| **L1** (gitignored) | `~/.claude/projects/<cwd-slug>/<session>.jsonl#L<line>` | Local, never leaves the machine. Direct-openable. |
| **L2 / L3** (committed) | `<session>.jsonl#L<line>` — **no path prefix** | Committed tiers must be de-identified (§6). |

**This is not cosmetic.** `<cwd-slug>` is Claude Code's slugification of the
*absolute* working directory, so on a real machine it is
`-home-alice-work-claude-skills`, not `-home-user-…` — **it embeds the operating
system username.** Since `source` and `first_source` are unconditionally
required at every tier, a naive implementation of "cite, don't invent" would
write a contributor's username into a shared, git-tracked `CLAUDE.md` on the
first promotion — precisely the identifying-data class §6 exists to keep out.
Rule 4 (cite) and the §6 admission policy would be in direct conflict, and rule
4 would win by being the more mechanical of the two.

**Resolution: promotion strips the prefix.** The transcript stays findable by
globbing `~/.claude/projects/*/<session>.jsonl` locally at read time — the
prefix is *derivable*, so storing it buys nothing and costs de-identification.
Provenance is fully preserved; only the machine-specific part is dropped.

**Windows: the L1 pattern rejects a native path, so the extractor must
normalize rather than record.** The schema's L1 back-pointer regex is
`^~/\.claude/projects/[^/]+/[A-Za-z0-9._-]+\.jsonl#L[0-9]+$` — a literal `~/`
and forward slashes. A path built from `%USERPROFILE%\.claude\projects\…`
matches nothing, so an extractor that records the OS path verbatim emits an atom
the schema **rejects outright** on Windows. Not a cosmetic difference.

The resolution is mechanical, not an open question: **`source` and `first_source`
store a canonical form, not an observed one.** The extractor derives
`~/.claude/projects/<dir>/<session>.jsonl#L<n>` — `~/`-relative, forward slashes
— from whatever the platform actually handed it, the same way §3.1.1's promotion
step derives the stripped form rather than storing what it saw. Recording is
already a transform here; this adds one more case to it.

Blast radius is one tier, and it is the local one: **L2 and L3 are already
platform-neutral**, because the stripped form is a bare `<session>.jsonl#L<n>`
with no path at all. So nothing committed is affected — only L1, which is
gitignored. That is a consequence of §3.1.1's de-identification stripping,
which turns out to have bought portability for free.

**The uniqueness that rests on, measured rather than assumed.** Claude Code
names transcripts by session id, and on a live install those filenames are
RFC-4122 UUIDs — checked, not inferred:

```
$ ls ~/.claude/projects/*/*.jsonl | head -1 | xargs basename
63840f04-72f5-56b5-b348-2faed7a24e12.jsonl
$ python3 -c "import uuid; u=uuid.UUID('63840f04-72f5-56b5-b348-2faed7a24e12'); print(u.version, u.variant)"
5 specified in RFC 4122
```

One install, one sample — enough to establish the shape, not enough to promise
the scheme is stable across versions. So **the glob must handle its own failure
rather than assume it cannot happen:**

| Glob result | Meaning | Behaviour |
|---|---|---|
| exactly 1 | normal | resolve |
| 0 | transcript aged out of Claude Code's retention | unresolvable — same as any dead back-pointer |
| **≥ 2** | ids collided, or the scheme changed | **unresolvable**, and log it: an atom whose provenance is ambiguous must not present as cited |

The ≥ 2 row is the one worth writing down. Without it, a naive implementation
takes the first match and silently attributes a claim to the wrong session —
a *wrong* citation, which is worse than a missing one under §6 rule 6
("cite, don't invent"). Note the fixtures deliberately use an
obviously-synthetic `01SESSION…` form rather than this shape, so nobody mistakes
a spec example for a real transcript reference; family 5 asserts that.

The trap is that a placeholder can hide this: `-home-user-` which *looks* de-identified because
the username is literally the word "user". A placeholder that flatters the
design is worse than no placeholder — the L2 and L3 fixtures in
`memory_schema.json` now use the portable form, so the examples demonstrate the
rule instead of hiding it.

> **The example above and `memory_schema.json`'s second example share an id
> (`atm_961f033d`) at different tiers — deliberate, not copy-paste.** `id` hashes
> `normalized_claim + project` (§4.1) with **no tier component**, so **L1 → L2
> keeps the id**: the same atom appears here at `tier: "L1"` and there at
> `tier: "L2"`, with the back-pointers stripped (§3.1.1) and `promoted_at` set.
> Read side by side, the pair is one atom's lifecycle. Stability matters —
> merging on re-observation (§4.1) depends on the id not moving as the atom
> climbs.
>
> **Calling it a lifecycle constrains the fixtures, so state the constraints.**
> The L1 snapshot is the *first* sighting of the atom the L2 example later
> became, which forces three things a reader can check: its `first_seen` must
> equal the L2's `first_seen` (promotion takes the **min**, §4.1.1 step 3 — so
> the earliest timestamp survives unchanged and cannot be a later one); its
> back-pointers must be the L2's `first_source` with the path prefix re-attached
> (§3.1.1 strips the prefix and **nothing else** — the line number may not
> drift); and its `sessions` must be a subset of the L2's, since promotion
> unions them. `last_seen`, `observations` and `confidence` are the fields free
> to move, because those are what accumulating evidence changes. The checker
> (§10.1, family 7) enforces all of this, because a prose claim that two
> fixtures are one story invites exactly one drift it cannot itself prevent:
> copying the L1 snapshot's timestamp from the L2's `last_seen` and its line
> number from the L2's `source` produces two atoms that each validate alone and
> contradict each other side by side.
>
> **L2 → L3 is the exception, and for a reason:** that step mints a *new*
> project-free id (§4.1.1 step 3), because the hash input itself changes when the
> `project` component drops. It is a merge of ≥ 2 distinct L2 atoms into one, so
> there is no single incumbent id to carry forward — which is exactly why
> `promoted_from_projects` exists to preserve the link back.

Full JSON Schema: [`assets/memory_schema.json`](skills/agent-memory/assets/memory_schema.json).

**Why the schema carries three fixtures, one per tier:** the `examples` array is
not illustration — it is the only thing that exercises the `allOf` branches.
Example 1 is L1 (`kind: "failure"`, full `<cwd-slug>` back-pointer) and exists
specifically to cover the **L1 branch of the back-pointer conditional**, the one
with PII consequences (§3.1.1); examples 2 and 3 cover L2 and L3 with the
stripped form. A tier absent from `examples` is a conditional branch nothing
tests.

Annotations stay in this doc: `examples` entries are instance data, so
`additionalProperties: false` rejects a `$comment` embedded in one. It remains
legal at schema level and inside `allOf` branches, where it is used.

#### 3.1.2 Invariants the schema cannot enforce — the tools own these

JSON Schema validates **one atom at a time**, so a valid atom does *not* imply a
valid store. Three invariants sit outside it and must be enforced in
`memory_extract.py` / `memory_promote.py`, not assumed:

| Invariant | Why the schema can't | Owner |
|---|---|---|
| `first_seen ≤ last_seen` | No cross-field comparison in JSON Schema | extract + merge |
| `id` unique across `atoms.jsonl` | `uniqueItems` applies within one array, not across a file's records | merge (an id collision is a **merge**, never a second record — §4.1) |
| A session id appearing in only one atom's `sessions` per claim | Same file-level limit | merge |

Only *within-atom* `sessions` uniqueness is schema-enforced (`uniqueItems: true`)
— which catches a claim restated twice in one session, the case §4.1's
durability gate actually depends on. The file-level cases are the tools' job.
Stated explicitly because "the schema validates" is otherwise an easy thing to
mistake for "the store is consistent."

---

## 4. Promotion and demotion

The single rule that makes this more than folder naming:

> **A claim climbs a tier because it RECURRED, not because it seemed important.**

Deterministic, no LLM call — consistent with root `CLAUDE.md`'s no-LLM-in-scripts
rule.

### 4.1 Promotion thresholds

| Transition | Requires |
|---|---|
| L0 → L1 | Extraction produces a well-formed atom with a live `source` back-pointer |
| L1 → L2 | **≥ 3 distinct `sessions`** (the gate — *not* `observations`, which is informational; see §3.1), spanning **≥ 2 distinct calendar days (UTC)**, same `project`, no contradiction open |
| L2 → L3 | Held at L2 in **≥ 2 distinct projects**, `age ≥ 30 days`, no contradiction in 30 days |

**Atom identity is project-scoped.**

```
scope=project : id = "atm_" + sha256(normalized_claim + "\0" + project).hexdigest()[:8]
scope=global  : id = "atm_" + sha256(normalized_claim).hexdigest()[:8]
```

`sha256` from stdlib `hashlib` — named explicitly because `hash()` is ambiguous
and Python's builtin `hash()` is **salted per process** for `str`, so using it
would produce different ids on every run and break merging outright.

`normalized_claim` is pinned exactly, because the ids in this doc and in
`memory_schema.json` are **worked examples of this contract** and must
reproduce:

```python
def normalize(claim: str) -> str:
    return re.sub(r"\s+", " ", claim.strip()).casefold().rstrip(".,;:!?")
```

Order matters — collapse whitespace, then casefold, then strip trailing
punctuation. Any deviation silently changes every id in the store.

**On the 8-hex (32-bit) id space** — this is an assumption, so here is the
arithmetic. Birthday collision probability `1 - exp(-n(n-1)/2N)`, `N = 2³²`:

| Atoms in one file | Collision probability |
|---|---|
| 500 (the §5.2 cap) | 0.0029 % |
| 1 000 | 0.0116 % |
| 5 000 | 0.29 % |

Acceptable at the 500-atom cap. **Raising the cap means widening the id.**
Aggregating the per-file figure across independent files: at a 5 000-atom cap,
30 files give `1-(1-0.0029)³⁰ ≈ 8.4 %`, 100 files ≈ 25 %, and it passes even
odds at ~239 files. A collision silently merges two unrelated claims' durability
counters — the exact failure project-scoping below exists to prevent — so it is
worth avoiding well before it becomes likely.

Hashing the claim text alone would let two unrelated claims that normalize alike in
different repos — "tests must pass before merge" is the obvious one — collide on
`id` and merge their `sessions` arrays. That would manufacture false durability,
because the L1→L2 gate above requires the sessions come from the **same**
project. The project component is what makes the gate mean what it says.

#### 4.1.1 The L2 → L3 merge

Because identity is project-scoped, a claim held at L2 in two projects exists as
**two atoms with different ids**. Promotion is therefore a merge, not a flag flip:

1. Group L2 atoms by `hash(normalized_claim)` — the project-free hash.
2. A group with **≥ 2 distinct `project` values**, each ≥ 30 days old and
   uncontested, is eligible.
3. Emit **one** new atom: `scope: "global"`, `tier: "L3"`, new project-free `id`,
   `sessions` = union, `observations` = sum, `first_seen` = min, `last_seen` =
   max, `first_source` = the `first_source` of the contributor with the earliest
   `first_seen`, **`source` = the `source` of the contributor with the latest
   `last_seen`**. Both back-pointers are `required` by the schema, so a merge
   that sets only `first_source` emits an atom the schema rejects; the pairing
   also preserves the field contract — `first_source` is oldest evidence,
   `source` is newest — across the merge boundary rather than only within a
   single atom's history.
4. Record every contributing project in **`promoted_from_projects`**. This field
   is required at L3 and exists for a specific reason: `scope` flips to `global`
   on promotion, and §3.1's conditional then *forbids* the single `project`
   field — so without this array the ≥ 2-projects evidence would be discarded at
   exactly the moment it stops being an eligibility test and becomes an audit
   trail. "Which projects earned this?" must stay answerable afterwards.
5. The contributing L2 atoms are **retained**, not deleted. L3 injection
   supersedes them; they remain as the provenance chain.

**The remaining required fields, stated because the schema requires all 13 and
step 3 only covered nine.** A `memory_promote.py` written literally against the
list above would emit an atom the schema rejects — the same defect this step
has already produced twice (`source`, then `promoted_from_projects`), so the
rule is now: *step 3 must account for every required field, not the interesting
ones.*

| Field | On merge | Why |
|---|---|---|
| `claim` | any contributor's | The grouping key is `hash(normalized_claim)`, so all contributors normalize identically. Take the earliest contributor's raw text for determinism — normalization is lossy on case and trailing punctuation, and the group would otherwise pick arbitrarily. |
| `confidence` | `max()` across **all** contributors | §4.1.3 fixes the order and the never-downgrades rule, but scopes its merge clause to §5.3 — the same-tier `SessionEnd` merge. The same principle applies here and is restated rather than assumed: a claim two projects hold, one `observed` and one `stated`, is `stated` at L3. |
| `redacted` | `true` if **any** contributor is | Conservative direction. A merged atom drawing on redacted evidence must not present as unredacted; over-claiming redaction costs nothing, under-claiming it loses the signal §3.1 requires the field to carry. |
| `kind` | must **agree**, or the group is ineligible | `kind` is *not* in the hash key, so two atoms with identical text but different `kind` can group. If two projects classify the same sentence differently, the "same claim" premise is what is shaky — not the classification. Refusing to merge keeps the claim live at L2 in each project and preserves this section's one-directional property: **L3 under-fires, it never mis-fires.** |

**Stated limit: this merge is lexical, so it only fires on near-identical
text.** Step 1 groups on `hash(normalized_claim)`, and `normalize()` (§4.1) only
collapses whitespace, casefolds, and strips trailing punctuation — it does no
semantic matching. Two projects that independently hold *"PR base branch is
dev"* and *"always target dev for PRs"* express the same rule and will **never**
merge, because the strings differ. The consequence is one-directional and
therefore acceptable: L3 promotion **under**-fires. A cross-project truth stays
duplicated at L2 in each project, where it is still injected at `SessionStart`
for that project — the user loses the global persona entry, not the memory. It
never produces a *wrong* L3 atom, only a missing one. Widening this would take
either an LLM (barred by this repo's no-LLM-in-scripts rule) or a synonym table
tuned per user, which is §9's territory, not v1's. The `adopt` review is where a
human can hand-merge two variants that the hash could not.

**Every promotion into a committed tier (L1→L2 and L2→L3) must also strip the
back-pointer prefix** per §3.1.1 — `~/.claude/projects/<cwd-slug>/X.jsonl#L12`
becomes `X.jsonl#L12`. This is not optional cleanup: skipping it writes an OS
username into a git-tracked file. It is the one transform that must happen at
*both* promotion boundaries, since L1→L2 is the first crossing into committed
territory.

Fast paths **(L1 → L2 only** — L2 → L3 is gated on distinct *projects*, not
session count, so neither shortcut applies there):

- `confidence: "stated"` — an explicit user directive ("always target dev") —
  needs **2** sessions, not 3. The user said it; we are counting whether it
  *sticks*, not whether it is real. **The ≥ 2-distinct-days clause still
  applies** — with exactly 2 sessions, both must not fall on the same day.
  Otherwise one long working day could mint an L2 claim.
- `confidence: "verified"` — a claim a script confirmed — promotes on **1**
  observation, and is the **only** path exempt from the distinct-days clause.
  It is not hearsay.

**A `redacted: true` atom needs human review before any committed tier — it is
not promotable on evidence alone.** The schema has asserted this in its
`redacted` description since it was written; it belongs here, because §4.1's
threshold table is what an implementer builds the gate from and it said nothing.
The reason is the flag's meaning: `redacted: true` says the pass **altered the
claim text**, which is positive evidence the source was sensitive — and
redaction is lexical, so "it found one thing" is not proof it found everything.
Recurrence cannot substitute for a human here; three sightings of a scrubbed
claim are three sightings of the same unresolved risk. The atom stays usable at
L1 and is surfaced at `adopt` rather than promoted past it.

**Both fast paths shorten the route from a transcript to a committed file, and
redaction is the only thing on it.** Worth stating here rather than trusting a
reader to combine §4.1 with §6: the recurrence gates are a *durability* filter,
not a secrets filter — a secret observed in three sessions across three days is
exactly as much a secret as one seen once. So the gates were never protecting
`CLAUDE.md` from a leak; they only made the leak slower. The `verified` path
removes even that, taking a claim from one sighting to a committed marker block
with **§6 rule 1's redaction pass as the sole barrier**. Two consequences:

- **The redaction pass must run on every promotion path, with no fast-path
  shortcut.** An implementation that optimises `verified` by skipping work
  "because a script already confirmed it" would skip the one check that matters.
  Script-confirmed says nothing about whether the text contains a credential —
  *"the staging key `sk-…` works"* is a plausible verified claim.
- **This is the first behavioural test `memory_promote.py` should have** (§10.1
  orders the validator first; this is what follows it): a `verified`, 1-
  observation atom carrying a secret must not reach L2. It is the shortest
  path in the system between raw transcript and committed file, so it is where
  a redaction regression surfaces first and costs most.

#### 4.1.2 `scope` is determined by tier — there is no third promotion path

`scope` is **not** free-form metadata an extractor chooses. It follows tier:

| Tier | `scope` | Produced by |
|---|---|---|
| L1 | `project` | extraction |
| L2 | `project` | L1 → L2 promotion |
| L3 | `global` | **only** the L2 → L3 merge (§4.1.1) |

**Extraction must always emit `scope: "project"`.** Allowing a
`tier: L1, scope: global` atom would create an **unreachable state**: L1 → L2
requires "same `project`", which a global atom has no field for, and L2 → L3 is
a merge over ≥ 2 *L2* atoms. Such an atom could never promote and would sit at
L1 until it expired at 90 days — silently, since nothing would flag it.

This is also right on the merits, not just for totality: **whether a claim is
global is not knowable at extraction.** "Stdlib-only" observed once in one repo
is a project fact; it becomes global only by holding in a second project. Having
the merge mint `global` is the design saying that out loud. Enforced by the
tier/scope conditional in the schema, so an extractor that gets this wrong fails
validation instead of quietly producing orphans.

#### 4.1.3 `confidence` is mutable, monotonic, and re-read at every gate

`confidence` is **not** frozen at extraction. Evidence genuinely strengthens: a
claim the agent first inferred can later be stated outright by the user, or
confirmed by a check. Freezing it would hold an atom to a stricter gate than its
evidence warrants — and the §3.1 / schema example pair (`atm_961f033d` at L1
`observed`, at L2 `stated`) is exactly that upgrade, not a fixture mismatch.

```
observed  <  stated  <  verified          # total order
```

1. **On merge (§5.3), `confidence = max(existing, incoming)`.** The `SessionEnd`
   merge already increments `observations` and extends `sessions`; it takes the
   max of the two confidences at the same time.
2. **Never downgrades.** A later inference cannot demote a claim the user stated
   or a check verified — otherwise a weak re-observation would silently re-impose
   the slower gate, and confidence would oscillate with observation order.
3. **The gate re-reads it at promotion time**, not at creation. An atom that was
   `observed` for two sessions and becomes `stated` in the third is judged on
   `stated`'s 2-session bar, which it has already cleared.

This matters because `confidence` selects both the session count (3 / 2 / 1) and
the distinct-days exemption — so *when* it may change decides which gate an atom
is actually held to. Left unstated, two implementers would reasonably build
different machines.

### 4.2 Contradiction handling

**Scope first, because this section promises more than §4.2.1 delivers.** The
detector groups atoms by `project`, so it covers **L1↔L1 and L1↔L2 within one
project** — every pair the promotion gate actually consults. It **cannot reach
L3 at all**: an L3 atom is `scope: "global"` and carries no `project` field
(§3.1's conditional *forbids* one), so it is never in any group the detector
forms. This is not an oversight to be patched with a loop change — §9.6 explains
why the L3 case is underdetermined rather than merely unimplemented. Read the
rest of this section as **L1/L2 only**.

When a new atom contradicts a claim at L2, the incumbent is **never silently
overwritten**:

1. Mark the incumbent `contested`, record the contradicting atom id.
2. A contested claim is **still injected**, tagged
   `[contested — newer evidence YYYY-MM-DD]`. Withholding it silently would be
   worse than surfacing the conflict. This *rendering* rule is tier-agnostic and
   deliberately so — the schema permits `contested` at any tier, so an L3 atom a
   human contests by hand at `adopt` renders the same way. Only **detection** is
   L1/L2-scoped; nothing about the display half depends on that limit.
3. Resolution requires a human decision at `adopt` time. Never automatic.

This mirrors `skillopt-sleep`'s staging discipline: **propose, never apply.**

#### 4.2.1 Detection at L1 — the gate needs it, so it must be defined

§4.1 gates L1 → L2 on *"no contradiction open"*, so detection cannot start at L2
or the gate references a state nothing produces. Detection runs **at merge time
in `SessionEnd`**, over atoms sharing a `project`, and is deliberately narrow
because it must be deterministic (no LLM, per this repo's rule):

| Rule | Fires when | Example |
|---|---|---|
| **Explicit negation** | Two atoms' normalized claims differ only by a negation token (`not`, `never`, `no longer`, `n't`) | "PR base is dev" vs "PR base is **not** dev" |
| **Same-subject conflict** | Same `kind`, and claims share a leading subject phrase (≥ 3 tokens) but end in different trailing values | "PR base branch is **dev**" vs "PR base branch is **main**" |

On a fire: mark the **older** atom `contested`, set `contested_by`, and — per
§4.1 — it is **no longer promotable** until a human resolves it at `adopt`. The
newer atom is not auto-blessed; both sit at L1.

**Only the older atom carries a flag, so state how the gate finds the newer
one.** The schema marks the incumbent (`contested`, `contested_by`) and gives
the newer atom nothing — which means §4.1's *"no contradiction open"* check
cannot be a field read for both sides. It is a **reverse join**: an atom is
blocked if its own `contested` is set **or** its id appears in any other atom's
`contested_by`. Deliberately not a mirrored `contests` field — that would be the
same fact in two places, needing to stay in sync, with nothing able to say which
copy was right. The scan is cheap by construction: §5.2 caps the store at 500
atoms and measured a full pass at 2–3 ms.

**Stated limits, because a narrow detector that claims completeness is worse
than one that doesn't.** These two rules catch direct reversals and value swaps.
They will **not** catch semantic contradiction ("always squash-merge" vs "keep
merge commits"), which needs meaning, not string shape. The consequence is
bounded and acceptable: an undetected contradiction means both claims promote,
and §4.2's L2/L3 handling — surface, tag, human resolves — catches it one tier
later. **Detection is a filter, never a guarantee**; the human gate at `adopt`
is what actually holds.

### 4.3 Demotion and expiry

- L1 atom not re-observed in 90 days → dropped. No ceremony.
- L2 claim whose supporting atoms have all expired → demoted to L1, one grace
  cycle, then dropped.
- L3 is **never auto-demoted**. It is capped instead and reviewed by a human on
  overflow. Auto-removing a persona-level fact is more damaging than carrying a
  stale one.

**"Overflow" needs a number, not a word.** §5.1's 2 KB / 4 KB are *injection*
budgets — they bound what enters context, not what accumulates on disk, so a
marker block could grow indefinitely while every session silently sees a
truncated view. That is the §1 failure this design exists to prevent, reproduced
one layer down. L1 got a real cap (500 atoms, evict by `last_seen`); L2 and L3
get the same treatment:

| Tier | Stored cap | On exceeding |
|---|---|---|
| **L2** | **60 atoms** per project — ~4 KB at the ~65-byte median claim, so the store and the injection budget bind at roughly the same point | Oldest-`last_seen` atoms beyond the cap are **demoted to L1**, not dropped: they re-enter the normal 90-day expiry path and can re-promote if still live. |
| **L3** | **30 atoms** global — ~2 KB, matching its injection budget | **No automatic action.** Refuse further L2 → L3 promotions and surface the overflow at `adopt` for a human to prune. Consistent with "never auto-demoted": the cap stops growth, it does not choose what to lose. |

The asymmetry is deliberate. L2 is project-local and recoverable — a wrong
demotion costs one re-promotion cycle. L3 is the always-injected persona tier
where a wrong deletion is invisible and permanent, so the cap blocks the
*inflow* rather than deciding the outflow.

---

## 5. Hook contracts

Three hooks. Each must be independently disableable by env var, following
`productivity/handoff`'s precedent.

### 5.1 `SessionStart` — read

- Load L3 (global) + L2 (current project, matched by cwd).
- Emit as `<agent_memory>` context.
- **Budget: 2 KB L3 + 4 KB L2.** Over budget → truncate by `last_seen` desc and
  say so in the block. A memory system that silently drops is worse than none.
- Disable: `AGENT_MEMORY_SESSIONSTART=0`
- **Never blocks.** Failure = no memory that session, exit 0.
- **No internal self-budget, unlike §5.2 — and the asymmetry is the point.**
  The `timeout: 5` in `hooks.json` is the whole latency contract here. Two
  reasons it can be, where `UserPromptSubmit` needed a tighter internal one:
  this hook runs **once per session**, not once per prompt, so a slow run costs
  a single startup rather than compounding across a conversation; and its work
  is **bounded by the byte caps above** (2 KB L3 + 4 KB L2) rather than by a
  scan whose cost grows with history — it reads two marker blocks and truncates,
  where recall scores up to 500 atoms. If §9.5's measurement shows interpreter
  cold-start alone approaching 5 s, that finding lands here too, and the honest
  response is the same: raise the number to the measured one rather than keep
  an unmet claim.
- **Never emit two contradictory lines unmarked.** L2 and L3 are injected
  together here, and §4.2.1's detector cannot reach L3 (§9.6), so nothing
  upstream guarantees they agree. Whatever this hook emits, an L2 claim and an
  L3 claim that collide for the current project must not both appear as plain
  assertions — the agent would receive two contradictory instructions with no
  signal which governs. **This is a constraint on the hook, not a resolution of
  §9.6:** that open decision picks *how* (specificity-wins shadowing, contest,
  or defer), and all three satisfy this line. It is stated here because the
  consequence lands at injection time, and retrofitting conflict-marking after
  `session_start.py` ships is more disruptive than honouring it from the first
  version.

### 5.2 `UserPromptSubmit` — recall

- Score L1 atoms against prompt text. Deterministic lexical scoring (token
  overlap + `kind` weight + recency). No embeddings, no API call.
- Inject **top 5 max, 1 KB max**.
- **A recalled atom carrying `contested` must render with the §4.2 tag**, not as
  a bare claim. §4.2 states that rule tier-agnostically, but this section is the
  contract `user_prompt_submit.py` gets built from — an implementer working
  strictly from here would ship a recall path that surfaces a contested claim as
  plain fact, which is the exact failure §4.2 forbids. Stated in both places on
  purpose: cross-references are not a contract.
- Disable: `AGENT_MEMORY_USERPROMPTSUBMIT=0`. All three disable vars mirror
  their hook name exactly, so a user who knows Claude Code's hook names can
  derive all three without reading this doc. An earlier `AGENT_MEMORY_RECALL`
  traded that property for a shorter name — a bad trade for a variable typed
  once into a shell profile, and one that leaves three vars following two
  conventions.

**Latency — two distinct limits, do not conflate them:**

| Limit | Value | Enforced by |
|---|---|---|
| Internal self-budget | **100 ms** | `user_prompt_submit.py` itself, against a monotonic clock: past budget it stops scoring and returns whatever it has (possibly nothing) |
| Hook timeout backstop | **1 second** | Claude Code, via `"timeout": 1` in `hooks.json` — **the hook `timeout` field is in SECONDS**, and 1 is the floor |

The backstop exists only to kill a wedged process. It is **not** the budget, and
an implementation that merely finishes under 1 s has missed the requirement.
This hook is on the critical path of every prompt; it is the one place where
being slow is worse than being absent.

**Bounding the work so 100 ms is reachable** (see open decision §9.5 — this is
asserted, not yet measured):

- `.memory/atoms.jsonl` is **capped at 500 atoms**. On overflow, evict by
  `last_seen` ascending. Scoring cost is then bounded regardless of history
  length.
- Scoring is a single linear pass, no index build, no sort of the full set —
  a bounded top-5 heap.
- Interpreter start-up is the dominant fixed cost and is **not** controllable
  from inside the script. If measurement shows cold start alone consumes most
  of the budget, the honest responses are to raise the budget to a measured
  number or drop this hook entirely — **not** to keep an unmet 100 ms claim in
  the spec.

### 5.3 `SessionEnd` — capture

- Async (`"async": true`, per `skillopt-sleep`'s precedent) — must never delay
  session teardown.
- Read the just-closed transcript → extract candidate atoms → **redact** →
  merge into `.memory/atoms.jsonl` (increment `observations`, extend `sessions`,
  **raise `confidence` to the max of old and new** per §4.1.3 — never lower it).
- Run the promotion pass. Promotions to L2/L3 are written to
  `.memory/staged/` — **never directly into `CLAUDE.md`**.
- **First run, before `.memory/atoms.jsonl` exists** (fresh clone, or a project
  that has never had a session end): **treat a missing file as an empty store
  and create it on first write.** A missing file is the normal initial state,
  not an error — every hook must read it that way, and §5.2's recall must return
  nothing rather than fail. §5.4 specifies what concurrent writers do to a file
  that exists; this is the case before that.
- Disable: `AGENT_MEMORY_SESSIONEND=0`

Adoption is a separate, explicit, human-invoked step:
`/cs:memory adopt` — backs up both `CLAUDE.md` files first.

### 5.4 Concurrency — two sessions, one `atoms.jsonl`

Multiple sessions on one repo (several terminals, or git worktrees) is ordinary,
not an edge case, and §5.3 is a **read-modify-write**: merge on `id`, increment
`observations`, extend `sessions`, evict over the 500-atom cap. Two `SessionEnd`
hooks finishing together will interleave and lose one session's writes. The
recall read in §5.2 has the matching hazard: reading a file mid-rewrite yields a
truncated JSONL tail.

Reuse the pattern this repo already has rather than inventing one —
`engineering/agent-harness/.../loop_controller.py:54-62` and
`engineering/skillopt-sleep/skillopt_sleep/state.py:77` both write via temp file
+ `os.replace`:

- **Writers** serialize on an exclusive lock (`.memory/atoms.lock`, `O_CREAT |
  O_EXCL`, stale-lock breaking at **60 s** by mtime), then write to a temp file in the same
  directory and `os.replace()` onto the target. `os.replace` is atomic within a
  filesystem, so a reader sees either the whole old file or the whole new one —
  never a partial one.
- **Readers take no lock at all.** `UserPromptSubmit` has a 100 ms budget
  (§5.2); blocking it on a lock held by an async `SessionEnd` would blow that
  budget for a hook whose failure mode is supposed to be "return nothing."
  Atomic replacement is what makes lock-free reading safe.
- A writer that cannot acquire the lock within **5 seconds gives up and drops
  its atoms**, logging the loss. Losing one session's L1 candidates is
  recoverable — they re-observe. A wedged `SessionEnd` blocking teardown is not.

  **Where the loss is logged, since this is the one place data disappears
  silently:** one line appended to **`.memory/errors.log`** (gitignored, `0600`,
  same discipline as `atoms.jsonl`) — ISO timestamp, session id, atom count
  dropped, reason. **Not stderr**: `SessionEnd` is `async`, so its stderr goes
  nowhere a human reads, which would make "logging the loss" a fiction. The log
  is capped at 200 lines (oldest dropped) so it cannot grow unbounded, and
  `/cs:memory status` surfaces any entry from the last 7 days — a log nobody is
  pointed at is the same as no log.

**The two timeouts are not on the same axis** — `5 s < 60 s` looks contradictory
until you see they answer different questions:

| Value | Question | Behaviour |
|---|---|---|
| **60 s** (mtime age) | "Is this lock *abandoned*?" | Older than 60 s → break it **immediately**, no waiting |
| **5 s** (wall clock) | "How long do I wait for a *live* lock?" | Still held and younger than 60 s → retry up to 5 s, then give up |

So a writer meeting a 61-second-old lock proceeds at once; one meeting a
3-second-old lock waits up to 5 s and drops its atoms if the holder is slower
than that. The stale-break path is not gated behind the 5 s wait — it is checked
first.

**Accepted race — record it as a choice, not an oversight.** Stale-lock breaking
by mtime is a TOCTOU: two writers could both judge a lock stale and both proceed.
Accepted deliberately, because the consequence is bounded by the design above —
each writer still commits via `os.replace`, so the loser's atoms are *lost*, not
*corrupted*, and lost L1 candidates re-observe on the next session. Paying for a
true mutex (a lock daemon, or `fcntl` semantics that vary across NFS and
Windows) would buy durability this tier does not need. **Do not "fix" this
without first showing the loss is actually observable** — L1 is the recoverable
tier by construction.

**This is a design constraint, not an implementation detail:** it is why the L1
store is one append-oriented JSONL file per project rather than per-session
files, and it must be settled before `session_end.py` is written.

Contract file: [`hooks/hooks.json`](hooks/hooks.json).

---

## 6. Layout and admission policy

```
<project>/
  CLAUDE.md                  # committed — L2 lives in a marker block
  .memory/
    atoms.jsonl              # GITIGNORED — L1
    atoms.lock               # GITIGNORED — writer lock (§5.4)
    errors.log               # GITIGNORED — dropped-atom losses (§5.4), capped 200 lines
    staged/                  # GITIGNORED — pending promotions
    adopted.log              # COMMITTED — audit trail of what was adopted, when
~/.claude/
  CLAUDE.md                  # L3, marker block
  projects/*/*.jsonl         # L0 — read-only, never copied
```

**Admission policy (HARD)** — the same split `engineering/llm-wiki/` already
draws in this repo between an ungoverned capture area and a committed, governed
knowledge area: raw capture stays local and disposable, and only *interpreted*
content is ever committed. Stated self-containedly here so it needs no
cross-repo context to check:

| Tier | Committed? | Rule |
|---|---|---|
| L0 | No | Never copied out of `~/.claude/`. Read in place. |
| L1 | **No** — gitignored | Raw observations. May contain incidental specifics. |
| L2/L3 | **Yes** | **Interpreted, de-identified, non-confidential only.** |

`.memory/` is ignored wholesale with a single negation for the audit log — it is
**not** a contradiction that the directory is gitignored while one file inside it
is committed, but it does need stating, since ignoring a directory outright makes
git skip its contents and a bare `!` on the file would not resurface it:

```gitignore
.memory/*                 # not `.memory/` — a directory-level ignore is never
!.memory/adopted.log      # descended into, so this negation could not re-include
```

`adopted.log` is committed on purpose: it records **what was promoted into
`CLAUDE.md` and when**, which is the audit trail for content that *is* already
committed. It therefore holds only claims that already cleared the L2/L3 bar
above. `atoms.jsonl` and `staged/` stay ignored because they hold pre-admission
material.

Non-negotiables, inherited from this repo's existing discipline:

1. **Redaction runs before any write**, using `productivity/handoff`'s
   17-pattern linter as the floor. Applies to L1 too, not just committed tiers —
   `skillopt-sleep`'s hardest-won lesson was that file-level redaction misses
   in-memory paths (root `CLAUDE.md`, deviation list).
2. **No secrets, no confidential figures, no PHI/PII** reaches L2/L3. A claim
   referencing sensitive data is stored as a *reference*, never a transcription.
3. **Runtime-created** files are locked down at creation: `.memory/` `chmod
   0700`, the files the hooks write `0600`. Scoped deliberately to
   hook-created files — git tracks no POSIX mode beyond the executable bit, so
   a fresh checkout materializes `adopted.log` at the cloner's umask and no
   in-repo declaration can change that. Anything whose confidentiality depends
   on mode bits must therefore be gitignored, which is why `atoms.jsonl` and
   `staged/` are and `adopted.log` (deliberately public, de-identified) is not.
4. Every promoted claim carries its L0 back-pointer. **Cite, don't invent.**
5. **This policy binds the spec's own examples, not just runtime data.** Every
   illustrative atom in `DESIGN.md` and `memory_schema.json` must be as
   de-identified as an atom the tool would be allowed to commit: generic project
   slugs, no private or unpublished repo names, no machine-specific paths beyond
   the `~/.claude/projects/<slug>/` shape the format itself requires. The
   failure this prevents: an example naming a repo that exists nowhere in the
   public tree is unverifiable to any reader *and* publishes a project name that
   was not ours to publish. **Fixture data is committed data.**

---

## 7. CodeGraph via MCP — separate and reversible

The one component of the Tencent project worth adopting **as code** is its MCP
server (`MemoryKnowledge/src/mcp/`), exposing 12 tools:

`code_search` · `code_explore` · `code_callers` · `code_callees` · `code_impact`
· `code_node` · `code_status` · `code_files` · `wiki_search` · `wiki_read` ·
`wiki_list` · `wiki_graph`

Standard MCP over stdio. No traffic interception, no billing change, no
reverse-engineered internals. Storage defaults to local SQLite + sqlite-vec +
FTS5 (`MemoryCore/src/core/store/factory.ts:6`); Tencent Cloud VectorDB is
opt-in, so there is no cloud dependency.

**Kept deliberately out of scope of this plugin.** It ships as an independent
`.mcp.json` entry so it can be adopted, evaluated, or removed without touching
the memory tiers. Bundling them would couple a local file format to a
third-party service's lifecycle. `code_impact` before edits is the genuinely
useful capability here and this repo has no equivalent.

---

## 8. Rejected: MemoryProxy

The Tencent project's actual Claude Code integration sets
`ANTHROPIC_BASE_URL=http://127.0.0.1:8096/claude-code/default` and terminates all
traffic in a Node proxy that mutates `body.system`
(`MemoryProxy/src/anthropicHandler.ts:848`) before forwarding upstream.

Rejected on four independent grounds, any one of which is sufficient:

**How the §8 citations were obtained** (so a reader can re-check rather than
trust): the upstream repo was cloned and read at commit
**`b44c6db5f5b1a011eed645efb1949840f99f961a`** (2026-08-05), the tip of `main`
at inspection time. Line references below are against that commit; upstream may
have moved since. The Chinese source comment quoted in point 1 is verbatim from
`MemoryProxy/src/agent-adapters/claude-code.ts`, lines 2–6.

1. **Reverse-engineered from Claude Code internals.**
   `MemoryProxy/src/agent-adapters/claude-code.ts:5` states its source as
   *"逆向 CC 源码 forkedAgent.ts / sideQuery.ts + 抓包实证"* — reverse-engineered CC
   source plus packet capture. It classifies requests by `cache_control` marker
   position (n-2 vs n-1). That is an unstable private detail; when it changes the
   failure is **silent**, not loud.
2. **Billing.** Overriding `ANTHROPIC_BASE_URL` with a proxy-issued token routes
   off Anthropic OAuth onto metered API billing, plus a second billed model
   (`MEMORY_LLM_API_KEY`) that runs extraction over every conversation.
3. **Data exposure.** Full prompts, file contents, and tool results are persisted
   as L0 by a third-party service and shipped to a second LLM. Incompatible with
   the compliance posture this repo maintains (`ra-qm-team/`, ISO 27001, MDR,
   GDPR) — that is a data-processing arrangement, not a config change.
4. **Maturity.** Zero test files repo-wide; CI runs install + pack with no test
   step; single squashed commit; v2.0.0 dated three days before inspection.

Everything of value the proxy provides is reachable through hooks, which are a
**supported** extension point. Nothing here requires interception.

---

## 9. Open decisions

Needed before implementation starts. **They are not equals, and listing them as
a flat numbered set understated that.** Two of the six decide whether there is a
system at all; the other four decide how a system that exists should behave:

| | Decision | Kind |
|---|---|---|
| **(2)** | Can L0 → L1 extraction work without an LLM? | **Load-bearing.** Everything downstream — the 3-session gate, the tier caps, the contradiction detector, the whole promotion machine — is only as good as what the extractor produces. A rule-based extractor with too little recall makes the rest correct and useless. |
| **(3)** | Plugin, or extend the nightly cycle? | **Load-bearing**, and answered by (2): §9.3's 2-week trial *is* the test of (2), and a "no" deletes this folder. |
| (1), (4), (5), (6) | write target · multi-repo L3 · recall budget · L3 contradiction | Local. Each changes one mechanism and leaves the rest standing. Even (5)'s worst case only deletes one hook (§9.5 option (c)); the tiering survives on `SessionStart` alone. |

Read that ordering as the honest one: §3–§5 are ~700 lines of settled contract
sitting downstream of a question nobody has measured yet. That is a real cost of
sequencing the spec before the spike, and it is recorded rather than smoothed
over — see §9.2's own framing.

**But be precise about which cost it is, because it decides whether trimming
§4–§5 now would help.** A "no" on (2) does not make the promotion machinery
*wrong* — recurrence counting, the tier caps and the contradiction detector all
operate on atoms **however those atoms were produced**, and none of them
reference the extraction method. It makes them **unused**. Those are different
risks with different remedies: content that would need rework is worth deferring,
content that would simply go unread is not — deleting reviewed text to re-derive
it later costs more than leaving it. So the imbalance is recorded here as a
sequencing lesson for the next spec of this size, not as a call to cut §4–§5.

1. **L2 write target.** Root `CLAUDE.md` here is already **88 KB**. Append a marker
   block, or a sibling `CLAUDE.memory.md` that `CLAUDE.md` references? *Leaning
   sibling file* — keeps generated content out of a hand-maintained doc and makes
   the diff reviewable.
2. **Extraction without an LLM.** §4 promotion is deterministic, but L0 → L1
   extraction — turning transcript prose into atomic claims — is not obviously
   rule-based. Options: (a) rule-based on explicit markers only (imperatives,
   corrections, `## Lessons` entries) — high precision, low recall, stdlib-only;
   (b) reuse `skillopt-sleep`'s documented opt-in LLM exception. *Leaning (a)*,
   since the repo's rule is strict and low recall is survivable when the
   promotion gate needs 3 observations anyway.

   **If (b) wins, it costs more than an import.** Root `CLAUDE.md`'s
   anti-patterns list currently reads *"**one** documented, opt-in exception"* and
   names `skillopt-sleep/backend.py` specifically. A second LLM-calling script
   makes that sentence false. The implementation PR would therefore have to
   **amend that bullet in root `CLAUDE.md`** — naming this exception, its
   justification, and its default-off switch — rather than quietly becoming an
   undocumented second carve-out. Treat that edit as part of the cost of (b),
   not as follow-up paperwork; it is a repo-wide rule change, and it is a real
   argument for (a) beyond recall.

   **`confidence: "verified"` is the sharpest version of this risk and needs
   deciding separately.** It is simultaneously the hardest level for a lexical
   extractor to assign — it requires recognising that *a check actually
   confirmed* the claim, not merely that someone asserted it — and the one with
   the lowest promotion bar (1 observation, and per §4.1 the only path exempt
   from the distinct-days clause). A single misclassification there is the
   cheapest possible route for a wrong claim to reach L2. Leaning: a rule-based
   extractor must **never** assign `verified` — reserve it for atoms minted by a
   tool that ran the check itself and can name it, and let prose-derived atoms
   top out at `stated`.
3. **Does this earn a plugin, or a `skillopt-sleep` sibling doc?** If (a) above
   proves too low-recall in a trial, the honest answer may be "extend the
   existing nightly cycle" and this folder is deleted. Decide after a 2-week
   trial of the extractor against real transcripts.
4. **Multi-repo L3.** L2→L3 requires observation in ≥ 2 projects. A user working
   in only one or two repos gives that gate a very thin sample, so L3 may need
   to stay manually curated until enough projects are in play. Decide whether a
   single-project user gets a documented "L3 is hand-authored only" mode rather
   than a promotion path that will essentially never fire.
5. **Is the 100 ms recall budget achievable at all?** §5.2 asserts it and bounds
   the work (500-atom cap, single linear pass), but a spawned `python3` pays
   interpreter cold-start before executing a line, and that cost is unbounded
   from inside the script — on a loaded machine it can consume most of the
   budget by itself. **Measure before implementing:** time a no-op
   `python3 -c pass` plus a 500-atom scoring pass at p50/p95 on a busy machine.

   **First measurement taken** (n=40, Linux container, otherwise idle — *not*
   the busy machine this calls for, so read it as a floor, not the answer):

   | | p50 | p95 | max |
   |---|---|---|---|
   | `python3 -c pass` | 12.4 ms | 30.8 ms | 36.0 ms |
   | Spawn + read 500 atoms + score + top-5 | 23.2 ms | 30.1 ms | 50.6 ms |
   | …of which in-script work | 2.1 ms | 3.0 ms | — |

   **This reframes the risk rather than settling it.** The scoring pass is
   ~2–3 ms, so the 500-atom cap is not the binding constraint and never was —
   **cold start is essentially the whole cost.** The budget question is a
   process-spawn question, and the levers that matter sit outside the script,
   where §5.2 already said they were unbounded. On this machine 100 ms holds
   with ~3× headroom; the 50.6 ms max shows the tail is real and would widen
   under load. Still needed to choose between the outcomes below: the same
   numbers on a machine doing real work.

   Outcomes: (a) it fits → build as specced; (b) it fits only sometimes → raise
   the budget to the measured p95 and state that number instead; (c) it does not
   fit → **drop `UserPromptSubmit` entirely** and let L2/L3 at `SessionStart`
   carry the system. Option (c) is a real, acceptable outcome — a recall hook
   that misses its budget on every prompt is worse than no recall hook.

   **(d) Attack the measured cost instead of budgeting around it — a warm
   resident process.** (a)–(c) all treat spawn cost as a constant to tolerate,
   which the measurement above says is the *only* cost that matters: the scan is
   2–3 ms, the interpreter is the other ~20 ms, and it is paid again on **every
   prompt for the life of every session** — a fixed tax, not a one-off. A small
   daemon holding the atom store in memory, with `user_prompt_submit.py` reduced
   to a socket write and a read, removes the dominant term rather than fitting
   inside it.

   Named as a real option because it is the only one that does, **not** as the
   recommendation — it is the most expensive by a wide margin, and its costs
   land squarely on this design's stated properties:

   - A hook that "never blocks, exit 0 on failure" (§5.2) becomes a hook with a
     liveness dependency. It must still fail open when the socket is missing,
     stale, or wedged — which means keeping the cold path anyway, so the
     complexity is *added to*, not swapped for, what (a)–(c) need.
   - Lifecycle: who starts it, what restarts it after a crash or reboot, how a
     stale socket is distinguished from a live one, and how it terminates when
     no session is using it. §5.4 already carries a stale-lock heuristic; this
     would need a second one for a different resource.
   - It is a long-lived local process holding memory contents in RAM, which is a
     different security surface from a script that reads a file and exits.
   - This repo's convention is stdlib-only scripts that run and exit; a resident
     service is a genuinely new shape here, not a variation on an existing one.

   **Sequencing:** (d) is only worth its cost if the busy-machine measurement
   turns (a) into (b) or (c). Measure first — the same instruction this decision
   opened with. If 100 ms holds under load, a daemon buys latency nobody needed.

   **If (c) wins, `hooks/hooks.json` must shrink too** — the `UserPromptSubmit`
   entry is already written there as a contract, so deleting the hook from this
   doc alone would leave the contract file asserting a hook the design no longer
   wants. A contract file must not outlive the decision that justified it.

6. **Contradiction against L3 — underdetermined, not merely unbuilt.** §4.2.1's
   detector groups by `project`; L3 atoms have none, so no automatic detection
   ever fires against the tier that is always in context and never
   auto-demoted (§4.3). That framing makes it sound like a missing loop. It is
   not. **The signal is genuinely ambiguous:** suppose L3 holds *"PR base branch
   is dev"* — earned across ≥ 2 projects — and a new project yields *"PR base
   branch is main"*. Two readings, opposite handling:

   - **Correction.** The global claim was over-generalised from too few
     projects. The L3 atom should be contested.
   - **Local exception.** The global claim is still right for most projects;
     this one legitimately differs. The L3 atom should be left alone, and the
     project-scoped claim should simply win *here*.

   Nothing in the string shape distinguishes them, and the rules of §4.2.1 fire
   identically on both. Guessing wrong is expensive in one direction: auto-
   contesting on every local exception would tag the persona tier as unreliable
   the first time any project deviates, which is exactly the "false permanence"
   failure §1 exists to avoid — inverted into false impermanence.

   **There is a live consequence to leave undecided carefully.** §5.1 injects L2
   and L3 together, so today two textually contradictory lines can enter the
   same context block with nothing marking the conflict. Whatever resolves this
   must fix that, not only the bookkeeping.

   Candidates, in rising cost: (a) **specificity wins** — when an L2 claim
   collides with an L3 claim for the current project, inject only the L2 and
   note the shadowing in the block; the L3 is never contested, because a local
   override is not evidence of error. Cheap, needs no new detector state, and
   matches how every config system already resolves this. (b) **Shadow-count
   promotion** — track how many distinct projects shadow an L3 atom, and contest
   it once that crosses a threshold; recurrence decides, consistent with §4.1's
   whole premise. (c) Out of v1 entirely; document that L3 is human-maintained
   after promotion. *Leaning (a) for v1 with (b) as the natural follow-on*, but
   this is not settled, and §4.2 is written to promise only what §4.2.1 can
   currently deliver until it is.

---

## 10. Planned file tree (not yet created)

Layout follows the shape every comparable agents+commands plugin in this repo
uses: the skill body nests under `skills/<plugin-name>/`, while `agents/`,
`commands/`, `hooks/` and `.claude-plugin/` sit at the plugin root. **4 of 5
comparable plugins point their manifest at that nested path** —
`skillopt-sleep`, `write-a-skill`, `agent-harness` and `handoff` all declare
`["./skills/<plugin-name>"]`. `engineering/llm-wiki/` is the exception worth
knowing about: it uses the *same* on-disk nesting (`skills/llm-wiki/`) but
declares the bare `["./skills"]`, which **is** one of root `CLAUDE.md`'s three
documented canonical forms ("plugin with `skills/` subdir"). Both load; the
difference is whether the manifest names the skill or the directory above it.

```
engineering/agent-memory/
  DESIGN.md                          ← this file (stays at root)
  .claude-plugin/plugin.json         ← "skills": ["./skills/agent-memory"]
  hooks/
    hooks.json                       ← contract, written
    session_start.py                 ← L2+L3 read
    user_prompt_submit.py            ← L1 recall, 100 ms budget
    session_end.py                   ← L0 capture + promotion, async
  agents/cs-memory-curator.md
  commands/cs-memory.md              ← status | adopt | why | forget
  skills/agent-memory/
    SKILL.md                         ← not written until §9 is resolved
    scripts/
      validate_examples.py           ← FIRST file to land (see below)
      memory_extract.py              ← L0 → L1
      memory_promote.py              ← L1 → L2 → L3, deterministic
      memory_inspect.py              ← --tier, --contested, --why <claim>
    references/
      memory_tiering_canon.md
      promotion_gate_design.md
      redaction_and_admission.md
    assets/
      memory_schema.json             ← written (moves here on implementation)
```

### 10.1 `validate_examples.py` — write it first, and it already exists

Across the review of this spec, **drift between `DESIGN.md`, the schema, and the
fixtures was the dominant defect class** — required-field drift, a tier the
examples never exercised, ids that stopped reproducing, headings inserted out of
order, a `confidence` value that contradicted its own lifecycle narrative. Every
one was caught by a check, and hand-checking does not scale as the schema moves
toward implementation.

The validator is written and tested: **[`assets/validate_examples.py.txt`](skills/agent-memory/scripts/validate_examples.py)**
— stdlib-only, **69 checks in seven families** (schema conformance · the
tier-dependent back-pointer · id reproduction from the doc's own published
`normalize()` · confidence monotonicity · document structure and links · prose
claims that must match measured reality · lifecycle coherence across a
multi-tier id group).

That count is **itself checked** — family 6's last assertion compares it against
the number of checks the run actually executed. A number in prose describing a
program's behaviour is drift waiting to happen unless the program owns it.

**To run it** (it is `.txt`, so it cannot be executed in place, and it resolves
its own paths by walking up from `__file__` — a `python3 <(cat …)` or `-c
"$(cat …)"` invocation gives it no real location and it will refuse to start):

```sh
python3 skills/agent-memory/scripts/validate_examples.py
```

**Run it before any further edit to this folder lands.** Nothing in CI gates the
drift class this section exists to prevent — the checker is only as good as the
habit of running it, and "a future editor tweaks a fixture in `DESIGN.md`
without knowing this file exists" is the failure that leaves. **It is now a real
`scripts/validate_examples.py`**; the `.py.txt` parking described below was
undone when the plugin shipped, and §11's placement question no longer gates it.

**The `.txt` parking is not what blocks CI**: a workflow step can `cp` it to a
temp `.py` and run it exactly as above, and `derive_counters.py` never sees the
temp file. The whole step, for whoever wires it:

```yaml
- name: agent-memory spec drift check
  run: |
    python3 engineering/agent-memory/skills/agent-memory/scripts/validate_examples.py
```

Not added to `ci-quality-gate.yml` here: that workflow runs on every PR in the
repo, and this one is spec-only for a folder §9.3 explicitly permits deleting
after a two-week trial. Adding a repo-wide job on that basis is the maintainer's
call, not a spec PR's — the snippet is here so saying yes costs one paste.
Wiring that step is a live option today, independent of the `audit/`-vs-here
placement decision.

What did block it was the checker's own design — see property 1.

Two properties make it worth more than a linter:

1. **It holds the algorithm `DESIGN.md` publishes and asserts the two match**,
   so doc and fixtures cannot silently disagree. **It must not get that property
   by `exec`-ing the doc's fenced block** — the obvious implementation, and the
   one this file used until it was caught. Executing the fence makes *"whoever
   can edit a markdown code block"* equal to *"whoever can run arbitrary code in
   this process."* Harmless while a maintainer runs it by hand
   on a branch they already trust — and **not** harmless under the CI step the
   paragraph above recommends, since `ci-quality-gate.yml` triggers on
   `pull_request`, which would have handed code execution to any PR author,
   fork included, through a prose file nobody reads as executable. The safety of
   the `exec` rested on a fact outside the file, and the obvious improvement
   (gate it in CI) silently falsified that fact. Source-text comparison keeps the
   anti-divergence property with no execution: change the doc's block and the
   checker fails until its own copy is updated to match.
2. **It is tested against injected regressions, not just the happy path** — four
   deliberate defects (an unstripped back-pointer, a broken tier→scope pair, a
   wrong id, a confidence downgrade) each make it exit 1. A checker that only
   ever passes proves nothing.

**Why it is parked as `.txt` and not shipped here:** this PR is spec-only, and a
`.py` in this folder is counted by `derive_counters.py` (measured: 663 → 664) —
a counted "tool" belonging to no plugin, in a folder deliberately without a
`SKILL.md`. Renaming it and counting it is a one-line change the moment the
maintainer rules that a spec-stage folder may carry tooling.

**On the precedent, since "rename it so the counter misses it" generalises
badly.** What makes this instance legitimate is not the intent, which is
unfalsifiable — it is that the file **is not a tool**. It ships in no plugin,
belongs to no `SKILL.md`, is not invoked by any workflow, and does nothing for a
user who installs something. Counting it would make `python_tools` *less*
accurate, not more. The abuse this could be mistaken for is the opposite case: a
real tool a real skill really uses, renamed to keep a headline number down. That
one is detectable by a single question a reviewer can ask — **is anything
supposed to run this?** Here the answer is no, and stays no until §10.1's
reversal condition fires, at which point it becomes a counted `.py` in the same
commit. If the maintainer would rather not have the pattern in the tree at all,
the fix is the `audit/` option in §11, where the question does not arise.

**The parking hack is a consequence of the location, not a fact about the
file.** Under `audit/` (the third option in the status header) it would be
unnecessary — that directory is pruned from `canonical_walk` entirely, so a
`.py` inside it moves no counter at all, verified. Anyone weighing where this
spec belongs should count that as a point against staying here: the same
validator would be a plain executable script, and "nothing in CI gates the drift
class this section is about" would be a straightforwardly fixable problem rather
than one blocked by a naming workaround.

**Two references break when that move happens — update both in the same commit:**

| Reference | Now | After the move |
|---|---|---|
| `DESIGN.md`'s link (§3.1) | `[…](skills/agent-memory/assets/memory_schema.json)` | `[…](skills/agent-memory/assets/memory_schema.json)` |
| The schema's own `$id` | `…/engineering/agent-memory/assets/…` | `…/engineering/agent-memory/skills/agent-memory/assets/…` |

`DESIGN.md` stays at the plugin root (it documents the plugin, not the skill), so
the relative link lengthens rather than staying put. Called out because every
other forward-looking wrinkle in this doc — the counter delta, the manifest-form
follow-up — already is, and a silently-dead link in the file that *is* the
contract would be the wrong thing to discover later.

**Counters on ship: skills +1, tools +8, refs +3, commands +1, agents +1,
plugins +1.** Tools is **not +3** — `derive_counters.py` counts *every*
`.py` outside repo-root `scripts/`, so the three `hooks/*.py` count alongside
the `scripts/*.py`. Verified empirically against this tree: adding one
file under `hooks/` moves `python_tools` 663 → 664. `productivity/handoff` is
the confirming precedent — its 7 `scripts/*.py` + 2 `hooks/*.py` are 9 counted
tools, i.e. the `hooks/` files are counted alongside the `scripts/` ones.

> **Corrected at implementation time.** This paragraph originally said **+6**,
> derived from §10's four-script tree (3 scripts + 3 hooks, with
> `validate_examples.py` already counted). The delivered surface is **5 scripts
> + 3 hooks = +8**: the fifth script is `memory_core.py`, a shared module with
> no CLI, added because duplicating the redaction patterns, id algorithm and
> lock protocol across seven files is the drift class this document exists to
> prevent. Measured on merge: `python_tools` 695 → 703. `README.md`'s
> "Deviations from `DESIGN.md`" list is authoritative for this and every other
> divergence. Verify with `scripts/derive_counters.py --check` before opening
> the implementation PR.

**Follow-up for the maintainer (not this PR):** the identical on-disk layout is
declared two different ways across the repo, and only one of them is documented.
Root `CLAUDE.md` lists three canonical `skills` forms; `["./skills"]` (what
`llm-wiki` uses) is among them, while `["./skills/<plugin-name>"]` (what the
other four use, and what this tree adopts to follow the majority) is not quite
any of them — it survives `check_plugin_json.py` only as a well-formed
`./`-prefixed array entry. **The question is which of the two the repo wants,
not whether to bless a fourth form**, since a documented form already covers
this layout. Either document the nested form, or migrate the four manifests to
the already-documented `["./skills"]`; both beat the shape being tribal
knowledge spread across five manifests.

---

## 11. Where this file should live

Deferred to the end deliberately: it is meta-discussion about the file,
not part of the design. It is recorded rather than dropped because a
future reader — or a skill-count auditor — will otherwise reasonably
wonder why a 1000-line non-skill folder sits in a domain directory.

**Why a design doc lives under `engineering/` rather than `documentation/`:**
root `CLAUDE.md` designates `documentation/` for pre-build specs, but that folder
is **gitignored** — invisible on GitHub, so nothing in it can be reviewed in a
PR. A design meant to be argued with *before* code exists cannot live there.
Stated here because a future reader (or a skill-count auditor) will otherwise
reasonably wonder why a 1000-line non-skill folder sits in a domain directory.

**There is a third option this note originally missed.** Top-level **`audit/`**
already solves this exact constraint: root
`CLAUDE.md` describes it as "an intentional, **public** audit record… committed
and visible to cloners," and `derive_counters.py` prunes it from
`canonical_walk` entirely (`EXCLUDED_TOP_LEVEL`, line 48) rather than merely
failing to find a `SKILL.md` in it. Its existing contents are the same shape as
this file — prose deliverables with verification criteria that later PRs use as
acceptance gates, which is precisely what this doc is for the implementation PR.
The choice is three-way, not the two-way one stated above it. **Neither option
is endorsed here** — the costs below are listed, not weighed, and the decision
is the maintainer's.

Costs on each side, so the trade is visible rather than argued:

**What staying under `engineering/` costs:**

- **The `.py.txt` parking hack (§10.1) stays necessary.** Because `audit/`
  is pruned from the walk, a `.py` inside it is not counted at all — verified:
  adding one leaves `python_tools` at 663. The validator could simply be an
  executable `validate_examples.py` rather than a file that must be copied
  before it can run. This is an ergonomic cost, not a blocker for CI gating —
  a workflow step can temp-copy the `.txt` today (§10.1).

**What moving to `audit/` costs:**

- **The two contract files relocate a second time.**
  `hooks/hooks.json` and `assets/memory_schema.json` are not documentation —
  they are intended to *become* live plugin files at paths a `plugin.json` will
  reference. Under `audit/` they would have to move again at implementation
  time, breaking the schema `$id` and the §3.1 link a second time (§10.1 already
  tracks one such move). Splitting spec-into-`audit/` from
  contracts-into-`engineering/` is the other way out, at the cost of separating
  two things written to be read together.

**Three other open items resolve differently depending on this one**, which is
why it is worth answering before the implementation PR rather than after:

| Item | Under `engineering/` | Under `audit/` |
|---|---|---|
| The `.py.txt` parking (§10.1) | required — a `.py` moves `python_tools` | unnecessary; ship a real `.py` |
| Splitting mechanical rationale into `references/` | moves `references` **746 → 747**, verified | free; the subtree is pruned |
| Relocating later | — | §10.1's two hard-coded paths break a **second** time |

The middle row is the one that is easy to miss: the repo's usual
`SKILL.md` → `references/` split — the obvious fix for this file's length — is
**not available** to a spec-only folder under a domain directory without moving
a headline counter. That is a constraint imposed by the location, not a
judgement about the content.

**This remains an open maintainer decision, not something this PR settles** —
see the note at the end of §10.

---

## 12. Attribution

Design ideas (L0→L3 tiering; ownership/visibility model) derived from
[TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory),
MIT, © 2026 Tencent. **No code vendored.** That project in turn credits
Karpathy's LLM Wiki concept, which this repo independently implements as
`engineering/llm-wiki/`.

Hook wiring and redaction patterns follow `productivity/handoff/`. Staging /
propose-never-apply discipline follows `engineering/skillopt-sleep/`.
