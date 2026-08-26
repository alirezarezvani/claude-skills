# Chapter 15: Representation Learning

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/representation.html

## Core Idea

What makes one representation better than another, and how do you get one without labels? The
chapter names the properties worth wanting — distributed, disentangled, capturing causal factors
— and the transfer mechanisms that let a representation earned on one task pay off on another.

## Frameworks Introduced

- **Greedy layer-wise unsupervised pretraining**: the historically important technique that
  restarted the field in 2006; the chapter is already candid that its value had shrunk by 2016.
- **Transfer learning and domain adaptation**: reuse a representation across tasks or
  distributions; **one-shot / zero-shot learning** as the limiting cases.
- **Distributed representations**: n binary features describe 2ⁿ regions, versus n regions for a
  one-hot/symbolic code. This exponential advantage is the central argument for learned features.
- **Disentangled factors**: separate underlying causes onto separate directions.
- **Exponential gains from depth**: deeper composition of distributed features again multiplies
  expressible structure.
- **Causal factors and semi-supervised learning**: unsupervised learning helps supervised learning
  exactly when p(x) and p(y|x) share structure — if the factors generating x include y's causes.
- **Regularization priors that define good representations**: smoothness, linearity, multiple
  explanatory factors, hierarchy, sparsity, simplicity of factor dependencies, shared factors
  across tasks, manifolds, temporal/spatial coherence.

## Mental Models

- Judge a representation by **what becomes linearly separable** in it — that is the operational
  version of "good features."
- Use the **shared-cause test** to predict whether unlabeled data will help: if p(x) tells you
  nothing about p(y|x), self-supervision will not rescue a supervised task.
- Read distributed-vs-symbolic as **the reason embeddings beat lookup tables**, and note that the
  advantage is combinatorial, not merely empirical.

## Anti-patterns

- **Expecting unsupervised pretraining to help unconditionally** — the chapter itself is careful
  here, and the 2016-era conclusion (it often does not, for large labeled datasets) was correct
  for the methods then available.
- **Claiming disentanglement without a metric or an intervention.**

## What changed after 2016

This chapter aged into relevance rather than out of it. Self-supervised learning became the
dominant paradigm — contrastive methods (SimCLR, MoCo, CLIP), masked prediction (BERT, MAE), and
next-token prediction at scale — vindicating the chapter's core bet while replacing every
specific method it lists. Two corrections: greedy layer-wise pretraining is now purely
historical, and unsupervised disentanglement was proven impossible without inductive bias
(Locatello et al. 2019). Linear-probe evaluation became the standard test of representation
quality. **Confidence: high.**

## Key Takeaways

1. Evaluate representations with linear probes and downstream transfer, not reconstruction.
2. Before investing in self-supervision, argue that p(x) and p(y|x) share causes.
3. Treat "disentangled" as a claim requiring an intervention-based test.

## Connects To

- **Ch 14**: autoencoders as one route to a representation.
- **Ch 1**: the promise made in the introduction, cashed out here.
- **references/book_to_2026_delta.md**: the self-supervised learning line.
