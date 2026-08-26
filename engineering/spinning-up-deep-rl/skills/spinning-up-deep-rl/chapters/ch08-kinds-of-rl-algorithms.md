# Chapter 8: Part 2 — Kinds of RL Algorithms

## Core Idea
Two branching questions organize modern RL: does the agent have or learn a **model** of the
environment, and **what does it learn** — a policy, a Q-function, a value function, or a
model. Every trade-off in algorithm design descends from those two choices.

## Frameworks Introduced
- **Branch 1: model-free vs model-based.** A model is a function predicting state transitions
  and rewards.
  - **Upside of a model: it allows the agent to plan** — think ahead, see what would happen
    across options, explicitly decide, then distil the planning results into a learned policy.
    AlphaZero is the famous case. When it works, it substantially improves sample efficiency.
  - **Downside: a ground-truth model is usually not available**, so it must be learned from
    experience, and **bias in a learned model gets exploited by the agent** — producing an
    agent that performs well against its own model and sub-optimally, or terribly, in the
    real environment. Model-learning is fundamentally hard; large amounts of time and compute
    can fail to pay off.
  - When to use model-based: you have a reliable model, or sample efficiency dominates and
    you can afford the model-bias risk.

- **Branch 2: what to learn in model-free RL — two families.**
  - **Policy Optimization.** Represent the policy explicitly as `pi_theta(a|s)` and optimize
    theta either directly by gradient ascent on `J(pi_theta)` or indirectly by maximizing
    local approximations of it. Almost always **on-policy**. Usually also learns an
    approximator `V_phi(s)` used in figuring out the policy update. Examples: A2C/A3C
    (direct), PPO (indirect, via a surrogate objective giving a conservative estimate of how
    much `J` will change).
  - **Q-Learning.** Learn an approximator `Q_theta(s,a)` to `Q*(s,a)`, usually with an
    objective based on the Bellman equation. Almost always **off-policy**. The policy comes
    from the connection `a(s) = argmax_a Q_theta(s,a)`. Examples: DQN, C51 (which learns a
    distribution over return whose expectation is `Q*`).

- **The policy-optimization vs Q-learning trade-off** (the single most quoted judgment in
  this book):
  - Policy optimization is **principled — you directly optimize for the thing you want** —
    which tends to make it stable and reliable.
  - Q-learning only *indirectly* optimizes agent performance, by training `Q_theta` to satisfy
    a self-consistency equation. **There are many failure modes for this kind of learning, so
    it tends to be less stable.**
  - But when Q-learning works it is **substantially more sample efficient**, because it can
    reuse data far more effectively.
  - How to use: pick the failure you can detect and afford. Instability you can see in a
    learning curve; sample inefficiency you can see in a compute bill.

- **The interpolation principle**: policy optimization and Q-learning are not incompatible,
  and under some circumstances turn out to be *equivalent* (Schulman et al 2017). A range of
  algorithms lives between them and trades off deliberately: **DDPG** (learns a deterministic
  policy and a Q-function that improve each other) and **SAC** (a variant using stochastic
  policies, entropy regularization and other tricks to stabilize learning; scores higher than
  DDPG on standard benchmarks).

- **Four ways to use a model** (there is no small set of clean clusters here; the model may
  be given or learned in each):
  1. **Pure planning** — never represent the policy at all. Model-predictive control (MPC):
     each time the agent observes, compute a plan optimal with respect to the model over a
     fixed window, execute only the first action, discard the rest, re-plan next step. Future
     rewards past the horizon can enter through a learned value function. Example: MBMF.
  2. **Expert iteration** — keep an explicit policy `pi_theta`, use a planning algorithm
     (e.g. Monte Carlo Tree Search) inside the model with candidate actions sampled from the
     current policy. The planner's output is an "expert" relative to the policy; update the
     policy toward it. Examples: ExIt, AlphaZero.
  3. **Data augmentation for model-free methods** — train a policy or Q-function with a
     model-free algorithm, but augment real experience with fictitious experience (MBVE), or
     train on purely fictitious experience ("training in the dream", World Models).
  4. **Embedding planning loops into policies** — make the planning procedure a subroutine of
     the policy so complete plans become side information, and train the policy output with
     any standard model-free algorithm. **The key advantage: model bias becomes less of a
     problem, because where the model is bad for planning the policy can learn to ignore it.**
     Example: I2A.

## Key Concepts
- **Model of the environment**: a function predicting state transitions and rewards.
- **Surrogate objective**: a local approximation of `J(pi_theta)` that is safe to maximize;
  the mechanism behind TRPO and PPO.
- **The deadly triad**: function approximation + bootstrapping + off-policy data, which
  together cause instability in value-learning algorithms (Sutton and Barto ch. 11.3). This
  is the concrete content of "Q-learning has many failure modes."
- **Modularity caveat**: the taxonomy is a tree and the real space is not. Advanced areas —
  exploration, transfer learning, meta learning — are omitted from it entirely.

## Reference Tables

| Choice | Buys you | Costs you |
|--------|----------|-----------|
| Model-based | Planning; large sample-efficiency gains when the model is good | Model must usually be learned; model bias gets exploited |
| Model-free | Easier to implement and tune; more developed and tested | Forfeits the sample-efficiency gains a model could give |
| Policy optimization | Stability, reliability, directly optimizes performance | Sample inefficiency (on-policy data only) |
| Q-learning | Substantial sample efficiency through data reuse | Instability; no guarantee good Bellman fit means good policy |

## Mental Models
- **Place any new algorithm with two questions**: model or no model, and what does it learn.
  That is what the taxonomy is for; it does not need to be exhaustive to do that job.
- **Model bias is an adversarial problem, not a noise problem.** The agent is actively
  optimizing against your model's errors. That is why "the model is only 95% accurate" does
  not translate into "the policy is 95% as good."
- **"Directly optimize the thing you want" is a design principle you can apply outside RL**:
  the further your training objective sits from your evaluation metric, the more failure modes
  you inherit.

## Anti-patterns
- **Reading the taxonomy as exhaustive or as a strict tree.** The book opens with that
  disclaimer: algorithm modularity is not well represented by a tree.
- **Assuming model-based is strictly better because it plans.** As of the guide's writing
  (September 2018), model-free methods were more popular and more extensively developed and
  tested, precisely because model-learning is hard.
- **Treating "it fits the Bellman equation well" as evidence the policy is good.** No such
  guarantee exists — this is the defining weakness of the whole Q-learning family.

## Key Takeaways
1. Two branching questions — model or not, and what to learn — generate the whole landscape.
2. Policy optimization: principled, stable, sample-hungry. Q-learning: sample-efficient,
   indirect, unstable.
3. The two families are not exclusive; DDPG and SAC live between them on purpose.
4. Model bias is exploited by the agent, which is the central risk of model-based methods.
5. Embedding a planner inside a policy is the model-based approach that most directly
   defuses model bias, because the policy can learn when to ignore the model.

## Connects To
- **Ch 3**: the six implemented algorithms, which are all model-free.
- **Ch 9**: the mathematics of the policy-optimization family.
- **Ch 17 and Ch 19**: DDPG and SAC as the concrete interpolations named here.
- **Ch 11**: the key-papers list, whose top-level sections mirror this taxonomy.
