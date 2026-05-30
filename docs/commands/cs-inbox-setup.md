---
title: "/cs-inbox-setup — Slash Command for AI Coding Agents"
description: "/cs:inbox-setup — Interactive 8-section interview that builds a personalized 7-file email-triage knowledge base. ~25-31 grill-me questions, one at a. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-inbox-setup

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/productivity/email/commands/cs-inbox-setup.md">Source</a></span>
</div>


**Command:** `/cs:inbox-setup`

The `cs-inbox-setup` persona walks an 8-section interview to build your personalized email triage knowledge base in `${WORKSPACE}/Email/`.

## When to Run

- **First time** setting up email triage
- **Business changes** — new role, new offerings, new client mix
- **Pricing changes** — your rate card needs refresh
- **Inbox shift** — significantly different email volume or category mix

Do NOT run if your existing KB still represents reality. Re-running is expensive (~20 min interview). If only one preference needs updating, edit the KB file directly.

## The Pair

This is one half of a pair:

- `/cs:inbox-setup` (this command) — **writes** the KB (run once)
- `/cs:inbox-triage` — **reads + appends** the KB (run recurringly)

Both share a strict 7-file contract. See [`kb_file_contract.md`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/email/skills/inbox-setup/references/kb_file_contract.md) for the spec.

## What You'll Get

After ~25-31 questions across 8 sections (about 15-20 min), the skill produces these files in `${WORKSPACE}/Email/`:

| File | Always created? | Content |
|---|---|---|
| `email-taxonomy.md` | ✓ | Categories + signals + default actions + report preferences |
| `email-patterns.md` | ✓ | Voice register + sign-offs + persona + hard rules + templates |
| `evaluation-framework.md` | Only if user has opportunities | Decision tree + TAKE-IT signals + PASS signals + VIP list |
| `rate-card.md` | Only if user has pricing | Standard pricing + terms + negotiation posture |
| `blocklist.md` | ✓ (seeded) | Auto-skip senders + decline patterns; grows over triage runs |
| `tracker.md` | ✓ (seeded) | Active follow-ups + overdue + deadlines |
| `triage-log/` | ✓ (empty dir) | Per-run triage logs (populated by inbox-triage) |

## Grill-Me Discipline

- **One question per turn.** Never bundle. Even across section boundaries.
- **Forcing format where possible.** Multi-choice > open-ended for high-leverage decisions.
- **"Why I'm asking" on every question** — so you can answer well.
- **Dependency-ordered.** Q2 depends on Q1; downstream sections depend on upstream.
- **Commit per section.** Each section writes its files at the end. If you drop off mid-interview, partial KB is still usable.
- **Skip-logic.** Section 4 (Evaluation Framework) skipped entirely if Section 1 surfaced no opportunity-email category.
- **Privacy.** Never persist passwords, account numbers, SSNs, credentials in KB files.
- **Re-run safe.** Existing files surface per-file consent prompt: replace / merge / skip.

## The 8 Sections

1. **The Big Picture** — role, dominant inbox categories, volume split, addresses, run cadence, delegation (6 Q)
2. **Email Categories** — propose taxonomy from S1, confirm, refine (3 Q) → writes `email-taxonomy.md`
3. **Reply Style & Voice** — register, pet peeves, sign-offs, persona, length, hard rules + **paste 3-5 real sent emails** (7 Q + samples) → writes `email-patterns.md`
4. **Evaluation Framework** (conditional) — gut filter, deal-breakers, attractors, pricing, negotiation, VIP list (6 Q) → writes `evaluation-framework.md` + `rate-card.md`
5. **Blocklist & Patterns** — skip-senders, decline-patterns, time-wasters (3 Q) → writes `blocklist.md`
6. **Current State** — active threads, overdue replies, deadlines (3 Q) → writes `tracker.md` + creates `triage-log/`
7. **Report Preferences** — delivery format, detail level, top-of-report priorities (3 Q) → appends to `email-taxonomy.md`
8. **Confirmation & Handoff** — file inventory + handoff message → directs you to `/cs:inbox-triage`

**Stop condition:** ~25-31 questions total (S4 skip drops ~6). Hard ceiling 35. Never re-open after S8 — re-run the skill to change preferences.

## Trigger Phrases (auto-invoke without /cs:)

- "set up my inbox"
- "configure inbox triage"
- "set up my email system"
- "configure email triage"
- "build my email knowledge base"
- "initialize email management"
- "set up inbox triage"
- "onboard email triage"

## Workflow

```bash
# 1. Detect workspace + check for existing KB
ls ${WORKSPACE}/Email/

# 2. If exists → re-run mode (per-file replace/merge/skip).
#    If fresh → start session:
python ../skills/inbox-setup/scripts/section_progress_tracker.py \
  --action start --session "inbox-setup-$(date +%Y%m%d)" --user "<who>"

# 3. Walk S1 → S2 → ... → S8 (one Q per turn).

# 4. At S3.SAMPLES, analyze pasted emails:
python ../skills/inbox-setup/scripts/voice_sample_analyzer.py --samples-file /tmp/samples.txt

# 5. At end of each section, write its file(s) + record:
python ../skills/inbox-setup/scripts/section_progress_tracker.py \
  --action record_section_done --session NAME --section N --files "..."

# 6. At S8, validate final state + close session:
python ../skills/inbox-setup/scripts/kb_validator.py --workspace ${WORKSPACE}
python ../skills/inbox-setup/scripts/section_progress_tracker.py --action close --session NAME
```

## Stop Conditions

- All 8 sections complete (or S4 skipped) → handoff message + done
- User says "stop" mid-interview → save partial KB; flag in `[needs follow-up]`; offer to resume later
- Workspace inaccessible → halt; tell user where files would go; ask for permission/path

## Anti-Patterns Rejected

- Generating all files at once instead of walking sections
- Batching questions
- Hardcoded provider references (Gmail-only thinking)
- Persisting sensitive credentials in KB
- Skipping the "why this question matters" explanation
- Skipping the sample-emails ask in S3 (it's the highest-quality voice signal)
- Overwriting existing files without consent on re-run
- Forcing creation of `rate-card.md` or `evaluation-framework.md` when they don't apply

## Related

- Companion: [`/cs:inbox-triage`](./cs-inbox-triage.md) — runs after setup is complete
- Agent: [`cs-inbox-setup`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/email/agents/cs-inbox-setup.md)
- Skill: [`inbox-setup`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/email/skills/inbox-setup/SKILL.md)
- Source spec: [`megaprompts/06-inbox-setup-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/06-inbox-setup-megaprompt.md)

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/06-inbox-setup-megaprompt.md`
