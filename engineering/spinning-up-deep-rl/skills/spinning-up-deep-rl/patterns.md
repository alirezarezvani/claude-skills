# Patterns

Concrete techniques from Spinning Up, each with when to use it, how it works, and what it costs.

## Reward-to-Go Weighting
**When to use** — always, over full-trajectory-return weighting. It is a two-line change.
**How** — weight each `grad log pi(a_t|s_t)` by `sum_{t'=t}^T r_t'` instead of `R(tau)`.
**Trade-offs** — strictly reduces variance at no cost. The dropped terms had zero mean and
nonzero variance, so removing them removes pure noise and cuts the sample trajectories needed.
(Ch 9)

## Value Function Baseline
**When to use** — any policy gradient method. Standard in VPG, TRPO, PPO and A2C.
**How** — subtract `V_phi(s_t)` from the weight; fit `V_phi` by minimizing
`E[(V_phi(s_t) - Rhat_t)^2]` with one or more gradient steps per epoch, starting from the
previous parameters, so it tracks the most recent policy.
**Trade-offs** — provably unbiased by EGLP; reduces variance and gives faster, more stable
learning. Costs a second network and its fitting budget. Under-fitting it is one of the most
drastic performance failures in policy gradients (Exercise 2.1). (Ch 9, Ch 12)

## Trust Region via KL Constraint
**When to use** — when a single bad policy gradient step can collapse performance, and you
can afford second-order machinery.
**How** — maximize surrogate advantage subject to `Dbar_KL <= delta`; Taylor-expand, solve
analytically via Lagrangian duality, then backtracking line search until the exact KL
constraint holds and surrogate advantage is positive. Use conjugate gradient for `H^{-1}g`.
**Trade-offs** — buys monotone-ish, fast improvement and larger safe steps. Costs complexity,
Hessian-vector products, and (in Spinning Up) no PyTorch implementation. (Ch 15)

## Clipped Surrogate Objective
**When to use** — as the first-order replacement for a trust region. The default modern choice.
**How** — `L = min(ratio * A, g(eps, A))` where `g` caps at `(1+eps)A` for positive advantage
and `(1-eps)A` for negative. Take multiple minibatch SGD steps per batch.
**Trade-offs** — much simpler than TRPO and empirically at least as good, but it removes the
*incentive* to move far rather than guaranteeing you do not. Pair it with KL early stopping.
(Ch 16)

## KL Early Stopping
**When to use** — alongside clipping, whenever you take many gradient steps per batch.
**How** — if the mean KL-divergence of the new policy from the old exceeds a threshold, stop
taking gradient steps for this batch.
**Trade-offs** — one extra measurement per step; catches the drift the clip alone allows.
Other PPO implementations use different tricks here. (Ch 16)

## Experience Replay Buffer
**When to use** — every off-policy value-learning algorithm.
**How** — store `(s,a,r,s',d)` tuples; sample minibatches uniformly for MSBE minimization.
Licensed by the fact that the Bellman equation is indifferent to how transitions were collected.
**Trade-offs** — wrong in both directions. Too small and you overfit to the most recent data
and things break; too large and learning slows. It needs tuning. (Ch 17)

## Target Networks
**When to use** — any MSBE minimization, because the target otherwise depends on the
parameters being trained.
**How** — keep a lagged copy. DQN-style: copy every fixed number of steps. DDPG-style:
polyak average once per main update, `phi_targ <- rho*phi_targ + (1-rho)*phi`, `rho` near 1.
**Trade-offs** — stabilizes learning; adds a network and a hyperparameter, and slows the
propagation of new information into the target. (Ch 17)

## Amortizing a Continuous Argmax into a Policy
**When to use** — an inner `max` over a continuous variable inside a loop you run constantly.
**How** — assume differentiability with respect to that variable, learn `mu_theta(s)` by
gradient ascent on `Q_phi(s, mu_theta(s))`, and substitute `max_a Q(s,a) ~= Q(s, mu(s))`.
**Trade-offs** — turns an intractable per-step optimization into a forward pass. Costs an
approximation whose errors the policy will actively exploit. (Ch 17)

## Clipped Double-Q
**When to use** — whenever a learned Q-function is being maximized over by a policy, i.e.
the whole DDPG family.
**How** — learn two Q-functions, use `min` of the two target values as the shared regression
target for both.
**Trade-offs** — fends off overestimation, which is DDPG's dominant failure. Costs a second
critic and introduces some underestimation bias. TD3 uses `Q_phi_1` alone in the policy loss;
SAC uses the `min` there too. (Ch 18, Ch 19)

## Delayed Policy Updates
**When to use** — when policy updates destabilize the Bellman target.
**How** — update the policy and all target networks once per `policy_delay` critic updates;
the paper recommends 2.
**Trade-offs** — damps volatility; slows policy improvement per environment step. (Ch 18)

## Target Policy Smoothing
**When to use** — deterministic policies over continuous actions.
**How** — `a'(s') = clip(mu_targ(s') + clip(eps, -c, c), a_Low, a_High)`, `eps ~ N(0, sigma)`.
**Trade-offs** — regularizes Q along the action dimension so a spurious sharp peak cannot be
exploited. A stochastic policy (SAC) gets a similar effect for free. (Ch 18, Ch 19)

## Entropy Regularization
**When to use** — when premature convergence to a bad local optimum is the risk, or when you
want an explicit explore-exploit dial.
**How** — add `alpha * H(pi(.|s_t))` to the reward at each timestep; propagate the term into
the value functions and the Bellman target.
**Trade-offs** — higher `alpha` means more exploration and faster later learning; the right
value is environment-specific and needs careful tuning. The entropy-constrained variant that
adapts `alpha` is generally preferred by practitioners over the fixed one. (Ch 19)

## Reparameterization Trick for Stochastic Policies
**When to use** — differentiating through an expectation whose distribution depends on the
parameters.
**How** — sample by a deterministic function of state, parameters and independent noise:
`a~ = tanh(mu_theta(s) + sigma_theta(s) * xi)`, `xi ~ N(0,I)`, converting the expectation over
actions into an expectation over noise.
**Trade-offs** — makes the policy differentiable end to end. The `tanh` squash bounds actions
but changes the distribution; log-probabilities are still closed-form. (Ch 19)

## Uniform Random Warm-Up (start_steps)
**When to use** — every off-policy algorithm here, at the beginning of training.
**How** — for a fixed number of steps take actions sampled uniformly over valid actions, then
switch to normal exploration.
**Trade-offs** — fills the replay buffer with diverse data before the policy can bias it.
Wasted steps if the environment is expensive. (Ch 17, Ch 18, Ch 19)

## Multi-Seed Reporting with Variance Bands
**When to use** — every reported RL result.
**How** — at least 3 seeds, 10 or more to be thorough; plot the mean as a solid line and the
standard deviation as a shaded band; smooth for display only.
**Trade-offs** — multiplies compute by the seed count. Without it, deep RL's seed sensitivity
means two seed groups can look like different distributions entirely. (Ch 10, Ch 13)

## Precommitted Final Runs
**When to use** — before reporting any comparison.
**How** — use the tuning stage to form hypotheses, then launch fresh final experiments for
every method compared and commit in advance to reporting whatever comes out.
**Trade-offs** — a weak form of preregistration; costs one more full experiment round and
removes the largest source of accidental self-deception. (Ch 10)

## Per-Claim Ablation
**When to use** — any method with more than one design decision, which is all of them.
**How** — swap out or remove each design element separately and measure.
**Trade-offs** — turns one bundled claim into several separately-confident ones. Costs one
experiment per element. Also the fastest way to learn which parts you can delete. (Ch 10)
