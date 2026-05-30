# syllabus

Course supplementary reading list generator. Takes any course syllabus (PDF / DOCX / text / image) and produces a curated `.docx` of recent peer-reviewed papers via Consensus search, with plain-language summaries calibrated to audience level + Bloom-higher-order discussion questions tied to learning outcomes.

## What this skill does

1. **Phase 0 grill-me** (3 forcing Qs): syllabus input format + course audience + year range
2. **Phase 1**: parse syllabus (PDF/DOCX/text/image) → extract topics + learning outcomes
3. **Phase 2**: group topics into 6-12 sections + grill-me forcing checkpoint (proceed/merge/split/add/remove)
4. **Phase 3**: targeted Consensus searches per section (1-2 queries each, sequential at 1 q/sec, **applied-domain weaving**)
5. **Phase 4**: write summaries (audience-calibrated jargon) + discussion questions (Bloom higher-order)
6. **Phase 5**: generate .docx via **bundled JS script** (`scripts/generate_reading_list.js`)
7. **Phase 6**: deliver file + audit summary

## Architectural pattern: bundled JS

This skill uses a **bundled JavaScript helper script** (`scripts/generate_reading_list.js`) for DOCX generation rather than inlining the 300+ lines of layout code in SKILL.md. Rationale:

- DOCX generation logic is reusable + complex
- Better separation of concerns: skill = orchestration + intelligence; script = mechanical document assembly
- Token-efficient: skill doesn't re-derive layout each run
- Easier to maintain and version

The skill orchestrates the pipeline and invokes the script with JSON input.

## Sibling skill relationship

Part of the **research pack** (sibling of `pulse`, `litreview`, `grants`, `patent`, `dossier`). Shares Agent Integrity Rules. Adds:

- **Audience calibration** — undergrad summaries define every term; grad summaries assume technical fluency
- **Applied-domain weaving** — search "X applications" not just "X" (boosts relevance dramatically)
- **Bundled JS script pattern** — first research-pack skill to use this layout

## Source spec

[`megaprompts/10-syllabus-megaprompt.md`](../../megaprompts/10-syllabus-megaprompt.md) (PR #657).

## Plugin layout

```
research/syllabus/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-syllabus.md
├── commands/cs-syllabus.md
└── skills/syllabus/
    ├── SKILL.md
    ├── references/
    │   ├── applied_domain_weaving.md       ← search-quality canon (7+ sources)
    │   ├── audience_calibration.md         ← undergrad vs grad summary jargon (7+ sources)
    │   └── bundled_script_pattern.md       ← why bundle vs inline (7+ sources)
    └── scripts/
        ├── citation_tracker.py             ← stdlib: Consensus three-count + 1s sequential
        ├── topic_grouper.py                ← stdlib: heuristic 6-12 section grouping
        ├── discussion_question_validator.py ← stdlib: Bloom higher-order quality check
        └── generate_reading_list.js        ← bundled Node.js: DOCX assembly (~300 lines)
```

## Dependencies

- **Consensus MCP** — Required for literature search
- **Node.js with `docx` package** — Required (`npm install docx`)
- **Bundled script** — `scripts/generate_reading_list.js` (shipped with skill, not external)
- **File reading** — PDF reader / DOCX parser via pandoc / vision for images

## License

MIT.
