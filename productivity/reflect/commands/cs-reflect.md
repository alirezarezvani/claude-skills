---
name: "cs-reflect"
description: "/cs:reflect — Mid-conversation reflection: halts current thread, re-reads full conversation from original goal forward, runs 5-dimension analysis (Macro / Gap / Reflective / Bias / Contextual), ends with Continue / Pivot / Pause recommendation. Flowing prose, no headers. Honest output — no manufactured problems."
---

# /cs:reflect — Mid-Conversation Reassessment

**Command:** `/cs:reflect`

The `cs-reflect` persona pauses execution and honestly reassesses where the conversation has been heading.

## When to Run

- Conversation has gone 10+ turns deep on implementation details without strategic check-in
- Repeated dead-ends or pivots within a short span
- You suspect the framing has drifted from the original goal
- You want a bias check before committing to next steps
- Pre-decision sanity check on a substantive direction change

## When NOT to Run

- Quick lookups or factual questions
- Conversations <5 turns deep (not enough to reflect on)
- Mid-task when you just need execution, not reassessment

## What You Get

A flowing-prose reassessment covering:

1. **Macro Perspective** — original goal vs current direction; drift detection
2. **Gap Analysis** — unverified assumptions, missing stakeholders, skipped constraints, dismissed alternatives
3. **Reflective Inquiry** — right problem vs adjacent easier one? Simpler path overcomplicated? Harder valuable path avoided?
4. **Bias Check** — confirmation / sunk cost / anchoring / complexity / recency
5. **Contextual Alignment** — does direction serve goals + best use of time

Closing with **one of three recommendations**:

- **Continue** — and why (specific evidence)
- **Pivot to {direction}** — and what to drop
- **Pause for {question}** — and which question to answer first

## Trigger Phrases (auto-invoke without /cs:)

**Explicit:**
- "reflect"
- "take a step back" / "step back"
- "zoom out"
- "are we missing something"
- "bigger picture"
- "what are we missing"
- "let's pause"
- "sanity check this"
- "are we on track"
- "are we overthinking this"
- "forest for the trees"

**Implicit (no phrase needed):**
- 10+ turns of implementation detail without strategic check-in
- User shows signs of frustration or stuck-ness
- Repeated dead-ends or pivots within a short span

## Discipline

- **Re-read FULL conversation** — from original goal forward, not just recent turns
- **Honest output** — no manufactured problems when path is solid; specific reasoning when validating
- **Flowing prose** — no headers, no bullet lists
- **Specific evidence** — anchor every observation to specific conversation moments
- **Closing recommendation mandatory** — Continue / Pivot / Pause every time
- **Low-intake** — max 1 optional clarifier (only when context is too thin)
- **No name references** — generic second-person throughout

## Workflow

```bash
# When triggered, the skill:
# 1. Halts current thread (no continuation of the in-progress task)
# 2. Re-reads full conversation from original goal
# 3. Runs 5-dimension analysis in head
# 4. Delivers flowing-prose reassessment

# Optional pre-flight: scan for bias patterns + depth signals
python ../skills/reflect/scripts/conversation_depth_analyzer.py --conversation /tmp/transcript.txt
python ../skills/reflect/scripts/bias_pattern_detector.py --conversation /tmp/transcript.txt

# Post-flight: validate output meets discipline
python ../skills/reflect/scripts/directional_recommendation_validator.py --output /tmp/output.txt
```

## Stop Conditions

- Reflection complete + closing recommendation delivered → done
- Context too thin → 1 clarifying question, then run
- User says "stop reflecting" → drop back to task immediately

## Anti-Patterns Rejected

- Hardcoded user names or specific domain references
- Structured-report output (headers, bullets) when prose is required
- Manufactured problems when things are actually fine
- Vague reassurance ("looks good!") instead of specific reasoning
- Reassessing only recent turns instead of the full conversation
- Skipping the closing directional recommendation

## Related

- Agent: [`cs-reflect`](../agents/cs-reflect.md)
- Skill: [`reflect`](../skills/reflect/SKILL.md)
- Source spec: [`megaprompts/02-reflect-megaprompt.md`](../../../megaprompts/02-reflect-megaprompt.md)
- Sibling: `/cs:capture` (productivity, brain-dump organizer)
- Adjacent (different shape): `/cs:grill-me`, `/cs:grill-with-docs`

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/02-reflect-megaprompt.md`
