# agent-memory

A four-tier memory ladder for Claude Code. **Promotion is earned by recurrence,
never asserted by confidence**, and nothing reaches a committed file without a
human adopting it.

Concept derived from [TencentCloud/TencentDB-Agent-Memory][tencent] (MIT). No
upstream code is included — see
[`.claude-plugin/authoring-notes.json`](.claude-plugin/authoring-notes.json) for
what was taken and what was deliberately rejected.

[tencent]: https://github.com/TencentCloud/TencentDB-Agent-Memory

---

## What it does

| Tier | Holds | Injected | Committed |
|---|---|---|---|
| **L0** | raw session transcripts | never | already on disk |
| **L1** | candidate atoms | on relevance, per prompt | no (gitignored) |
| **L2** | this project's context | every session start | yes, after adopt |
| **L3** | stable cross-project persona | always | yes, after adopt |

**L1 → L2** needs ≥ 3 distinct sessions spanning ≥ 2 distinct calendar days. A
claim stated outright needs 2 sessions — the day rule still applies. A
deterministically verified claim promotes on one observation and is the only
day-exempt path. **L2 → L3** needs ≥ 2 distinct projects and ≥ 30 days.

Two gates refuse rather than guess: a **redacted** claim never promotes on
evidence alone, and a claim with an **open contradiction** freezes until a human
resolves it.

## Install and use

The three hooks in [`hooks/hooks.json`](hooks/hooks.json) run the loop
unattended. Each is disabled independently:

```bash
AGENT_MEMORY_SESSIONSTART=0      # stop injecting L2 + L3
AGENT_MEMORY_USERPROMPTSUBMIT=0  # stop L1 recall
AGENT_MEMORY_SESSIONEND=0        # stop capture
```

```bash
cd skills/agent-memory/scripts
python3 memory_inspect.py --tier L1              # what's stuck, and why
python3 memory_inspect.py --why "<claim>"        # full provenance + source line
python3 memory_inspect.py --contested            # disputed claims, both directions
python3 memory_promote.py                        # dry-run the gates; writes nothing
python3 validate_examples.py                     # 69 checks over the spec + schema
```

Every script takes `--sample` and `--output json`. `/cs:memory` wraps all of it;
`/cs:memory adopt` is the only path that writes to a `CLAUDE.md`, and it backs
both files up first.

## Contents

```
DESIGN.md                       the spec: schema, gates, hook contracts, open decisions
hooks/hooks.json                three hook contracts
hooks/session_start.py          inject L3 + L2, mark cross-tier conflicts
hooks/user_prompt_submit.py     recall L1 on a 100 ms internal budget
hooks/session_end.py            capture, redact, detect, merge, stage
skills/agent-memory/SKILL.md    6/6 PASS on the write-a-skill checklist
  scripts/memory_core.py        shared: ids, redaction, locking, contradictions
  scripts/memory_extract.py     L0 → L1, rule-based, no LLM
  scripts/memory_promote.py     L1 → L2 → L3, stages proposals
  scripts/memory_inspect.py     read-only: --tier / --contested / --why
  scripts/validate_examples.py  69 checks in seven families
  assets/memory_schema.json     13 required fields, five conditionals
  references/                   three references, 6–7 sources each
agents/cs-memory-curator.md     refuses to adopt what it cannot cite
commands/cs-memory.md           status | why | contested | adopt | forget
```

## Deviations from `DESIGN.md`

`DESIGN.md` was written before the implementation and reviewed at length. Where
the built thing differs from the planned thing, **this list is authoritative**.

1. **`memory_core.py` exists.** §10's planned tree lists four scripts and no
   shared module. Building it that way would have duplicated the redaction
   patterns, the id algorithm and the lock protocol across seven files — which
   is precisely the drift class the spec exists to prevent. The module has no
   CLI and is not a plugin-facing tool.
2. **The tool count in §10.1 is wrong.** It says `+6` (3 scripts + 3 hooks).
   The delivered surface is 5 scripts + 3 hooks = **8**. Corrected in the
   counters; §10.1's text is left as the historical record of the estimate.
3. **`mark_contradictions()` was added to the core.** §4.2.1 specifies detection
   running at merge time in `SessionEnd` but assigns it to no file. It lives in
   the core so the promoter and the inspector share one definition of "open
   contradiction" rather than three.
4. **Cross-tier conflict marking marks both sides.** §5.1 requires that an L2
   and an L3 claim colliding must not both appear as plain assertions, and says
   all three candidate policies satisfy it. The implementation marks both and
   picks no winner — the least committal option, and the one that does not have
   to be undone if the open decision lands on specificity-wins.
5. **The 100 ms recall budget is met, on this machine.** §9.5 asserted the
   budget without measurement and offered dropping the hook as option (c).
   Measured: spawn-plus-recall p50 ≈ 29 ms, p95 ≈ 31 ms, max ≈ 35 ms against a
   populated store; the scoring pass itself 2–3 ms over 500 atoms. Interpreter
   start-up is the whole cost. **This does not close §9.5** — one machine is not
   a portability claim, and a slower host may still force option (c).
6. **`--why` quotes the source line.** Not specified anywhere; added because
   "cite, don't invent" is unfalsifiable if a human cannot see the cited line.
   It prints nothing when the back-pointer resolves `ambiguous`.

## What would make this worth deleting

Stated plainly because §9.3 permits it and the trial is the point:

- **Recall is too low to matter.** Rule-based extraction is deliberately
  high-precision. If a two-week trial produces a handful of atoms and none
  reach L2, the honest response is to remove the folder — not to loosen gates
  until something passes.
- **Nobody reviews the staged promotions.** The entire security argument rests
  on a human at the `adopt` gate. If staged items are accepted unread, the gate
  is theatre.
- **`--why` is never run.** Provenance nobody checks is provenance nobody needs.

## License

MIT. Concept attribution: TencentDB-Agent-Memory (MIT, © Tencent). See
[`../../LICENSE`](../../LICENSE).
