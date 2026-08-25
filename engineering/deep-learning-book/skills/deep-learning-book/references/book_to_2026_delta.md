# The 2016 → 2026 Delta

The book was published in 2016. *Attention Is All You Need* appeared in 2017. Everything below
tracks what a reader should hold, discount, or replace — per chapter, with a confidence level on
each claim.

Confidence levels: 🟢 well-established and replicated · 🟡 supported but contested or
context-dependent · 🔴 folklore, named as folklore.

---

## Chapters that aged well (read as current)

| Ch | Why it holds |
|---|---|
| 2, 3, 4 | Mathematics does not age. 🟢 |
| 5 | The learning-theory frame is current — with one correction (double descent, below). 🟢 |
| 11 | The practical workflow became the backbone of MLOps practice. 🟢 |
| 16 | The directed/undirected taxonomy classifies models invented since, including transformers as chain-rule factorizations. 🟢 |
| 18 | Score matching became diffusion; NCE became contrastive learning. The chapter's ideas travelled further than its models. 🟢 |

## The five corrections that matter

### 1. Double descent qualifies the U-curve (ch05)

The classical capacity curve — error falls, then rises past the optimum — is incomplete. Past the
interpolation threshold, test error can descend a second time. Belkin et al. (2019) named it;
Nakkiran et al. (2020) showed model-wise, epoch-wise and sample-wise variants in deep networks.
The bias–variance algebra is unchanged; the *advice* "shrink the model when it overfits" is no
longer the only correct move. 🟢

### 2. AdamW: weight decay ≠ L2 under adaptive optimizers (ch07, ch08)

Adding an L2 term to the loss and applying weight decay to the update are equivalent for plain
SGD and **not** equivalent for Adam, because the adaptive denominator rescales the penalty.
Loshchilov & Hutter (2017/2019) decoupled them; AdamW is now the default. The book's Ch 7 treats
the two as interchangeable. 🟢

### 3. Transformers displaced recurrence (ch10, ch12)

Vaswani et al. (2017) removed recurrence entirely: attention gives an O(1) path between any two
positions and parallelizes over sequence length. What survives from Ch 10: the vanishing/exploding
gradient analysis, gradient clipping, teacher forcing, exposure bias. What is superseded: the
architecture recommendation. Note the return of linear-time recurrence in state-space models
(S4, 2021; Mamba, 2023) for long context — which makes Ch 10's analysis live again. 🟢

### 4. Diffusion displaced the Part III generative models (ch14, ch18, ch20)

The line runs directly through the book: denoising autoencoders (Ch 14) → denoising score
matching (Ch 18) → score-based generative models (Song & Ermon, 2019) → DDPM (Ho et al., 2020).
Diffusion now dominates image, audio and video generation; autoregressive transformers dominate
text. VAEs survive mainly as latent-space compressors inside latent-diffusion pipelines. GANs
remain useful for few-step generation. Boltzmann machines are historical. 🟢

### 5. Self-supervised learning vindicated Ch 15 while replacing its methods

The chapter's bet — that unsupervised representation learning would matter — was right, and every
specific method it lists was replaced. Contrastive (SimCLR, MoCo, CLIP), masked prediction (BERT,
MAE) and next-token prediction at scale are the modern routes. Two corrections: greedy layer-wise
pretraining is now purely historical 🟢, and unsupervised disentanglement was shown impossible
without inductive biases or supervision (Locatello et al., 2019) 🟢.

## Additions the book has no chapter for

| Topic | Status |
|---|---|
| **Neural scaling laws** (Kaplan 2020; Hoffmann 2022) | Quantifies Ch 1's "scale matters" and Ch 11's data-vs-capacity decision. 🟢 |
| **Normalization placement** — pre-norm vs post-norm residual, LayerNorm/RMSNorm over BatchNorm | Standard for deep sequence stacks. 🟢 |
| **Warmup + cosine decay schedules** | Standard for transformer training. 🟢 |
| **Calibration** (Guo et al., 2017) | Modern networks are systematically overconfident; temperature scaling is the cheap fix. Ch 3 does not mention it. 🟢 |
| **RLHF / DPO alignment** | Entirely outside the book. 🟢 |
| **Mixture-of-Experts** | The mature form of Ch 12's conditional computation. 🟢 |
| **Mixed precision (fp16 loss scaling, bf16)** | Made Ch 4's numerics an operational daily concern. 🟢 |
| **Lottery-ticket / pruning theory** (Frankle & Carbin, 2019) | Active; the strong form remains contested. 🟡 |
| **"Batch norm works by reducing internal covariate shift"** | The original explanation; challenged by Santurkar et al. (2018), who attribute the effect to smoothing the loss landscape. Treat the mechanism as unsettled. 🟡 |
| **"Local minima are the problem in deep nets"** | 🔴 Folklore the book itself corrects: high-dimensional critical points are overwhelmingly saddles (Ch 8). |
| **"You need a GPU cluster to learn deep learning"** | 🔴 Folklore. Every mechanism in Parts I–II is observable on a laptop-scale model. |

## How to use this file

When a chapter's advice conflicts with current practice, the conflict is almost always in the
**recommendation**, not the **analysis**. The book explains why things fail; the field has changed
what it reaches for. Keep the diagnosis, replace the prescription.

## Sources

1. Vaswani et al., "Attention Is All You Need," NeurIPS 2017 — arXiv:1706.03762.
2. Loshchilov & Hutter, "Decoupled Weight Decay Regularization," ICLR 2019 — arXiv:1711.05101.
3. Belkin, Hsu, Ma & Mandal, "Reconciling modern machine-learning practice and the classical
   bias–variance trade-off," PNAS 116(32), 2019; Nakkiran et al., "Deep Double Descent," ICLR 2020.
4. Ho, Jain & Abbeel, "Denoising Diffusion Probabilistic Models," NeurIPS 2020 — arXiv:2006.11239;
   Song & Ermon, "Generative Modeling by Estimating Gradients of the Data Distribution,"
   NeurIPS 2019.
5. Kaplan et al., "Scaling Laws for Neural Language Models," 2020 — arXiv:2001.08361;
   Hoffmann et al., "Training Compute-Optimal Large Language Models," 2022 — arXiv:2203.15556.
6. Locatello et al., "Challenging Common Assumptions in the Unsupervised Learning of Disentangled
   Representations," ICML 2019 (best paper) — arXiv:1811.12359.
7. Guo, Pleiss, Sun & Weinberger, "On Calibration of Modern Neural Networks," ICML 2017;
   Santurkar et al., "How Does Batch Normalization Help Optimization?," NeurIPS 2018.
8. Dosovitskiy et al., "An Image is Worth 16x16 Words" (ViT), ICLR 2021 — arXiv:2010.11929;
   Liu et al., "A ConvNet for the 2020s" (ConvNeXt), CVPR 2022.
