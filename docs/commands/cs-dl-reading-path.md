---
title: "/cs-dl-reading-path — Slash Command for AI Coding Agents"
description: "/cs-dl-reading-path — Build a prerequisite-closed reading path through the Deep Learning book from a goal, a background and the hours you actually. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-dl-reading-path

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/deep-learning-book/commands/cs-dl-reading-path.md">Source</a></span>
</div>


**Command:** `/cs-dl-reading-path [goal]`

The book's part order is not its dependency order. Front-to-back means weeks in Chapters 2–4
before touching a network, which is where most readers stop.

## Procedure

1. **Ask three things** if the user has not said them, one at a time:
   - What do you want to be able to *do* afterwards?
   - Background: `none` / `math` / `applied` / `research`?
   - Realistic study hours per week?
2. **Run the planner:**
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/deep-learning-book/scripts/reading_path_planner.py \
       --goal "<goal>" --background <bg> --hours-per-week <n>
   ```
3. **Handle the refusals rather than working around them.**
   - Exit 3 — the goal is outside the book. Relay what covers it; do not invent a path.
   - Exit 4 — the goal is unroutable. Ask the printed questions, one per turn.
4. **Relay the path** with the hour budget, and flag that the hours are a planning heuristic to
   recalibrate after chapter one.
5. **Offer the study scaffolding**: `skills/deep-learning-book/assets/study_log_template.md` and
   `skills/deep-learning-book/assets/chapter_worksheet.md`, plus the retrieval-practice cadence from
   `skills/deep-learning-book/references/study_method_canon.md`.

## What to say about Part I

Most applied readers should skim Chapters 2–4 once for vocabulary, start at Chapter 5, and
return to a specific section when Chapter 8 needs it. Readers heading for Part III should work
Part I properly — those chapters compound, and so do the gaps.
`skills/deep-learning-book/references/prerequisite_map.md` has the dependency graph and the three strategies.
