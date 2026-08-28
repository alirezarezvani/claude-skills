# Chapter 7: Part 1 — Key Concepts in RL

## Core Idea
RL is the study of agents learning by trial and error; formally, the agent maximizes
expected return J(pi) over trajectories, and almost every algorithm gets there through one
of four value functions, all of which obey Bellman self-consistency equations.

## Frameworks Introduced
- **The agent-environment interaction loop**: at every step the agent sees a (possibly
  partial) observation, chooses an action, and receives a reward. The environment changes
  because of the action, and may also change on its own.
  - How: name the five MDP pieces before writing any code — states S, actions A, reward
    function R, transition function P, start-state distribution rho_0.

- **The RL optimization problem**: `pi* = argmax_pi J(pi)`, where
  `J(pi) = E_{tau ~ pi}[R(tau)]` and the trajectory distribution is
  `P(tau|pi) = rho_0(s_0) * prod_t P(s_{t+1}|s_t,a_t) * pi(a_t|s_t)`.
  - When to use: as the definition every algorithm is trying to approximate. If an algorithm
    optimizes something else (a Bellman residual, a surrogate objective), that substitution
    is the source of its failure modes.

- **The four value functions**:
  - `V^pi(s)` — on-policy value: expected return starting in s and acting by pi forever.
  - `Q^pi(s,a)` — on-policy action-value: same, but take an arbitrary a first.
  - `V*(s)` — optimal value: expected return acting optimally from s.
  - `Q*(s,a)` — optimal action-value: take arbitrary a, then act optimally.
  - Two connections that come up constantly: `V^pi(s) = E_{a~pi}[Q^pi(s,a)]` and
    `V*(s) = max_a Q*(s,a)`.

- **The optimal-action shortcut**: if you have `Q*`, you get the optimal policy for free:
  `a*(s) = argmax_a Q*(s,a)`. There may be several maximizers, all optimal, but there is
  always an optimal policy that picks deterministically.
  - When to use: this is the entire justification for Q-learning as a family — learn `Q*`
    and the policy is a lookup. Ch17 explains what breaks when the argmax is over a
    continuous space.

- **Bellman equations**: "the value of your starting point is the reward you expect to get
  from being there, plus the value of wherever you land next."
  - On-policy: `V^pi(s) = E_{a~pi, s'~P}[r(s,a) + gamma V^pi(s')]`
  - Optimal:   `V*(s)   = max_a E_{s'~P}[r(s,a) + gamma V*(s')]`
  - The one crucial difference is the presence of the `max` over actions in the optimal form,
    reflecting that an agent free to choose must pick the highest-value action.
  - **Bellman backup** = the right-hand side, the reward-plus-next-value.

- **The advantage function**: `A^pi(s,a) = Q^pi(s,a) - V^pi(s)`. How much better taking a
  specific action is than randomly selecting one according to pi, assuming you follow pi
  afterwards.
  - When to use: whenever relative quality is what matters and absolute value is noise.
    Crucially important to policy gradient methods (ch9).

## Key Concepts
- **State vs observation**: a state s is a complete description of the world; an observation
  o may omit information. Fully observed vs partially observed environments. Notation
  routinely writes s where o is technically correct.
- **Action space**: the set of valid actions. **Discrete** (Atari, Go) versus **continuous**
  (robot control, real-valued vectors). The distinction has profound consequences: some
  algorithm families apply directly only to one case.
- **Policy**: deterministic `a_t = mu(s_t)` or stochastic `a_t ~ pi(.|s_t)`. In deep RL these
  are **parameterized** — parameters theta or phi written as a subscript. "Policy" is often
  used interchangeably with "agent."
- **Trajectory** (also **episode**, **rollout**): `tau = (s_0, a_0, s_1, a_1, ...)`.
- **Finite-horizon undiscounted return**: `R(tau) = sum_{t=0}^{T} r_t`.
- **Infinite-horizon discounted return**: `R(tau) = sum_{t=0}^{inf} gamma^t r_t`, with
  `gamma` in (0,1).
- **MDP**: the 5-tuple `<S, A, R, P, rho_0>`. Markov property: transitions depend only on the
  most recent state and action, not on prior history.

## Code Examples
A deterministic continuous-action policy is just an MLP:

```python
pi_net = nn.Sequential(
    nn.Linear(obs_dim, 64), nn.Tanh(),
    nn.Linear(64, 64),      nn.Tanh(),
    nn.Linear(64, act_dim)
)
obs_tensor = torch.as_tensor(obs, dtype=torch.float32)
actions = pi_net(obs_tensor)
```

**Categorical policies** (discrete actions) are built exactly like a classifier: observation
in, layers, a final linear layer giving logits per action, softmax to probabilities. Sampling
uses the framework's built-in categorical sampler. Log-likelihood is a vector index:
`log pi_theta(a|s) = log [P_theta(s)]_a`.

**Diagonal Gaussian policies** (continuous actions) always have a network mapping observations
to mean actions `mu_theta(s)`. The covariance is diagonal, so it is a vector, represented one
of two ways:
1. A single **state-independent** vector of log standard deviations — standalone parameters.
   *Spinning Up's VPG, TRPO and PPO do it this way.*
2. A network `log sigma_theta(s)` mapping states to log standard deviations, optionally
   sharing layers with the mean network. *SAC does it this way, and SAC with state-independent
   log stds did not work (ch19).*

Log standard deviations, not standard deviations, because logs are free to range over
(-inf, inf) while stds must be nonnegative, and unconstrained parameters are easier to train.
Nothing is lost: exponentiate to recover.

Sampling: `a = mu_theta(s) + sigma_theta(s) * z` with `z ~ N(0, I)` (elementwise product).

Log-likelihood for a k-dimensional action:
`log pi_theta(a|s) = -0.5 * ( sum_i [ (a_i - mu_i)^2 / sigma_i^2 + 2 log sigma_i ] + k log 2pi )`

## Mental Models
- **A discount factor is two arguments in one**: intuitively, cash now beats cash later;
  mathematically, an infinite sum of rewards may not converge and is hard to work with.
- **The formalism is starker than the practice.** Deep RL routinely sets up algorithms to
  optimize the *undiscounted* return while using discount factors when *estimating value
  functions*. Expect the line to be blurred in real code.
- Treat **Q\* as a policy in disguise** and **V\* as a scoring function**: only the action-value
  form directly yields an action.
- Ask of every value function: **is it time-dependent?** Unless stated otherwise, value
  functions mean infinite-horizon discounted return. Finite-horizon undiscounted value
  functions would need time as an argument — because what a state is worth depends on how
  much time is left.

## Anti-patterns
- **Reading `s` in an equation as a true state.** In partially observed settings the action
  is conditioned on the observation; the notation is convention, not a claim.
- **Assuming an algorithm ports across action-space types.** Moving a method between discrete
  and continuous spaces can require substantial rework, not a flag.
- **Learning `V*` and expecting to act.** Without `Q*` or a model you cannot extract the
  action from the value.

## Key Takeaways
1. The goal is always `argmax_pi E_{tau~pi}[R(tau)]`; everything else is machinery for
   approximating it.
2. Four value functions, two of them optimal; `V^pi = E_a[Q^pi]` and `V* = max_a Q*` connect them.
3. Bellman equations hold for all four; the `max` is what separates optimal from on-policy.
4. `a*(s) = argmax_a Q*(s,a)` is why Q-learning is a viable family at all.
5. Advantage `A = Q - V` is the relative-quality signal that policy gradients are built on.
6. Log standard deviations are parameterized, not standard deviations, and state-independence
   is an implementation choice that differs across the algorithms in this book.

## Connects To
- **Ch 8**: the taxonomy built on what each algorithm chooses to learn.
- **Ch 9**: where the advantage function becomes the policy gradient weight.
- **Ch 17**: the continuous-action argmax problem, straight out of `a*(s) = argmax_a Q*(s,a)`.
- **Ch 12**: Exercise 1.1 asks you to implement the diagonal Gaussian log-likelihood above.
