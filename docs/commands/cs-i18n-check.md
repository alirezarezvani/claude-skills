---
title: "/cs-i18n-check — Slash Command for AI Coding Agents"
description: "Check translation files and code before a release - missing keys, broken placeholders, CLDR plural forms, hardcoded UI strings.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-i18n-check

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/i18n-localization/commands/cs-i18n-check.md">Source</a></span>
</div>


Check translation files and UI code before a release: `$ARGUMENTS` (default: the project's locales folder and `src/`).

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/locale_sync.py <locales dir> --source-locale <source>
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/hardcoded_strings.py <source dir>
```

## Report

1. The verdict line of each script.
2. Blockers grouped by locale, with file and key, and the fix for each (add the plural keys, restore the placeholder, use `=0`).
3. Hardcoded strings you checked and confirm are user-facing, with file:line. Name any you judged false positives.
4. Warnings, briefly. Do not fill missing translations with English or machine output; list them for a translator.
