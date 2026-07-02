# How Self-Model Regeneration Works

Detailed reference for the 5-step mechanical feedback loop. Read this if you're debugging the loop, adding integrations, or want to understand the architecture deeply.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLAG LIFECYCLE                               │
│                                                                 │
│  quality-gate.py (Stop)                                         │
│    │                                                             │
│    │ self-model stale? ──yes──► write .self-model-stale          │
│    │                             exit 2                          │
│    │                                                             │
│    │ self-model fresh? ──yes──► cleanup orphaned flag            │
│    │                             exit 0 or 1                     │
│    │                                                             │
│    ▼                                                             │
│  .self-model-stale (on disk)                                     │
│    │                                                             │
│    ▼                                                             │
│  health-check.py (SessionStart)                                  │
│    │                                                             │
│    │ flag exists + model stale? ──► REGENERATE_NEEDED            │
│    │ flag exists + model fresh? ──► CLEANED_ORPHAN               │
│    │ no flag?                    ──► nothing                     │
│    │                                                             │
│    ▼                                                             │
│  AI Regeneration (SessionStart)                                  │
│    │                                                             │
│    │ 1. Read newer growth-logs                                   │
│    │ 2. Read ratings-tracker                                     │
│    │ 3. 3-version rotation                                       │
│    │ 4. Synthesize new self-model.md                             │
│    │                                                             │
│    ▼                                                             │
│  log-regeneration.py                                             │
│    │                                                             │
│    │ 1. Write JSONL audit record (fsync)                         │
│    │ 2. Verify log exists                                        │
│    │ 3. Delete .self-model-stale                                 │
│    │                                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Script Reference

### quality-gate.py

**Purpose:** Stop hook. Detects when self-model is stale and writes the flag.

**Input:** File system state (memory directory, growth-logs, self-model.md).

**Output:** Exit code + stderr messages.
- Exit 0: Clean. All databases fresh, self-model current.
- Exit 1: Warnings. Some databases stale, but self-model is current. Fixable retroactively.
- Exit 2: Hard block. Self-model is stale relative to growth data. Session ran with outdated identity.

**`--json` flag:** Prints structured JSON to stdout:
```json
{
  "exit_code": 2,
  "exit_label": "hard_block",
  "self_model": {
    "stale": true,
    "reason": "growth-log entries newer than self-model: 2026-07-02, 2026-07-01",
    "sources": ["2026-07-02", "2026-07-01"]
  },
  "databases": [
    {"name": "growth-log", "days": 0.5, "status": "ok"},
    {"name": "decisions/log", "days": 2.1, "status": "ok"},
    {"name": "output-index", "days": 4.0, "status": "warning"},
    {"name": "ratings-tracker", "days": 2.0, "status": "ok"},
    {"name": "persona-portrait", "days": 8.0, "status": "critical"}
  ]
}
```

**Staleness detection algorithm:**
1. Get self-model.md mtime
2. For each growth-log entry (YYYY-MM-DD*.md):
   - If entry mtime >= self-model mtime → entry is newer
3. If any entry is newer → stale → write flag → exit 2

**Why `>=` and not `>`:** FAT32/exFAT filesystems have 2-second mtime resolution. A growth-log written within the same 2-second window as the self-model would appear "equal." Using `>=` ensures we flag staleness rather than missing it.

**Flag cleanup:** If `.self-model-stale` exists but self-model is actually fresh (all growth-logs older), the script removes the orphaned flag. This handles the edge case where log-regeneration.py failed to delete the flag but the AI did regenerate.

### health-check.py

**Purpose:** SessionStart hook. Reads the flag file and emits structured signals.

**Key contract:** **NEVER blocks.** Always exits 0. This is a soft monitoring layer — it informs, never prevents. The boundary between soft (health-check) and hard (quality-gate) is deliberate.

**Signals (to stderr):**
```
SELF_MODEL:REGENERATE_NEEDED:model_missing
SELF_MODEL:REGENERATE_NEEDED:empty_file
SELF_MODEL:REGENERATE_NEEDED:growth_logs_newer(3):2026-07-02,2026-07-01,...
SELF_MODEL:CLEANED_ORPHAN:model_fresh:flag_was_2026-07-02T12:00:00
SELF_MODEL:WARN:future_mtime:3600s_ahead
SELF_MODEL:WARN:truncated_file:20bytes
SELF_MODEL:JSON:{"action":"regenerate","reason":"...","trigger":"flag","sources":[...]}
```

**Also checks (informational):**
- **disk:** Free space in GB, warns at 50GB, refuses at 15GB
- **ram:** Used percentage and free/total MB (cross-platform: wmic/Linux procfs/macOS vm_stat)
- **gpu:** NVIDIA GPU temperature, utilization, VRAM (nvidia-smi, skipped if unavailable)
- **tmp:** File count in temp directory, warns at 500 files
- **config:** Integrity check for the three scripts (quality-gate, health-check, log-regeneration)
- **growth:** Days since last growth-log entry, warns at 3 days
- **skills:** Count of active skills

**`--json` flag:** Collects all check results and prints structured JSON to stdout:
```json
{
  "disk": {"name": "disk", "free_gb": 200, "level": "OK"},
  "ram": {"name": "ram", "pct": 45, "free_mb": 8192, "total_mb": 16384},
  "gpu": {"name": "gpu", "temp_c": 55, "util_pct": 30, "vram_used_mb": 2048, "vram_total_mb": 8192, "level": "OK"},
  "tmp": {"name": "tmp", "count": 120, "level": "OK"},
  "config": {"name": "config", "missing": [], "level": "OK"},
  "growth": {"name": "growth-log", "latest": "2026-07-02", "days": 0, "level": "OK"},
  "skills": {"name": "skills", "count": 8, "level": "OK"},
  "self_model_flag": {"signal": "REGENERATE_NEEDED", "reason": "growth_logs_newer(2)", "action": "regenerate", "payload": {...}},
  "exit_code": 0
}
```

### log-regeneration.py

**Purpose:** Post-regeneration cleanup and audit. Called by AI after synthesizing new self-model.md.

**Usage:**
```bash
python log-regeneration.py \
  --old v2 \
  --new v3 \
  --sources "2026-07-02,2026-07-01" \
  --trigger flag
```

**Crash-consistent ordering:**
1. **JSONL write + fsync FIRST** — If this crashes, flag persists → health-check re-detects next session
2. **Log verification** — Confirms the log file exists and has content. If verification fails, exits 1 WITHOUT deleting flag.
3. **Flag deletion SECOND** — If this crashes, audit trail exists → health-check cleans orphan next session

**Audit trail format** (`.self-model-regeneration.jsonl`, one JSON object per line):
```json
{"timestamp": "2026-07-02T12:00:00+00:00", "trigger": "flag", "sources": ["2026-07-02", "2026-07-01"], "old_version": "v2", "new_version": "v3", "flag_cleaned": true}
```

**`--json` flag:** Outputs structured result:
```json
{
  "success": true,
  "timestamp": "2026-07-02T12:00:00+00:00",
  "trigger": "flag",
  "sources": ["2026-07-02", "2026-07-01"],
  "old_version": "v2",
  "new_version": "v3",
  "flag_cleaned": true,
  "log_appended": true,
  "log_verified": true
}
```

## SessionStart Sequence (Full)

When health-check.py signals `REGENERATE_NEEDED`, the AI should:

1. Parse the `SELF_MODEL:JSON:{...}` payload from stderr
2. Read all growth-logs listed in `sources`
3. Read `ratings-tracker.md` for capability deltas
4. Execute 3-version rotation:
   - `self-model.md` → `self-model.v1.md`
   - `self-model.v1.md` → `self-model.v2.md`
   - `self-model.v2.md` → `self-model.v3.md` (oldest rotates out)
5. Write new `self-model.md` synthesizing growth data
6. Call `log-regeneration.py --old <prev> --new <current> --sources "..." --trigger flag`
7. Read the new self-model → continue normal startup

## Integration Points

### Hook Configuration

The skill uses Claude Code's hook system:

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | health-check.py | Detect flag, system health |
| Stop | quality-gate.py | Detect staleness, write flag |

### Complementarity with handoff

```
Session N-1 (end)
  ├── handoff: "Here's what I did and where I left off" → next agent
  └── quality-gate.py: "Here's what I learned" → flag → next session's self

Session N (start)
  ├── health-check.py: detects flag → AI regenerates self-model
  ├── self-model.md: "Here's who I am and what I know about myself"
  └── handoff from previous: "Here's the task context"
```

Handoff is the explicit, intentional transfer of task context to a different agent. Self-model regeneration is the implicit, automatic accumulation of self-knowledge for the same agent across sessions. They compose, never conflict.

## Design Decisions

### Why SessionStart for regeneration, not Stop?

The AI's attention is freshest at startup. At session end, after hours of work, synthesis quality degrades. Regenerating at SessionStart means the self-model benefits from the AI's peak cognitive state.

This was a key finding from adversarial expert review: the original design regenerated at Stop, which produced degraded self-models that compounded errors across sessions.

### Why filesystem flags instead of structured data?

A `.self-model-stale` file on disk is unambiguous causal evidence. No parsing, no interpretation, no heuristics. The file exists → regeneration is needed. The file doesn't exist → self-model is current. This is the simplest possible interface — and therefore the hardest to break.

### Why crash-consistent ordering (log before flag delete)?

If we delete the flag first and then crash during log write, we lose both the flag (trigger) and the log (audit trail). The regeneration disappears without a trace. By writing the log first (with fsync), we guarantee that either:
- Both succeed: normal lifecycle
- Log succeeds, flag delete fails: orphaned flag → health-check cleans it
- Log fails: flag persists → health-check re-detects next session

No state combination results in lost data.

### Why 3-version rotation?

Self-model regeneration is creative synthesis — it can produce degraded models. The 3-version history provides a rollback mechanism. If the new self-model is worse than the previous version, the previous version is still available.

## Known Limitations

| Limitation | Impact | Planned Fix (v1.1) |
|-----------|--------|-------------------|
| Mtime-based detection | git checkout resets timestamps | Content-hash-based freshness |
| Single-instance only | Two concurrent AIs may race | PID-based lock file |
| No content validation | Regenerated model could be low quality | Mechanical quality checks |
| No multi-agent support | One self-model for one agent | Agent-ID namespaced models |
| Manual flag bypass (`touch`) | Users can defeat staleness detection | TTL-based secondary check |

These are documented limitations, not bugs. A content-hash-based freshness check is planned for v1.1.

## Testing

Smoke tests are in `scripts/tests/test_staleness.py` (27 tests, 8 classes):

```bash
# Run with unittest (stdlib, no dependencies)
python scripts/tests/test_staleness.py

# Run with pytest
python -m pytest scripts/tests/test_staleness.py -v
```

Test classes:
- `TestDaysSince` — days_since() return type and edge cases
- `TestFindPersona` — _find_persona() glob and fallback
- `TestFlagLifecycle` — flag write → read → delete round-trip
- `TestGrowthLogFilenameRegex` — date pattern validation
- `TestMtimeStalenessLogic` — FAT32 resolution, clock skew
- `TestLogRegenerationOrdering` — crash-consistent write ordering
- `TestExitCodes` — quality-gate.py exit code semantics
- `TestHealthCheckSignals` — REGENERATE_NEEDED and CLEANED_ORPHAN signals
- `TestLogRegenerationScript` — CLI interface and crash-safety

All tests use stdlib only (`unittest`, `tempfile`, `subprocess`, `importlib`).
