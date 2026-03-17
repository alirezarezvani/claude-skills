---
title: "Content Creator → Redirected — Agent Skill for Marketing"
description: "Deprecated redirect skill that routes legacy 'content creator' requests to the correct specialist. Use when a user invokes 'content creator', asks to. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Content Creator → Redirected

<div class="page-meta" markdown>
<span class="meta-badge">:material-bullhorn-outline: Marketing</span>
<span class="meta-badge">:material-identifier: `content-creator`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/content-creator/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install marketing-skills</code>
</div>


> **This skill has been split into two specialist skills.** Use the one that matches your intent:

| You want to... | Use this instead |
|----------------|-----------------|
| **Write** a blog post, article, or guide | [content-production](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/content-production) |
| **Plan** what content to create, topic clusters, calendar | [content-strategy](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/content-strategy) |
| **Analyze brand voice** | [content-production](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/content-production) (includes `brand_voice_analyzer.py`) |
| **Optimize SEO** for existing content | [content-production](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/content-production) (includes `seo_optimizer.py`) |
| **Create social media content** | [social-content](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/social-content) |

## Why the Change

The original `content-creator` tried to do everything: planning, writing, SEO, social, brand voice. That made it a jack of all trades. The specialist skills do each job better:

- **content-production** — Full pipeline: research → brief → draft → optimize → publish. Includes all Python tools from the original content-creator.
- **content-strategy** — Strategic planning: topic clusters, keyword research, content calendars, prioritization frameworks.

## Proactive Triggers

- **User asks "content creator"** → Route to content-production (most likely intent is writing).
- **User asks "content plan" or "what should I write"** → Route to content-strategy.

## Output Artifacts

| When you ask for... | Routed to... |
|---------------------|-------------|
| "Write a blog post" | content-production |
| "Content calendar" | content-strategy |
| "Brand voice analysis" | content-production (`brand_voice_analyzer.py`) |
| "SEO optimization" | content-production (`seo_optimizer.py`) |

## Communication

This is a redirect skill. Route the user to the correct specialist — don't attempt to handle the request here.

## Related Skills

- **content-production**: Full content execution pipeline (successor).
- **content-strategy**: Content planning and topic selection (successor).
- **content-humanizer**: Post-processing AI content to sound authentic.
- **marketing-context**: Foundation context that both successors read.
