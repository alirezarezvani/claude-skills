---
title: "Handoff — Agent Skill for Codex & OpenClaw"
description: "Compact the current conversation into a handoff document for another agent to pick up. References existing artifacts (PRDs, plans, ADRs, issues. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Handoff

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `handoff`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/handoff/skills/handoff/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> Derived from [Matt Pocock's handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (MIT). Matt's no-duplication discipline preserved verbatim. Additions: tools + references + cs-* wrapper (see [references/companion_tooling.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/handoff/skills/handoff/references/companion_tooling.md)).

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to a path produced by `mktemp -t handoff-XXXXXX.md` (read the file before you write to it).

Suggest the skills to be used, if any, by the next session.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Sections

- **Goal of next session** (from user argument or inferred)
- **State of play** (what's done, what's blocking)
- **Open decisions** (what the next agent must decide)
- **Skills to use** (concrete list)
- **Artifacts** (paths/URLs to PRDs, plans, ADRs, issues, branches, PRs — do not duplicate)

## Tooling

See [references/companion_tooling.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/handoff/skills/handoff/references/companion_tooling.md). Tools: template + dedup + recommender. Agent: `cs-handoff-author`. Command: `/cs:handoff`.

---

**Version:** 1.0.0
**Derived:** Matt Pocock (MIT) + this repo's wrapper
