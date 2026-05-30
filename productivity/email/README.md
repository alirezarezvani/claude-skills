# email

**Workflow-pair plugin.** Two paired skills (`inbox-setup` + `inbox-triage`) that together implement a personalized recurring email triage system.

The pair shares a strict 7-file knowledge-base contract at `${WORKSPACE}/Email/`. `inbox-setup` writes; `inbox-triage` reads + appends. PR #657's cross-skill consistency audit verified the file contract aligns verbatim between the two megaprompts.

## How the pair works

```
┌──────────────────────┐         ┌──────────────────────────────┐
│   /cs:inbox-setup    │   ───►  │  ${WORKSPACE}/Email/          │
│                      │  writes │  ├── email-taxonomy.md         │
│  Interactive         │         │  ├── email-patterns.md         │
│  interview (~25-31   │         │  ├── evaluation-framework.md*  │
│  grill-me questions  │         │  ├── rate-card.md*             │
│  across 8 sections). │         │  ├── blocklist.md              │
│  Run ONCE.           │         │  ├── tracker.md                │
│                      │         │  └── triage-log/               │
└──────────────────────┘         └──────────────────────────────┘
                                          │
                                          │ reads + appends
                                          ▼
                                 ┌──────────────────────────────┐
                                 │   /cs:inbox-triage           │
                                 │                              │
                                 │   Recurring (1-3x/day) or    │
                                 │   on-demand. Classifies      │
                                 │   recent emails, drafts      │
                                 │   replies (NEVER SENDS),     │
                                 │   delivers report, updates   │
                                 │   blocklist + tracker.       │
                                 └──────────────────────────────┘

  * Conditional — created only if user has opportunities/pricing
```

## What each skill does

### inbox-setup (run once)

Interactive interview using **grill-me discipline** — one question at a time, dependency-ordered, forcing format where possible, "why I'm asking" on every question. Walks 8 sections (~25-31 questions, hard ceiling 35):

1. **The Big Picture** — role, dominant categories, volume split, cadence (6 Q)
2. **Email Categories** — propose taxonomy, confirm, refine (3 Q)
3. **Reply Style & Voice** — register, pet peeves, signatures, persona, length, hard rules + **3-5 real sent-email samples** for voice extraction (7 Q)
4. **Evaluation Framework** (conditional) — gut filter, deal-breakers, attractors, pricing, negotiation, VIP list (6 Q) — skipped if no opportunities
5. **Blocklist & Patterns** — auto-skip senders, patterns, time-wasters (3 Q)
6. **Current State** — active threads, overdue replies, deadlines (3 Q)
7. **Report Preferences** — delivery format, detail level, top-of-report priorities (3 Q)
8. **Confirmation & Handoff** — file inventory + handoff to triage

Generates the 7-file KB. Re-runnable; existing files surface a per-file replace/merge/skip prompt.

### inbox-triage (run recurringly)

**Light-intake by design** — most invocations skip questions and run with KB-default preferences. At most 2 grill-me override questions:

- Q1 (optional) — override default search window (asked only for on-demand runs outside normal cadence)
- Q2 (optional) — skip categories this run (asked only when user invokes with skip intent)

Then 10 execution steps: search window → search email → classify → research new senders → generate recommendations → draft replies (**NEVER SENDS**) → deliver report → update KB → log internally → handle empty inbox.

## The 7-file shared contract

The contract is the **integration boundary** between the two skills. Any drift breaks the pair. See `skills/*/references/kb_file_contract.md` for the canonical spec (mirrored on both sides with write-perspective + read-perspective text).

| File | Setup writes | Triage reads | Triage updates |
|---|:---:|:---:|:---:|
| `email-taxonomy.md` | ✓ | ✓ | — |
| `email-patterns.md` | ✓ | ✓ | — |
| `evaluation-framework.md` (conditional) | ✓ | ✓ if exists | — |
| `rate-card.md` (conditional) | ✓ | ✓ if exists | — |
| `blocklist.md` | seeded | ✓ | ✓ (appends new declines + patterns) |
| `tracker.md` | seeded | ✓ | ✓ (appends + resolves follow-ups) |
| `triage-log/` | empty dir | — | ✓ (writes per-run log) |

## Source specs

- [`megaprompts/06-inbox-setup-megaprompt.md`](../../megaprompts/06-inbox-setup-megaprompt.md) (PR #657)
- [`megaprompts/07-inbox-triage-megaprompt.md`](../../megaprompts/07-inbox-triage-megaprompt.md) (PR #657)

The megaprompts are canonical; these plugins are working implementations. Drift between any megaprompt and its skill is a bug — re-grill with `/cs:grill-with-docs` if they diverge.

## Plugin layout

```
engineering/email/
├── .claude-plugin/plugin.json     ← multi-skill: ["./skills/inbox-setup", "./skills/inbox-triage"]
├── README.md
├── agents/
│   ├── cs-inbox-setup.md           ← interview persona, 8-section grill enforcer
│   └── cs-inbox-triage.md          ← recurring-run persona, DRAFTS-ONLY enforcer
├── commands/
│   ├── cs-inbox-setup.md           ← /cs:inbox-setup
│   └── cs-inbox-triage.md          ← /cs:inbox-triage
└── skills/
    ├── inbox-setup/
    │   ├── SKILL.md                ← Path-B converted from megaprompt 06
    │   ├── references/
    │   │   ├── kb_file_contract.md          ← shared contract (write side)
    │   │   ├── grill_me_section_walk.md     ← 8-section discipline
    │   │   └── voice_calibration.md         ← sample-based voice extraction
    │   └── scripts/
    │       ├── kb_validator.py              ← stdlib: validates 7-file output
    │       ├── section_progress_tracker.py  ← stdlib: 8-section walk state
    │       └── voice_sample_analyzer.py     ← stdlib: extracts patterns from samples
    └── inbox-triage/
        ├── SKILL.md                ← Path-B converted from megaprompt 07
        ├── references/
        │   ├── kb_file_contract.md          ← same contract (read side, mirrored)
        │   ├── triage_decision_framework.md ← TAKE-IT / WORTH / PASS / FLAG taxonomy
        │   └── drafts_only_safety.md        ← the NEVER-SEND discipline canon
        └── scripts/
            ├── kb_reader.py                ← stdlib: reads + validates 7 files
            ├── search_window_calculator.py ← stdlib: cadence + now → window
            └── draft_safety_validator.py   ← stdlib: enforces never-send check
```

## Quick start

```bash
# 1. Run inbox-setup ONCE (interactive interview):
#    Use /cs:inbox-setup or trigger phrases like "set up my inbox"

# 2. After setup, run inbox-triage on cadence (e.g., 2x/day):
#    Use /cs:inbox-triage or trigger phrases like "triage my inbox"

# Validate the KB contract at any time:
python skills/inbox-setup/scripts/kb_validator.py --workspace ${WORKSPACE}

# Compute the search window for an on-demand run:
python skills/inbox-triage/scripts/search_window_calculator.py --cadence 2x-daily --now 2026-05-15T14:00
```

## License

MIT.
