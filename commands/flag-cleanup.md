---
description: Run the quarterly feature-flag cleanup workflow on the current repo
---

# /flag-cleanup

Run the full feature-flag cleanup workflow:

1. Scan for stale flags (older than 90 days, used in ≤2 places)
2. For each candidate, identify the introducing PR/issue and current owner
3. Generate a removal plan grouped by owner
4. Run kill-switch audit against the flag-doc registry
5. Output a markdown report ready to share with the team

## Usage

```
/flag-cleanup
/flag-cleanup --max-age-days 60
/flag-cleanup --flag-doc runbooks/flags.md
```

## Implementation

This command dispatches to the `feature-flags-architect` skill:

```bash
SKILL=engineering/feature-flags-architect/skills/feature-flags-architect

# Step 1: scan for debt
python "$SKILL/scripts/flag_debt_scanner.py" --repo . --max-age-days "${MAX_AGE_DAYS:-90}" --format json > .flag-debt.json

# Step 2: audit kill switches
python "$SKILL/scripts/kill_switch_audit.py" --repo . --flag-doc "${FLAG_DOC:-docs/feature-flags.md}" --format json > .kill-switch-audit.json

# Step 3: synthesize a markdown report
# (Claude reads both JSON files, groups by owner, drafts the cleanup plan)
```

## Output

A markdown report with:

- **Stale flag candidates** grouped by owner, with introducing commit links
- **Undocumented flags** that fail the kill-switch audit
- **Incomplete documentation** (missing fields per flag)
- **Suggested removal PRs** — one per owner

## Pre-conditions

- Run from a git repository with the source code committed
- A flag-doc registry exists (default: `docs/feature-flags.md`)
- The `feature-flags-architect` skill is installed

## Post-conditions

- `.flag-debt.json` and `.kill-switch-audit.json` written to repo root (ignored via `.gitignore`)
- Markdown report streamed to terminal
- Recommended next step printed (which removal PR to start with)
