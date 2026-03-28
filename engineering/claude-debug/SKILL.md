---
name: "claude-debug"
description: "Use when the user reports a bug, test failure, crash, flaky test, performance issue, or any unexpected behavior that requires systematic investigation. Enforces a 5-phase debugging protocol with PreToolUse hook gates that block code edits until root cause is confirmed. Triggers: 'debug this', 'why is this failing', 'fix this flaky test', 'investigate this crash'."
---

# Claude Debug — Phase-Gated Debugging Protocol

Structured debugging that prevents AI agents from editing code until root cause is confirmed. Five phases enforced by `PreToolUse` hooks — the agent physically cannot write to files during analysis phases.

## Why Phase Gates

AI agents guess. They see an error, form an immediate hypothesis, and start editing code. When the guess is wrong, they edit again. This guessing spiral wastes 20-30 minutes on bugs that take 10 minutes with discipline.

Phase gates make guessing structurally impossible. A `PreToolUse` hook intercepts every `Edit` and `Write` call and checks the current debug phase. In phases 1-3, edits are denied with a system message explaining what the agent should do instead. The agent cannot bypass this — hooks execute before the tool call reaches the filesystem.

Rules say "please reproduce first." Hooks say "no, you cannot edit files right now."

## Protocol — 5 Phases in Strict Order

### Phase 1: REPRODUCE (edits blocked)

Run the failing command or test. See it fail. Capture the exact error output.

Do NOT:
- Read source code
- Form hypotheses
- Open files in the suspected area

Do:
- Run the exact command the user described, 2-3 times
- Capture full error output (stack trace, exit code, stderr)
- Record the reproduction command for Phase 5

Gate: actual error output captured. Session state advances to `isolate`.

### Phase 2: ISOLATE (diagnostic edits only)

Narrow down WHERE the bug occurs using evidence, not intuition.

- Read source files along the code path indicated by the error
- Add diagnostic logging marked with `// DEBUG` or `# DEBUG` comments
- Re-run with diagnostics to pinpoint the exact location
- Apply the bug-type strategy (see below)

Only edits containing `// DEBUG` or `# DEBUG` markers are allowed by the hook. This lets the agent add temporary logging without being able to modify actual logic.

Gate: specific file, function, and line identified with diagnostic evidence. Session advances to `root_cause`.

### Phase 3: ROOT CAUSE (edits blocked)

Understand WHY the code fails, not just where.

- Analyze: expected state vs actual state at the isolated location
- Apply "5 Whys" — ask why repeatedly until the true cause is found
- Remove all `// DEBUG` diagnostic logging

Root cause template:
> The bug occurs because [COMPONENT] assumes [ASSUMPTION], but [WHAT ACTUALLY HAPPENS], causing [SYMPTOM] when [TRIGGER].

Gate: present root cause analysis to user and ask "Do you agree, or should I investigate further?" Wait for explicit confirmation. Session advances to `fix`.

### Phase 4: FIX (edits allowed)

Apply the minimal change that addresses the confirmed root cause.

- Remove any remaining `// DEBUG` lines first
- Edit only files directly related to the root cause
- Prefer a 1-line fix over a refactor
- Never change unrelated code

Session advances to `verify`.

### Phase 5: VERIFY

Confirm the fix works without regressions.

- Run the exact reproduction command from Phase 1 — must pass
- Run related tests — must pass
- For flaky or intermittent bugs: run 5+ times
- If verification fails: root cause was wrong, return to Phase 2

Session advances to `complete` when all verification passes.

## Bug-Type Strategies

Apply the matching strategy during Phase 2 (ISOLATE).

### Crash / Panic

Read the stack trace backward. Find the first frame in your code. Trace the bad value (`None`, out-of-bounds index, null pointer) to where it was produced. The bug is at the production site, not the consumption site.

### Wrong Output

Binary search through the data pipeline. Log the value at the midpoint. Correct there? Bug is downstream. Wrong? Upstream. Three iterations to find the corruption point in a 10-stage pipeline.

### Intermittent / Flaky

Run 10 times. Capture logs from a passing run AND a failing run. Diff the logs. The first divergence point reveals the race condition. Identify the shared state and the missing synchronization.

### Regression

Use `git bisect` to binary search through commit history. Find the exact commit that introduced the bug. Read its diff. Understand the unintended side effect. Fix while preserving the commit's original intent.

### Performance / Timeout

Add timing instrumentation at stage boundaries. Find which stage takes 95% of the time. Drill into that stage: tight loop? Deadlock? O(n^2) algorithm that used to work at small scale?

### Test Failure

Trace the assertion backward. Expected X, got Y. Where does Y come from? Follow the value through the call chain to the point where actual diverges from expected.

> See [references/bug-strategies.md](references/bug-strategies.md) for detailed techniques and worked examples for each bug type.

## Session State

Track progress in `.claude/debug-session.json`:

```json
{
  "phase": "reproduce",
  "bug": "test_auth_login times out after 30s",
  "started": "2025-01-15T10:30:00Z",
  "evidence": {},
  "retries": 0
}
```

The `PreToolUse` hook reads this file on every `Edit`/`Write` call and enforces the gate rules:

| Phase | Edit/Write allowed? | Exception |
|-------|---------------------|-----------|
| `reproduce` | No | None |
| `isolate` | Only if content contains `// DEBUG` or `# DEBUG` | None |
| `root_cause` | No | None |
| `fix` | Yes | None |
| `verify` | Yes | None |
| No session file | Yes | Normal coding, not in debug mode |

## Gate Mechanism

The hook is a Python script registered as a `PreToolUse` handler:

```python
# Hook checks: is there an active debug session?
# If yes: what phase? Is this edit allowed?
# If denied: return {"decision": "deny", "message": "...guidance..."}
```

The denial message tells the agent what phase it is in and what it should do instead. The agent reads this message and adjusts its approach. There is no workaround unless the user explicitly advances the phase.

## Debug Summary Template

After Phase 5, produce:

```
## Debug Summary
- Bug: [user's original report]
- Symptom: [what was observed]
- Root cause: [why it happened — the confirmed analysis]
- Fix: [what changed and why]
- Files modified: [list]
- Verification: [test results, number of runs]
```

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/debug "description"` | Start a debug session |
| `/debug:status` | Show current phase and guidance |
| `/debug:skip` | Advance to next phase (escape hatch) |
| `/debug:bisect` | Start automated git bisect for regressions |
| `/debug:log` | Manage diagnostic logging markers |
| `/debug:report` | Generate postmortem report |
| `/debug:end` | End session, clean up state |
| `/debug:history` | Show past debug sessions |

## Installation

**Zero-install (rules file only):**

```bash
mkdir -p .claude/rules
curl -o .claude/rules/debug.md https://raw.githubusercontent.com/krabat-l/claude-debug/master/rules/debug.md
```

**Full plugin (with hook enforcement):**

```bash
claude plugin add claude-debug
```

**Multi-tool support:** adapters for Cursor (`.cursor-plugin/`) and Codex (`.codex/instructions.md`) are included in the source repository.

Source: [github.com/krabat-l/claude-debug](https://github.com/krabat-l/claude-debug)

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|---|---|
| Reading code before reproducing | You'll anchor on a hypothesis before seeing the actual error |
| "I can see the bug, let me just fix it" | Surface symptoms mislead 40% of the time. Reproduce first. |
| Editing code during isolation | You'll conflate your changes with the original bug behavior |
| Skipping root cause confirmation | The user checkpoint catches wrong-direction investigations before they waste time |
| Fixing more than the root cause | Unrelated changes introduce new bugs and obscure what actually fixed the issue |
| Declaring "done" after tests pass once | Flaky bugs require 5+ verification runs |
| Piling fixes on a wrong root cause | If Phase 5 fails, return to Phase 2 with fresh investigation, not more patches |
| Removing diagnostic logging too early | Keep `// DEBUG` markers until Phase 4 so isolation evidence is preserved |

## Cross-References

- **`engineering/focused-fix`** — Use for feature-level systematic repair across many files. Claude-debug is for single-bug investigation; focused-fix is for "make this whole feature work."
- **`engineering/incident-commander`** — Use for production incidents requiring coordination. Claude-debug handles the technical investigation; incident-commander handles the response process.
- **`engineering/tech-debt-tracker`** — If debugging reveals systemic issues beyond the immediate bug, log them as tech debt rather than fixing everything in one session.

## Quick Reference

| Phase | Action | Edits? | Gate |
|---|---|---|---|
| REPRODUCE | Run failing test, capture error | Blocked | Error output captured |
| ISOLATE | Diagnostic logging, binary search | `// DEBUG` only | File + function + line identified |
| ROOT CAUSE | Analyze why, present to user | Blocked | User confirms analysis |
| FIX | Minimal change for confirmed cause | Allowed | Change applied |
| VERIFY | Run tests, check regressions | Allowed | All tests pass |
