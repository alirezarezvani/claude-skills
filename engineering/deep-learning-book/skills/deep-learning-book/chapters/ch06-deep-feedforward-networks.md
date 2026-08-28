# Chapter 6: Deep Feedforward Networks

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/mlp.html

## Core Idea

An MLP is a composed chain of parametric functions trained by gradient descent, where the choice
of output unit follows from the assumed output distribution and the choice of hidden unit follows
from gradient behaviour. Backpropagation is not learning; it is the chain rule scheduled well.

## Key Concepts

- **Universal approximation**: one sufficiently wide hidden layer can approximate any continuous
  function on a compact set. It says nothing about learnability, sample efficiency, or the size
  required — depth is how you get the same function with far fewer units.
- **Output units follow the distribution**: linear + MSE → Gaussian; sigmoid + binary
  cross-entropy → Bernoulli; softmax + cross-entropy → categorical; mixture density → multimodal.
- **Hidden units**: ReLU as the sane default; leaky/parametric ReLU, ELU, GELU/Swish (post-2016)
  for smoothness; sigmoid/tanh only where saturation is desired (gates).
- **Saturation**: sigmoid/tanh gradients vanish in the tails, which is why they are poor hidden
  units and fine as gates.
- **Backpropagation**: reverse-mode automatic differentiation over the computation graph. Cost is
  roughly one forward pass, memory is the stored activations.
- **Computation graph / autodiff**: the abstraction every framework implements. Forward mode is
  cheap in inputs; reverse mode is cheap in outputs — losses are scalar, hence reverse.

## Mental Models

- Pick the output unit from the **likelihood** (Ch 3), then pick the loss as its negative log.
  Every "which loss?" question reduces to "which distribution?"
- Read **ReLU's advantage as gradient preservation**, not nonlinearity per se: it is piecewise
  linear, so the gradient through an active unit is exactly 1.
- Treat activation memory as the **real** cost of depth in training: the backward pass needs the
  forward activations, which is why checkpointing trades compute for memory.

## Anti-patterns

- **Citing universal approximation to justify a shallow model** — the theorem allows an
  exponentially wide layer, which is not an engineering plan.
- **Sigmoid hidden layers** in a deep stack.
- **Pairing a sigmoid output with MSE**: gradients vanish exactly where the model is most wrong.
  Use cross-entropy.

## What changed after 2016

Smooth activations (GELU, SiLU/Swish) became the default in transformers; gated variants
(GLU, SwiGLU) are now standard in large language model feedforward blocks. Residual connections
(He et al. 2015) are mentioned here only in passing but became the structural default for every
deep stack. Reverse-mode autodiff is unchanged. **Confidence: high.**

## Key Takeaways

1. Derive the loss from the output distribution rather than picking it by habit.
2. Default to ReLU-family hidden units; reserve saturating units for gates.
3. Budget activation memory as a first-class constraint, not an implementation detail.

## Connects To

- **Ch 3**: the distributions that determine output units.
- **Ch 8**: why gradient preservation matters at depth.
- **scripts/model_arithmetic.py**: parameter, FLOP and activation-memory accounting for a stack.
