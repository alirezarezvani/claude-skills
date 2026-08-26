# Chapter 17: Deep Deterministic Policy Gradient (DDPG)

## Core Idea
DDPG concurrently learns a Q-function and a policy: it uses off-policy data and the Bellman
equation to learn the Q-function, and uses the Q-function to learn the policy. It exists
because `max_a Q*(s,a)` — trivial over discrete actions — is intractable over continuous ones,
and DDPG replaces that max with a learned, differentiable approximation.

## Quick Facts
- **Off-policy.**
- **Continuous action spaces only.**
- Can be thought of as **deep Q-learning for continuous action spaces.**
- The Spinning Up implementation **does not support parallelization.**

## Frameworks Introduced
- **The continuous-argmax problem, and the substitution that solves it.** With finitely many
  discrete actions, the max poses no problem — compute Q for each and compare, which also
  immediately hands you the maximizing action. With a continuous action space you cannot
  exhaustively evaluate, and a general optimization subroutine would have to run **every time
  the agent wants to take an action**, which is unacceptable. But because the action space is
  continuous, `Q*(s,a)` is presumed **differentiable with respect to the action** — so you can
  learn a policy `mu(s)` by gradient ascent and approximate
  `max_a Q(s,a) ~= Q(s, mu(s))`.
  - When to use this pattern: any time an inner argmax over a continuous variable sits inside
    an outer loop. Amortize it into a learned function.

- **Mean-Squared Bellman Error (MSBE)** — the loss that all deep Q-learning minimizes:
  ```
  L(phi, D) = E_{(s,a,r,s',d) ~ D}[ ( Q_phi(s,a) - ( r + gamma*(1-d)*max_a' Q_phi(s',a') ) )^2 ]
  ```
  `d` indicates whether `s'` is terminal, using the Python convention of `True` as 1: when
  `d == True` the Q-function should show the agent gets no additional reward after this state.

- **Trick One: Replay Buffers.** All standard algorithms training a deep network to approximate
  `Q*(s,a)` use an experience replay buffer — the set `D` of previous experiences.
  - **The buffer size is a real tuning decision, in both directions:** it should be large
    enough to contain a wide range of experiences, but keeping everything may not be good
    either. **Use only the very-most recent data and you overfit to it and things break; use
    too much experience and you may slow down learning.**
  - **Why old data is admissible at all** — this is the cleanest statement of what off-policy
    means: **the Bellman equation does not care which transition tuples are used, how the
    actions were selected, or what happens after a given transition**, because the optimal
    Q-function must satisfy it for *all* possible transitions. So any transition you have ever
    experienced is fair game for MSBE minimization.

- **Trick Two: Target Networks.** The target `r + gamma*(1-d)*max_a' Q_phi(s',a')` depends on
  the same parameters `phi` being trained, which makes MSBE minimization unstable. The fix is
  a second network that lags the first, with parameters `phi_targ`.
  - **DQN-style**: copy the main network into the target every fixed number of steps.
  - **DDPG-style**: **polyak averaging**, once per main network update:
    `phi_targ <- rho * phi_targ + (1-rho) * phi`, with `rho` in (0,1), usually close to 1.
    (`rho` is called `polyak` in the code.)

- **DDPG detail: the max in the target.** Since the max over continuous actions is the original
  problem, DDPG uses a **target policy network** `mu_theta_targ` to compute an action that
  approximately maximizes `Q_phi_targ`, found the same way as the target Q-function — by
  polyak averaging the policy parameters over training. Final Q-loss:
  ```
  L(phi,D) = E[ ( Q_phi(s,a) - ( r + gamma*(1-d)*Q_phi_targ(s', mu_theta_targ(s')) ) )^2 ]
  ```

- **Policy learning is one line**: maximize `E_{s~D}[ Q_phi(s, mu_theta(s)) ]` by gradient
  ascent **with respect to policy parameters only** — the Q-function parameters are treated
  as constants.

## Exploration vs. Exploitation
DDPG trains a **deterministic policy off-policy**. Because the policy is deterministic,
on-policy exploration would probably not try a wide enough variety of actions early on to
find useful learning signal. So **noise is added to actions at training time**.
- The original DDPG paper recommended **time-correlated OU noise**, but **more recent results
  suggest uncorrelated, mean-zero Gaussian noise works perfectly well** — and since it is
  simpler, it is preferred.
- You may reduce the noise scale over training to get higher-quality data. **Spinning Up does
  not do this and keeps the noise scale fixed throughout.**
- **At test time, no noise is added** — that is how you see how well the policy exploits what
  it has learned.
- **`start_steps` trick**: for a fixed number of steps at the beginning, the agent takes
  actions sampled from a **uniform random distribution over valid actions**, then reverts to
  normal DDPG exploration.

## Reference Tables

The DDPG loop:

| Step | Action |
|------|--------|
| Init | Set target parameters equal to main: `theta_targ <- theta`, `phi_targ <- phi` |
| Act | Observe `s`, select `a = clip(mu_theta(s) + epsilon, a_Low, a_High)`, `epsilon ~ N` |
| Store | Execute `a`, observe `s'`, `r`, `d`; store `(s,a,r,s',d)` in `D`; reset if terminal |
| Update | Sample a batch `B` from `D`; compute targets `y = r + gamma*(1-d)*Q_phi_targ(s', mu_theta_targ(s'))` |
| | One gradient descent step on `(Q_phi(s,a) - y)^2` averaged over `B` |
| | One gradient ascent step on `Q_phi(s, mu_theta(s))` averaged over `B` |
| | Polyak-update both target networks |

| Relevant paper | Why it is on the list |
|----------------|----------------------|
| Silver et al. 2014, *Deterministic Policy Gradient Algorithms* | Establishes the theory underlying deterministic policy gradients (DPG) |
| Lillicrap et al. 2016, *Continuous Control With Deep RL* | Adapts the theoretically-grounded DPG algorithm to the deep RL setting, giving DDPG |

## Anti-patterns
- **DDPG on a discrete action space.** The entire design is the continuous-action workaround.
- **Trusting the original paper's full recipe.** Ch10 uses DDPG as its example: the paper
  suggests a complex architecture, an initialization scheme and batch normalization, none of
  which are strictly necessary, and some of the best DDPG results use simpler networks.
- **Assuming DDPG is stable.** It is **frequently brittle with respect to hyperparameters and
  other kinds of tuning** — that is the premise of ch18.
- **Shape bugs in the Q-function.** Exercise 2.2 (ch12) plants exactly one in DDPG's critic
  and it silently ruins learning through broadcasting.

## Key Takeaways
1. `Q(s, mu(s))` replaces `max_a Q(s,a)` — the whole reason DDPG exists.
2. Replay buffers are licensed by the Bellman equation's indifference to how data was collected.
3. Target networks fix the moving-target instability; DDPG uses polyak averaging, DQN uses copies.
4. Two target networks in DDPG: target Q *and* target policy.
5. Explore with additive Gaussian action noise plus uniform-random `start_steps`; no noise at test.
6. Replay buffer size is a genuine trade-off, wrong in both directions.

## Connects To
- **Ch 7**: `a*(s) = argmax_a Q*(s,a)` and the Bellman optimality equation this is built on.
- **Ch 8**: DDPG as the named interpolation between policy optimization and Q-learning.
- **Ch 18**: TD3, the three tricks that fix DDPG's brittleness.
- **Ch 12**: Exercise 2.2, the silent bug planted in this algorithm.
