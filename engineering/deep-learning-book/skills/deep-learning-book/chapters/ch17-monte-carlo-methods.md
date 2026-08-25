# Chapter 17: Monte Carlo Methods

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/monte_carlo.html

## Core Idea

When a sum or integral is intractable, estimate it with samples. The estimator is unbiased and
its error shrinks as 1/√n regardless of dimension — which is why sampling survives where
quadrature does not. The difficulty moves from computing the integral to obtaining the samples.

## Key Concepts

- **Monte Carlo estimation**: approximate E_p[f(x)] by the sample mean; variance falls as 1/n,
  standard error as 1/√n.
- **Importance sampling**: sample from a tractable q and reweight by p/q. Variance depends
  entirely on how well q matches p·f — a bad proposal gives an estimator that is unbiased and
  useless.
- **Markov chain Monte Carlo (MCMC)**: build a chain whose stationary distribution is the target,
  then use its states as (correlated) samples.
- **Gibbs sampling**: resample each variable from its conditional given the rest; the natural
  MCMC scheme for graphical models.
- **Burn-in / mixing time**: the chain needs time to forget its initialization and to move
  between modes.
- **The mixing problem between separated modes**: with well-separated modes, transition
  probability between them is tiny and the chain reports a single mode as if it were everything.
- **Tempering / annealing** as remedies: flatten the distribution so the chain can travel.

## Mental Models

- Treat a Monte Carlo estimate as a **measurement with error bars**; report the standard error,
  because "the estimate is unbiased" says nothing about whether n was large enough.
- Diagnose a suspiciously confident sampler as a **mixing failure**, not a modelling success.
- Read importance sampling's variance condition as: **you must already know roughly where the
  mass is** — this is why proposals matter more than sample counts.

## Anti-patterns

- **Reporting MCMC samples without a mixing diagnostic.**
- **Trusting importance weights with huge dynamic range** — an effective sample size of ~1 is
  common and invisible unless measured.

## What changed after 2016

The chapter's methods remain textbook-correct, but their role in deep generative modelling
shrank: diffusion models replaced slow MCMC-based sampling with a fixed, finite denoising chain,
and modern generation is dominated by ancestral sampling from autoregressive models. Where MCMC
is still used — Bayesian deep learning, some energy-based models — HMC/NUTS variants dominate
over plain Gibbs. **Confidence: high.**

## Key Takeaways

1. Always pair a Monte Carlo estimate with its standard error.
2. Check mixing before believing anything an MCMC sampler tells you about multimodality.
3. Recognize the pattern "intractable expectation → sample it" — it recurs throughout Ch 18–20.

## Connects To

- **Ch 16**: the undirected models that need sampling in the first place.
- **Ch 18**: sampling as an ingredient in partition-function estimation.
- **Ch 20**: sampling as generation.
