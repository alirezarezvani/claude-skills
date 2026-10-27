---
title: "/cs-access-diff — Slash Command for AI Coding Agents"
description: "Just the roster diff - find leavers with enabled accounts, logins after exit, orphaned and ownerless service accounts, unreviewed movers and inactive. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-access-diff

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/ra-qm-team/access-lifecycle/commands/cs-access-diff.md">Source</a></span>
</div>


Answer one question about `$ARGUMENTS`: **who has access the HR roster says they should not?**

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/access-lifecycle/scripts/access_diff.py --roster <roster.csv> --accounts <accounts.csv> \
  --inactive-days <policy> [--privileged-review-days <policy>] [--leaver-grace-days <policy>] [--as-of YYYY-MM-DD]
```

If no inactivity period was given, ask for the policy. PCI DSS 8.2.6 uses 90 days; that is not a default for everyone.

## What blocks (exit 4)

- A terminated person with an enabled account, or any login after the exit date.
- A privileged account matching nobody on the roster, or a privileged service account with no owner.

## What warns (exit 2)

- Standard orphans and ownerless service accounts, movers not reviewed since their role change,
  overdue privileged reviews, inactive accounts.

## Report

Verdict first, then blockers with account, person and action. Flag any login after exit as a security event
for whoever owns incident response. List data-quality warnings (duplicate IDs or emails) before the findings they affect.
