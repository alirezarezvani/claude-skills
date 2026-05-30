# reflect

Mid-conversation reflection skill. Pauses execution and **zooms out from detail-mode** to honestly reassess direction, assumptions, and bias.

## What this skill does

When invoked mid-conversation (explicitly or via implicit signals like 10+ turns deep on details without strategic check-in), the skill:

1. **Halts the current thread** and re-reads the full conversation from the original goal forward — not just recent turns
2. Runs the **5-dimension analysis framework**:
   - **Macro Perspective** — original goal vs current direction; drift detection
   - **Gap Analysis** — unverified assumptions, missing stakeholders, skipped constraints, dismissed alternatives
   - **Reflective Inquiry** — is the problem framed correctly? Right problem vs adjacent easier one? Simpler path overcomplicated? Harder valuable path avoided?
   - **Bias Check** — confirmation / sunk cost / anchoring / complexity / recency
   - **Contextual Alignment** — does direction serve actual goals + best use of time + external factors honored
3. Delivers **flowing prose** (no headers, conversational tone)
4. Ends with a **clear directional recommendation**: Continue / Pivot / Pause

## Sibling skill relationship

Productivity sibling of `capture` (Slice 1). Both share light-prompt-flow shape, max-1-question intake, fast-to-action discipline. Different mode: `capture` organizes external dumps; `reflect` re-examines internal conversation state.

## Honest-output discipline

The skill explicitly does NOT manufacture problems when things are on track. "This is solid because X" is a valid output. **Vague reassurance ("looks good!") is rejected** — when the path is solid, the skill states specific reasoning for why; when the path needs correction, the skill states specific evidence from the conversation.

## Source spec

[`megaprompts/02-reflect-megaprompt.md`](../../megaprompts/02-reflect-megaprompt.md) (PR #657).

## Plugin layout

```
productivity/reflect/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-reflect.md             ← reflection persona, honest-output enforcer
├── commands/cs-reflect.md           ← /cs:reflect (or auto-triggers on phrases)
└── skills/reflect/
    ├── SKILL.md
    ├── references/
    │   ├── cognitive_bias_canon.md         ← 5 biases + recognition cues (7+ sources)
    │   ├── honest_output_discipline.md     ← anti-manufactured-problems (7+ sources)
    │   └── conversation_reflection_practice.md  ← Schön reflective practice canon (7+ sources)
    └── scripts/
        ├── bias_pattern_detector.py        ← stdlib: regex scan for 5-bias signals in conversation
        ├── conversation_depth_analyzer.py  ← stdlib: turn count + implicit-trigger signal detection
        └── directional_recommendation_validator.py  ← stdlib: verify output ends with Continue/Pivot/Pause
```

## Dependencies

**None.** Pure-reasoning skill — most portable in the v2 collection. Works in Claude Code CLI + Claude.ai web natively.

## License

MIT.
