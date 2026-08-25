# Chapter 3: Probability and Information Theory

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/prob.html

## Core Idea

Deep learning models are probability distributions, and losses are log-likelihoods. This chapter
installs the vocabulary — random variables, the common distributions, expectation, Bayes' rule,
entropy, KL divergence, cross-entropy — that makes "why this loss?" answerable rather than
conventional.

## Key Concepts

- **Frequentist vs Bayesian probability**: rates of events vs degrees of belief. Deep learning
  uses the Bayesian reading for parameters and the frequentist one for evaluation, mostly
  without saying so.
- **Marginal / conditional / chain rule**: the algebra every graphical model in Ch 16 runs on.
- **Common distributions**: Bernoulli, categorical, Gaussian, exponential, Laplace, Dirac,
  empirical, and mixtures. Each corresponds to an output layer you will actually build.
- **Self-information and Shannon entropy**: surprise, and expected surprise.
- **KL divergence**: asymmetric. D(p‖q) ≠ D(q‖p), and the asymmetry decides whether your fitted
  model covers all modes or concentrates on one.
- **Cross-entropy**: H(p,q) = H(p) + D(p‖q). Minimizing cross-entropy over q is minimizing KL,
  because H(p) is constant in q — this is why classification uses it.
- **Structured probabilistic models**: factorization of a joint into conditionals over a graph.

## Mental Models

- Read every loss as a **negative log-likelihood** under an assumed output distribution: MSE is
  a Gaussian with fixed variance, cross-entropy is a categorical, MAE is a Laplace. If you know
  the assumed distribution, you know when the loss is wrong for your data.
- Use KL **direction** as a design lever: forward KL (data ‖ model) is mode-covering and gives
  blurry averages; reverse KL (model ‖ data) is mode-seeking and gives sharp but partial fits.
  This one fact explains most of Ch 19 and 20.
- Treat softmax as **exp-then-normalize on logits**, and remember from Ch 4 that it must be
  computed in a shift-stabilized form.

## Anti-patterns

- **Choosing MSE for a bounded or count-valued target** — you have assumed a Gaussian on data
  that is not Gaussian, and the residual structure will tell you so.
- **Reading KL as a distance**: it is not symmetric and does not satisfy the triangle inequality.
- **Interpreting softmax outputs as calibrated probabilities** without checking calibration —
  the chapter's math does not promise calibration, and modern networks are typically
  overconfident (Guo et al. 2017, post-dating the book).

## What changed after 2016

The probabilistic core is unchanged. Two additions matter: the calibration literature (deep
networks are systematically overconfident; temperature scaling is the cheap fix), and the rise
of losses that are *not* clean log-likelihoods — contrastive/InfoNCE objectives, and preference
losses such as DPO. The chapter's "every loss is a likelihood" framing needs that caveat now.
**Confidence: high** for calibration; **high** for the contrastive family being outside the
chapter's scope.

## Key Takeaways

1. State the output distribution before choosing the loss; the loss follows from it.
2. When a generative model looks blurry, suspect forward KL; when it looks mode-collapsed,
   suspect reverse KL.
3. Check calibration separately from accuracy — the book does not, and the gap is real.

## Connects To

- **Ch 5**: maximum likelihood as the estimator that justifies these losses.
- **Ch 16–19**: graphical models, sampling, and variational inference all run on this algebra.
- **Ch 20**: the KL asymmetry decides GAN vs VAE failure modes.
