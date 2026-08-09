# agent-memory — design spec (NOT YET IMPLEMENTED)

**Status:** design stage. No `SKILL.md`, no `plugin.json`, no Python. This folder
holds a specification and two contract files (`hooks/hooks.json`,
`assets/memory_schema.json`) so the shape can be reviewed before anything is
built. Repo counters are intentionally untouched — `scripts/derive_counters.py`
counts skills by `SKILL.md`, and this folder deliberately has none.

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
three failure modes this repo already sees at 362 skills:

1. **Bloat** — root `CLAUDE.md` in this repo is ~40 KB of release notes, loaded
   into every session regardless of whether the task touches `markdown-html/` or
   `ra-qm-team/`.
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

### 2.5 Conclusion

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

Every field is mandatory. An atom missing provenance is discarded, not stored.

```json
{
  "id": "atm_7f3a9c21",
  "claim": "PR base branch is dev, never main",
  "scope": "project",
  "project": "claude-skills",
  "kind": "constraint",
  "first_seen": "2026-08-09T10:14:22Z",
  "last_seen": "2026-08-09T10:14:22Z",
  "observations": 1,
  "sessions": ["01EM5xmJ7AmTMg31rq68BCym"],
  "source": "~/.claude/projects/-home-user-claude-skills/01EM....jsonl#L412",
  "confidence": "observed",
  "redacted": false
}
```

- `kind` ∈ `constraint` · `preference` · `fact` · `decision` · `failure`
- `sessions` is a **set** — this is what makes the promotion gate countable.
  Re-stating a claim twice in one session does not increment durability.
- `source` is a back-pointer into L0. Any promoted claim must be traceable to a
  transcript line, or it cannot be promoted. This is the anti-fabrication rule.
- `confidence` ∈ `observed` (agent inferred it) · `stated` (user said it
  directly) · `verified` (a check confirmed it). `stated` and `verified` promote
  faster — see §4.

Full JSON Schema: [`assets/memory_schema.json`](assets/memory_schema.json).

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
| L1 → L2 | `observations ≥ 3` across **≥ 3 distinct sessions**, ≥ 2 of them on distinct days, same `project`, no contradiction open |
| L2 → L3 | Held at L2 in **≥ 2 distinct projects**, `age ≥ 30 days`, no contradiction in 30 days |

Fast paths:

- `confidence: "stated"` — an explicit user directive ("always target dev") —
  needs **2** sessions, not 3. The user said it; we are counting whether it
  *sticks*, not whether it is real.
- `confidence: "verified"` — a claim a script confirmed — promotes on **1**
  observation. It is not hearsay.

### 4.2 Contradiction handling

When a new atom contradicts a claim at L2/L3, the incumbent is **never silently
overwritten**:

1. Mark the incumbent `contested`, record the contradicting atom id.
2. A contested L2/L3 claim is **still injected**, tagged
   `[contested — newer evidence YYYY-MM-DD]`. Withholding it silently would be
   worse than surfacing the conflict.
3. Resolution requires a human decision at `adopt` time. Never automatic.

This mirrors `skillopt-sleep`'s staging discipline: **propose, never apply.**

### 4.3 Demotion and expiry

- L1 atom not re-observed in 90 days → dropped. No ceremony.
- L2 claim whose supporting atoms have all expired → demoted to L1, one grace
  cycle, then dropped.
- L3 is **never auto-demoted**. It is capped instead (§5.3) and reviewed by a
  human on overflow. Auto-removing a persona-level fact is more damaging than
  carrying a stale one.

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

### 5.2 `UserPromptSubmit` — recall

- Score L1 atoms against prompt text. Deterministic lexical scoring (token
  overlap + `kind` weight + recency). No embeddings, no API call.
- Inject **top 5 max, 1 KB max**.
- Disable: `AGENT_MEMORY_RECALL=0`
- **Hard latency budget: 100 ms.** Over → return nothing. This hook is on the
  critical path of every single prompt; it is the one place where being slow is
  worse than being absent.

### 5.3 `SessionEnd` — capture

- Async (`"async": true`, per `skillopt-sleep`'s precedent) — must never delay
  session teardown.
- Read the just-closed transcript → extract candidate atoms → **redact** →
  merge into `.memory/atoms.jsonl` (increment `observations`, extend `sessions`).
- Run the promotion pass. Promotions to L2/L3 are written to
  `.memory/staged/` — **never directly into `CLAUDE.md`**.
- Disable: `AGENT_MEMORY_SESSIONEND=0`

Adoption is a separate, explicit, human-invoked step:
`/cs:memory adopt` — backs up both `CLAUDE.md` files first.

Contract file: [`hooks/hooks.json`](hooks/hooks.json).

---

## 6. Layout and admission policy

```
<project>/
  CLAUDE.md                  # committed — L2 lives in a marker block
  .memory/
    atoms.jsonl              # GITIGNORED — L1
    staged/                  # GITIGNORED — pending promotions
    adopted.log              # committed — audit trail of what was adopted, when
~/.claude/
  CLAUDE.md                  # L3, marker block
  projects/*/*.jsonl         # L0 — read-only, never copied
```

**Admission policy (HARD)** — deliberately mirrors gaios's `raw/` vs `wiki/`
split, which is the same problem:

| Tier | Committed? | Rule |
|---|---|---|
| L0 | No | Never copied out of `~/.claude/`. Read in place. |
| L1 | **No** — gitignored | Raw observations. May contain incidental specifics. |
| L2/L3 | **Yes** | **Interpreted, de-identified, non-confidential only.** |

Non-negotiables, inherited from this repo's existing discipline:

1. **Redaction runs before any write**, using `productivity/handoff`'s
   17-pattern linter as the floor. Applies to L1 too, not just committed tiers —
   `skillopt-sleep`'s hardest-won lesson was that file-level redaction misses
   in-memory paths (root `CLAUDE.md`, deviation list).
2. **No secrets, no confidential figures, no PHI/PII** reaches L2/L3. A claim
   referencing sensitive data is stored as a *reference*, never a transcription.
3. `.memory/` is `chmod 0700`, files `0600`.
4. Every promoted claim carries its L0 back-pointer. **Cite, don't invent.**

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

Needed before implementation starts:

1. **L2 write target.** Root `CLAUDE.md` here is already ~40 KB. Append a marker
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
3. **Does this earn a plugin, or a `skillopt-sleep` sibling doc?** If (a) above
   proves too low-recall in a trial, the honest answer may be "extend the
   existing nightly cycle" and this folder is deleted. Decide after a 2-week
   trial of the extractor against real transcripts.
4. **Multi-repo L3.** L2→L3 requires observation in ≥ 2 projects. With two repos
   attached (`claude-skills`, `gaios`) the sample is thin; L3 may need to stay
   manually curated for now.

---

## 10. Planned file tree (not yet created)

```
engineering/agent-memory/
  DESIGN.md                      ← this file
  SKILL.md                       ← not written until §9 is resolved
  .claude-plugin/plugin.json
  hooks/
    hooks.json                   ← contract, written
    session_start.py             ← L2+L3 read
    user_prompt_submit.py        ← L1 recall, 100 ms budget
    session_end.py               ← L0 capture + promotion, async
  scripts/
    memory_extract.py            ← L0 → L1
    memory_promote.py            ← L1 → L2 → L3, deterministic
    memory_inspect.py            ← --tier, --contested, --why <claim>
  references/
    memory_tiering_canon.md
    promotion_gate_design.md
    redaction_and_admission.md
  assets/
    memory_schema.json           ← written
  agents/cs-memory-curator.md
  commands/cs-memory.md          ← status | adopt | why | forget
```

Counters on ship: skills +1, tools +3, refs +3, commands +1, agents +1,
plugins +1. Verify with `scripts/derive_counters.py --check`.

---

## 11. Attribution

Design ideas (L0→L3 tiering; ownership/visibility model) derived from
[TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory),
MIT, © 2026 Tencent. **No code vendored.** That project in turn credits
Karpathy's LLM Wiki concept, which this repo independently implements as
`engineering/llm-wiki/`.

Hook wiring and redaction patterns follow `productivity/handoff/`. Staging /
propose-never-apply discipline follows `engineering/skillopt-sleep/`.
