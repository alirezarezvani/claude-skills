---
title: "/cs-notebooklm — Slash Command for AI Coding Agents"
description: "/cs:notebooklm — NotebookLM browser automation. Action-routing intake (Q1: read / add source / Studio output / create new) + per-action Q2-Q4. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-notebooklm

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/research/notebooklm/commands/cs-notebooklm.md">Source</a></span>
</div>


**Command:** `/cs:notebooklm`

The `cs-notebooklm` persona controls Google NotebookLM via browser automation across 4 core actions.

## Critical Prerequisite

**Requires browser automation environment.** Works in:

- Claude Code CLI with computer-use
- Claude Chrome Extension
- Playwright / Puppeteer with screenshot + click tools

Does NOT work in:

- Claude.ai web (no browser automation) — skill exits cleanly at Step 0

## When to Run

- Want to ask your existing NotebookLM notebook a question (Action 1)
- Want to add a source (URL / text / file / Google Doc / YouTube) to a notebook (Action 2)
- Want to generate a Studio output (Audio Overview / Infographic / Slides / Study Guide / etc.) (Action 3)
- Want to create a new notebook from scratch (Action 4)

## Action-Routing Intake (2-4 Forcing Questions)

| Q | Asks | Notes |
|---|---|---|
| Q1 | Action: read / add source / Studio output / create new | Forcing — refuses to start without commitment |
| Q2 | Notebook name or URL (actions 1-3) OR title for new notebook (action 4) | Drives navigation |
| Q3 | Action-specific parameter (question text / source type / Studio output type / initial sources) | Branches per Q1 |
| Q4 | Studio custom prompt detail | Asked only if Q1=3 (Studio); mandatory |

Most invocations stop at Q3. Q4 only fires for Studio generation.

## What You Get

Per action:

| Action | Result |
|---|---|
| Read/Extract | Clean response from notebook chat (not raw dump) |
| Add Sources | Confirmation of ingestion (with screenshot) |
| Studio Output | Confirmation that generation started + "NotebookLM will notify you when ready" — fire-and-notify |
| Create New | New notebook URL + confirmation of initial sources added |

## Studio Output Types

All 9 types supported:

- Audio Overview (5-10 min generation — fire-and-notify)
- Study Guide
- Briefing Doc
- Timeline
- FAQ
- Table of Contents
- Infographic
- Slides (slide deck)
- Mind Map

## Mandatory Custom Prompts

Default Studio prompts produce mediocre output. The skill ALWAYS opens the customization menu and writes a detailed custom prompt before submitting.

Examples per output type:

| Output | Example custom prompt |
|---|---|
| Audio Overview | "Two-host conversation for a non-technical executive, 8-10 min, focus on business implications not technical depth" |
| Infographic | "Decision-tree style, action-oriented, 6 panels max, monochrome navy" |
| Study Guide | "Undergrad-level, definitions + 3 practice questions per concept" |
| Slides | "12 slides max, 1-2 sentences per slide, presenter notes with examples per slide" |

## Discipline

- **Step 0 environment check** — verify browser automation; fail fast if not
- **Screenshot-first** — every UI action preceded by screenshot
- **find()-before-click** — semantic finders over pixel coordinates
- **Never auto-handle login** — detect login wall, stop, tell user to log in manually
- **Studio custom prompts always** — open customization menu, write detailed prompt
- **Fire-and-notify for slow ops** — Studio generation doesn't block this session
- **Tool-agnostic language** — "browser automation tool", not "Claude Chrome Extension"

## Trigger Phrases (auto-invoke without /cs:)

- "open NotebookLM"
- "check my [notebook name] notebook"
- "pull info from NotebookLM"
- "ask my notebook about X"
- "add [source] to NotebookLM"
- "create an infographic in NotebookLM"
- "use NotebookLM Studio"
- "generate a slide deck from my notebook"
- "what does my notebook say about X"
- Any variation involving NotebookLM

## Workflow

```bash
# Step 0: environment check (silent if available; halt if not)

# Phase 0 intake (Q1 + Q2 minimum; Q3-Q4 branch per action)
python ../skills/notebooklm/scripts/action_router.py \
  --action read_extract --notebook "Q3 prep" --question "what are the latest trends?"

# Studio output flow includes custom prompt generation:
python ../skills/notebooklm/scripts/custom_prompt_template_generator.py \
  --output-type infographic --audience executive --length compact

# Async classification (for "should I wait or fire-and-notify?")
python ../skills/notebooklm/scripts/async_action_classifier.py --action audio_overview
# Returns: FIRE_AND_NOTIFY (5-10 min generation)

# Execute action via browser automation (screenshot → find → click → verify)
# Return clean summary
```

## Stop Conditions

- Browser automation unavailable → halt at Step 0 with clear message
- Q1 action commitment refused → halt, re-ask
- Login wall detected → halt, ask user to log in manually
- Page layout changed unexpectedly → screenshot, ask user for guidance
- 3 consecutive UI find() failures → halt, alert user

## Anti-Patterns Rejected

- Tool-specific names without abstraction (e.g., hardcoding "Claude Chrome Extension")
- Synchronous waiting on Studio generations (especially Audio Overview)
- Skipping screenshots between actions
- Using pixel coordinates when semantic find() is available
- Attempting to handle login flows automatically
- Generating Studio outputs without opening customization menu
- Using default Studio prompts (always write custom)

## Related

- Agent: [`cs-notebooklm`](https://github.com/alirezarezvani/claude-skills/tree/main/research/notebooklm/agents/cs-notebooklm.md)
- Skill: [`notebooklm`](https://github.com/alirezarezvani/claude-skills/tree/main/research/notebooklm/skills/notebooklm/SKILL.md)
- Source spec: [`megaprompts/03-notebooklm-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/03-notebooklm-megaprompt.md)
- Research-domain siblings (different shape): `/cs:pulse`, `/cs:litreview`, `/cs:grants`, `/cs:dossier`, `/cs:patent`, `/cs:syllabus`

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/03-notebooklm-megaprompt.md`
