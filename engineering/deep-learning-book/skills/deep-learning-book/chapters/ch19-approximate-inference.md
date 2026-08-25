# Chapter 19: Approximate Inference

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/inference.html

## Core Idea

Computing p(h|x) — the posterior over latents — is intractable for most interesting models. The
fix is to reframe inference as optimization: choose a tractable family q, and maximize a lower
bound on the log-likelihood. The gap between the bound and the truth is exactly a KL divergence.

## Frameworks Introduced

- **Inference as optimization**: pick q(h) to maximize the **evidence lower bound (ELBO)**,
  L(q) = log p(x) − D_KL(q(h) ‖ p(h|x)). Maximizing L both fits the model and tightens the bound.
- **Expectation maximization (EM)**: alternate between setting q to the current posterior
  (E-step) and maximizing with respect to parameters (M-step).
- **MAP inference and sparse coding**: taking a point estimate of h is a degenerate q (a Dirac);
  sparse coding's inference step is exactly MAP inference.
- **Variational inference and mean field**: restrict q to a factorized family, q(h) = ∏ q(hᵢ),
  and derive fixed-point updates. Tractability is bought with an independence assumption.
- **Reverse-KL consequences**: the ELBO uses D(q‖p), which is mode-seeking — variational
  posteriors are characteristically **too narrow**, and underestimate uncertainty.
- **Learned approximate inference / amortization**: train a network to output q's parameters
  directly, replacing per-example optimization with one forward pass.

## Mental Models

- Read the ELBO as **"log-likelihood minus the cost of your approximation"** — improving q and
  improving the model are the same optimization.
- Expect **underestimated variance** from mean-field posteriors, and never report variational
  uncertainty as calibrated without checking.
- Treat amortization as the **encoder** of Chapter 14: the VAE is exactly this idea plus the
  reparameterization trick.

## Anti-patterns

- **Reporting a mean-field posterior's credible intervals as if they were exact.**
- **Blaming the model for a poor fit** that is actually a too-restrictive q — diagnose the bound
  before the model.

## What changed after 2016

Amortized variational inference became routine (VAEs and descendants); normalizing flows and
importance-weighted bounds (IWAE) gave tighter, more expressive posteriors than mean field. But
the strategic picture changed more: modern large generative models largely **avoid latent-variable
posteriors altogether** — autoregressive transformers have no posterior to infer, and diffusion
models use a fixed forward process, so their "inference" is trivial by construction. Variational
inference remains central in Bayesian deep learning and in structured latent-variable modelling.
**Confidence: high.**

## Key Takeaways

1. Write the ELBO down for any latent-variable model you train; it tells you what you are
   actually optimizing.
2. Assume a mean-field posterior is over-confident until proven otherwise.
3. Ask whether your problem needs a latent posterior at all — many modern designs are structured
   to avoid one.

## Connects To

- **Ch 13 / Ch 14**: the latent-variable models needing inference, and amortization.
- **Ch 20**: the VAE, assembled from this chapter plus the reparameterization trick.
- **Ch 3**: the KL asymmetry that dictates the narrow-posterior failure mode.
