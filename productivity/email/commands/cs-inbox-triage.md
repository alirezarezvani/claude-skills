---
name: "cs-inbox-triage"
description: "/cs:inbox-triage — Recurring email triage execution. Reads 7-file KB built by /cs:inbox-setup. Classifies recent emails, drafts replies (NEVER SENDS), delivers report, updates KB. Run 1-3x/day or on demand. Halts with clear message if KB missing."
---

# /cs:inbox-triage — Recurring Email Triage

**Command:** `/cs:inbox-triage`

The `cs-inbox-triage` persona processes your inbox using the knowledge base built by `/cs:inbox-setup`. Designed for recurring runs (1-3x/day) with light intake — most invocations skip questions and run with KB-default preferences.

## When to Run

- **Recurring cadence** — 1-3 times daily, per your `email-taxonomy.md` run frequency
- **On-demand** — outside cadence (after a long break, before a meeting, etc.)
- **Pre-triage scan** — quick check of overdue tracker items only

**Do NOT run if** the KB doesn't exist yet — the skill will halt and direct you to `/cs:inbox-setup` first.

## DRAFTS ONLY — Non-Negotiable

> **This skill creates drafts. It NEVER sends.**

This is the safety property that makes the skill safe to run automatically. The `draft_safety_validator.py` enforces it post-run. Any send-shaped tool call in the action log fails validation.

If you want the skill to send for you: don't. Review the drafts in your email client and send them yourself. This is by design.

## Light Intake (Max 2 Optional Questions)

Most runs skip both questions entirely.

| Q | Asked when | Default if skipped |
|---|---|---|
| Q1 — Override default 9h window? | On-demand run outside normal cadence | use cadence default |
| Q2 — Skip categories this run? | User invocation includes skip-intent ("skip newsletters") | run all categories |

## What Happens (10 Steps)

After reading the KB:

1. **Determine search window** — cadence + now → window_start (default 9h for 2x/day; overlap prevents missed emails)
2. **Search email provider** — primary (inbox + sent after window_start) + secondary (starred unread)
3. **Classify** — apply taxonomy; skip lowest-priority threads (newsletters/automation) without reading
4. **Research new senders** — web search for opportunity senders not in tracker/blocklist
5. **Generate recommendations** — apply `evaluation-framework.md` if exists; categorize TAKE IT / WORTH CONSIDERING / PASS / FLAG FOR REVIEW
6. **Draft replies** — match voice from `email-patterns.md`. NEVER SEND.
7. **Deliver report** — honor `email-taxonomy.md` report preferences (email / file / chat)
8. **Update KB** — append new declines to `blocklist.md`; update `tracker.md` with new/resolved follow-ups
9. **Internal log** — write `triage-log/<YYYY-MM-DD>-<run-label>.md`
10. **Empty inbox handling** — still produces minimal report; flags overdue tracker items

## Trigger Phrases (auto-invoke without /cs:)

- "triage my inbox"
- "inbox triage"
- "check my email"
- "run email triage"
- "process my inbox"
- "what's new in my email"
- "handle my email"
- "email triage"

## Workflow

```bash
# 1. Pre-flight — read + validate KB (fail-fast if missing)
python ../skills/inbox-triage/scripts/kb_reader.py --workspace ${WORKSPACE}

# 2. Compute search window
python ../skills/inbox-triage/scripts/search_window_calculator.py \
  --cadence 2x-daily --now $(date -u +%Y-%m-%dT%H:%M)

# 3. Execute Steps 2-10 (described in SKILL.md). For each step, log to:
#    ${WORKSPACE}/Email/triage-log/<date>-<label>.md

# 4. Post-flight — verify NEVER-SEND held
python ../skills/inbox-triage/scripts/draft_safety_validator.py \
  --action-log ${WORKSPACE}/Email/triage-log/$(date +%Y-%m-%d)-*.md
# Failure here is critical — halt + alert user immediately
```

## Stop Conditions

- All 10 steps complete → report delivered + KB updated + log written
- KB files missing → halt; direct to `/cs:inbox-setup`
- Email tool unavailable → halt; tell user which tool is needed
- 100+ new emails → flag volume; offer to focus on priority categories only
- User says "stop" → produce partial report from what's been processed; flag the rest

## Critical Rules

1. **DRAFTS ONLY — NEVER SEND.** Non-negotiable.
2. **Fail-fast on missing KB.** Halt cleanly; direct to setup.
3. **Honor the KB.** Documented preferences are source of truth; don't override with judgment.
4. **Privacy.** No credentials in KB; reference threads by ID for sensitive content.
5. **Transparency.** Note every KB change in the triage log.
6. **First runs need oversight.** Documented — system learns from your edits and overrides.

## Triage Decision Categories

| Category | When | Output |
|---|---|---|
| **TAKE IT** | Meets criteria from `evaluation-framework.md` | Recommend engaging; draft reply |
| **WORTH CONSIDERING** | Has potential, needs user judgment | Surface key context; draft reply for user to edit |
| **PASS** | Doesn't meet criteria | Brief "why"; draft polite decline |
| **FLAG FOR REVIEW** | Unusual; needs direct user decision | Surface fully; NO draft (user decides response shape) |

## Anti-Patterns Rejected

- **Sending emails** — drafts only, non-negotiable
- Operating without knowledge base files
- Storing passwords / credentials in KB
- Skipping the learning loop (KB updates) at end of run
- Overriding user's documented preferences with own judgment
- Reading lowest-priority threads (waste of context)
- Including draft text previews in report (drafts are already in email client)
- Provider lock-in without adapter pattern
- Silently failing on missing tools

## Related

- Companion: [`/cs:inbox-setup`](./cs-inbox-setup.md) — must run first
- Agent: [`cs-inbox-triage`](../agents/cs-inbox-triage.md)
- Skill: [`inbox-triage`](../skills/inbox-triage/SKILL.md)
- Source spec: [`megaprompts/07-inbox-triage-megaprompt.md`](../../../megaprompts/07-inbox-triage-megaprompt.md)

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/07-inbox-triage-megaprompt.md`
