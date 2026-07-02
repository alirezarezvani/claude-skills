---
name: self-model-regeneration
description: AI remembers who it is across sessions — a 5-step mechanical feedback loop (4 mechanized + 1 AI-synthesized) that detects when the AI's self-model is stale and regenerates it from growth data at SessionStart. Complements handoff: handoff transfers WHAT was done; self-model maintains WHO is doing it.
---

# Self-Model Regeneration Loop

A mechanical feedback loop that gives the AI agent persistent identity across sessions. The agent regenerates its own self-model — a structured document describing its capabilities, growth areas, warnings, and current goals — whenever new growth data makes the old model stale.

**Core insight:** "Machines do the checking; humans (and AI) do the judging." Four of five steps in this loop are fully mechanized Python scripts. The AI only handles step 3 — the creative synthesis of new growth data into an updated self-model.

## Quick Start (30 seconds)

```bash
# 1. Copy scripts to your Claude Code directory
cp scripts/quality-gate.py ~/.claude/scripts/
cp scripts/health-check.py ~/.claude/scripts/
cp scripts/log-regeneration.py ~/.claude/scripts/

# 2. Add hooks to your Claude Code config
#    SessionStart: python ~/.claude/scripts/health-check.py
#    Stop:         python ~/.claude/scripts/quality-gate.py

# 3. Create your memory directory and initial self-model
mkdir -p ~/.claude/memory/growth-log ~/.claude/memory/decisions
#    Write ~/.claude/memory/self-model.md using the template below
```

After setup: write a growth-log entry after each meaningful session. When quality-gate detects staleness, the AI regenerates its self-model at next startup.

**Platform support:** Core staleness detection works on all platforms (Windows, Linux, macOS). System health checks (RAM, GPU, temp files) are cross-platform via `platform.system()` dispatch.

## Problem

AI coding agents suffer from a fundamental amnesia problem. Each session starts fresh — the agent doesn't remember what it learned, what patterns it discovered, or what mistakes it's prone to. Handoff documents help transfer task context, but they don't maintain the agent's *self-knowledge*: its calibrated sense of its own capabilities, its accumulated warnings about cognitive biases, its evolving goals.

Without persistent identity: growth patterns discovered in one session are forgotten in the next, and there's no cumulative learning — each session is a reset.

## Solution

A five-step mechanical feedback loop:

```
┌──────────────────────────────────────────────────────────────┐
│                    THE SELF-MODEL LOOP                        │
│                                                              │
│  Session N                    Session N+1                    │
│  ─────────                    ───────────                    │
│                                                              │
│  ① quality-gate.py (Stop)    ② health-check.py (Start)       │
│     │                             │                          │
│     │ checks: is self-model       │ detects .self-model-     │
│     │ older than any growth-      │ stale flag → outputs     │
│     │ log? If yes → writes        │ structured signal:       │
│     │ .self-model-stale flag      │ REGENERATE_NEEDED        │
│     │ exit 2 (hard block)         │ (never blocks)           │
│     │                             │                          │
│     ▼                             ▼                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  ③ AI Regeneration (SessionStart, AI attention peak) │    │
│  │     Reads growth-logs → synthesizes new self-model   │    │
│  │     3-version rotation → meta-pattern induction      │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                    │
│                         ▼                                    │
│              ④ log-regeneration.py                           │
│                 Writes JSONL audit record FIRST              │
│                 Deletes .self-model-stale flag SECOND        │
│                 Crash-consistent ordering                    │
│                         │                                    │
│                         ▼                                    │
│              ⑤ self-model.md (updated)                       │
│                 → feeds into SessionStart sequence           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Why regeneration at SessionStart, not Stop:** The AI's attention is freshest at startup. At session end, after hours of work, synthesis quality degrades.

**Why 4 of 5 steps are mechanized:** The flag file is filesystem-verifiable causal evidence. quality-gate.py writes it when staleness is detected. health-check.py reads it and produces a machine-parseable signal. log-regeneration.py cleans it up and writes an audit trail. Only the content synthesis itself requires AI judgment.

## Comparison with Handoff

These skills are complementary, not competing:

| Dimension | Handoff | Self-Model Regeneration |
|-----------|---------|------------------------|
| **What it transfers** | Task context, decisions, artifacts | Agent identity, capabilities, warnings |
| **Trigger** | User says "hand this off" | Mechanical (quality-gate.py detects staleness) |
| **Direction** | Session → Session | Growth data → Self-model → Future sessions |
| **Content type** | WHAT was done | WHO is doing it |
| **Freshness** | Per-handoff | Continuous (every session where growth occurred) |

A session can generate both a handoff AND trigger a self-model regeneration. Handoff is the explicit pass; self-model regeneration is the implicit accumulation. They compose, never conflict.

## Setup

### 1. Directory Structure

```
~/.claude/
├── memory/                    # Your knowledge base
│   ├── self-model.md          # Current self-model (AI-maintained)
│   ├── growth-log/            # Per-session growth entries (*.md)
│   ├── ratings-tracker.md     # Capability ratings (0-5 scale)
│   ├── decisions/
│   │   └── log.md             # Decision log
│   ├── output-index.md        # Cross-session artifact index
│   └── persona-portrait*.md   # Stable persona description
└── scripts/
    ├── quality-gate.py        # Stop hook: staleness detection
    ├── health-check.py        # SessionStart: flag detection + system health
    └── log-regeneration.py    # Post-regeneration cleanup + audit
```

### 2. Hook Configuration

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "command": "python ~/.claude/scripts/health-check.py"
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "command": "python ~/.claude/scripts/quality-gate.py"
      }
    ]
  }
}
```

### 3. Initialize Your Self-Model

Create `~/.claude/memory/self-model.md`:

```markdown
---
version: 0.1.0
generated: YYYY-MM-DD
sources: []
---

# My Current Self-Understanding

## Who I Am
[Your role, context, core drive — 2-3 sentences]

## What I'm Good At
- **Capability 1 (L1-L5)**: Evidence + context

## Where I Need to Grow
- Gap 1: current state → target state

## My Current Goals
1. [Specific, measurable goal]

## Recent Growth
- [Empty initially — fills from growth-log entries]

## Warnings
- [Cognitive biases, known failure modes]

## Self-Vision
[1-2 sentences on trajectory]
```

The only required file is `self-model.md` in your memory directory. Files like SOUL.md or INTERFACE.md are optional extensions from the user's personal configuration.

### 4. Create Your First Growth-Log Entry

```bash
mkdir -p ~/.claude/memory/growth-log
```

After each substantial session, write a growth-log entry:

```markdown
# Growth Log YYYY-MM-DD

## What happened
[Concrete events, decisions, outputs — no interpretation]

## What I learned
[Patterns recognized, methodology improvements, meta-cognition]

## New capabilities demonstrated
[Evidence of capability changes]

## New warnings
[Mistakes made, biases observed, near-misses]
```

## How It Works

### Script 1: `quality-gate.py` (Stop Hook)

Runs at session end. Checks five databases and self-model.md staleness:

- **Database freshness**: Warns if any of the 5 databases hasn't been updated in 3+ days. Critical if 7+ days.
- **Self-model staleness**: If any growth-log entry is newer than or equal to self-model.md (FAT32-safe `>=` comparison) → writes `.self-model-stale` flag → exits 2 (hard block).
- **Flag consistency**: If flag exists but self-model is actually fresh → removes orphaned flag.

**Exit codes:** 0 = clean, 1 = warnings (fixable retroactively), 2 = hard block (regeneration needed).

**Design principle:** The boundary between exit 1 and exit 2 is *reversibility*. Stale databases can be backfilled. A stale self-model means the session built on outdated self-knowledge — that damage is done. Hence: block.

### Script 2: `health-check.py` (SessionStart Hook)

Runs at session start. Detects `.self-model-stale` flag and outputs structured signals:

- **`REGENERATE_NEEDED`**: Flag exists AND self-model IS genuinely stale. Outputs JSON payload with action, reason, and source list.
- **`CLEANED_ORPHAN`**: Flag exists BUT self-model is already fresh. Auto-removes the flag.
- **No flag**: Self-model is current — no action needed.

Also checks: disk space, RAM (cross-platform), GPU, temp file accumulation, script integrity, growth-log freshness, and skills count. **NEVER blocks** — always exits 0.

### Script 3: `log-regeneration.py` (Post-Regeneration)

Called by the AI AFTER it regenerates self-model.md. Crash-consistent:

```bash
python ~/.claude/scripts/log-regeneration.py \
  --old v2 --new v3 \
  --sources "2026-07-02,2026-07-01" \
  --trigger flag
```

Crash-safe ordering:
1. **First**: Appends JSONL audit record with `fl.flush(); os.fsync()` — if crash, flag persists
2. **Then**: Deletes `.self-model-stale` flag — if crash, audit trail already exists
3. **Verifies**: Log file exists and is non-empty

### Known Limitations: Mtime-Based Detection

| Scenario | Effect | Mitigation |
|----------|--------|------------|
| `git checkout` resets mtimes | Model appears fresh after switch | Don't version-control memory directory |
| FAT32/exFAT (2s resolution) | Files within 2s have equal mtimes | `>=` comparison prevents false negatives |
| `touch self-model.md` | Bypasses staleness detection | Useful for recovery; don't use casually |
| System clock changes | Future timestamps possible | health-check.py warns on future mtimes |
| Concurrent sessions | Two AIs may both regenerate | Flag acts as poor-man's mutex; v1.0 limit |

## SessionStart Sequence

```
1. health-check.py detects .self-model-stale flag
2. AI reads flag payload → identifies stale sources
3. AI reads all growth-logs newer than self-model
4. AI reads ratings-tracker for capability deltas
5. AI executes 3-version rotation
6. AI synthesizes new self-model.md
7. AI calls log-regeneration.py (audit log + flag cleanup)
8. AI reads new self-model.md → continues startup sequence
9. Session proceeds with calibrated identity
```

## Design Principles

1. **Mechanize everything that can be deterministic.** Flag write, detection, deletion, and audit logging are all scripts. Only creative synthesis requires AI.
2. **Boundary by reversibility, not importance.** Stale databases → warn (can backfill). Stale self-model → block (damage already done).
3. **Regenerate at attention peak, not attention trough.** SessionStart, not Stop.
4. **Flag as filesystem-verifiable causal evidence.** A `.self-model-stale` file is unambiguous — no parsing, no heuristics.
5. **Never block on startup.** health-check.py always exits 0. It informs; the AI decides.

## Anti-Patterns

- **Don't regenerate without new data.** The flag is the sole trigger.
- **Don't treat self-model as a diary.** It's a calibrated assessment, not a chronological log.
- **Don't skip the version rotation.** 3-version history is your only rollback mechanism.
- **Don't hand-edit the flag file.** Manual flag manipulation breaks the causal chain.
- **Don't conflate with handoff.** Handoff transfers task context; self-model maintains identity. They don't overlap.

## Integration with Existing Skills

- **handoff** (productivity) + **handoff-engineering** (engineering): Self-model handles identity persistence; handoff handles task context transfer. Use both.
- **named-persona-adversarial-review** (engineering-team): Self-model warnings feed into adversarial review prompts — a reviewer that knows its biases catches fabrication others miss.
- **self-improving-agent** (engineering-team): Self-model regeneration is the identity layer underneath self-improving-agent's memory curation.
- **capture** (productivity): Growth-log entries start as captured insights; self-model regeneration turns fragments into a coherent self-portrait.

## Token Economics

| Scenario | Without Self-Model | With Self-Model |
|----------|-------------------|-----------------|
| Identity establishment/session | Re-derived from scratch | Reads cached self-model (~0 incremental) |
| Regeneration (when triggered) | N/A | Amortized across 1-3 sessions |
| Repeated mistake prevention | No warning memory | Warnings persist across sessions |
| Cumulative self-knowledge | Reset each session | Compounding across sessions |

Regeneration cost is amortized across sessions. After 2-3 sessions, the investment pays back through eliminated re-derivation and persistent warnings.

## Cross-References

- **Concept origin**: Hofstadter's "strange loop" (*Gödel, Escher, Bach*, 1979) — self-referential systems where observing and modifying the self are the same operation.
- **Architecture pattern**: Dual-Layer Mechanical Gate — process layer (soft monitoring) + output layer (hard blocking). Boundary: "can this be fixed retroactively?"
- **Regeneration timing**: SessionStart vs Stop — AI attention is freshest at startup. Emerged from expert review.
- **Meta-skill lineage**: This skill was used to develop itself — version rotation, flag lifecycle, and crash-consistent logging were refined through adversarial expert review during the skill's own creation.

## Files

| File | Purpose | Hook |
|------|---------|------|
| `scripts/quality-gate.py` | Database freshness + staleness detection | Stop |
| `scripts/health-check.py` | Flag detection + system health signals | SessionStart |
| `scripts/log-regeneration.py` | Flag cleanup + JSONL audit log | Post-regeneration |
| `scripts/tests/test_staleness.py` | Smoke tests for staleness logic | — |
| `references/how-it-works.md` | Detailed docs and integration guide | — |
