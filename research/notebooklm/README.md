# notebooklm

Browser-automation skill for controlling Google's NotebookLM (https://notebooklm.google.com). The only **browser-automation shape** in the v2 collection — distinct from the research-pack convention.

## Critical Portability Notice

> **Requires:** A browser automation environment (Claude Code CLI with computer-use, Claude Chrome Extension, or equivalent). Skill will gracefully fail in non-automation contexts with a clear "not supported" message.

This skill cannot run in Claude.ai web (no browser automation). It detects environment at Step 0 and exits cleanly if unsupported.

## What this skill does

Four core actions controlled via the grill-me action-routing intake:

| Action | Q1 picks | UI flow |
|---|---|---|
| **Read/Extract** | 1 | Ask the notebook's chat a question, return clean response |
| **Add Sources** | 2 | Push URL / text / file / Google Doc / synthesized content into a notebook |
| **Generate Studio Outputs** | 3 | Audio Overview, Study Guide, Briefing Doc, Timeline, FAQ, Table of Contents, Infographic, Slides, Mind Map |
| **Create New Notebook** | 4 | Initialize with title + initial sources |

## Domain folder — research (semantic) vs shape difference

This skill lives in `research/` (with pulse/litreview/grants/dossier/patent/syllabus) because its **user-facing semantic domain** is research — users automate NotebookLM as part of their research workflow.

But the **technical shape** is completely different from the research-pack:
- No Consensus / Agent Integrity Rules
- No 1 q/sec rate limits (browser automation has different constraints)
- No DOCX generation (NotebookLM outputs come from NotebookLM itself)
- No three-count tracking
- Async discipline is fundamentally different (UI generation can take 5-10 min)

Users find it where they expect (research/), but it's the only research-domain skill with this shape.

## Source spec

[`megaprompts/03-notebooklm-megaprompt.md`](../../megaprompts/03-notebooklm-megaprompt.md) (PR #657).

## Plugin layout

```
research/notebooklm/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-notebooklm.md          ← browser-automation persona, async-discipline enforcer
├── commands/cs-notebooklm.md        ← /cs:notebooklm (or auto-triggers on phrases)
└── skills/notebooklm/
    ├── SKILL.md
    ├── references/
    │   ├── browser_automation_canon.md         ← screenshot-first / find-before-click (7+ sources)
    │   ├── studio_output_custom_prompts.md     ← why default prompts mediocre + per-type templates (7+ sources)
    │   └── async_action_discipline.md          ← fire-and-notify pattern for slow UI ops (7+ sources)
    └── scripts/
        ├── action_router.py                    ← stdlib: Q1-Q4 answers → action plan + UI flow
        ├── custom_prompt_template_generator.py ← stdlib: studio output type + audience → custom prompt starter
        └── async_action_classifier.py          ← stdlib: action → wait-or-notify-and-move-on
```

## Dependencies

- **Browser automation tool** — Required. Examples:
  - Claude Code CLI with computer-use
  - Claude Chrome Extension
  - Playwright / Puppeteer with screenshot + click tools
- **NotebookLM account** (Google) — User-provided, never auto-login

## License

MIT.
