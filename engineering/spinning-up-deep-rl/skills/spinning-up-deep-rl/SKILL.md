---
name: spinning-up-deep-rl
description: "Knowledge base from \"Spinning Up in Deep RL\" by Joshua Achiam (OpenAI, MIT-licensed). Use when applying Achiam's frameworks for RL fundamentals and MDPs, the model-free algorithm taxonomy, policy gradient derivations, the six reference algorithms (VPG, TRPO, PPO, DDPG, TD3, SAC), debugging silently-failing RL code, or running rigorous multi-seed RL experiments."
---

# Spinning Up in Deep RL

**Author**: Joshua Achiam (OpenAI) | **Source**: spinningup.readthedocs.io, MIT | **Chapters**: 20 | **Generated**: 2026-08-25

## How to Use This Skill

- **No argument** — load the core frameworks below
- **A topic** — ask about `advantage function`, `target networks`, `entropy regularization`;
  I resolve it through the Topic Index and read that chapter file
- **`chNN`** — I load that chapter's summary
- **"what chapters do you have?"** — the full index

```
/cs:spinning-up-deep-rl                      # core frameworks + chapter index
/cs:spinning-up-deep-rl entropy regularization   # topic index -> ch19, read that chapter
/cs:spinning-up-deep-rl ch09                 # one chapter summary
```

When you ask about something not in Core Frameworks, I read the relevant chapter file before
answering rather than guessing from the index.

---

## Core Frameworks & Mental Models

### The RL problem
`pi* = argmax_pi J(pi)`, where `J(pi) = E_{tau~pi}[R(tau)]`. Every algorithm approximates
this; where it substitutes a different objective (a Bellman residual, a surrogate), that
substitution is the source of its failure modes. Four value functions — `V^pi`, `Q^pi`, `V*`,
`Q*` — all obey Bellman self-consistency, and `a*(s) = argmax_a Q*(s,a)` is why Q-learning
is a viable family at all. Advantage `A^pi(s,a) = Q^pi(s,a) - V^pi(s)` is the relative-quality
signal policy gradients run on. (ch07)

### The two branching questions
Place any algorithm by asking: **does it have or learn a model**, and **what does it learn**
(policy, Q-function, value function, model). That generates the whole landscape. (ch08)

### Policy optimization vs Q-learning — the central trade-off
- **Policy optimization** is *principled: you directly optimize the thing you want.* Stable
  and reliable. On-policy, so it cannot reuse data, so it is sample-hungry.
- **Q-learning** only *indirectly* optimizes performance, by training `Q_theta` to satisfy a
  self-consistency equation. Many failure modes, so less stable. But substantially more
  sample efficient when it works, because it reuses everything.
- **Satisfying the Bellman equations well carries no guarantee of good policy performance.**
- The two are not exclusive — DDPG and SAC live between them deliberately. (ch08)

### The policy gradient template
`grad J = E[ sum_t grad log pi_theta(a_t|s_t) * Phi_t ]`. Five valid choices of `Phi_t`:
full return, reward-to-go, reward-to-go minus a baseline, `Q^pi`, and `A^pi`. All share an
expectation and differ in variance. Two rules get you from the first to the last:
- **Don't let the past distract you** — drop rewards obtained before the action. Those terms
  had zero mean and nonzero variance: pure noise.
- **Baselines** — by the EGLP lemma, any state-only `b(s)` can be added or subtracted freely.
  The standard choice is `V^pi(s_t)`, learned by MSE regression onto reward-to-go. (ch09)

### The policy-gradient loss is not a loss function
Its data distribution depends on the parameters, and it does not measure performance even in
expectation. Only at the current parameters, with data from those parameters, does it have
the negative gradient of performance. **You can send it to negative infinity while performance
craters, and it usually will. Only average return means anything.** (ch09)

### Broken RL code almost always fails silently
It runs fine; the agent just never learns. Usually something is computed with the wrong
equation, on the wrong distribution, or piped to the wrong place. **If it doesn't work, assume
there's a bug** before touching hyperparameters. Debug by measuring everything and reading the
code critically. The archetype is one missing `squeeze`: a `[N]` vs `[N,1]` shape mismatch is
broadcast-compatible, raises nothing, and silently turns the Bellman backup into an `[N,N]`
matrix. (ch10, ch12)

### Learn by doing
Write your own implementations, **shortest correct version** of each, **simplest algorithms
first**. VPG, DQN, A2C, PPO, DDPG, roughly in that order; ~250-300 lines each. Single-threaded
before parallel. **Iterate fast in simple environments — under 5 minutes turnaround at the
debug stage.** Do not attempt Atari or Humanoid before the toy task works. Read papers for
their ablations and supplementary material, but **do not overfit to paper details** (the
original DDPG's architecture, init scheme and batch norm are not strictly necessary) **or to
existing implementations** (their abstractions serve reuse, not your single use case). (ch10)

### Rigor: four standards
1. **Fair comparisons** — tune the baseline as hard as your method; never handicap it.
2. **Remove stochasticity as a confounder** — at least 3 seeds, 10 or more to be thorough.
   Two seed groups can produce curves that look like different distributions.
3. **High-integrity experiments** — launch fresh final runs and precommit to reporting them.
   Tuning produces hypotheses; final runs produce conclusions.
4. **Check each claim separately** — ablate every design decision. (ch10)

### The safe-step family (on-policy)
VPG takes an unconstrained gradient step, so a single bad step can collapse performance.
**TRPO** constrains the step in **KL-divergence between policies, not distance in parameter
space**, then backtracking-line-searches until the exact constraint holds. **PPO** drops the
constraint and instead **clips the objective so the policy gains nothing by moving far**,
which is first-order, far simpler, and empirically at least as good. (ch14, ch15, ch16)

### The overestimation family (off-policy)
DDPG amortizes the intractable continuous `max_a Q(s,a)` into a learned policy:
`max_a Q(s,a) ~= Q(s, mu(s))`. It needs a **replay buffer** (licensed because the Bellman
equation is indifferent to how data was collected) and **target networks** (because the target
otherwise depends on the parameters being trained). Its failure mode is **Q-value
overestimation, which the policy actively exploits**. **TD3** answers with clipped double-Q,
delayed policy updates and target policy smoothing. **SAC** adds **entropy regularization**,
making the explore-exploit trade-off an explicit coefficient `alpha`. (ch17, ch18, ch19)

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction.md) | Introduction | The missing middle step, Code Design Philosophy |
| [ch02](chapters/ch02-installation.md) | Installation | Install-then-verify, MuJoCo optionality |
| [ch03](chapters/ch03-algorithm-lineup.md) | Algorithms: What's Included and Why | The two lineages, on/off-policy trade-off, code template |
| [ch04](chapters/ch04-running-experiments.md) | Running Experiments | One flag per kwarg, ExperimentGrid, save-dir suffixes |
| [ch05](chapters/ch05-experiment-outputs.md) | Experiment Outputs | Tools not files, watch-then-measure |
| [ch06](chapters/ch06-plotting-results.md) | Plotting Results | `Performance` alias, prefix autocompletion, seed averaging |
| [ch07](chapters/ch07-key-concepts-in-rl.md) | Part 1: Key Concepts in RL | MDPs, four value functions, Bellman equations, advantage |
| [ch08](chapters/ch08-kinds-of-rl-algorithms.md) | Part 2: Kinds of RL Algorithms | Taxonomy, model bias, policy-opt vs Q-learning |
| [ch09](chapters/ch09-intro-to-policy-optimization.md) | Part 3: Intro to Policy Optimization | Log-derivative trick, EGLP lemma, reward-to-go, baselines |
| [ch10](chapters/ch10-spinning-up-as-a-researcher.md) | Spinning Up as a Deep RL Researcher | Learn by doing, three idea frames, four rigor standards |
| [ch11](chapters/ch11-key-papers-in-deep-rl.md) | Key Papers in Deep RL | 13-section topic map |
| [ch12](chapters/ch12-exercises.md) | Exercises | Problem Set 1 and 2, the silent DDPG bug |
| [ch13](chapters/ch13-benchmarks.md) | Benchmarks | The parity disclosure, family-specific metrics |
| [ch14](chapters/ch14-vpg.md) | Vanilla Policy Gradient | The six-step loop |
| [ch15](chapters/ch15-trpo.md) | Trust Region Policy Optimization | KL trust region, line search, conjugate gradient |
| [ch16](chapters/ch16-ppo.md) | Proximal Policy Optimization | PPO-Clip, KL early stopping |
| [ch17](chapters/ch17-ddpg.md) | Deep Deterministic Policy Gradient | MSBE, replay buffers, target networks, polyak |
| [ch18](chapters/ch18-td3.md) | Twin Delayed DDPG | Clipped double-Q, delayed updates, target smoothing |
| [ch19](chapters/ch19-sac.md) | Soft Actor-Critic | Entropy regularization, reparameterization, squashed Gaussian |
| [ch20](chapters/ch20-logger-and-utilities.md) | Logger, MPI Tools and Run Utils | EpochLogger pattern, MPI PyTorch order |

## Topic Index

- **Advantage function** ch07, ch09, ch14
- **Baselines** ch09
- **Bellman equations** ch07, ch17
- **Benchmarks / parity** ch13, ch01
- **Clipped double-Q** ch18, ch19
- **Continuous action spaces** ch07, ch17
- **Debugging / silent failure** ch10, ch12
- **DDPG** ch17, ch03, ch08
- **Entropy regularization** ch19
- **Exploration vs exploitation** ch14, ch17, ch19
- **GAE** ch09, ch14
- **Installation** ch02
- **KL divergence / trust region** ch15, ch16
- **Logging** ch20, ch05
- **MDPs** ch07
- **Model-based RL** ch08
- **MPI / parallelization** ch20, ch02, ch04
- **MSBE** ch17
- **Off-policy** ch03, ch08, ch17
- **On-policy** ch03, ch08, ch14
- **Papers / literature** ch11, ch10
- **Plotting** ch06, ch13
- **Policies (categorical, Gaussian, squashed)** ch07, ch19
- **Policy gradient derivation** ch09
- **PPO** ch16, ch03
- **Q-learning** ch08, ch07
- **Replay buffer** ch17
- **Reparameterization trick** ch19, ch10
- **Research process / rigor** ch10, ch13
- **Reward-to-go** ch09
- **Running experiments** ch04, ch05
- **SAC** ch19, ch03, ch08
- **Seeds / variance** ch10, ch13, ch04
- **Target networks / polyak** ch17, ch18
- **TD3** ch18, ch12
- **TRPO** ch15, ch03
- **Value functions** ch07, ch09
- **VPG** ch14, ch09

## Supporting Files

- [glossary.md](glossary.md) · [patterns.md](patterns.md) · [cheatsheet.md](cheatsheet.md)

## Scope & Limits

Covers the Spinning Up documentation only, as of the January 2020 PyTorch update. It does
**not** cover: DQN and the discrete-action value-learning family (referenced, never
implemented here), recurrent or convolutional architectures, partially-observed settings,
model-based implementations, exploration/meta-RL/hierarchy beyond ch11's reading list, or any
deep RL work after early 2020. The six implementations are educational; ch13 says which are
research-grade. For topics beyond this source, I say so rather than improvising.

---

*Compiled from OpenAI's Spinning Up in Deep RL documentation (MIT, Copyright (c) 2018 OpenAI),
primarily developed by Joshua Achiam. Structured study notes, not a reproduction of the source.*
