# Chapter 9: Part 3 — Intro to Policy Optimization

## Core Idea
Three results build the policy gradient you actually implement: the simplest analytical
expression for `grad J`, a rule that lets you **drop useless terms** (reward-to-go), and a
rule that lets you **add useful terms** (baselines) — ending at the advantage-weighted form
`grad J = E[ sum_t grad log pi_theta(a_t|s_t) * A^pi(s_t,a_t) ]`.

## Frameworks Introduced
- **The general policy gradient form**: every variant is
  `grad_theta J(pi_theta) = E_{tau~pi_theta}[ sum_{t=0}^{T} grad_theta log pi_theta(a_t|s_t) * Phi_t ]`
  and the whole subject is *which* `Phi_t` you choose. Five valid choices, all with the same
  expectation and different variance:
  1. `Phi_t = R(tau)` — the full trajectory return (the simplest form)
  2. `Phi_t = sum_{t'=t}^{T} R(s_t', a_t', s_{t'+1})` — the **reward-to-go**
  3. `Phi_t = reward-to-go - b(s_t)` — reward-to-go with a **baseline**
  4. `Phi_t = Q^{pi_theta}(s_t, a_t)`
  5. `Phi_t = A^{pi_theta}(s_t, a_t)` — the **advantage**, the one Spinning Up's VPG uses
  - When to use: choice 5 in practice; the list is the map for reading any policy gradient paper.

- **The derivation, in five facts.** Worth memorizing because every extension reuses them:
  1. `P(tau|theta) = rho_0(s_0) * prod_t P(s_{t+1}|s_t,a_t) * pi_theta(a_t|s_t)`
  2. **Log-derivative trick**: `grad_theta P(tau|theta) = P(tau|theta) * grad_theta log P(tau|theta)`
  3. `log P(tau|theta) = log rho_0(s_0) + sum_t [ log P(s_{t+1}|s_t,a_t) + log pi_theta(a_t|s_t) ]`
  4. **Gradients of environment functions are zero** — the environment has no dependence on theta,
     so `rho_0`, `P` and `R` all vanish under `grad_theta`.
  5. Therefore `grad_theta log P(tau|theta) = sum_t grad_theta log pi_theta(a_t|s_t)`.
  - Chained: expand the expectation, bring the gradient inside the integral, apply the
    log-derivative trick, return to expectation form, substitute fact 5.

- **The EGLP lemma (Expected Grad-Log-Prob)**: for any parameterized distribution `P_theta`,
  `E_{x~P_theta}[ grad_theta log P_theta(x) ] = 0`.
  - Proof in three lines: all distributions are normalized (`integral P_theta(x) = 1`); take
    the gradient of both sides (`= grad 1 = 0`); apply the log-derivative trick.
  - When to use: it is the engine behind both the drop rule and the add rule. The author notes
    it has no standard name in the literature but comes up often enough to deserve one.

- **"Don't let the past distract you" (the drop rule)**: agents should only reinforce actions
  on the basis of their **consequences**. Rewards obtained *before* an action have no bearing
  on how good that action was. Formally, all terms with `t' < t` are zero in expectation.
  - Why it is better, precisely: those dropped terms had **zero mean but nonzero variance** —
    they added pure noise to the sample estimate. Removing them reduces the number of sample
    trajectories needed.

- **Baselines (the add rule)**: an immediate consequence of EGLP is that for any function `b`
  depending only on state, `E_{a_t~pi}[ grad log pi(a_t|s_t) * b(s_t) ] = 0`. So you may add
  or subtract any such term without changing the gradient in expectation.
  - **The most common baseline is the on-policy value function `V^pi(s_t)`**, which empirically
    reduces variance and gives faster, more stable learning.
  - The conceptual appeal: it encodes the intuition that **if an agent gets what it expected,
    it should "feel" neutral about it.**
  - In practice `V^pi` cannot be computed exactly, so it is approximated by a network `V_phi`
    updated concurrently with the policy (so it always approximates the *most recent* policy).
    The simplest learning rule, used by VPG, TRPO, PPO and A2C, is mean-squared error:
    `phi_k = argmin_phi E_{s_t, Rhat_t ~ pi_k}[ (V_phi(s_t) - Rhat_t)^2 ]`, via one or more
    gradient steps starting from `phi_{k-1}`.

## Key Concepts
- **Policy gradient**: `grad_theta J(pi_theta)`. Algorithms that optimize this way are
  policy gradient algorithms — VPG and TRPO are; **PPO is often called one though this is
  slightly inaccurate.**
- **Reward-to-go**: `Rhat_t = sum_{t'=t}^{T} R(s_t', a_t', s_{t'+1})`.
- **Baseline**: any state-only function subtracted from the weight.
- **Sample estimate**: `ghat = (1/|D|) * sum_{tau in D} sum_t grad log pi_theta(a_t|s_t) * Phi_t`.
- **GAE (Generalized Advantage Estimation)**: the widely-used method for approximating the
  advantage function; Spinning Up's VPG, TRPO and PPO all use it. The book strongly advises
  studying the paper.
- **Epoch** (in this context): one experience-collection phase plus one policy gradient update.

## Code Examples
The whole simple algorithm is 128 lines (`spinup/examples/pytorch/pg_math/1_simple_pg.py`).
The three pieces that matter:

```python
# 1. Policy network
logits_net = mlp(sizes=[obs_dim] + hidden_sizes + [n_acts])

def get_policy(obs):
    return Categorical(logits=logits_net(obs))

def get_action(obs):
    return get_policy(obs).sample().item()

# 2. The "loss" whose gradient is the policy gradient
def compute_loss(obs, act, weights):
    logp = get_policy(obs).log_prob(act)
    return -(logp * weights).mean()

# 3. One gradient step
optimizer.zero_grad()
batch_loss = compute_loss(obs=..., act=..., weights=...)
batch_loss.backward()
optimizer.step()
```

Upgrading to reward-to-go changes one function and two lines:

```python
def reward_to_go(rews):
    n = len(rews)
    rtgs = np.zeros_like(rews)
    for i in reversed(range(n)):
        rtgs[i] = rews[i] + (rtgs[i+1] if i+1 < n else 0)
    return rtgs

# was:  batch_weights += [ep_ret] * ep_len
batch_weights += list(reward_to_go(ep_rews))
```

For a diagonal Gaussian policy, `log_prob(act)` returns per-component log probabilities of
shape `(batch, act_dim)` when RL needs shape `(batch,)`. Sum them:

```python
logp = get_policy(obs).log_prob(act).sum(axis=-1)
```

## Worked Example
**The policy gradient "loss" is not a loss function.** This is the single most consequential
warning in the chapter, and it differs from supervised learning in two ways:

1. **The data distribution depends on the parameters.** A supervised loss is defined on a
   fixed data distribution independent of the parameters being optimized. Here the data must
   be sampled from the most recent policy.
2. **It does not measure performance.** We care about `J(pi_theta)`, and this "loss" does not
   approximate it — not even in expectation. It is useful only because, *evaluated at the
   current parameters with data generated by those parameters*, it has the negative gradient
   of performance.

After the first gradient step there is no connection to performance at all. You can send
this loss to negative infinity while policy performance craters — and it usually will.
Researchers sometimes call this the policy "overfitting" to a batch; the phrase is
descriptive but should not be taken literally, since it does not refer to generalization error.

**The practical rule: in policy gradients, only average return means anything. The loss
function means nothing.** The ML habit of reading "loss went down, all is well" is wrong here.

## Anti-patterns
- **Using the loss curve as a training health signal.** See above. Watch `AverageEpRet`.
- **Weighting every action by the full-trajectory return** when reward-to-go is a two-line
  change that strictly reduces variance.
- **Forgetting to sum log-probabilities across action dimensions** for Gaussian policies —
  a shape bug that will not raise, in the same family as the ch12 DDPG bug.
- **Treating a baseline as a bias**: baselines are provably zero-mean under EGLP. They change
  variance, never the expected gradient.

## Key Takeaways
1. One template, five valid weights `Phi_t`; the advantage form is the destination.
2. The whole derivation rests on the log-derivative trick plus the fact that environment
   gradients vanish.
3. EGLP is a single lemma that licenses both dropping past rewards and adding baselines.
4. Reward-to-go removes terms with zero mean and nonzero variance — pure noise reduction.
5. The value baseline is learned by mean-squared regression onto reward-to-go, concurrently
   with the policy.
6. The policy gradient loss is not a performance measure and must never be read as one.

## Connects To
- **Ch 7**: the advantage function and value functions this chapter puts to work.
- **Ch 14**: VPG, the direct implementation of the final advantage-weighted form.
- **Ch 15 and Ch 16**: TRPO and PPO, which replace the plain gradient step with a
  trust-region-constrained one.
- **Ch 12**: Exercise 2.1 measures exactly what happens when `V_phi` is not fit properly.
