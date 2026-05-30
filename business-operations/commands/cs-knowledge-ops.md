---
description: Company SOP + runbook authoring with 5W2H completeness checks. NOT personal PKM (that's llm-wiki). NOT engineering-specific runbooks. Direct invocation of the knowledge-ops skill.
argument-hint: "<process / system / incident to document>"
---

# /cs:knowledge-ops — Company SOPs + runbooks

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
