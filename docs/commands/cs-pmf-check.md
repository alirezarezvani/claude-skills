---
title: "/cs-pmf-check — Slash Command for AI Coding Agents"
description: "/cs:pmf-check — Are you before or after product/market fit? A focused Andreessen-mode interrogation that scores the felt signals + the Sean Ellis 40%. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-pmf-check

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/productivity/andreessen/commands/cs-pmf-check.md">Source</a></span>
</div>


**Command:** `/cs:pmf-check`

A focused slice of the `cs-andreessen` persona aimed at one question: are you before or after
product/market fit? Per Andreessen, PMF is the only milestone that matters and it is **not subtle** —
if you have to squint to see it, you don't have it.

## When to Run

- "Are we at product/market fit?"
- You're deciding whether to scale (spend on growth/sales) or keep iterating on the product.
- You're tempted to raise/hire/expand and want a hard read on whether the fit is real first.

## What You Get

A focused interrogation, then a deterministic verdict:

1. **The felt-signal test** (Andreessen): are customers buying as fast as you can make it? Is usage
   growing as fast as you can add servers? Is money piling up? Are you hiring support as fast as you can?
2. **The Sean Ellis 40% gate** (Ellis, not Andreessen): do ≥40% of users say they'd be "very
   disappointed" without you?
3. **Verdict:** `BEFORE-PMF` / `APPROACHING-PMF` / `AFTER-PMF` + explicit confidence.
4. **One next move:** before PMF → what to change (product/segment/team). After PMF → pour fuel,
   stop deliberating, feed demand.

## Discipline

- **PMF is not subtle.** "Approaching" is the honest verdict for warm-but-ambiguous signals; don't
  inflate it to "after."
- **Retention is the strongest single signal.** A leaky bucket means you are before PMF no matter
  how good acquisition looks.
- **Label the Ellis test as Ellis's, not Andreessen's.** Confidence levels mandatory.
- **No capitulation** to wishful reads without new evidence.

## Workflow

```bash
python ../skills/andreessen/scripts/pmf_signal_scorer.py \
  --ellis-pct 45 --retention 8 --organic 7 --demand 8 --frequency 7
```

## Related

- Agent: [`cs-andreessen`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/andreessen/agents/cs-andreessen.md)
- Skill: [`andreessen`](https://github.com/alirezarezvani/claude-skills/tree/main/productivity/andreessen/skills/andreessen/SKILL.md)
- Parent command: [`/cs:andreessen`](./cs-andreessen.md)

---

**Version:** 1.0.0
