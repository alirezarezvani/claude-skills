# Chapter 19: Soft Actor-Critic (SAC)

## Core Idea
SAC optimizes a **stochastic** policy in an **off-policy** way, forming a bridge between
stochastic policy optimization and DDPG-style approaches. Its central feature is **entropy
regularization**: the policy is trained to maximize a trade-off between expected return and
the randomness of the policy.

## Quick Facts
- **Off-policy.**
- The version implemented here is **continuous action spaces only** — an alternate version,
  with a slightly changed policy update rule, can handle discrete action spaces.
- **Does not support parallelization.**
- SAC is **not a direct successor to TD3** — they were published roughly concurrently — but it
  incorporates the clipped double-Q trick, and its inherent policy stochasticity gives it
  something like target policy smoothing for free.

## Frameworks Introduced
- **Entropy-regularized RL.** Entropy `H(P) = E_{x~P}[-log P(x)]` says how random a random
  variable is: a coin that almost always comes up heads has low entropy, a fair coin has high
  entropy. The agent gets a bonus reward at each timestep proportional to policy entropy,
  changing the RL problem to:
  ```
  pi* = argmax_pi E_{tau~pi}[ sum_t gamma^t ( R(s_t,a_t,s_{t+1}) + alpha * H(pi(.|s_t)) ) ]
  ```
  `alpha > 0` is the trade-off coefficient. **This has a close connection to the
  exploration-exploitation trade-off: increasing entropy results in more exploration, which
  can accelerate learning later on, and can prevent the policy from prematurely converging to
  a bad local optimum.**

- **The modified value functions.** `V^pi` includes the entropy bonus from **every** timestep;
  `Q^pi` includes it from every timestep **except the first**. They connect by
  ```
  V^pi(s) = E_{a~pi}[ Q^pi(s,a) ] + alpha * H(pi(.|s))
          = E_{a~pi}[ Q^pi(s,a) - alpha * log pi(a|s) ]
  ```
  **This setup is a little bit arbitrary** — you could instead have `Q^pi` include the first
  timestep's bonus — and **the choice of definition varies slightly across papers on the
  subject.** Check before comparing equations across sources.

- **What SAC keeps from TD3, and what it changes.** SAC learns a policy `pi_theta` and two
  Q-functions `Q_phi_1`, `Q_phi_2`.
  - **Same as TD3**: both Q-functions learned by MSBE minimization regressing to a **single
    shared target**; the target computed using **target Q-networks obtained by polyak
    averaging**; the **clipped double-Q trick**.
  - **Different from TD3**: (1) the target includes an **entropy regularization term**;
    (2) the **next-state actions in the target come from the current policy, not a target
    policy**; (3) **no explicit target policy smoothing** — TD3 trains a deterministic policy
    and so needs added noise to smooth, whereas **SAC's policy stochasticity is sufficient to
    get a similar effect**.

- **The Q-loss.** Rewrite the entropy-regularized Bellman equation using
  `H = -log pi`, approximate the expectation with samples, and take the min over the two
  critics:
  ```
  y(r,s',d) = r + gamma*(1-d) * ( min_{j=1,2} Q_{phi_j,targ}(s', a'~) - alpha * log pi_theta(a'~|s') )
  where a'~ ~ pi_theta(.|s')
  ```
  **Notation matters here:** `r` and `s'` come from the **replay buffer**, but `a'~` must be
  **sampled fresh from the current policy** — hence the tilde. Mixing these up is a silent bug.

- **Policy learning via the reparameterization trick.** The policy should maximize `V^pi(s)`,
  i.e. `E_{a~pi}[ Q^pi(s,a) - alpha log pi(a|s) ]`. The expectation's distribution depends on
  the policy parameters, which is the pain point; the reparameterization trick rewrites it as
  an expectation over **noise**, which has no parameter dependence. Using a **squashed Gaussian
  policy**:
  ```
  a~_theta(s, xi) = tanh( mu_theta(s) + sigma_theta(s) * xi ),   xi ~ N(0, I)
  ```
  giving the policy objective
  ```
  max_theta E_{s~D, xi~N}[ min_{j=1,2} Q_phi_j(s, a~_theta(s,xi)) - alpha * log pi_theta(a~_theta(s,xi)|s) ]
  ```
  **almost the same as DDPG and TD3 policy optimization, except for the min-double-Q trick,
  the stochasticity, and the entropy term.** Note that unlike TD3 (which uses `Q_phi_1` only),
  **SAC uses the min of the two approximators in the policy loss too.**

## Reference Tables

**Two ways SAC's policy differs from the VPG/TRPO/PPO policies** — both are load-bearing:

| Difference | SAC | VPG / TRPO / PPO |
|-----------|-----|------------------|
| **Squashing function** | `tanh` ensures actions are bounded to a finite range. Before the tanh the policy is a factored Gaussian; after it, it is not. Log-probabilities are still computable in closed form (see the paper appendix) | No squashing |
| **Std dev parameterization** | log stds are **outputs of the neural network**, so they depend on state in a complex way | log stds are **state-independent parameter vectors** |

**SAC with state-independent log std devs, in the authors' experience, did not work.**

| Variant | Status |
|---------|--------|
| Fixed entropy coefficient `alpha` | What Spinning Up implements, for simplicity |
| Entropy-constrained (varies `alpha` over training) | **Generally preferred by practitioners** |
| Older SAC that also learns a value function `V_psi` | Superseded; the docs cover the modern version that omits it |

## Exploration vs. Exploitation
SAC trains a stochastic policy with entropy regularization and explores **on-policy**.
**`alpha` explicitly controls the explore-exploit trade-off** — higher means more exploration,
lower means more exploitation. **The right coefficient may vary from environment to environment
and could require careful tuning.** At test time, **remove the stochasticity and use the mean
action instead of a sample**; this tends to improve performance over the stochastic policy.
(This is why `test_policy` has a SAC-only `--deterministic` flag — see ch5.) `start_steps`
uniform-random exploration at the beginning applies here too.

## Anti-patterns
- **Evaluating SAC with the stochastic policy.** The correct evaluation policy is the
  deterministic mean; `test_policy` defaults to the stochastic one and needs `-d`.
- **Using state-independent log stds in SAC** because that is what PPO does. It did not work.
- **Sampling the target's next action from the replay buffer.** It must come fresh from the
  current policy.
- **Assuming SAC's `Q^pi` definition matches another paper's.** The placement of the
  first-timestep entropy bonus is a convention that varies.
- **Treating `alpha` as a set-and-forget constant across environments.** It is the
  explore-exploit dial and is environment-specific; the entropy-constrained variant exists
  because tuning it by hand is hard.

## Key Takeaways
1. Entropy regularization is the defining feature: maximize return plus `alpha` times policy
   entropy, which directly controls exploration.
2. SAC keeps TD3's clipped double-Q and polyak targets, adds an entropy term to the target,
   uses the current policy (not a target policy) for next-state actions, and needs no explicit
   smoothing.
3. The squashed Gaussian plus reparameterization trick makes the stochastic policy
   differentiable end to end.
4. SAC uses `min` over both critics in the policy loss; TD3 uses only `Q_phi_1`.
5. State-dependent log stds are required — state-independent ones did not work.
6. Evaluate with the mean action. Spinning Up ships the fixed-`alpha` variant; practitioners
   generally prefer the entropy-constrained one.

## Connects To
- **Ch 18**: TD3, whose clipped double-Q trick SAC borrows and whose smoothing it obviates.
- **Ch 7**: the diagonal Gaussian policy and the two ways of parameterizing log stds.
- **Ch 5**: the SAC-only `--deterministic` flag on `test_policy`.
- **Ch 10**: the reparameterization trick is on the required deep-learning background list.
