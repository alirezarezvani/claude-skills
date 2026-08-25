# Chapter 18: Confronting the Partition Function

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/partition.html

## Core Idea

For undirected models, the log-likelihood gradient splits into a positive phase (push energy down
on data) and a negative phase (push energy up everywhere the model believes) — and the negative
phase requires samples from the model itself. Every technique in this chapter is a way to afford
that negative phase, or to avoid needing Z at all.

## Frameworks Introduced

- **Positive and negative phase**: the gradient of log Z is an expectation under the *model*.
  This is the structural reason undirected models are expensive.
- **Contrastive divergence (CD-k)**: initialize the negative chain at the data and run k steps.
  Fast; biased; produces spurious modes in regions the short chain never visits.
- **Stochastic maximum likelihood / persistent CD (PCD)**: keep the chain's state across parameter
  updates so it has effectively run for a long time. Better mixing, at the cost of a chain that
  can fall behind fast-moving parameters.
- **Pseudolikelihood**: replace the joint with a product of conditionals — Z cancels. Cheap; a
  different objective, so it optimizes for a different thing.
- **Score matching**: match ∇_x log p instead of p, which eliminates Z because the gradient of
  log Z with respect to x is zero. **Ratio matching** and **denoising score matching** are the
  variants.
- **Noise-contrastive estimation (NCE)**: turn density estimation into a classification problem —
  real data versus noise — and treat the normalizer as a learned parameter.
- **Annealed importance sampling (AIS)** and **bridge sampling**: estimate Z itself, mainly for
  evaluation.

## Mental Models

- Read the whole chapter as **four escape routes from Z**: sample it (CD/PCD), sidestep it
  (pseudolikelihood, score matching), learn around it (NCE), or estimate it for evaluation only
  (AIS).
- Treat score matching's trick — **differentiate with respect to x, not θ, so Z vanishes** — as
  the single most consequential idea in Part III for modern practice.
- Expect **spurious modes** from short-chain training; they are a predictable artifact, not a bug
  in your code.

## Anti-patterns

- **Comparing likelihoods across undirected models without estimating Z** — the numbers are not
  comparable.
- **Using CD-1 and reporting it as maximum likelihood.**

## What changed after 2016

Score matching's downstream career is the story here. Denoising score matching plus a noise
schedule became score-based generative modelling (Song & Ermon 2019) and DDPM (Ho et al. 2020) —
the diffusion family that now dominates image, audio and video generation. NCE became the
backbone of contrastive representation learning (word2vec's negative sampling, then InfoNCE and
CLIP). AIS remains the standard tool for evaluating likelihoods when Z is unknown. Contrastive
divergence and PCD are largely historical. **Confidence: high.**

**This is the chapter whose ideas travelled furthest — read it even if you never train a
Boltzmann machine.**

## Key Takeaways

1. When a normalizer blocks you, ask which of the four escape routes fits your objective.
2. Learn score matching properly; diffusion models are unintelligible without it.
3. Never compare unnormalized likelihoods.

## Connects To

- **Ch 17**: the sampling machinery the negative phase depends on.
- **Ch 14**: denoising autoencoders as score estimators.
- **Ch 20**: the generative models built from these objectives.
