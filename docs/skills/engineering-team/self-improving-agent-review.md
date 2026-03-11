---
title: "/si:review — Analyze Auto-Memory"
description: "/si:review — Analyze Auto-Memory - Claude Code skill from the Engineering - Core domain."
---

# /si:review — Analyze Auto-Memory

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Engineering - Core</span>
<span class="meta-badge">:material-identifier: `review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/self-improving-agent/skills/review/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-skills</code>
</div>


Performs a comprehensive audit of Claude Code's auto-memory and produces actionable recommendations.

## Usage

```
/si:review                    # Full review
/si:review --quick            # Summary only (counts + top 3 candidates)
/si:review --stale            # Focus on stale/outdated entries
/si:review --candidates       # Show only promotion candidates
```

## What It Does

### Step 1: Locate memory directory

```bash
# Find the project's auto-memory directory
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"

# Fallback: check common path patterns
# ~/.claude/projects/<user>/<project>/memory/
# ~/.claude/projects/<absolute-path>/memory/

# List all memory files
ls -la "$MEMORY_DIR"/
```

If memory directory doesn't exist, report that auto-memory may be disabled. Suggest checking with `/memory`.

### Step 2: Read and analyze MEMORY.md

Read the full `MEMORY.md` file. Count lines and check against the 200-line startup limit.

Analyze each entry for:

1. **Recurrence indicators**
   - Same concept appears multiple times (different wording)
   - References to "again" or "still" or "keeps happening"
   - Similar entries across topic files

2. **Staleness indicators**
   - References files that no longer exist (`find` to verify)
   - Mentions outdated tools, versions, or commands
   - Contradicts current CLAUDE.md rules

3. **Consolidation opportunities**
   - Multiple entries about the same topic (e.g., three lines about testing)
   - Entries that could merge into one concise rule

4. **Promotion candidates** — entries that meet ALL criteria:
   - Appeared in 2+ sessions (check wording patterns)
   - Not project-specific trivia (broadly useful)
   - Actionable (can be written as a concrete rule)
   - Not already in CLAUDE.md or `.claude/rules/`

### Step 3: Read topic files

If `MEMORY.md` references or the directory contains additional files (`debugging.md`, `patterns.md`, etc.):
- Read each one
- Cross-reference with MEMORY.md for duplicates
- Check for entries that belong in the main file (high value) vs. topic files (details)

### Step 4: Cross-reference with CLAUDE.md

Read the project's `CLAUDE.md` (if it exists) and compare:
- Are there MEMORY.md entries that duplicate CLAUDE.md rules? (→ remove from memory)
- Are there MEMORY.md entries that contradict CLAUDE.md? (→ flag conflict)
- Are there MEMORY.md patterns not yet in CLAUDE.md that should be? (→ promotion candidate)

Also check `.claude/rules/` directory for existing scoped rules.

### Step 5: Generate report

Output format:

```
📊 Auto-Memory Review

Memory Health:
  MEMORY.md:        {{lines}}/200 lines ({{percent}}%)
  Topic files:      {{count}} ({{names}})
  CLAUDE.md:        {{lines}} lines
  Rules:            {{count}} files in .claude/rules/

🎯 Promotion Candidates ({{count}}):
  1. "{{pattern}}" — seen {{n}}x, applies broadly
     → Suggest: {{target}} (CLAUDE.md / .claude/rules/{{name}}.md)
  2. ...

🗑️ Stale Entries ({{count}}):
  1. Line {{n}}: "{{entry}}" — {{reason}}
  2. ...

🔄 Consolidation ({{count}} groups):
  1. Lines {{a}}, {{b}}, {{c}} all about {{topic}} → merge into 1 entry
  2. ...

⚠️ Conflicts ({{count}}):
  1. MEMORY.md line {{n}} contradicts CLAUDE.md: {{detail}}

💡 Recommendations:
  - {{actionable suggestion}}
  - {{actionable suggestion}}
```

## When to Use

- After completing a major feature or debugging session
- When `/si:status` shows MEMORY.md is over 150 lines
- Weekly during active development
- Before starting a new project phase
- After onboarding a new team member (review what Claude learned)

## Tips

- Run `/si:review --quick` frequently (low overhead)
- Full review is most valuable when MEMORY.md is getting crowded
- Act on promotion candidates promptly — they're proven patterns
- Don't hesitate to delete stale entries — auto-memory will re-learn if needed
