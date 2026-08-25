# Chapter 13: Linear Factor Models

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/linear_factors.html

## Core Idea

The simplest generative models: sample latent factors from a simple prior, map them linearly to
observations, add noise. Probabilistic PCA, factor analysis, ICA, sparse coding and slow feature
analysis are all this one template with different priors — and they are the scaffolding for
everything in Chapters 14–20.

## Key Concepts

- **The template**: h ~ p(h); x = Wh + b + noise. Change p(h) and the noise model, get a
  different named method.
- **Factor analysis**: Gaussian latent prior, diagonal (per-feature) observation noise.
- **Probabilistic PCA**: factor analysis with isotropic noise; recovers PCA as noise → 0.
- **Independent component analysis (ICA)**: non-Gaussian independent latents — this is what makes
  the factors identifiable, which Gaussian models cannot be (any rotation fits equally well).
- **Sparse coding**: a heavy-tailed (Laplace/Cauchy) prior; inference is an optimization, not a
  closed form, which makes encoding expensive.
- **Slow feature analysis**: a prior that useful factors change slowly over time.
- **Manifold interpretation of PCA**: the model concentrates probability near a linear subspace.

## Mental Models

- Read each model as **a prior choice**, and read the prior as the assumption that buys
  identifiability. Gaussian latents are rotation-invariant, so a Gaussian model cannot tell you
  *which* factors — only which subspace.
- Treat sparse coding as the moment where **inference becomes iterative**; that cost is precisely
  what autoencoders (Ch 14) amortize with a learned encoder.
- Use these as the **linear baseline** for any representation-learning claim: if a linear factor
  model matches your deep encoder, the depth is not earning its cost.

## Anti-patterns

- **Skipping this chapter and starting at Ch 20** — VAEs read as arbitrary machinery without the
  latent-variable template established here.
- **Expecting interpretable factors from a Gaussian-latent model.**

## What changed after 2016

The template survived; the emphasis moved. Nonlinear ICA identifiability results (Hyvärinen et
al., 2016–2020) clarified when latent factors are recoverable at all, and the disentanglement
literature — notably Locatello et al. (2019) — showed that unsupervised disentanglement is
impossible without inductive biases or supervision, which is a formal statement of this
chapter's identifiability point. Sparse coding returned as a tool for interpreting neural
networks (sparse autoencoders over LLM activations, 2023–2024). **Confidence: high.**

## Key Takeaways

1. Name the latent prior when you propose any generative model; it determines what is learnable.
2. Use a linear factor model as the baseline before claiming a deep representation helps.
3. Remember that identifiability, not fit quality, is what non-Gaussian priors buy.

## Connects To

- **Ch 14**: autoencoders amortize the inference these models do by optimization.
- **Ch 15**: what makes a representation good.
- **Ch 20**: the VAE is this template with a nonlinear decoder and amortized inference.
