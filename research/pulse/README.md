# pulse

Multi-source recency research skill. Takes the pulse of any topic across Reddit, Hacker News, the open web, and (optionally) X/Twitter within a configurable recent window — synthesizing what people are saying *right now* into a single coherent briefing.

This is the **research-pack shape** anchor — its Agent Integrity Rules block transfers to `litreview`, `grants`, `syllabus`, `patent`, `dossier`, `notebooklm`, and `research` (the orchestrator).

## What it does

1. **Grill-me intake** — 2–4 forcing questions, one at a time: topic specificity, angle (trend/sentiment/problems/opportunities/comparison), time window (7d/14d/30d/60d/90d), platform scope.
2. **Parallel Phases 1–3** — Reddit + Hacker News + open web fire concurrently. 1 q/sec rate limit per platform; sequential calls within each platform.
3. **Optional Phase 4** — X/Twitter via Grok / X API / browser automation if available. Skipped with note otherwise.
4. **Synthesis** — cross-platform pattern detection: consensus, controversy, pain points, excitement, emerging trends, gaps.
5. **Output** — markdown file at `${RESEARCH_DIR}/pulse/<topic-slug>-<YYYY-MM-DD>.md` AND full briefing in chat.

The skill is **recency-oriented** — it captures the current conversation, not the canonical reference.

## Research-pack conventions (preserved verbatim per PR #657 audit)

- **Execution discipline:** Phases 1–3 run in parallel; sequential calls within each phase; 1 q/sec rate limit per platform.
- **Source discipline:** Cite only sources returned by this session's tool calls. Training knowledge labeled `[Background — not from search]` and excluded from primary findings count.
- **Three-count tracking:** Queries sent / sources received / sources cited. Surfaced in the audit log inline in the synthesis section.
- **Retry policy:** On failure → wait 3s → retry once → log. After 3 consecutive failures across all sources: stop, alert user, share what was collected.

## Source spec

[`megaprompts/01-pulse-megaprompt.md`](../../megaprompts/01-pulse-megaprompt.md) (PR #657). The megaprompt is canonical; this plugin is the working implementation. Drift between the two is a bug — re-grill with `/cs:grill-with-docs` if they diverge.

## Plugin layout

| File | Role |
|---|---|
| `skills/pulse/SKILL.md` | The skill itself (Claude reads this when triggered) |
| `skills/pulse/scripts/time_window_calculator.py` | Deterministic Unix-timestamp + Reddit `t=` parameter computation from window string |
| `skills/pulse/scripts/citation_tracker.py` | JSON-backed three-count audit log (sent / received / cited) |
| `skills/pulse/scripts/topic_slug_generator.py` | Filesystem-safe slug + duplicate-date detection for output paths |
| `skills/pulse/references/research_pack_conventions.md` | The Agent Integrity Rules canon (7+ sources) |
| `skills/pulse/references/cross_platform_synthesis.md` | Consensus/controversy/pain detection across platforms (7+ sources) |
| `skills/pulse/references/parallel_execution_discipline.md` | 1 q/sec rationale + plan-tier signals (7+ sources) |
| `agents/cs-pulse.md` | Pulse persona (forcing intake, three-count enforcer, graceful degradation) |
| `commands/cs-pulse.md` | `/cs:pulse <topic>` slash command for explicit invocation |

## Quick start

```bash
# Compute timestamps for a 30-day window
python skills/pulse/scripts/time_window_calculator.py --window 30d

# Start a citation tracker session
python skills/pulse/scripts/citation_tracker.py --action start --session pulse-2026-05-15-claude-code

# Generate the output-file slug for a topic
python skills/pulse/scripts/topic_slug_generator.py --topic "self-hosted LLM deployment" --date 2026-05-15
```

## License

MIT.
