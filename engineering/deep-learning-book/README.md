# deep-learning-book — study companion for *Deep Learning* (Goodfellow, Bengio & Courville)

A navigable, executable, **date-stamped** companion to the 2016 MIT Press textbook that is free
to read at [deeplearningbook.org](https://www.deeplearningbook.org/).

Twenty chapter files, a glossary, a patterns file, a cheatsheet, four references and four
deterministic tools — plus the thing a static compilation cannot give you: a **2016 → 2026 delta
layer** that says, per chapter, what still holds, what was superseded, and what is now purely
historical.

## Why this is a companion and not a compiled skill

This repository ships [`engineering/book-to-skill`](../book-to-skill/), which compiles a document
on disk into a knowledge-base skill. It was deliberately **not** used here, for three reasons its
own rights gate makes binding:

1. The book is copyrighted (MIT Press, 2016). Free to read ≠ free to redistribute.
2. deeplearningbook.org states that its HTML-only presentation is a deliberate friction against
   copying, required by the authors' contract, and that PDF distribution is not permitted.
3. This repository is public, and `book-to-skill`'s rights gate refuses a `shareable` package
   without `public-domain`, `open-license`, `internal-docs` or `author-permission`. None applies.
   (Its hard rule 1 also forbids scraping a book from the web, so the pipeline could not have run
   against a URL in any case.)

So this skill contains **no passages, paragraphs, figures, or per-paragraph paraphrase**. Every
chapter file is original synthesis — what the chapter establishes, how to use it, where it has
aged — with a link to the official free chapter. The organizing structure is the book's published
table of contents, which is factual metadata. Full reasoning in
[`references/rights_and_use.md`](skills/deep-learning-book/references/rights_and_use.md).

**The rule this sets for the repository:** when a user asks to convert a copyrighted work into a
shareable skill, build a companion that indexes and updates the source, not a compilation that
reproduces it. Compile only when the rights gate clears, and keep the output local when it does not.

## What is in it

```
skills/deep-learning-book/
├── SKILL.md              core frameworks + chapter index + topic index (~1.9k tokens, resident)
├── chapters/ch01..ch20   one file per chapter, each with "What changed after 2016"
├── glossary.md           every key term → its chapter
├── patterns.md           techniques as instruments, with trade-offs
├── cheatsheet.md         decision tables: loss choice, fit verdict, optimizer defaults
├── references/           delta layer · prerequisite map · study method · rights
├── scripts/              4 stdlib tools
└── assets/               layer spec · chapter worksheet · study log
```

## The tools

| Tool | Does | Refuses |
|---|---|---|
| `reading_path_planner.py` | Goal + background + hours → prerequisite-closed, ordered path with an hour budget | A goal outside the book (exit 3, names what covers it); an unroutable goal (exit 4, prints the questions) |
| `training_diagnostics.py` | Measurements → ranked cause + next action + chapter, rules in priority order | Diagnosing with no instruments (exit 4). Never reports a NaN as overfitting |
| `capacity_planner.py` | Gap + params-per-example → ordered regularization ladder | A validation error materially below training error (exit 4 — leaky split) |
| `model_arithmetic.py` | Layer stack → parameters, FLOPs, activation memory per example | A stack whose shapes do not connect (exit 5); an unknown layer type (exit 4) |

All four are standard-library only, support `--help` / `--sample` / `--output json`, make no
network calls, and load no frameworks.

## The delta layer

The book was published in 2016; *Attention Is All You Need* appeared in 2017. Five corrections
carry most of the weight, each cited and confidence-rated in
[`references/book_to_2026_delta.md`](skills/deep-learning-book/references/book_to_2026_delta.md):

1. **Double descent** qualifies Chapter 5's U-shaped capacity curve — "shrink the model when it
   overfits" is no longer the only correct move, and `capacity_planner.py` encodes the correction.
2. **AdamW**: weight decay and L2 are not equivalent under an adaptive optimizer; Chapter 7 treats
   them as interchangeable.
3. **Transformers** displaced Chapter 10's recurrence — keep its gradient-flow analysis, drop its
   architecture recommendation. (State-space models made that analysis live again.)
4. **Diffusion** grew directly out of Chapter 14's denoising autoencoders and Chapter 18's score
   matching, and displaced Chapter 20's model list.
5. **Self-supervised learning** vindicated Chapter 15's bet while replacing every method it names;
   unsupervised disentanglement was proven impossible without inductive bias.

The general rule the file states: the conflict is almost always in the **recommendation**, not the
**analysis**. Keep the diagnosis, replace the prescription.

## Use it

```bash
S=engineering/deep-learning-book/skills/deep-learning-book/scripts

python3 $S/reading_path_planner.py --goal "train and debug convnets" --background applied --hours-per-week 5
python3 $S/training_diagnostics.py --train-loss 0.02 --val-loss 1.9 --tiny-subset-fits yes
python3 $S/capacity_planner.py --params 12000000 --train-examples 50000 --train-error 0.01 --val-error 0.22
python3 $S/model_arithmetic.py --spec skills/deep-learning-book/assets/example_layer_spec.json
```

Slash commands: `/cs:deep-learning` (navigate and date the answer), `/cs:dl-reading-path`,
`/cs:dl-diagnose`. Agent: `cs-deep-learning-tutor`.

## Distinct from

- **`engineering/book-to-skill`** — the converter. This is what you build when its rights gate
  says no.
- **`engineering-team/senior-ml-engineer`** — production MLOps, deployment, serving. This is the
  theory underneath.
- **`engineering/llm-cost-optimizer`** — LLM economics, which the book predates entirely.
- **`teach` / `learn` skills** — general study workflows. This is one specific text, with its
  dependency graph and its expiry dates.

## Scope

The twenty chapters and the delta between them and 2026 practice. **Not covered**, because the
book does not cover them: reinforcement learning beyond passing mention, LLM training
infrastructure, RLHF/DPO, agentic systems, MLOps tooling, fairness and safety evaluation. The
skill is built to say so rather than improvise.

## Attribution

*Deep Learning*, Ian Goodfellow, Yoshua Bengio and Aaron Courville, MIT Press, 2016 —
https://www.deeplearningbook.org/. All rights in the book remain with its authors and publisher.
This companion is an independent work: no text, figures, or exercises from the book are
reproduced here, and it is not endorsed by or affiliated with the authors or MIT Press. The
companion's own content is MIT-licensed as part of this repository.
