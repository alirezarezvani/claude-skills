# Chapter 15: Trust Region Policy Optimization (TRPO)

## Core Idea
Take the **largest step possible to improve performance** while satisfying a constraint on
how close the new and old policies are — measured in **KL-divergence between policies**, not
distance in parameter space, because seemingly small parameter differences can produce very
large performance differences.

## Quick Facts
- **On-policy.**
- Works with **discrete or continuous** action spaces.
- **Supports MPI parallelization.**
- **Tensorflow only** in Spinning Up; there is no PyTorch TRPO.

## Key Equations
The theoretical update — maximize surrogate advantage subject to a KL trust region:

```
theta_{k+1} = argmax_theta  L(theta_k, theta)
              s.t.          Dbar_KL(theta || theta_k) <= delta
```

The **surrogate advantage** measures how `pi_theta` performs relative to the old policy
*using data from the old policy* (an importance-weighted advantage):

```
L(theta_k, theta) = E_{s,a ~ pi_theta_k}[ (pi_theta(a|s) / pi_theta_k(a|s)) * A^{pi_theta_k}(s,a) ]

Dbar_KL(theta || theta_k) = E_{s ~ pi_theta_k}[ D_KL( pi_theta(.|s) || pi_theta_k(.|s) ) ]
```

Both the objective and the constraint are **zero at `theta = theta_k`**, and the gradient of
the constraint is **also zero there**.

## Frameworks Introduced
- **Taylor-expand to make it solvable.** Expand objective and constraint to leading order
  around `theta_k`:
  ```
  L(theta_k, theta)        ~=  g^T (theta - theta_k)
  Dbar_KL(theta||theta_k)  ~=  0.5 * (theta - theta_k)^T H (theta - theta_k)
  ```
  **By happy coincidence, `g` — the gradient of the surrogate advantage at `theta_k` — is
  exactly equal to the policy gradient `grad_theta J(pi_theta)`.** Lagrangian duality then
  solves the approximate problem analytically:
  ```
  theta_{k+1} = theta_k + sqrt( 2*delta / (g^T H^{-1} g) ) * H^{-1} g
  ```
  **Stopping here would be exactly the Natural Policy Gradient.**

- **Backtracking line search — the fix that makes it TRPO.** Because the Taylor expansion
  introduces approximation error, that update may violate the KL constraint or fail to improve
  the surrogate advantage. So:
  ```
  theta_{k+1} = theta_k + alpha^j * sqrt( 2*delta / (g^T H^{-1} g) ) * H^{-1} g
  ```
  where `alpha` in (0,1) is the **backtracking coefficient** and `j` is the **smallest
  nonnegative integer** such that the new policy satisfies the KL constraint and produces a
  positive surrogate advantage.
  - When to use this pattern generally: whenever you solve an approximated problem and can
    cheaply check the exact condition, shrink the step until the exact condition holds.

- **Conjugate gradient instead of a matrix inverse.** Computing and storing `H^{-1}` is
  painfully expensive for networks with thousands or millions of parameters. TRPO solves
  `Hx = g` for `x = H^{-1} g` with conjugate gradient, which needs only a function computing
  the matrix-vector product `Hx`, never `H` itself:
  ```
  Hx = grad_theta( (grad_theta Dbar_KL(theta || theta_k))^T x )
  ```

## Reference Tables

| Hyperparameter | Role |
|----------------|------|
| `delta` | KL-divergence limit — the size of the trust region |
| `alpha` | Backtracking coefficient, in (0,1) |
| `K` | Maximum number of backtracking steps; `j` ranges over {0, 1, ..., K} |

The full loop is VPG's six steps with steps 5 replaced by: (a) conjugate gradient to compute
`xhat_k ~= Hhat_k^{-1} ghat_k`, where `Hhat_k` is the Hessian of the sample average
KL-divergence, then (b) the backtracking line search using
`theta_{k+1} = theta_k + alpha^j * sqrt(2 delta / (xhat_k^T Hhat_k xhat_k)) * xhat_k`.

## Mental Models
- **Trust region in policy space, not parameter space.** This is the whole insight. Ordinary
  policy gradient methods keep policies close in *parameter* space, but small parameter
  differences can mean very large performance differences — **so a single bad step can
  collapse the policy performance.** That is what makes large step sizes dangerous with
  vanilla policy gradients, and it is why VPG's sample efficiency suffers: it has to take
  small steps.
- **TRPO buys back sample efficiency by making large steps safe**, and tends to improve
  performance **quickly and monotonically**.
- Read the algorithm as **three nested approximations** — surrogate objective, Taylor
  expansion, conjugate gradient — each with a guard, the last being the line search.

## Exploration vs. Exploitation
Identical to VPG: stochastic policy, on-policy sampling, randomness decaying over training as
the update rule pushes toward exploiting known rewards, with local optima as the risk.

## Anti-patterns
- **Skipping the line search** and shipping the analytic solution. That is Natural Policy
  Gradient, and the approximation error it inherits may violate the constraint or fail to
  improve anything.
- **Forming `H` explicitly.** The matrix-vector product formulation exists because the matrix
  does not fit.
- **Reaching for TRPO in PyTorch inside Spinning Up.** It does not exist; use PPO.

## Key Takeaways
1. Constrain the *policy* change in KL, not the *parameter* change — the core contribution.
2. Surrogate advantage is importance-weighted old-policy data; both it and the KL constraint
   vanish at `theta_k`.
3. `g` (surrogate advantage gradient) equals the policy gradient — that is why VPG's machinery
   is reusable here.
4. Analytic solution = Natural Policy Gradient; TRPO adds a backtracking line search on top.
5. Conjugate gradient replaces the intractable `H^{-1}`.
6. Three relevant papers: Schulman 2015 (original), Schulman 2016 (GAE, used here), Kakade and
   Langford 2002 (the theory motivating and connecting to TRPO's foundations).

## Connects To
- **Ch 14**: the VPG loop TRPO modifies, and the collapse risk it removes.
- **Ch 16**: PPO, which pursues the same goal with first-order methods.
- **Ch 12**: Exercise 2.1 uses TRPO to demonstrate the value-fitting failure mode.
- **Ch 10**: "monotonic improvement theory" — the optional math background this rests on.
