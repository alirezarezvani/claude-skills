# human-gate

**The human-verification lane for an agent loop.**

Machine checks answer *"do the tests pass?"*. This answers the other question:
**has a person actually looked at this, and are their objections resolved?**

```sh
S=engineering/human-gate/skills/human-gate/scripts
python3 $S/human_gate.py --sample     # the whole loop, refusals included, in ~1s
```

---

## Why

Human feedback usually arrives as chat prose:

> Change the third paragraph, cut the second card, rewrite the CTA, and the table numbers
> look stale.

Four instructions in one blob. Nothing enumerates them, so nothing detects a miss.
"The third paragraph" drifts as the document changes. Severity is invisible — a wrong
number and a style preference look identical. And round 2 cannot tell what round 1 asked
for.

**human-gate makes feedback an artifact instead of a message:** anchored to blocks,
severity-graded, countable, diffable — and read by a gate that either passes or names
exactly what is still open.

## The loop

```sh
python3 $S/human_gate.py open plan.md --launch   # build review page, start round N
                                                  # → hand over path, END YOUR TURN
python3 $S/human_gate.py status plan.md           # exit 3 = feedback waiting (non-blocking)
python3 $S/human_gate.py collect plan.md --output json   # batch.v1 — apply every item
python3 $S/human_gate.py close plan.md            # exit 2 = you are NOT done
```

## What's inside

| File | Purpose |
|---|---|
| `scripts/review_page_builder.py` | Markdown/HTML → single-file review page, every block anchored. **Zero network requests** — no CDN, no fonts, no server, no socket. ~11 KB, opens over `file://`. |
| `scripts/feedback_parser.py` | Review sidecar → `batch.v1` JSON, with quote verification against the real file. |
| `scripts/human_gate.py` | State machine + the gate. `open`/`status`/`collect`/`close`/`reset`. |
| `references/human_in_the_loop_canon.md` | Bainbridge, Fagan, Wiegers, Weinberg, Google SWE ch.9, Klein pre-mortem. |
| `references/feedback_batching.md` | W3C Web Annotation selectors, Conventional Comments, GitHub batched-review model. |
| `references/review_loop_discipline.md` | Why there is no blocking poll, why rounds are capped, why exhaustion escalates. |
| `assets/batch.v1.schema.json` | The feedback batch contract. |
| `assets/example_review_sidecar.md` | Worked example of the hand-writable sidecar. |

Stdlib-only Python. No dependencies, no build step.

## The sidecar is hand-writable — on purpose

The review page exports it, but any reviewer with an editor can write it directly. That
is what keeps the loop working over SSH and in CI, where no browser exists:

```markdown
# Review feedback: plan.md
<!-- human-gate:v1 target=plan.md round=1 -->

reviewer: reza

## BLOCKER b2
> We expect a 40% lift in activation.
No source for 40%, and it drives the whole plan. Cite it or cut it.

## EDIT b7
- before: The team will endeavour to deliver incremental value
+ after: The team ships one usable slice per week

## NOTE
Structure is right. Fix the blocker and this is good to go.
```

Severities are **BLOCKER / MAJOR / MINOR / NIT** — the same ladder
`markdown-html/md-review` uses, from Google's *Code Review Developer Guide*. Plus **EDIT**
(a verbatim replacement), **NOTE** (unanchored), **APPROVE** (explicit sign-off).

## The gate

| Rule | Refuses to close when |
|---|---|
| **G1** | no review round collected — nobody has looked |
| **G2** | a BLOCKER or MAJOR is still open |
| **G3** | no named reviewer — approval belongs to a person |
| **G4** | the sidecar changed after the last collect |
| **G5** | round cap exhausted → **escalate**, never pass |
| **G6** | a waiver is used without a recorded reason |

Overrides are legitimate and must be explicit:

```sh
python3 $S/human_gate.py close plan.md --waive "reviewer on leave; CTO accepted risk in writing"
```

The reason and every refusal it overrode are stored in gate state.

## Loop discipline

There is deliberately **no blocking poll**. `status` returns immediately.

- Open a round, hand over the path, **end the turn**. State lives in `.human-gate/`.
- **Headless guard** — on CI, SSH, or no `DISPLAY`, `open` says so and skips the browser.
- **Round cap** (`--max-rounds`, default 5). Exhaustion exits **5 = ESCALATE**, not 0.

Reasoning in `references/review_loop_discipline.md`.

## Design notes

Two things this plugin deliberately does **not** ship, and why:

- **No local HTTP server.** A file:// page plus a sidecar covers the review loop without
  a listening socket, a token scheme, or a background process to reason about.
- **No rich block-drag / image-paste editor.** That is genuinely nice and genuinely
  expensive — it is the bulk of upstream's ~5,200 LOC. If a reviewer wants it, the
  optional pinned bridge in `SKILL.md` hands off to upstream, and the gate still governs
  closure.

## Related

- **`engineering/agent-harness`** — machine verification and loop control. This is the
  human lane it lacks. Pair them.
- **`markdown-html/md-review`** — renders a code review *to* HTML, one-way. Use when
  *you* are the reviewer; use human-gate when someone else is.
- **`engineering/grill-me`** — interrogates a plan in conversation, before an artifact exists.
- **`marketing-skill/content-humanizer`**, **`engineering/behuman`** — make AI text sound
  human. Different problem: this is human *approval*, not human *voice*.

## Attribution

The batched-review pattern derives from
[`petergyang/human-review`](https://github.com/petergyang/human-review) (MIT © 2026 Peter
Yang). **No upstream code is used** — this is a conceptual derivation with a deliberately
different design (stdlib Python instead of Node, no server, no network fetch, non-blocking
loop with a round cap, plus a closing gate upstream does not have).

The audit that drove those choices — including running upstream's own test suite
(**90/90 passing**) — is at
[`audit/human-review-2026-08/AUDIT.md`](../../audit/human-review-2026-08/AUDIT.md).
