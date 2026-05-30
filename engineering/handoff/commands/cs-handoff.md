---
name: "cs-handoff"
description: "/cs:handoff <next-session-focus> — Compact the current conversation into a handoff document for a fresh agent. Tailored to next-session focus (deploy/review/debug/design/test). Replaces PRD/ADR/issue/commit content with references. Recommends specific skills for the next session."
argument-hint: "What will the next session be used for?"
---

# /cs:handoff — Session Handoff

**Command:** `/cs:handoff <next-session-focus>`

Hand off the current conversation to a fresh agent. Tailored to the focus argument.

## When to Run

- Ending a long session; want continuity
- Switching contexts mid-flight
- Handing work to another team/person/agent
- Starting a parallel session that needs current state

## The Five Sections (per Matt Pocock)

1. **Goal of next session** — outcome the next session must achieve (tailored to focus)
2. **State of play** — done / in-progress / blocking, with paths + refs
3. **Open decisions** — what the next agent must decide, with options + current leans
4. **Skills to use** — concrete list from `skill_recommender.py`
5. **Artifacts** — paths + URLs ONLY (never inline content)

## Hard Rule (Matt's)

> "Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead."

The `artifact_deduplicator.py` enforces this — FAIL verdict blocks the handoff.

## Workflow

```bash
# 1. Generate template tailored to focus
python ../skills/handoff/scripts/handoff_template_generator.py \
  --next-focus "<focus from command argument>" \
  --mktemp

# 2. Fill in the 5 sections from current conversation state

# 3. Pre-flight: dedup check
python ../skills/handoff/scripts/artifact_deduplicator.py path/to/draft.md
#   CLEAN or WARN (with justified findings) → proceed
#   FAIL → refactor; replace duplicated content with refs

# 4. Populate skills section
python ../skills/handoff/scripts/skill_recommender.py path/to/draft.md
#   Use top recommendations for "Skills to use"

# 5. Share the file path. Next agent reads + acts.
```

## Tailoring Logic

| Focus argument keyword | Section emphasis |
|---|---|
| ship/deploy/PR | Deployment commands, checks, approvers, rollback |
| review/audit | Checklist, sensitive files, similar patterns |
| debug/fix/investigate | Symptom, repro steps, tried-already |
| design/plan/scope | Outcome, constraints, rejected alternatives |
| test/qa | Test plan, existing coverage, edge cases |
| (other) | Immediate action, blocker, files, open decisions |

## Length Target

50-100 lines. Anything longer probably duplicates an artifact.

## Related

- Agent: [`cs-handoff-author`](../agents/cs-handoff-author.md)
- Skill: [`handoff`](../skills/handoff/SKILL.md)
- Adjacent: `/cs:caveman`, `/cs:grill-me`, `/cs:write-a-skill`

---

**Version:** 1.0.0
**Derived:** Matt Pocock's handoff (MIT) + this repo's wrapper
