# Chapter 14: Vanilla Policy Gradient (VPG)

## Core Idea
Push up the probabilities of actions that lead to higher return and push down the
probabilities of actions that lead to lower return, until you arrive at the optimal policy.
That is the whole idea underlying policy gradients, and VPG is its most direct expression.

## Quick Facts
- **On-policy.**
- Works with **discrete or continuous** action spaces.
- The Spinning Up implementation **supports MPI parallelization**.

## Key Equations
The advantage-weighted policy gradient (the end point of ch9):

```
grad_theta J(pi_theta) = E_{tau ~ pi_theta}[ sum_{t=0}^{T} grad_theta log pi_theta(a_t|s_t) * A^{pi_theta}(s_t,a_t) ]
```

Stochastic gradient ascent on policy performance:

```
theta_{k+1} = theta_k + alpha * grad_theta J(pi_theta_k)
```

**The notation mismatch worth knowing about:** `J(pi_theta)` here denotes the expected
**finite-horizon undiscounted** return, but policy gradient implementations typically compute
**advantage estimates based on the infinite-horizon discounted return** — despite otherwise
using the finite-horizon undiscounted policy gradient formula. This is the ch7 blurring of
the two return formulations, appearing in production code.

## Frameworks Introduced
- **The VPG loop** (the template TRPO and PPO both modify, so learn it once):
  1. Collect a set of trajectories `D_k` by running `pi_k = pi(theta_k)` in the environment.
  2. Compute rewards-to-go `Rhat_t`.
  3. Compute advantage estimates `Ahat_t` (any method of advantage estimation) based on the
     current value function `V_{phi_k}`.
  4. Estimate the policy gradient:
     `ghat_k = (1/|D_k|) * sum_{tau in D_k} sum_t grad_theta log pi_theta(a_t|s_t)|_{theta_k} * Ahat_t`
  5. Update the policy by standard gradient ascent `theta_{k+1} = theta_k + alpha_k * ghat_k`,
     or another gradient ascent algorithm like Adam.
  6. Fit the value function by regression on mean-squared error:
     `phi_{k+1} = argmin_phi (1/(|D_k| T)) * sum sum (V_phi(s_t) - Rhat_t)^2`, typically via
     gradient descent.

## Exploration vs. Exploitation
VPG trains a **stochastic policy in an on-policy way**, so it explores by sampling actions
from the latest version of that policy. How random that is depends on both initial conditions
and the training procedure. **Over training the policy typically becomes progressively less
random**, because the update rule encourages exploiting rewards already found — **which may
cause the policy to get trapped in local optima.** (This paragraph is identical for TRPO and
PPO; it is a property of the on-policy stochastic-policy family, not of VPG specifically.)

## Code Examples
Loading and using a trained PyTorch model:

```python
ac = torch.load('path/to/model.pt')
actions = ac.act(torch.as_tensor(obs, dtype=torch.float32))
```

The TF1 saved graph exposes three keys: `x` (state input placeholder), `pi` (samples an
action conditioned on `x`), and `v` (value estimate for states in `x`).

## Anti-patterns
- **Expecting monotonic improvement.** VPG has none; the step size is unconstrained and a
  bad step can collapse performance. That collapse is what TRPO (ch15) exists to prevent.
- **Under-fitting the value function.** Exercise 2.1 (ch12) shows a policy gradient agent
  with an untrained value function gets stuck early. The advantage estimate is only as good
  as `V_phi`.
- **Reading the loss.** See ch9's worked example.

## Reference Tables

| Relevant paper | Why it is on the list |
|----------------|----------------------|
| Sutton et al. 2000, *Policy Gradient Methods for RL with Function Approximation* | A timeless classic of RL theory; contains references to the earlier work that led to modern policy gradients |
| Schulman 2016(a), *Optimizing Expectations* | Chapter 2 is a lucid introduction to policy gradient theory, including pseudocode |
| Duan et al. 2016, *Benchmarking Deep RL for Continuous Control* | A clear benchmark paper showing how VPG in the deep RL setting compares with other deep RL algorithms |
| Schulman et al. 2016(b), *High Dimensional Continuous Control Using GAE* | Spinning Up's VPG uses GAE for computing the policy gradient |

## Key Takeaways
1. VPG is the advantage-weighted policy gradient plus mean-squared value regression — nothing else.
2. The six-step loop is the base template; TRPO changes step 5, PPO changes step 5 differently.
3. Discrete or continuous, MPI-parallelizable, both backends available.
4. Its weakness is step-size safety: nothing stops a single update from collapsing the policy.
5. Exploration decays as a side effect of exploitation, with local optima the known risk.

## Connects To
- **Ch 9**: the derivation that produces this exact gradient, and GAE.
- **Ch 15**: TRPO, which constrains the step this chapter leaves unconstrained.
- **Ch 12**: Exercise 2.1, on what happens when `V_phi` is not fit.
- **Ch 13**: the benchmark caveat — VPG is educational-grade, not research-grade.
