---
title: "/cs-capture — Slash Command for AI Coding Agents"
description: "/cs:capture <dump-text-or-path> — Explicit invocation of the brain-dump organizer. Captures an unstructured stream of thoughts/tasks/ideas and. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-capture

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/productivity/capture/commands/cs-capture.md">Source</a></span>
</div>


**Command:** `/cs:capture <dump-text-or-path>`

The `cs-capture` persona organizes a dump into 4 actionable sections with zero information loss.

## When to Run

- You have an unstructured block of mixed thoughts to organize
- You need workspace connections surfaced (Glob+Grep verified)
- You want concrete next-action offers, not generic "consider X" suggestions

The skill ALSO triggers automatically without `/cs:capture` when you:
- Use trigger phrases like "brain dump", "let me dump some ideas", "here's everything on my mind", "I need to organize my thoughts"
- Paste a long unstructured block of mixed ideas (implicit trigger)

`/cs:capture` is the explicit form — useful when your dump doesn't include the trigger phrasing but you still want the organize behavior.

## What You Get

**For a typical 8+ item dump (4-section format):**

```
## Projects & Ideas
{clustered themes with embedded questions/decisions}

## Tasks
{flat scannable action list}

## Connections
{real workspace links — Glob+Grep verified, never fabricated}

## How I Can Help
{concrete offers — what + where}

**Which of these should I tackle?**
```

**For a small dump (≤5 unrelated items, compressed format):**

```
## What I heard
- ...

## How I can help
- ...

Which should I tackle?
```

## Discipline

- **Capture everything** — zero loss; trivial items go in; user prunes later
- **Preserve voice** — no corporate-ifying; "build something crazy with AI" stays as that
- **Match output to input** — small dumps get compressed format, not forced 4 sections
- **No fabrication** — Section 3 only surfaces real workspace matches
- **No action without pick** — only auto-action is the organization itself
- **Max 1 clarifier per dump** — only when one item is genuinely ambiguous between task and project

## Workflow

```bash
# 1. (Optional) Pre-classify the dump as a heuristic seed
python ../skills/capture/scripts/dump_classifier.py path/to/dump.txt

# 2. (Optional) Recommend output format
python ../skills/capture/scripts/complexity_estimator.py path/to/dump.txt

# 3. Inventory the workspace for Section 3 candidates
python ../skills/capture/scripts/workspace_inventory.py \
  --root . --keywords "<extracted-keywords-from-dump>"

# 4. Persona organizes + delivers four (or compressed) sections.
# 5. Persona ends with "Which of these should I tackle?" and waits.
```

## Stop Conditions

- Four sections (or compressed) delivered → done with the auto-action portion
- User picks a Section-4 offer → execute that offer
- User says "go" without picking → honor it but flag any items you weren't sure about

## Anti-Patterns Rejected

- Fabricating workspace connections that weren't actually verified
- Dropping items deemed "trivial"
- Corporate-ifying the user's casual language
- Forcing 4-section structure when input is small
- Acting on Section-4 offers immediately without approval
- Splitting decisions/questions into separate top-level categories instead of embedding them
- Vague Section-4 offers ("you might want to consider…")

## Related

- Agent: [`cs-capture`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/capture/agents/cs-capture.md)
- Skill: [`capture`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/capture/skills/capture/SKILL.md)
- Source spec: [`megaprompts/05-capture-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/05-capture-megaprompt.md)
- Adjacent commands: `/cs:grill-me` (slow deliberate plan grill), `/cs:grill-with-docs` (docs-anchored grill), `/cs:handoff` (session continuation)

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/05-capture-megaprompt.md`
