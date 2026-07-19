# litreview

Academic literature orientation skill. Turns a research question into a strategically planned mini literature review, delivered as a researcher-friendly Word document (`.docx`).

The output is a **launching pad** — not a finished review, but the orientation document that lets a researcher entering an unfamiliar field start reading and searching with confidence. Think: what a generous colleague who knows the field would tell you over coffee.

## What this skill does

1. **Phase 0 — Grill-me intake** (3 forcing questions): research question specificity + framework hint + tentative depth
2. **Phase 1 — Initial reconnaissance** (one broad search via the free lane — PubMed E-utilities + OpenAlex, keyless — to map themes, terminology, methodological distinctions; if the Consensus MCP is connected, additionally search there)
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
- Source: PubMed + OpenAlex, optionally Consensus (academic) vs Reddit/HN/Web (recency)
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
        ├── free_search.py              ← stdlib: free keyless search lane (PubMed E-utilities + OpenAlex via urllib)
        ├── citation_tracker.py         ← stdlib: JSON-backed three-count audit (sent/received/cited)
        ├── framework_recommender.py    ← stdlib: heuristic PICO/SPIDER/Decomp suggestion from Q1
        └── cross_search_aggregator.py  ← stdlib: repeat-hits + recurring-authors + citation-per-year
```

## Dependencies

- **Free keyless APIs** (default search lane, no key/account) — PubMed E-utilities (`eutils.ncbi.nlm.nih.gov`, ≤3 req/s keyless) + OpenAlex (`api.openalex.org`, polite pool via `mailto`)
- **Consensus MCP** (optional enhancement) — used only when connected in the session; one runtime check, no plan-tier detection
- **`docx` Node.js library** (required) — `npm install docx`
- **DOCX skill** (reference) — hyperlink / table / list / validation patterns
- **DOCX validation step** — zip-integrity check: `python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).testzip()" output.docx` (no output = intact), then confirm required sections present

## Quick start

```bash
# Free-lane search (keyless: PubMed + OpenAlex)
python skills/litreview/scripts/free_search.py --query "LLM clinical reasoning" --source both --max 10

# Track citations across the session
python skills/litreview/scripts/citation_tracker.py --action start --session litreview-2026-05-15

# Recommend a framework from a research question
python skills/litreview/scripts/framework_recommender.py --question "How do LLMs perform on clinical reasoning?"

# After all searches complete, aggregate cross-search intelligence
python skills/litreview/scripts/cross_search_aggregator.py --session litreview-2026-05-15
```

## License

MIT.
