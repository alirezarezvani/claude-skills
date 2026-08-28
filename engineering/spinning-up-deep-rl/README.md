# Spinning Up in Deep RL

Knowledge-base plugin compiled from **Spinning Up in Deep RL by Joshua Achiam (OpenAI)** by
[`engineering/book-to-skill`](../book-to-skill/). 20 chapters indexed.

## What is in here

| File | Contents |
|------|----------|
| `skills/spinning-up-deep-rl/SKILL.md` | Core frameworks, chapter index, topic index (resident, under 4k tokens) |
| `skills/spinning-up-deep-rl/chapters/` | One summary per chapter — loaded on demand, never all at once |
| `skills/spinning-up-deep-rl/glossary.md` | Every significant term, alphabetized, with its chapter |
| `skills/spinning-up-deep-rl/patterns.md` | Techniques and design patterns with trade-offs |
| `skills/spinning-up-deep-rl/cheatsheet.md` | Decision rules, thresholds and trade-off matrices |

## Use

```
/cs:spinning-up-deep-rl                    # core frameworks + chapter index
/cs:spinning-up-deep-rl <topic>            # resolve via topic index, read one chapter
/cs:spinning-up-deep-rl ch05               # read one chapter summary
```

Or invoke the `cs-spinning-up-deep-rl` agent for a working session anchored to this source.

## Provenance and limits

**Source:** OpenAI's [Spinning Up in Deep RL](https://spinningup.openai.com/)
([openai/spinningup](https://github.com/openai/spinningup)), primarily developed by
**Joshua Achiam**. Compiled from the `docs/` reStructuredText tree at the January 2020
PyTorch update.

**Rights basis:** `open-license`. The source is **MIT, Copyright (c) 2018 OpenAI**, which
permits derivative distribution. The full upstream notice is reproduced in
[`LICENSE`](LICENSE) alongside this package's own; the top-level `license` field in
`plugin.json` covers the scaffolding only.

Generated, not hand-authored: every claim traces to the source document. It carries that source's
blind spots, and it is a set of structured notes — **not a copy of the work and not a substitute
for reading it**.

**What it does not cover:** DQN and the discrete-action value-learning family, recurrent or
convolutional architectures, partially-observed settings, model-based implementations, and any
deep RL work after early 2020. The six implementations documented are educational; `ch13` records
which are research-grade (DDPG, TD3, SAC) and which are not (VPG, TRPO, PPO).

Distribution: `shareable`. Regenerate or extend with
`python3 engineering/book-to-skill/skills/book-to-skill/scripts/extract_document.py`, then re-run
`book_skill_validator.py` before loading the result.
