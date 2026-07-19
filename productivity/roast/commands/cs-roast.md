---
name: "cs-roast"
description: "/cs:roast — Convene a 5-angle adversarial panel (Critic, Champion, Analyst, Investigator, Customer) on an idea, then a Judge delivers one GO / RESHAPE / KILL verdict with the cheapest 48-hour test to de-risk it. Pressure-test before you build."
argument-hint: "[the idea to roast]"
---

# /cs:roast — 5-Angle Idea Panel → One Verdict

**Command:** `/cs:roast [the idea]`

Claude's default is to agree with you. `/roast` is the opposite. It convenes five independent
reviewers who tear an idea apart and build it up from every angle, then acts as the Judge to deliver
one honest verdict. Run it before you sink time and money into building the wrong thing.

## When to Run

- "Roast / pressure-test / stress-test this idea"
- "Validate this business idea" / "convene the panel"
- "Give me a brutal second opinion before I build this"
- You want a real GO/KILL call — and you can take a "no."

## When NOT to Run

- You want encouragement or gentle brainstorming. This exists to tell you the idea is dead when it is.
- A cross-functional enterprise decision needing the full C-suite → use `/cs:boardroom`.
- A purely factual lookup with no decision attached.

## What You Get

1. **One shared brief** — assembled from idea / who / money / edge / constraints (`brief_builder.py`).
2. **Five reviewers in parallel**, each scoring their own dimension 1-10:
   - The Critic ("what kills this?"), The Champion ("the 10x upside?"), The Analyst ("does the logic
     hold?", no web), The Investigator ("what does the market say?", web), The Customer ("would I pay?").
3. **One verdict** — `GO / RESHAPE / KILL` + confidence, from the weighted synthesizer (not an average;
   demand/fatal-flaw/logic gates can veto a GO), with the real tension named and resolved.
4. **A money read** + **the cheapest 48-hour test** with explicit pass/fail signals.

## Trigger Phrases (auto-invoke without /cs:)

- "roast this idea" / "roast my idea"
- "pressure-test this" / "stress-test this idea"
- "validate this business idea" / "convene the panel"
- "brutal second opinion before I build"

## Discipline

- **Same brief to all five** — they must judge the same thing.
- **Parallel, not sequential** — five `Task` calls in one message so they think independently.
- **Never average** — run the synthesizer, resolve the tension.
- **Gates veto a GO** — no buyer, a landed fatal flaw, or broken logic caps the call below GO.
- **End on a falsifiable test** — name it, cost it, time-box it, state pass/fail.

## Workflow

```bash
# 1. Assemble the shared brief
python ../skills/roast/scripts/brief_builder.py \
  --idea "..." --who "..." --money "..." --edge "..." --constraints "..."

# 2. Fire all five reviewers in parallel (one Task each, subagent_type: general-purpose),
#    pasting the same brief into each. Collect five 1-10 scores.

# 3. Synthesize the call (weighting + veto gates + tension, NOT an average)
python ../skills/roast/scripts/verdict_synthesizer.py \
  --critic 4 --champion 8 --analyst 7 --investigator 5 --customer 6

# 4. Design the cheapest test from the riskiest assumption
python ../skills/roast/scripts/cheapest_test_designer.py --risk price --price 99
```

## Stop Conditions

- Verdict issued (GO/RESHAPE/KILL) + confidence + cheapest test → done.
- User brings new evidence → re-roast the changed dimension. Otherwise hold the call.
- User says "stop" → drop it.

## Related

- Agent: [`cs-roast-judge`](../agents/cs-roast-judge.md)
- Skill: [`roast`](../skills/roast/SKILL.md)
- Siblings: `/cs:andreessen` (single market-first lens), `/cs:boardroom` (enterprise C-suite)

---

**Version:** 1.0.0
