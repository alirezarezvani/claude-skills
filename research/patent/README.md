# patent

Patent prior-art and landscape intelligence skill. Refuses to be "generic patent help" — every invocation commits to **one of five sub-use-cases** before any search runs, and the chosen sub-use-case dictates the entire search strategy, ranking heuristics, and DOCX emphasis.

## The 5 Sub-Use-Cases

| Sub-use-case | Search strategy | DOCX emphasis |
|---|---|---|
| **Novelty search** (am I novel) | Narrow + claims-text focused | Closest art + claim-differentiation |
| **Freedom-to-operate** (will I get sued) | Broad + active patents only; jurisdiction-filtered | FTO flags + claim-by-claim risk |
| **Competitive landscape** (who plays here) | Breadth + filer tally + CPC trends | Filer map + investment hotspots |
| **Acquisition diligence** (does target really own X) | Specific assignee + portfolio scope + assignment chain | Portfolio table + ownership verification |
| **Litigation prior-art** (kill a specific patent) | Target patent + adjacent art before priority date | Knock-out candidates ranked by relevance |

**Out of scope:** trademark, copyright, trade-secret. Flagged at intake.

## Sibling skill relationship

Part of the **research pack** (sibling of `pulse`, `litreview`, `grants`, `dossier`). Shares Agent Integrity Rules. Adds:

- **Sub-use-case routing** as a non-skippable Q2 commitment (refuses generic "patent help")
- **CPC/IPC class follow-up** queries (catches art keyword search misses)
- **Family resolution** (deduplicates same-invention filings across jurisdictions)
- **Date discipline** (filing vs priority vs publication vs grant — surfaces legally-relevant date per sub-use-case)
- **Mandatory legal disclaimer** for novelty + FTO sub-use-cases

## Source spec

[`megaprompts/11-patent-megaprompt.md`](../../megaprompts/11-patent-megaprompt.md) (PR #657).

## Plugin layout

```
research/patent/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-patent.md
├── commands/cs-patent.md
└── skills/patent/
    ├── SKILL.md
    ├── references/
    │   ├── sub_use_case_routing.md         ← 5-sub-use-case canon (7+ sources)
    │   ├── cpc_classification_canon.md     ← CPC/IPC class follow-up rationale (7+ sources)
    │   └── legal_disclaimer_discipline.md  ← when + why mandatory (7+ sources)
    └── scripts/
        ├── citation_tracker.py             ← multi-source three-count (Google Patents + Espacenet + USPTO + Lens.org)
        ├── family_resolver.py              ← deduplicates same-invention across jurisdictions
        └── sub_use_case_router.py          ← deterministic search-strategy selection from intake answers
```

## Dependencies

- **`web_fetch`** — Required (Google Patents, Espacenet, USPTO)
- **`WebSearch`** — Required (academic prior art adjacent to patents)
- **`bash_tool` + `curl`** — Required for Lens.org if BYOK key
- **Node.js `docx` library** — Required
- **Lens.org API key** — Optional, BYOK; enables citation-graph section

## License

MIT.
