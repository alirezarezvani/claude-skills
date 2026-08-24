# Hook discipline — running on someone else's critical path

Three hooks carry this skill. Two of them run on a path where being slow or
crashing is worse than being absent. This file is the standard they are held to.

---

## 1. Fail open, always

**Confidence: high. Non-negotiable.**

Every hook exits 0 on every failure, emitting nothing. A hook that can break
session start has converted an optional feature into a single point of failure
for the whole tool.

Concretely, in each hook: the entire body is wrapped, a missing store is the
*normal first-run state* rather than an error, malformed JSON on stdin returns
silently, and a missing transcript returns silently.

The test that matters: **delete `.memory/`, corrupt `atoms.jsonl`, and remove
read permission on it — three sessions must still start normally.**

## 2. Two latency limits, and conflating them is the common error

**Confidence: high on the distinction; the measurements are stated with their
method below.**

| Limit | Value | Enforced by |
|---|---|---|
| Internal self-budget | 100 ms | the recall script itself, against a monotonic clock |
| Hook timeout backstop | 1 s | Claude Code, via the `timeout` field |

The hook `timeout` field is in **seconds**, and 1 is its floor. It exists to
kill a wedged process. **Finishing under 1 s does not satisfy the requirement** —
the recall hook runs on every prompt, so its cost compounds across a
conversation in a way a session-start cost does not.

**Measured, on the machine this was built on:** bare interpreter start
(`python3 -c pass`) p50 ≈ 12 ms / p95 ≈ 31 ms; full spawn-plus-recall against a
populated store p50 ≈ 29 ms / p95 ≈ 31 ms / max ≈ 35 ms; the scoring pass itself
2–3 ms over 500 atoms. Method: 15 sequential subprocess spawns, wall clock
around `subprocess.run`. **Confidence: high for this machine, low as a general
claim** — a cold filesystem cache, a slower disk, or a heavier interpreter
start-up will move these, and the honest response to a measurement that blows
the budget is to raise the number to the measured one or drop the hook, never to
keep an unmet claim.

The implication is worth stating because it inverts the intuition: **the script
is not the cost — the interpreter is.** Optimizing the scoring loop below ~2 ms
buys nothing. Only removing the process spawn would.

## 3. Readers take no lock

**Confidence: high.**

The recall hook reads without any lock at all. Blocking a 100 ms budget on a
lock held by an async teardown hook would blow the budget for a hook whose
entire failure mode is supposed to be "return nothing."

This is only safe because every **writer** commits via a temp file plus
`os.replace`, which is atomic within a filesystem. A reader therefore sees the
whole old file or the whole new one, never a half-written one. The lock-free
read and the atomic write are one design, not two.

Precedent in this repo, reused rather than reinvented:
`engineering/agent-harness/.../loop_controller.py` and
`engineering/skillopt-sleep/skillopt_sleep/state.py` both use the same
temp-file-plus-replace pattern.

## 4. The two timeouts are on different axes

**Confidence: high.** `5 s < 60 s` looks contradictory until you see the
questions differ:

| Value | Question | Behaviour |
|---|---|---|
| 60 s (lock mtime age) | "is this lock *abandoned*?" | older → break it immediately, no waiting |
| 5 s (wall clock) | "how long do I wait for a *live* lock?" | still held and young → retry up to 5 s, then give up |

The stale-break check runs **first**, so a writer meeting a 61-second-old lock
proceeds at once.

**Accepted race, recorded as a choice:** two writers can both judge a lock stale
and both proceed. The consequence is bounded — each still commits atomically, so
the loser's atoms are *lost*, not *corrupted*, and lost candidates re-observe on
the next session. Paying for a true mutex would buy durability this tier does not
need. Do not "fix" this without first showing the loss is observable.

## 5. Where silent loss is logged, and why not stderr

**Confidence: high.**

When a writer gives up, it appends one line to `.memory/errors.log` — timestamp,
count dropped, reason — capped at 200 lines, mode 0600.

**Not stderr.** The capture hook is `async`, so its stderr goes nowhere a human
reads. "We log the loss" to a stream nobody sees is a fiction. The log is also
surfaced by `/cs:memory status` for recent entries: a log nobody is pointed at is
the same as no log.

## 6. Never emit two contradictory lines unmarked

**Confidence: high on the constraint; the resolution *policy* is deliberately
left open.**

Session start injects project context and the global persona **together**, and
the contradiction detector structurally cannot compare them (a global atom has
no project). So nothing upstream guarantees they agree.

The hook therefore re-checks the pair at injection time and, on a collision,
marks **both** with an explicit conflict note rather than picking a winner. This
satisfies the constraint without deciding precedence — which remains an open
question. Marking both is the least committal option, and the one that does not
have to be undone if the decision lands on specificity-wins.

## 7. A recalled contested claim is never a bare claim

**Confidence: high.**

It is still injected — silently withholding a claim the user might be relying on
is worse than surfacing a disputed one — but always tagged
`[contested — newer evidence <date>]`. This rendering rule is tier-agnostic: it
applies wherever a contested atom surfaces, including one a human contested by
hand.

## 8. Every hook is independently disableable

**Confidence: high.** `AGENT_MEMORY_SESSIONSTART`, `AGENT_MEMORY_USERPROMPTSUBMIT`,
`AGENT_MEMORY_SESSIONEND`, each honouring `=0`.

The names mirror the Claude Code hook names exactly, so a user who knows the
hook names can derive all three without reading any documentation. A shorter,
cleverer name for one of them would trade that property for characters typed
once into a shell profile.

## Sources

1. Claude Code hooks reference — <https://code.claude.com/docs/en/hooks> — hook
   names, the `timeout` field's units, and `async` semantics.
2. `productivity/handoff` in this repo — the per-hook env-var disable precedent
   and its redaction linter's pattern coverage.
3. `engineering/skillopt-sleep` in this repo — `async` teardown work, and
   staging rather than applying.
4. `engineering/agent-harness` in this repo — atomic state writes via
   `os.replace`.
5. POSIX `rename(2)` / CPython `os.replace` — atomic replacement within a
   filesystem, the property lock-free reading depends on.
6. Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), ch. 3 —
   crash-safe file replacement and why partial writes are the hazard.
7. Google SRE Workbook, ch. on overload and graceful degradation — the
   fail-open posture: a degraded optional feature beats a hard dependency.
