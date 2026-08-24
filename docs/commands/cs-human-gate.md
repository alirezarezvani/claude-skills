---
title: "/cs-human-gate — Slash Command for AI Coding Agents"
description: "/cs:human-gate — Get real human review on an artifact and prove it happened. Builds a single-file review page, collects batched feedback as. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-human-gate

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/human-gate/commands/cs-human-gate.md">Source</a></span>
</div>


**Command:** `/cs:human-gate <artifact> [step]`

Machine checks answer *"do the tests pass?"*. This answers the other one:
**has a person actually looked at this, and are their objections resolved?**

## When to Run

- Before shipping anything external, irreversible, or regulated
- "Let me review that first" / "get sign-off" / "have someone check this"
- "Don't ship until I've seen it"
- You have applied feedback and are about to declare done
- A plan, spec, RFC, report, migration, or customer-facing artifact is ready

## When NOT to Run

- To make AI text sound human → `content-humanizer` / `behuman` (different problem entirely)
- To review a code diff yourself → `md-review` or `code-reviewer`
- To pressure-test an idea before any artifact exists → `grill-me`
- For machine-checkable verification → `agent-harness`

## Pre-flight

Refuse to proceed and say which is missing:

1. **Artifact exists** and is `.md` or `.html`.
2. **A named reviewer** is identified — a person, not "the team". The gate enforces this (G3).
3. **Round budget agreed** — default 5. An uncapped review loop is a way to avoid deciding.
4. **Stakes established** — reversible or not? One-way doors need an explicit APPROVE,
   not merely an absence of blockers.

## Steps

```sh
S=engineering/human-gate/skills/human-gate/scripts
```

### 1. `open` — start a round

```sh
python3 $S/human_gate.py open "$ARTIFACT" --launch
```

Builds a single-file review page (zero network requests, opens over `file://`) and records
round N. Prints the sidecar path.

**Then end the turn.** Do not poll. On a headless host `open` detects it, skips the browser,
and tells you to hand over the path — the reviewer can write the sidecar by hand in any editor.

### 2. `status` — non-blocking check

```sh
python3 $S/human_gate.py status "$ARTIFACT"
```

| Exit | Meaning |
|---|---|
| 0 | collected and clear — `close` would pass |
| 2 | collected, but `close` would refuse — prints which rules, same code `close` uses |
| 3 | feedback waiting — collect it |
| 4 | nothing on disk yet — end the turn again |

Branch on the code alone: 0 clear · 2 blocked · 3 collect me · 4 nothing yet.

### 3. `collect` — read the batch

```sh
python3 $S/human_gate.py collect "$ARTIFACT" --output json
```

Emits `batch.v1`: every item with severity, block anchor, quote, and the blocking total.
Quotes are verified against the real file — a mismatch is reported, not swallowed.

**Apply every item.** `EDIT` items carry `after` across **verbatim** — that is the
reviewer's own wording, not a suggestion to paraphrase. If the artifact is generated from
a source, apply the edit there too or it disappears on the next build.

### 4. `close` — the gate

```sh
python3 $S/human_gate.py close "$ARTIFACT"
```

| Rule | Refuses when |
|---|---|
| G1 | no round collected — nobody has looked |
| G2 | a BLOCKER or MAJOR is still open |
| G3 | no named reviewer |
| G4 | the sidecar changed after the last collect |
| G5 | round cap exhausted → escalate |
| G6 | waiver used without a recorded reason — **G1 can never be waived** |
| G7 | the round carries unresolved integrity problems (mistyped severity, EDIT with no replacement, quote not in the file) |

**Exit 2 means you are not done.** Report what is open, not a summary that implies success.

Legitimate override, recorded:

```sh
python3 $S/human_gate.py close "$ARTIFACT" --waive "reviewer on leave; CTO accepted risk in writing"
```

## Output digest

Report back exactly this shape:

```
GATE: <PASSED | REFUSED | ESCALATE>
Reviewer: <name>
Rounds: <n> of <max>
Open: <BLOCKER/MAJOR items, by block id>
Applied: <what you changed, and in which source files>
Next: <the one action, or "none — done">
```

## Try it

```sh
python3 engineering/human-gate/skills/human-gate/scripts/human_gate.py --sample
```

Runs the whole loop in a temp dir — including the refusals — in about a second.
