# Chapter 4: Numerical Computation

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/numerical.html

## Core Idea

Real arithmetic on finite hardware fails in specific, predictable ways — underflow, overflow,
ill-conditioning — and gradient-based optimization inherits every one of them. This is the
shortest chapter with the highest debugging payoff.

## Key Concepts

- **Underflow / overflow**: numbers rounding to zero (then dividing) or exceeding representable
  range (then becoming inf/NaN).
- **Stabilized softmax**: subtract the max logit before exponentiating; mathematically identical,
  numerically survivable. `log_softmax` exists for the same reason.
- **Conditioning**: how much a function's output moves for small input moves; for a matrix, the
  condition number from Ch 2.
- **Gradient descent** and the first-order Taylor picture; **critical points**: minima, maxima,
  saddles.
- **Jacobian and Hessian**; second-order Taylor expansion, and the optimal step size implied by
  curvature.
- **Newton's method** and why it is not the default in deep learning: the Hessian is n×n in the
  parameter count.
- **Constrained optimization / KKT**: the framing that makes Ch 7's norm penalties readable as
  constraints.

## Mental Models

- Read a **NaN in the loss** as a numerics report first and a modelling bug second: check
  log(0), division by a near-zero denominator, exp of a large logit, and an exploding gradient
  in that order.
- Think of the Hessian's **eigenvalue spread as the terrain**: a large condition number is a
  narrow ravine, and the largest safe step size is set by the largest eigenvalue while progress
  is set by the smallest.
- Prefer the **log-domain** whenever probabilities are multiplied — this is the single highest
  yield habit in this chapter.

## Anti-patterns

- **Hand-rolling softmax or cross-entropy** in a training loop instead of using the fused,
  stabilized primitive.
- **Blaming the learning rate for every divergence**: ill-conditioning produces the same symptom
  and does not respond to the same fix.
- **Reaching for a second-order optimizer** in a model with millions of parameters without
  understanding the memory cost.

## What changed after 2016

Mixed-precision training (fp16 with loss scaling; then bf16, which trades mantissa bits for
exponent range specifically to avoid these failures) made this chapter's content a daily
operational concern rather than a background caution. Gradient clipping became standard practice
for transformer training. **Confidence: high.**

## Key Takeaways

1. Work in log-space by default for anything probabilistic.
2. When training diverges, separate "step too large" from "problem ill-conditioned" — they need
   different fixes.
3. Understand KKT well enough to read weight decay as a constraint; Ch 7 assumes it.

## Connects To

- **Ch 8**: every optimization difficulty named here recurs there at scale.
- **Ch 7**: the constrained-optimization view of regularization.
- **scripts/training_diagnostics.py**: mechanizes the NaN/divergence triage above.
