# Cheatsheet

Decision rules and thresholds. One line each; the chapter has the reasoning.

## Loss selection (ch03, ch06)

| Target | Distribution | Output unit | Loss |
|---|---|---|---|
| Real, unbounded | Gaussian | linear | MSE |
| Binary | Bernoulli | sigmoid | binary cross-entropy |
| One of K | Categorical | softmax | cross-entropy |
| Real, heavy-tailed | Laplace | linear | MAE |
| Multimodal real | Mixture | mixture density | NLL of the mixture |

Never pair sigmoid output with MSE — the gradient vanishes where the model is most wrong.

## Underfit vs overfit (ch05, ch11)

| Train error | Val error | Verdict | First action |
|---|---|---|---|
| High | High | Underfit / optimization | Check LR, init, capacity — **not** more data |
| Low | High | Overfit | More data → augmentation → regularization |
| Low | Low | Working | Stop; check the metric is the right one |
| ~0 on 20 examples: fails | — | Bug | Fix the pipeline before anything else |

Past the interpolation threshold, prefer more data / longer training / more regularization over
shrinking the model (double descent, ch05).

## Optimizer defaults (ch08)

| Situation | Reach for |
|---|---|
| Any starting point | AdamW, LR ~1e-3 (small nets) / ~1e-4 (large), warmup + cosine decay |
| Recurrence in the graph | Add gradient clipping, always |
| Tiny batches | Group/layer norm, not batch norm |
| Loss flat, grad norm large | Ill-conditioning — momentum, adaptive, or normalization |
| Loss NaN | Numerics first: log(0), div by ~0, exp overflow, exploding grad |

## Regularization ladder (ch07)

More real data → label-preserving augmentation → early stopping → decoupled weight decay →
label smoothing → dropout → smaller model. One at a time; measure the gap after each.

## Architecture prior (ch09, ch10)

| Data | Prior that fits | Note |
|---|---|---|
| Grid, translation-invariant statistics | Convolution | Cheapest when data is limited |
| Sequence, long-range dependence | Attention/transformer | The 2016 RNN advice is superseded |
| Sequence, very long context | State-space / linear recurrence | Post-2016; ch10's gradient analysis applies |
| Arbitrary tabular columns | Neither | Locality prior is false |

## Generative model taxonomy (ch20)

| Family | Handles Z by | Characteristic failure |
|---|---|---|
| Autoregressive | Chain rule — no Z | Slow sequential sampling |
| VAE | Bounding likelihood (ELBO) | Blurry samples |
| GAN | Avoiding likelihood | Mode collapse, unstable training |
| Diffusion / score-based | Learning ∇ log p | Many sampling steps (mitigable) |
| Boltzmann machines | Sampling the negative phase | Historical; do not start here |

## Numerical hygiene (ch04)

Log-space for probability products · stabilized/fused softmax and cross-entropy · clip gradients
with recurrence · bf16 over fp16 when range matters · check condition number before blaming LR.

## Study-order rule (ch01–ch20)

Ch 5 and Ch 11 are the highest-value chapters for a practitioner and can be read early.
Ch 2–4 are prerequisites for Ch 8 specifically. Ch 13→14→19→20 is the only strict chain in
Part III. Ch 18 is worth reading even if you never train an undirected model — score matching
became diffusion.
