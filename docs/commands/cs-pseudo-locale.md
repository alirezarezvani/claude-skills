---
title: "/cs-pseudo-locale — Slash Command for AI Coding Agents"
description: "Generate an en-XA (or ar-XB right-to-left) pseudo-locale from the source strings to find hardcoded text, truncation and concatenation in the running. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-pseudo-locale

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/i18n-localization/commands/cs-pseudo-locale.md">Source</a></span>
</div>


Generate a pseudo-locale from the source locale file in `$ARGUMENTS` and register it for development builds.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/pseudo_localize.py <source file> -o <locales>/en-XA/<name>
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/pseudo_localize.py <source file> --bidi -o <locales>/ar-XB/<name>   # RTL
```

Register the pseudo-locale in the i18n config for development builds only, then tell the user what to look for:

- plain, unaccented English: a hardcoded string
- `[[...` with no closing `]]`: truncated text
- two `[[ ]]` pairs in one label: runtime concatenation
- broken layout in `ar-XB`: left/right CSS instead of logical properties
