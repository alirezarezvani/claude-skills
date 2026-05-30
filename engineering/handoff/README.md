# handoff

Conversation-handoff document generator. Saves the current state of a conversation so a fresh agent can pick up the work cleanly.

## Attribution

**Derived from [Matt Pocock's handoff](https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff)** (MIT). Matt's no-duplication discipline preserved verbatim — handoff docs reference existing artifacts by path/URL, never duplicate them.

## What this adds on top of Matt's original

| Addition | Where | Why |
|---|---|---|
| **3 stdlib Python tools** | `skills/handoff/scripts/` | Template generator (tailored to next-session focus), artifact deduplicator (find references that should replace inline content), skill recommender (which skills next session needs) |
| **3 in-depth references** (5+ sources each) | `skills/handoff/references/` | Handoff structure · Deduplication discipline · Skill matching for next session |
| **cs-handoff-author persona agent** | `agents/cs-handoff-author.md` | Continuity-focused handoff author with hard rule against duplication |
| **`/cs:handoff` slash command** | `commands/cs-handoff.md` | One-shot handoff generation with argument hint |

## Matt's original (preserved)

> "Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to a path produced by `mktemp -t handoff-XXXXXX.md` (read the file before you write to it). Suggest the skills to be used, if any, by the next session. Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead. If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly."

## Quick start

```bash
# Generate a handoff template scaffold tailored to next-session focus
python skills/handoff/scripts/handoff_template_generator.py --next-focus "ship PR 2"

# Detect artifacts in a handoff draft that could be replaced by references
python skills/handoff/scripts/artifact_deduplicator.py path/to/draft-handoff.md

# Recommend skills for the next session based on handoff content
python skills/handoff/scripts/skill_recommender.py path/to/handoff.md
```

## License

MIT (matching Matt's upstream).
