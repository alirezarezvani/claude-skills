---
disable-model-invocation: true
description: Lint UI source for unfinished work - controls that do nothing, dead links, placeholder copy, removed focus rings - and flag template defaults.
argument-hint: "<file or directory with UI source>"
---

# /cs-ui-finish-lint

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
