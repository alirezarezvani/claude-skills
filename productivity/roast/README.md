# roast — 5-Angle Idea Panel → One Verdict

> Pressure-test a business idea before you build it. The opposite of Claude's default agreeableness.

`/roast` convenes a panel of five independent reviewers who attack an idea from every angle, then a
Judge synthesizes one honest **GO / RESHAPE / KILL** verdict with the cheapest 48-hour test to
de-risk it.

## The five seats

| Seat | The question it answers | Web? |
|---|---|---|
| **The Critic** | "What kills this?" — fatal flaws, fastest way it dies | no |
| **The Champion** | "What's the 10x upside?" — biggest case for it | no |
| **The Analyst** | "Does the logic actually hold?" — first principles | **forbidden** |
| **The Investigator** | "What does the real market say?" — evidence, competitors | **required** |
| **The Customer** | "Would I actually pay?" — first-person target buyer | no |

All five fire **in parallel** with the **same brief** so they judge independently. The Judge then
weights the scores (Customer + Critic heaviest, Champion lightest), applies veto gates (no buyer / a
landed fatal flaw / broken logic caps a GO), names the real tension, and resolves it.

## Quick start

```bash
# 1. Assemble the shared brief
python skills/roast/scripts/brief_builder.py --sample

# 2. (the skill fires the five reviewers in parallel as subagents)

# 3. Synthesize the call — NOT an average
python skills/roast/scripts/verdict_synthesizer.py --sample

# 4. Design the cheapest 48-hour test
python skills/roast/scripts/cheapest_test_designer.py --risk price --price 99
```

Or just say **"roast this idea: …"** or run `/cs:roast`.

## What's in the box

- **Skill:** [`skills/roast/SKILL.md`](skills/roast/SKILL.md)
- **Agent:** [`agents/cs-roast-judge.md`](agents/cs-roast-judge.md)
- **Command:** [`commands/cs-roast.md`](commands/cs-roast.md) — `/cs:roast`
- **3 stdlib tools:** `brief_builder.py`, `verdict_synthesizer.py`, `cheapest_test_designer.py`
- **3 references** (5-7 sources each), **2 assets** (brief worksheet + worked example)

## Not the same as

- **`productivity/andreessen`** — a single market-first operator. Roast is five lenses → a judge.
- **`c-level-advisor` `/cs:boardroom`** — an enterprise C-suite pipeline needing onboarding. Roast is
  a zero-setup, solo-founder gut check.
- **`engineering/grill-me`** — interrogates to clarify a plan; issues no verdict. Roast judges.

## License

MIT.
