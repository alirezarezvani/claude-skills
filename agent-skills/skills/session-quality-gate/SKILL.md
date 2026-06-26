---
name: session-quality-gate
description: Verifies session quality before ending — catches rationalized incompleteness, stale learning logs, and low disk space. Use when ending a complex coding session. Use when the agent has made multiple file edits and is about to stop. Use when you want to ensure learning was captured before shipping.
---

# Session Quality Gate

## Overview

Before ending a complex coding session, verify that the session produced genuine learning — not just working code. Code can pass all tests while the thinking behind it was sloppy: untested assumptions, skipped lessons, rationalized shortcuts. This skill checks the human side of quality.

Unlike `shipping-and-launch` (which checks production readiness) and `code-review-and-quality` (which checks code correctness), this skill checks **session quality**: did we actually learn from this work, or did we just ship and forget?

## When to Use

- Complex task completed (3+ file edits) and agent is about to stop
- Long coding sessions where "done" often means "code works but thinking was sloppy"
- Any session where you want to build the habit of capturing lessons over time
- When disk space is a concern on the working machine

## Process

### 1. Self-Audit

Before stopping, verify output across four dimensions:

| Dimension | Check |
|-----------|-------|
| Consistency | Does the output contradict itself or existing rules? |
| Completeness | Is every user requirement addressed? Nothing skipped? |
| Groundedness | Are claims backed by evidence, or assumed without verification? |
| Honesty | Is anything over-packaged? Are limitations and failures acknowledged? |

If any dimension fails, fix it before stopping. Loop until all four are green.

### 2. Learning Capture

Check that at least one learning artifact was updated today:

```
~/.claude/projects/<project>/memory/
├── ratings-tracker.md       # Skill progression
├── decisions/log.md         # Decision records
├── growth-log/              # Daily learning entries
├── output-index.md          # Session output inventory
└── tooling_capabilities.md  # Known tools catalog
```

If no library was updated and the task was complex (3+ file edits), capture at minimum:
- New facts → persona/ratings
- Decisions made → decisions/log
- Failures or insights → growth-log

### 3. Disk Check

Verify free space on the home-directory filesystem:

- **<15GB**: Critical — block stop, require cleanup
- **<50GB**: Warn but allow stop
- **50GB+**: Normal

### 4. Rationalization Detection

Watch for these patterns in the last assistant response:
- "This is a pre-existing issue" (without addressing it)
- "Skipping tests/lint/coverage for now"
- "Tests are broken but we'll fix later"
- "Not addressing the failing build"

These indicate incomplete work dressed as acceptance.

## Optional: Automated Enforcement

For teams that want programmatic enforcement, a [standalone Stop hook](https://github.com/YuhaoLin2005/delivery-gate) (200-line Python, stdlib only) implements these checks automatically. The hook receives the session transcript on stdin and exits 0 (pass) or 2 (block). Install separately if you want hard enforcement rather than a just-in-time checklist.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The code works, that's what matters" | Working code with sloppy thinking accumulates technical debt in your understanding, not just the codebase |
| "I'll document the lesson next session" | By next session, the context is gone. Capture while it's fresh |
| "This was a simple fix, no learning to capture" | Even small fixes teach something — a better pattern, a bug class, a tool quirk |
| "The learning libraries feel like overhead" | They're an investment: 5 minutes now saves hours of repeating the same mistake |
| "Disk space is fine, I checked yesterday" | Check every session. One large download can eat 50GB silently |

## Red Flags

- Agent rationalizing skipped tests with "pre-existing issue"
- Complex multi-file edits completed but no growth-log update
- Disk below 15GB with no cleanup action taken
- Session ends without a single library being touched
- Same mistake appearing across multiple sessions (learning not captured)

## Verification

Before ending a complex session:

- [ ] Self-audit: Consistency, Completeness, Groundedness, Honesty — all clear
- [ ] At least one learning library updated today (growth-log minimum)
- [ ] Disk space checked and above threshold
- [ ] No rationalization patterns in the last response

## See Also

- `shipping-and-launch` — Checks production readiness (code quality, security, monitoring). Complementary: this checks session quality.
- `code-review-and-quality` — Reviews code for bugs and style. Different scope: code output vs. thinking process.
- `doubt-driven-development` — Surfaces uncertainty before it becomes risk. Related mindset.
- `self-audit` — The core four-dimension framework extracted as a standalone skill.
- [delivery-gate](https://github.com/YuhaoLin2005/delivery-gate) — Standalone Python hook for automated enforcement of these checks.
