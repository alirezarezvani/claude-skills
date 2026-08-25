# Chapter 2: Linear Algebra

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/linear_algebra.html

## Core Idea

The minimum linear algebra a deep learning practitioner needs, chosen for what appears later:
tensors and broadcasting, norms, eigendecomposition, SVD, the pseudoinverse, and PCA derived
from scratch. This is a filter, not a course — it teaches what Chapters 4, 5, 8 and 13 will use.

## Key Concepts

- **Tensor / broadcasting**: an n-dimensional array plus the rules for combining shapes. Most
  real "model bugs" are shape bugs.
- **Norms**: L2 (Euclidean), L1 (sparsity-friendly, non-differentiable at 0), max-norm,
  Frobenius. The choice of norm *is* the choice of what "small" means in a regularizer.
- **Eigendecomposition**: A = V diag(λ) V⁻¹ for square matrices; the eigenvalues tell you the
  local curvature story later in Ch 4 and 8.
- **Singular value decomposition (SVD)**: A = U D Vᵀ, defined for *any* matrix. The general tool
  where eigendecomposition needs square and diagonalizable.
- **Moore–Penrose pseudoinverse**: the least-squares / minimum-norm solution when a system is
  over- or under-determined.
- **Condition number**: ratio of largest to smallest singular value; large means small input
  perturbations produce large output changes — the numerical fragility Ch 4 confronts.
- **PCA**: derived here as the linear encoder/decoder minimizing L2 reconstruction error, which
  is exactly the framing Ch 13–14 generalize.

## Mental Models

- Read a matrix as a **function on space**, and its singular values as how much it stretches
  each orthogonal direction. Condition number = worst stretch / least stretch.
- Use SVD as the **default** decomposition and reach for eigendecomposition only when symmetry
  buys you something (it does for Hessians).
- Treat a regularizer's norm as a **prior over parameter space**: L2 says "small and spread",
  L1 says "mostly zero."

## Anti-patterns

- **Skipping to Chapter 6.** Ch 4 and 8's discussion of ill-conditioning is unreadable without
  eigenvalues and condition number, and readers who skip typically bounce off Ch 8.
- **Memorizing decompositions as identities** instead of as geometry — the geometry is what
  transfers to optimization.

## What changed after 2016

Nothing in the mathematics. What changed is the practice: in half-precision training, condition
number stopped being a theoretical concern and became an operational one (loss scaling, bf16 over
fp16 precisely because of dynamic range). **Confidence: high.**

## Key Takeaways

1. Track shapes explicitly; treat a shape mismatch as a modelling error, not a typing error.
2. Pick your norm deliberately when you regularize — you are choosing the shape of the prior.
3. Learn PCA in this chapter's form (encoder/decoder minimizing reconstruction) so Ch 13–14 read
   as generalizations rather than new material.

## Connects To

- **Ch 4**: conditioning and numerical stability use exactly these quantities.
- **Ch 13**: PCA reappears as a linear factor model with an explicit probabilistic story.
- **Ch 8**: Hessian eigenvalues explain why gradient descent stalls.
