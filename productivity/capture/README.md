# capture

Brain-dump organizer. Catches an unstructured stream of mixed thoughts, tasks, and ideas and transforms it into a clean four-section actionable system with zero information loss.

## What it does

When the user dumps (explicitly with phrases like "brain dump" / "let me get this out of my head", or implicitly by pasting a long unstructured block of mixed ideas), the skill:

1. Captures everything (zero loss; trivial items go in)
2. Asks at most ONE mid-organization clarifying question — only if a single item is genuinely ambiguous between task and project
3. Returns four sections:
   - **Projects & Ideas** — clustered themes with embedded questions/decisions
   - **Tasks** — flat scannable action list
   - **Connections** — real workspace links (Glob/Grep verified — never fabricated)
   - **How I Can Help** — concrete offers with `what + where`
4. Ends with a directive question: "Which of these should I tackle?"
5. Waits for the user's pick before any further action.

When the dump is small (≤5 items, unrelated), the skill drops into a compressed output instead of forcing 4 sections.

## Source spec

This skill is a Path-B direct conversion of [`megaprompts/05-capture-megaprompt.md`](../../megaprompts/05-capture-megaprompt.md) (PR #657). The megaprompt is the canonical spec; this plugin is the working implementation. Drift between the two is a bug — re-grill with `/cs:grill-with-docs` if they diverge.

## Plugin layout

| File | Role |
|---|---|
| `skills/capture/SKILL.md` | The skill itself (Claude reads this when triggered) |
| `skills/capture/scripts/workspace_inventory.py` | Glob+Grep helper for Section 3 — given a working dir + keyword list, returns a structured inventory of file matches + folder structure. Stdlib-only. |
| `skills/capture/scripts/dump_classifier.py` | Regex-classify dump lines into task / decision / question / project-component. Heuristic, not authoritative. |
| `skills/capture/scripts/complexity_estimator.py` | Count items in dump; recommend full 4-section vs compressed output format. |
| `skills/capture/references/workspace_detection.md` | Context-specific detection tactics (CLI / web / MCP / inaccessible) |
| `skills/capture/references/voice_preservation.md` | Concrete examples of corporate-speak anti-patterns |
| `skills/capture/references/complexity_matching.md` | When to compress vs full 4-section, with worked examples |
| `agents/cs-capture.md` | Capture-organizer persona (no-fabrication, voice-preservation enforcer) |
| `commands/cs-capture.md` | `/cs:capture <dump>` slash command for explicit invocation |

## Quick start

```bash
# Run the workspace-inventory helper against this repo
python skills/capture/scripts/workspace_inventory.py --root . --keywords "skill,megaprompt,capture"

# Classify a dump file
python skills/capture/scripts/dump_classifier.py path/to/dump.txt

# Estimate output complexity
python skills/capture/scripts/complexity_estimator.py path/to/dump.txt
```

## License

MIT.
