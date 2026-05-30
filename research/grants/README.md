# grants

NIH grant research skill for clinical researchers. Produces a strategic NIH funding overview as an editable `.docx`:

1. **Research positioning analysis** — 5-facet Consensus search producing gap quotes + draft Significance/Innovation language
2. **Institute mapping** — Which NIH institutes are actually funding this area (via RePORTER)
3. **Targeted grant discovery** — NOSIs, open FOAs, funded overlap filtered to mapped institutes
4. **Strategic recommendations** — Career-stage + project-scope mechanism matching, program officer guidance, submission timeline

## Sibling skill relationship

Part of the **research pack** (sibling of `pulse`, `litreview`; future siblings: `patent`, `dossier`, `syllabus`). All share the Agent Integrity Rules block (1 q/sec, source discipline, three-count tracking, retry-once-after-3s, stop-after-3-consecutive-failures).

**Different from `litreview`:**
- Adds **RePORTER POST** queries (not just Consensus) — NIH-specific funded-project data
- Adds **NOSI fetch** for `NOT-*` opportunity numbers
- DOCX has 9 sections (vs 8 in litreview) — adds Strategic Recommendations + Study Sections sections
- NIH-only scope; non-NIH funders out of scope

## Source spec

[`megaprompts/08-grants-megaprompt.md`](../../megaprompts/08-grants-megaprompt.md) (PR #657).

## Plugin layout

```
research/grants/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-grants.md             ← NIH-funding persona, RePORTER POST enforcer
├── commands/cs-grants.md           ← /cs:grants <research-idea>
└── skills/grants/
    ├── SKILL.md                    ← Path-B converted from megaprompt 08
    ├── references/
    │   ├── nih_mechanism_matching.md   ← career stage × scope → mechanism canon (7+ sources)
    │   ├── reporter_post_patterns.md   ← RePORTER curl POST templates + plan-tier (7+ sources)
    │   └── docx_9_sections.md          ← 9-section .docx spec + technical reqs (7+ sources)
    └── scripts/
        ├── citation_tracker.py         ← stdlib: Consensus + RePORTER three-count audit
        ├── fiscal_year_calculator.py   ← stdlib: current FY + 3-prior window (RePORTER-aware)
        └── mechanism_matcher.py        ← stdlib: career stage + scope + prelim → mechanism recommendation
```

## Dependencies

- **Consensus MCP** — Required for 5-facet positioning search
- **`bash_tool` + `curl`** — Required for RePORTER POST queries (NOT `web_fetch` — RePORTER is POST-only)
- **`web_fetch`** — Required for NOSI HTML pages
- **`docx` Node.js library** — Required for DOCX generation
- **DOCX skill** — Reference for hyperlink/table/list patterns

## License

MIT.
