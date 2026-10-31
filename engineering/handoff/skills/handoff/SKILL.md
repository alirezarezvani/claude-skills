---
name: handoff
description: "Compact the current conversation into a handoff document for another agent to pick up, referencing existing artifacts (PRDs, plans, ADRs, issues, commits, diffs) by path or URL instead of duplicating them. Use whenever the user wants to hand off to a fresh agent, is ending a session mid-task, asks for a handoff doc or a summary of state, decisions and next steps for the next session, or starts a new session that picks up prior work."
argument-hint: "What will the next session be used for?"
license: MIT
metadata:
  derived_from: "https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff"
  original_author: "Matt Pocock (@mattpocock)"
  original_license: MIT
  voice: "Matt Pocock — no-duplication, reference-existing-artifacts, tailored to next-session focus"
  version: 1.0.0
---

# Handoff

> Derived from [Matt Pocock's handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff) (MIT). Matt's no-duplication discipline preserved verbatim. Additions: tools + references + cs-* wrapper (see [references/companion_tooling.md](references/companion_tooling.md)).

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

See [references/companion_tooling.md](references/companion_tooling.md). Tools: template + dedup + recommender. Agent: `cs-handoff-author`. Command: `/cs-handoff`.

---

**Version:** 1.0.0
**Derived:** Matt Pocock (MIT) + this repo's wrapper

## More in this skill

Load these only when the task needs them.

- [references/deduplication_discipline.md](references/deduplication_discipline.md) — Deduplication Discipline for Handoffs
- [references/handoff_structure.md](references/handoff_structure.md) — Handoff Document Structure
- [references/next_session_skill_matching.md](references/next_session_skill_matching.md) — Skill Matching for the Next Session

- `python3 scripts/artifact_deduplicator.py --help` — Detect content in a handoff draft that should be referenced not duplicated
- `python3 scripts/handoff_template_generator.py --help` — Generate a handoff document scaffold tailored to next-session focus
- `python3 scripts/skill_recommender.py --help` — Recommend which skills the next session should use
