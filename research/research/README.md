# research

**The runtime orchestrator for the research domain.** Hybrid router + fallback (Architecture C) — classifies any research request deterministically and either delegates to a specialist or runs its own plan-decompose-multi-source-search-synthesize-cite workflow.

## Distinct from `engineering/autoresearch-agent/`

These two skills share the word "research" but serve **completely different use cases**:

| Skill | Use case |
|---|---|
| **`research/research/`** (this skill) | "Research X" — a query router. Routes to specialist (pulse, grants, litreview, etc.) or runs own fallback workflow. |
| **`engineering/autoresearch-agent/`** | Karpathy's "autoresearch" — autonomous file-optimization experiment loop. "Make this code faster", "improve my prompts." File-optimization, not query routing. |

No overlap. They coexist.

## What this skill does

Every invocation produces one of three outcomes:

1. **Delegation** — classified as specialist-domain, routes there. User sees specialist's output.
2. **Fallback execution** — classified as general research. Runs own plan → search → synthesize workflow.
3. **Clarification request** — classification ambiguous. Asks one forcing question to disambiguate, then routes.

The skill **never silently runs its fallback** when a specialist would have done better. Routing transparency is the key trustability property.

## The 6 routing targets

| Specialist | Routes when question mentions | Domain |
|---|---|---|
| `pulse` | reddit / hn / x / buzz / sentiment / trending / "what's people saying" / "pulse on" / "take the pulse" | Multi-source recency research |
| `grants` | NIH / grant / R01 / K-award / RePORTER / NOSI / "grants for" | NIH grant-funding intelligence |
| `litreview` | literature review / PICO / SPIDER / systematic review / "review papers on" | Academic literature orientation |
| `syllabus` | syllabus attached / course outline / "reading list for my class" | Course supplementary reading |
| `patent` | prior art / FTO / freedom to operate / patent / invention novelty | Patent prior-art + landscape |
| `dossier` | "dossier on" / "due diligence" / "background check" / "competitor research" / "prep me for [meeting]" | Decision-grade entity research |

All 6 routing targets now exist in `research/` (post-cleanup PR #667).

## Source spec

[`megaprompts/13-research-megaprompt.md`](../../megaprompts/13-research-megaprompt.md) (PR #657).

## Plugin layout

```
research/research/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-research.md            ← router persona, routing-transparency enforcer
├── commands/cs-research.md          ← /cs:research <question>
└── skills/research/
    ├── SKILL.md
    ├── references/
    │   ├── hybrid_router_architecture.md         ← router-vs-run + routing transparency (7+ sources)
    │   ├── deterministic_classification_canon.md ← keyword > LLM for routing (7+ sources)
    │   └── fallback_workflow_canon.md            ← plan-decompose-search-synthesize (7+ sources)
    └── scripts/
        ├── classifier.py              ← stdlib: deterministic signal matching → routing decision
        ├── routing_transparency_logger.py  ← stdlib: JSON audit of routing decisions + overrides
        └── fallback_decomposer.py     ← stdlib: heuristic question → 3-5 sub-questions
```

## Dependencies

- **`WebSearch`** + **`WebFetch`** — Required for fallback workflow
- **Specialist skills** — Required for delegation (research/pulse, grants, litreview, syllabus, patent, dossier)
- **Node.js `docx` library** — Required if user picks document output (Q2 = standalone)
- **Consensus MCP** — Optional; used in fallback if academic sub-questions surface

## License

MIT.
