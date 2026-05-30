# dossier

Decision-grade entity research. Produces a **hypothesis-tested dossier** on a specific company, person, nonprofit, or government org — built around hypothesis-testing rather than encyclopedic summary.

## Non-generic by design

The skill refuses to be "tell me about Microsoft". Every invocation forces the user to expose their hypothesis upfront (Q4 — **mandatory**), so the dossier **tests** it rather than confirms it.

| ❌ Generic ask | ✅ Decision-grade ask |
|---|---|
| "Tell me about Microsoft." | "I'm pitching Microsoft Tuesday. My hypothesis is they're consolidating AI spend on Foundry. Validate or disprove, and give me 3 conversation hooks tied to what you find." |

The forcing Q4 is the non-generic anchor. Without it, the skill produces a Wikipedia summary.

## Sibling skill relationship

Part of the **research pack** (sibling of `pulse`, `litreview`, `grants`). Shares Agent Integrity Rules (1 q/sec, source discipline, three-count tracking, retry-once-after-3s, stop-after-3-consecutive-failures).

**Different from siblings:**
- **Hypothesis-testing discipline** — ≥30% of search budget allocated to **disconfirming** evidence
- **Source-tier discipline** — every flag tagged primary / secondary / tertiary
- **Subject-type routing** — different source matrix for person / company / nonprofit / gov
- **Verdict** in Executive Summary: SUPPORTED / PARTIALLY SUPPORTED / DISPROVEN / INCONCLUSIVE
- Uses WebSearch + WebFetch + free APIs (not Consensus)

## Source spec

[`megaprompts/12-dossier-megaprompt.md`](../../megaprompts/12-dossier-megaprompt.md) (PR #657).

## Plugin layout

```
research/dossier/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-dossier.md             ← hypothesis-testing persona; Q4 enforcer
├── commands/cs-dossier.md           ← /cs:dossier <entity>
└── skills/dossier/
    ├── SKILL.md
    ├── references/
    │   ├── hypothesis_testing_discipline.md   ← why disconfirming; ≥30% rule (7+ sources)
    │   ├── subject_type_source_matrix.md      ← person/company/nonprofit/gov sources (7+ sources)
    │   └── conversation_hook_quality.md       ← finding-tied vs generic (7+ sources)
    └── scripts/
        ├── citation_tracker.py                ← supporting/disconfirming + source-tier counts
        ├── disconfirming_evidence_balance.py  ← enforces ≥30% disconfirming queries
        └── source_tier_classifier.py          ← URL → primary/secondary/tertiary
```

## Dependencies

- **`WebSearch`** + **`WebFetch`** — required (news, public web)
- **`bash_tool` + `curl`** — required for free APIs (SEC EDGAR, GitHub, ProPublica)
- **Node.js `docx` library** — required for DOCX generation
- **Optional BYOK MCPs** — LinkedIn, Crunchbase, Apollo, Pitchbook, SimilarWeb (surfaced in audit log when used)

## License

MIT.
