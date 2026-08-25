# Chapter 10: Sequence Modeling — Recurrent and Recursive Nets

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/rnn.html

## Core Idea

Recurrence shares parameters across time the way convolution shares them across space, which lets
one model handle variable-length sequences. The price is that gradients must traverse many
multiplicative steps, producing the vanishing/exploding gradient problem — and gated
architectures exist to pay it.

## Frameworks Introduced

- **Unfolding the computational graph**: a recurrent definition becomes a deep feedforward graph
  with tied weights.
- **BPTT (backpropagation through time)** and **truncated BPTT**.
- **Teacher forcing**: train on ground-truth previous tokens; note the train/inference mismatch
  (exposure bias) it creates.
- **Vanishing and exploding gradients**: repeated multiplication by the recurrent Jacobian; the
  spectral radius decides which.
- **Gradient clipping** for the exploding half; **gating** for the vanishing half.
- **LSTM** (input/forget/output gates plus a cell with an additive path) and **GRU** (a
  two-gate simplification). The additive cell path is the mechanism — it makes the gradient path
  through time approximately linear.
- **Bidirectional RNNs**; **encoder–decoder / sequence-to-sequence** with a fixed-size context.
- **Attention** appears here as the fix for the encoder–decoder bottleneck.
- **Deep RNNs, recursive (tree-structured) nets, echo state networks, leaky units, skip
  connections through time.**

## Mental Models

- Read gating as **learned, data-dependent memory management**: the forget gate decides how long
  the additive highway stays open.
- Treat the fixed-size context vector in vanilla seq2seq as a **bottleneck** — the whole reason
  attention was invented.
- Expect **exposure bias** whenever you teacher-force: the model has never seen its own mistakes
  during training.

## Anti-patterns

- **Reaching for an RNN by default in 2026** for a task where a transformer is the standard
  baseline and the sequence fits in context.
- **Training a long-sequence RNN without gradient clipping.**
- **Ignoring the train/inference mismatch** in autoregressive generation.

## What changed after 2016

**The largest single delta in the book.** Attention, described here as an enhancement to
recurrent seq2seq, became the whole architecture with *Attention Is All You Need* (Vaswani et al.
2017) — one year after publication. Transformers replaced RNNs for essentially all large-scale
sequence work: parallel training over sequence positions, direct O(1) path length between any two
tokens, and much better scaling. What survived: gradient clipping, teacher forcing, exposure bias,
and the vanishing/exploding analysis. What returned: linear-time recurrent architectures
(S4/Mamba-style state-space models, 2021–2024) as a long-context alternative, which makes this
chapter's material relevant again rather than obsolete. **Confidence: high.**

**Read this chapter for the gradient-flow analysis, not for the architecture recommendation.**

## Key Takeaways

1. Learn the vanishing/exploding analysis here — it explains residual connections, LayerNorm
   placement, and state-space models alike.
2. Clip gradients whenever a recurrence is in the graph.
3. Treat this chapter's architecture advice as historical; treat its diagnosis as current.

## Connects To

- **Ch 8**: the same optimization pathologies, in the time dimension.
- **Ch 12**: NLP and speech applications built on these.
- **references/book_to_2026_delta.md**: the transformer displacement, in detail.
