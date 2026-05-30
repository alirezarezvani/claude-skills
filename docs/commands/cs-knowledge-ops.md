---
title: "/cs-knowledge-ops — Slash Command for AI Coding Agents"
description: "Company SOP + runbook authoring with 5W2H completeness checks. NOT personal PKM (that's llm-wiki). NOT engineering-specific runbooks. Direct. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-knowledge-ops

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/business-operations/commands/cs-knowledge-ops.md">Source</a></span>
</div>


Run the `knowledge-ops` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`sop_generator.py`** — Standard Operating Procedure with 5W2H scaffolding (Who/What/When/Where/Why/How/How-much). Industry tuning `--profile {ops,support,finance,hr,it,regulated}` for compliance-tier scaffolding.

2. **`runbook_validator.py`** — Runbook completeness check: every step has owner, expected duration, observable success/failure signal, rollback path. Flags ambiguity ("verify the service is up" → "what's the verification command?").

3. **`kb_ingester.py`** — Markdown KB ingestion: cross-link detection, glossary drift, orphan-page detection.

## Distinct from

- `engineering/llm-wiki` — personal PKM (your second brain). Knowledge-ops is the **company** wiki.
- `engineering-team/runbook-generator` — engineering-specific runbooks (system ops). Knowledge-ops is org-wide.
- `project-management/*` — Jira/Confluence delivery tracking, not authoring.
- `business-operations/skills/process-mapper` (sibling) — process *design*, not documentation.
