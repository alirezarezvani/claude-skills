# Chapter 14: Autoencoders

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/autoencoders.html

## Core Idea

An autoencoder learns to copy its input imperfectly, and the constraint that prevents perfect
copying is where the learning happens. Undercompleteness, sparsity, denoising and contraction are
four different ways to impose that constraint — each defines a different notion of "useful".

## Frameworks Introduced

- **Undercomplete autoencoder**: bottleneck smaller than the input. With linear units and MSE it
  recovers PCA's subspace.
- **Regularized autoencoders**: capacity can exceed the input dimension as long as something else
  prevents identity — this is the chapter's key move.
- **Sparse autoencoder**: penalize code activation; interpretable as a latent prior (Ch 13).
- **Denoising autoencoder (DAE)**: corrupt the input, reconstruct the clean version. The learned
  map estimates the *score* — it points back toward the data manifold, which is the direct
  ancestor of score-based diffusion models.
- **Contractive autoencoder (CAE)**: penalize the Jacobian norm of the encoder, so the
  representation resists input perturbation except along the manifold.
- **Manifold learning view**: the encoder is sensitive along tangent directions of the data
  manifold and insensitive orthogonal to it.
- **Stochastic encoders and decoders**: autoencoders as p(h|x) and p(x|h).
- **Predictive sparse decomposition**; **applications**: dimensionality reduction, semantic
  hashing, pretraining.

## Mental Models

- Ask "**what stops it from learning the identity?**" — the answer names the inductive bias, and
  a model with no answer learns nothing useful.
- Read a DAE's learned vector field as **pointing uphill in density**. Once you see that,
  diffusion models are the same idea run at many noise levels.
- Treat the encoder as **amortized inference**: it replaces the per-example optimization of
  sparse coding with one forward pass.

## Anti-patterns

- **An overcomplete autoencoder with no regularizer** — it can and will learn a copy.
- **Judging representation quality by reconstruction error**: low reconstruction error can mean
  the code memorized the input, which is the opposite of useful.

## What changed after 2016

The denoising idea became the foundation of modern generative modelling: denoising score matching
(Vincent 2011) → score-based models (Song & Ermon 2019) → DDPM (Ho et al. 2020) → the diffusion
family. Greedy layerwise autoencoder pretraining, presented here as a live technique, disappeared
— displaced first by better initialization/normalization and then by large-scale supervised and
self-supervised pretraining. The VAE overshadowed the deterministic autoencoders for generation,
while masked autoencoders (He et al. 2021) revived the corruption idea for vision pretraining.
**Confidence: high.**

## Key Takeaways

1. Always name the constraint that prevents identity before training an autoencoder.
2. Do not use reconstruction error as a representation-quality metric; evaluate downstream.
3. Learn the denoising/score connection here — it is the cheapest on-ramp to diffusion models.

## Connects To

- **Ch 13**: sparse coding, amortized.
- **Ch 15**: what a "good" representation means.
- **Ch 20**: VAEs, and the diffusion line that grew from denoising.
