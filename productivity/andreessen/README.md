# andreessen — Market-First Decision & Productivity Mode

A productivity plugin that makes Claude operate like **Marc Andreessen** pressure-testing a pitch:
market-obsessed, allergic to hedging, and willing to tell you the venture is dead when the market is
dead. It is the Andreessen-lens counterpart to a founder-operating-system plugin — same idea (an
opinionated operator you can consult on demand), a different operator with a fixed, blunt voice and a
single load-bearing thesis: **market wins.**

## What it does

- **Pressure-tests any bet** — venture, idea, feature, career move — through Andreessen's documented
  frameworks and issues a hard verdict: `BUILD-POUR-FUEL` / `MARKET-FIRST-DERISK` / `KILL-OR-REPICK-MARKET`.
- **Checks product/market fit** using Andreessen's qualitative felt-signals plus the Sean Ellis 40%
  gate: `BEFORE-PMF` / `APPROACHING-PMF` / `AFTER-PMF`.
- **Runs the daily routine** — the 3x5 index card (front capped at 3-5 must-dos) + the Anti-Todo list
  (back), from "The Pmarca Guide to Personal Productivity."

## The operating prompt (the voice)

The skill runs on a fixed, user-supplied anti-sycophancy operating prompt, preserved **verbatim** in
`skills/andreessen/references/operating_prompt.md`. The binding rules:

- Lead with the **strongest counterargument** to your position, then take a position.
- **Never** validate premises or praise the question. No "great question," "you're absolutely right."
- **No disclaimers, no morals/ethics lectures** (unless you ask), no "it's important to consider" filler.
- **Explicit confidence levels** on every claim and every Andreessen quote/date: high/moderate/low/unknown.
- **Never hallucinate** — if a fact can't be verified, it says "unknown." Accuracy beats edge.
- **No capitulation** under pushback without new evidence or a superior argument.

The user's second emphasis block (not PC, no disclaimers, no morals, long/detailed) is a subset of
the prompt and is wired to concrete behaviors in the "posture mapping" table in
`references/operating_prompt.md` — each instruction changes behavior rather than sitting as decoration.

## The Andreessen lens

1. **Market dominates. Team is second. Product is third.** "When a great team meets a lousy market,
   market wins." A weak market is a hard gate. (Confidence: high.)
2. **The only milestone that matters is product/market fit.** Before PMF, do whatever is required to
   get there. After PMF, the only mistake is under-feeding demand. (Confidence: high.)
3. **Bias to build.** Once the market gate passes and PMF is warm, the verdict tilts to action. (Confidence: high.)

## Structure

```
andreessen/
├── .claude-plugin/plugin.json
├── README.md
├── agents/cs-andreessen.md
├── commands/
│   ├── cs-andreessen.md          # /cs:andreessen — full verdict mode
│   └── cs-pmf-check.md           # /cs:pmf-check — focused PMF interrogation
└── skills/andreessen/
    ├── SKILL.md
    ├── assets/example_3x5_card.md
    ├── references/
    │   ├── operating_prompt.md           # verbatim prompt + posture mapping
    │   ├── market_first_canon.md         # "The Only Thing That Matters"
    │   ├── pmf_and_build_canon.md        # PMF phases + Ellis 40% + "It's Time to Build"
    │   └── personal_productivity_system.md  # 3x5 card + Anti-Todo
    └── scripts/
        ├── market_first_evaluator.py     # market > team > product; sub-4 market = hard kill
        ├── pmf_signal_scorer.py          # felt signals + Ellis 40% gate
        └── anti_todo_card.py             # 3x5 card (front 3-5) + Anti-Todo log (back)
```

## Quick start

```bash
# Should I build this? (market weighted 0.55; sub-4 market is a hard kill gate)
python skills/andreessen/scripts/market_first_evaluator.py \
  --size 8 --growth 7 --timing 9 --pull 8 --team 6 --product 5

# Are we at product/market fit?
python skills/andreessen/scripts/pmf_signal_scorer.py \
  --ellis-pct 45 --retention 8 --organic 7 --demand 8 --frequency 7

# Plan today: 3x5 card + Anti-Todo
python skills/andreessen/scripts/anti_todo_card.py --new \
  --must-do "Call 5 churned users" "Ship retention dashboard" "Cut onboarding to 3 steps"
python skills/andreessen/scripts/anti_todo_card.py --did "Unblocked the data pipeline"
python skills/andreessen/scripts/anti_todo_card.py --summary

# Every script supports --sample and --output-format json
```

## Slash commands

- `/cs:andreessen` — full market-first verdict mode (venture / idea / feature / career bet, or daily card).
- `/cs:pmf-check` — focused before/after product/market fit interrogation.

## Attribution

The operating prompt is user-supplied and preserved verbatim. The frameworks are Marc Andreessen's,
cited with explicit confidence levels in the references. This is an *inspired-by* skill and is **not
affiliated with or endorsed by Marc Andreessen or a16z.**

---

**Version:** 2.9.0 (ships in repo release v2.9.0)
**License:** MIT
