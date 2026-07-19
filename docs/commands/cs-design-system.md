---
title: "/cs-design-system — Slash Command for AI Coding Agents"
description: "Run the one-time markdown-html design-system onboarding wizard. Captures brand primary/accent (HEX) + heading/body Google Fonts + design style. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-design-system

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/markdown-html/commands/cs-design-system.md">Source</a></span>
</div>


Run the design-system wizard:

```bash
python3 markdown-html/skills/design-system/scripts/onboard.py $ARGUMENTS
```

## Modes

| Flag | Behavior |
|---|---|
| (no flag) | Interactive — walks 10 questions one at a time. Default. |
| `--defaults` | Zero-touch: writes built-in defaults (`#0A1628` navy + `#00D4AA` teal + Inter + technical + sticky TOC + `./markdown-html-out/`) without prompting. Useful for CI or first-test. |
| `--set key=value` | Non-interactive override (repeatable). Dotted keys supported: `brand.primary=#FF6B35`, `typography.heading_font=Lora`, `design_style=editorial`. |
| `--show` | Print the 10 questions + the current effective config (project > global > defaults). |
| `--reset` | Delete the saved config at the chosen scope. |
| `--scope project` | Save to `./.markdown-html/design-system.json` (per-repo override) instead of global `~/.config/markdown-html/design-system.json`. |

## The 10 questions

1. Default output directory (path; must be writable)
2. Brand primary HEX
3. Brand accent HEX (optional; auto-derives if blank)
4. Heading Google Font (12 safe defaults)
5. Body Google Font
6. Design style: editorial / technical / minimal / playful
7. Syntax-highlighting theme: light / dark / auto
8. TOC behavior: sticky-sidebar / collapsible-top / inline / none
9. Company / project name (optional, shows in footer)
10. Logo URL (optional, base64-embedded at render time)

## Hard refusals

- `default_output_dir` empty or unwritable → exit 3. Pick a path you control.
- WCAG AA body-text contrast fails (< 4.5:1) → exit 4. Pick a darker primary, blank `brand.bg`/`brand.text` to let derivation pick a passing pair, or override `brand.text` explicitly.
- WCAG link contrast walked iteratively; falls back to a passing color if accent on bg can't reach 4.5:1.

## After onboarding

Inspect the effective config:

```bash
python3 markdown-html/skills/design-system/scripts/config_loader.py --show
python3 markdown-html/skills/design-system/scripts/config_loader.py --status
```

Then convert markdown via `/cs:markdown-html <path>.md`.

## Bypass

`MARKDOWN_HTML_NO_CONFIG=1` skips saved config and returns DEFAULTS only. Useful for headless CI, ephemeral test containers, and evaluator loops. Never set it silently for an interactive user.
