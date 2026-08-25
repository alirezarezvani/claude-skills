# Chapter 5: Machine Learning Basics

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/ml.html

## Core Idea

Everything after this chapter is a special case of it: a task, a performance measure, an
experience, a capacity choice, and the generalization gap that capacity choice produces. If you
read one chapter of Part I, read this one.

## Key Concepts

- **Task / performance measure / experience (T, P, E)**: the definition that forces you to name
  the metric before the model.
- **Capacity**: the range of functions a learner can express. Representational capacity vs
  *effective* capacity (what the optimizer actually reaches).
- **Underfitting / overfitting** and the classical **U-shaped** generalization-error curve.
- **Bias–variance decomposition**: expected error splits into bias², variance, and irreducible
  noise. Regularization trades variance for bias.
- **No Free Lunch theorem**: averaged over *all* data-generating distributions, every algorithm
  ties. Therefore all progress comes from priors matched to the distributions we actually face.
- **Regularization**: any change intended to reduce generalization error but not training error.
- **Maximum likelihood estimation** and its **MAP** counterpart; consistency and efficiency.
- **Hyperparameters and validation sets**: never tune on test.
- **Curse of dimensionality, local constancy, manifold hypothesis**: why nearest-neighbour-style
  priors fail and why deep models assume data concentrates near a low-dimensional manifold.

## Mental Models

- Ask "**what is the prior?**" before "what is the model?" — No Free Lunch says the prior is
  where all the leverage is.
- Read regularization as **moving mass in the bias–variance budget**, so that "add dropout" and
  "get more data" are alternative purchases of the same thing.
- Treat the **train/val gap** as your primary instrument: gap small + error high = underfit
  (capacity or optimization); gap large = overfit (regularization or data).

## Anti-patterns

- **Tuning against the test set** — including "just peeking once."
- **Comparing models on different splits**, or reporting a single seed for a small dataset.
- **Believing the U-curve unconditionally.** See below: this is the one place where the 2016
  text is now known to be incomplete.

## What changed after 2016

**This is the chapter's one substantive correction.** The classical U-shaped capacity curve is
not the whole picture. In the heavily overparameterized regime, test error can fall again past
the interpolation threshold — "double descent" (Belkin et al. 2019; Nakkiran et al. 2020), which
post-dates the book. Modern large models routinely sit in a regime the 2016 framing predicts
should overfit catastrophically and does not. The bias–variance decomposition remains correct as
algebra; the *managerial advice* "reduce capacity when you overfit" is no longer the only right
move. **Confidence: high** — double descent is widely replicated. Practical consequence: try
"more data / more regularization / train longer" before "smaller model."

## Key Takeaways

1. Write down T, P, E in one sentence before writing any model code.
2. Use the train/val gap to choose your next action; do not guess.
3. Hold the U-curve loosely — check whether you are past the interpolation threshold before
   shrinking a model that overfits.

## Connects To

- **Ch 7**: every regularizer named here, in depth.
- **Ch 11**: this chapter's diagnostics turned into a workflow.
- **scripts/capacity_planner.py**: mechanizes the gap-to-action rule, double descent included.
