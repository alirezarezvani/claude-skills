# litreview

Academic literature orientation skill. Turns a research question into a strategically planned mini literature review, delivered as a researcher-friendly Word document (`.docx`).

The output is a **launching pad** — not a finished review, but the orientation document that lets a researcher entering an unfamiliar field start reading and searching with confidence. Think: what a generous colleague who knows the field would tell you over coffee.

## What this skill does

1. **Phase 0 — Grill-me intake** (3 forcing questions): research question specificity + framework hint + tentative depth
2. **Phase 1 — Initial reconnaissance** (one broad Consensus search to map themes, terminology, methodological distinctions)
3. **Phase 2 — Framework + sub-areas** (PICO default; SPIDER / Decomposition / hybrid fallbacks)
4. **Interactive checkpoint** — show framework breakdown table + sub-areas + depth-selector; wait for user confirmation before consuming search budget
5. **Phase 3 — Targeted searches** (sequential, 1 q/sec, budget-allocated by depth tier)
6. **Phase 4 — DOCX research guide** (8 sections: Topic Overview, Start Here, How the Field Got Here, Sub-area Guides, Key Research Groups, Open Questions, Bibliography, Audit Log)

## Sibling skill relationship

`litreview` is part of the **research pack** (sibling of `pulse`, future siblings: `grants`, `patent`, `dossier`, `syllabus`). All share:

- The Agent Integrity Rules block (1 q/sec rate limit, source discipline, three-count tracking, retry-once-after-3s, stop-after-3-consecutive-failures)
- The grill-me intake discipline
- The hard rule: cite only what the search tool returned this session

Different from `pulse`:
- Source: Consensus (academic) vs Reddit/HN/Web (recency)
- Output: 8-section DOCX vs multi-platform briefing
- Discipline: sequential within single source vs parallel across sources

## Source spec

[`megaprompts/09-litreview-megaprompt.md`](../../megaprompts/09-litreview-megaprompt.md) (PR #657). Canonical. Drift = bug.

## Plugin layout

```
research/litreview/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-litreview.md             ← academic-research persona, checkpoint enforcer
├── commands/cs-litreview.md           ← /cs:litreview <research-question>
└── skills/litreview/
    ├── SKILL.md                        ← Path-B converted from megaprompt 09
    ├── references/
    │   ├── framework_selection.md      ← PICO / SPIDER / Decomposition canon (7+ sources)
    │   ├── search_budget_allocation.md ← 5/10/20 depth tiers + cross-search intelligence (7+ sources)
    │   └── docx_8_sections.md          ← Research guide DOCX spec + technical requirements (7+ sources)
    └── scripts/
        ├── citation_tracker.py         ← stdlib: JSON-backed three-count audit (sent/received/cited)
        ├── framework_recommender.py    ← stdlib: heuristic PICO/SPIDER/Decomp suggestion from Q1
        └── cross_search_aggregator.py  ← stdlib: repeat-hits + recurring-authors + citation-per-year
```

## Dependencies

- **Consensus MCP** (required) — literature search
- **`docx` Node.js library** (required) — `npm install docx`
- **DOCX skill** (reference) — hyperlink / table / list / validation patterns
- **DOCX validation script** — `python scripts/office/validate.py output.docx`

## Quick start

```bash
# Track citations across the session
python skills/litreview/scripts/citation_tracker.py --action start --session litreview-2026-05-15

# Recommend a framework from a research question
python skills/litreview/scripts/framework_recommender.py --question "How do LLMs perform on clinical reasoning?"

# After all searches complete, aggregate cross-search intelligence
python skills/litreview/scripts/cross_search_aggregator.py --session litreview-2026-05-15
```

## License

MIT.
