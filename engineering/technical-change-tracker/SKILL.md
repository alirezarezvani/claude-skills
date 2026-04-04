---
name: "technical-change-tracker"
description: |
  Track code changes with structured JSON records and accessible HTML output for AI session continuity. Use when user says /tc, /tc init, /tc create, /tc update, /tc status, /tc resume, /tc close, /tc export, /tc dashboard, or /tc retro.
---

# Technical Change (TC) Tracker

Track every code change with structured JSON records and accessible HTML output.
When an AI bot session expires or is abandoned, the next bot picks up exactly where the last one left off.

## Install

```bash
git clone https://github.com/Elkidogz/technical-change-skill.git
```

## Commands

| Command | Description |
|---------|-------------|
| `/tc init` | Initialize TC tracking in current project |
| `/tc create <name>` | Create a new TC record |
| `/tc update <tc-id>` | Update a TC (status, files, tests) |
| `/tc status [tc-id]` | View TC status |
| `/tc resume <tc-id>` | Resume from previous session handoff |
| `/tc close <tc-id>` | Deploy and close a TC |
| `/tc export` | Regenerate all HTML from JSON |
| `/tc dashboard` | Regenerate dashboard |
| `/tc retro <changelog.json>` | Batch-create TCs from project history |

## Features

- **JSON records** with append-only revision history and field-level change tracking
- **State machine**: Planned > In Progress > Blocked > Implemented > Tested > Deployed
- **Test cases** with log snippet evidence and manual approval
- **AI session handoff**: progress, next steps, blockers, key context, decisions
- **Non-blocking**: TC bookkeeping runs as background subagent, never interrupts coding
- **Retroactive**: `/tc retro` batch-creates TCs from existing undocumented history
- **WCAG AA+ HTML**: dark theme, rem-based fonts, CSS-only dashboard filters
- **Zero dependencies**: Python stdlib only

## State Machine

```
planned --> in_progress --> implemented --> tested --> deployed
   |             |               |            |          |
   +-> blocked <-+               +-> in_progress <------+
```

## Repository

https://github.com/Elkidogz/technical-change-skill

MIT License.
