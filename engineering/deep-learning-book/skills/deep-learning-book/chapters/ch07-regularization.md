# Chapter 7: Regularization for Deep Learning

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/regularization.html

## Core Idea

Regularization is anything that trades training error for generalization error, and this chapter
is the catalogue: norm penalties, data augmentation, noise, early stopping, parameter sharing,
sparsity, ensembling, dropout, and adversarial training — with their equivalences made explicit.

## Frameworks Introduced

- **L2 / weight decay**: shrinks parameters along low-curvature Hessian directions. Under a
  quadratic approximation, it damps each eigen-direction by λᵢ/(λᵢ+α) — directions the loss does
  not care about get pulled to zero.
- **L1**: yields genuine sparsity; equivalent to a Laplace prior on parameters.
- **Norm penalty as constraint**: via KKT (Ch 4), a penalty is a soft version of a norm ball.
  Explicit projection (max-norm) is sometimes better behaved.
- **Dataset augmentation**: the most reliable regularizer when the invariance is real. Choose
  transformations that preserve the label — and check that they do.
- **Noise injection**: on inputs (≈ L2 penalty for some models), on weights (encourages flat
  minima), on labels (label smoothing).
- **Early stopping**: the cheapest regularizer; under a quadratic approximation it is
  approximately equivalent to L2 with a strength set by the number of steps.
- **Parameter tying / sharing**: the strongest form — it removes parameters instead of penalizing
  them. Convolution is parameter sharing (Ch 9).
- **Bagging and ensembles**: variance reduction by averaging independently trained models.
- **Dropout**: approximate ensembling over exponentially many sub-networks at the cost of one.
- **Adversarial training**: penalizing sensitivity to worst-case local perturbation.

## Mental Models

- Order regularizers by **cost per unit of gap closed**: more real data > augmentation > early
  stopping > weight decay > dropout > architecture surgery.
- Read weight decay as **"forget the directions the data does not constrain"** — that is exactly
  what the eigen-analysis says.
- Treat dropout as an **ensemble**, so its interaction with batch normalization (train/test
  statistics mismatch) is expected rather than surprising.

## Anti-patterns

- **Stacking every regularizer at once** and then tuning — you cannot attribute the effect.
- **Augmenting with label-destroying transforms** (horizontal flip on digits, aggressive crops on
  fine-grained classes).
- **Dropout inside a residual transformer block plus batch norm plus heavy weight decay** without
  measuring; modern stacks regularize far more lightly than 2016 practice.

## What changed after 2016

Weight decay and L2 were shown to be *not* equivalent under adaptive optimizers, which is why
**AdamW** (Loshchilov & Hutter 2017/2019) decouples them — this post-dates the book and is now
the default. Dropout largely left large-scale vision and language models, displaced by
normalization, augmentation and sheer data volume. Label smoothing and stochastic depth became
common. **Confidence: high** for AdamW; **high** for the decline of dropout at scale.

## Key Takeaways

1. Add regularizers one at a time and measure the gap after each.
2. Use decoupled weight decay (AdamW) rather than L2-in-the-loss with an adaptive optimizer.
3. Prefer parameter sharing over penalties when a real invariance exists.

## Connects To

- **Ch 5**: the bias–variance budget these all spend from.
- **Ch 8**: optimizer choice changes what weight decay means.
- **Ch 11**: which regularizer to reach for, given a measured gap.
