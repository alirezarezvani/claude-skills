---
title: "/cs-ui-finish-lint — Slash Command for AI Coding Agents"
description: "Lint UI source for unfinished work - controls that do nothing, dead links, placeholder copy, removed focus rings - and flag template defaults.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-ui-finish-lint

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/product-team/design-qa/commands/cs-ui-finish-lint.md">Source</a></span>
</div>


Lint `$ARGUMENTS` for unfinished work.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/design-qa/scripts/finish_lint.py <path>
```

## Report

1. The verdict line (CLEAN, FINDINGS or BLOCKED) and the generic-risk rating.
2. Blockers with file:line and the fix, one line each. Offer to fix them.
3. HIGH findings: say which ones may be wired elsewhere, and suppress those only with a reason.
4. Template traits as a short list. They are warnings, not defects: ask whether the brief wants them.

This checks source only. For contrast, focus and reflow in the real page, run `/cs-design-qa` with a URL.
