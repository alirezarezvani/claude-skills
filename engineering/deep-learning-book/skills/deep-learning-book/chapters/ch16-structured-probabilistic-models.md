# Chapter 16: Structured Probabilistic Models for Deep Learning

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/graphical_models.html

## Core Idea

A joint distribution over n variables is exponentially large; a graph that encodes conditional
independence makes it tractable. Directed models factor into conditionals, undirected models into
unnormalized potentials divided by a partition function — and that partition function is the bill
Chapters 17–19 spend their pages paying.

## Frameworks Introduced

- **The challenge of unstructured modelling**: memory, statistical efficiency, and inference cost
  all scale with the number of parameters in a full joint.
- **Directed models (Bayesian networks)**: p(x) = ∏ p(xᵢ | parents(xᵢ)). Normalized by
  construction — no partition function.
- **Undirected models (Markov random fields)**: p(x) = (1/Z) ∏ φ_c(x_c) over cliques. Z is the
  partition function, and it is a sum over all configurations.
- **Energy-based models**: p(x) ∝ exp(−E(x)). Any positive distribution can be written this way.
- **Separation / d-separation**: reading conditional independence off the graph.
- **Converting between graph types; factor graphs** for disambiguating factorization.
- **Sampling from graphical models**: ancestral sampling (easy, directed) vs Gibbs sampling
  (needed for undirected).
- **Structure learning and latent variables**; the **restricted Boltzmann machine (RBM)** as the
  worked example.

## Mental Models

- Use the rule of thumb: **directed = easy sampling, harder inference with explaining-away;
  undirected = natural for mutual constraints, hard normalization.**
- Read an energy function as a **soft constraint set**: low energy where constraints are
  satisfied. Design E, and p follows.
- Remember that the partition function is not an inconvenience — it is **the** obstacle that
  organizes all of Part III.

## Anti-patterns

- **Writing an undirected model and ignoring Z** until training refuses to work.
- **Assuming a graph's missing edge means independence in the data** — it means the *model*
  asserts independence.

## What changed after 2016

Deep undirected graphical models (deep Boltzmann machines, RBM stacks) are now largely historical
as generative workhorses. But energy-based modelling did not die: it returned via score matching
and diffusion (which sidestep Z entirely by learning ∇ log p rather than p), and via
energy-based reinterpretations of contrastive learning. Autoregressive factorization — the
directed side of this chapter — became the dominant paradigm through transformer language models,
which are exactly chain-rule factorizations with a huge neural conditional. **Confidence: high.**

## Key Takeaways

1. Classify any generative proposal as directed or undirected first; it predicts which problems
   you will have.
2. When Z is intractable, look for a formulation that never needs it (score, ratio, or
   autoregressive).
3. Read modern LLMs as ancestral sampling from a directed chain — the framing here still applies.

## Connects To

- **Ch 17–19**: the three responses to intractability (sample it, approximate Z, approximate the
  posterior).
- **Ch 20**: the models built on these foundations.
