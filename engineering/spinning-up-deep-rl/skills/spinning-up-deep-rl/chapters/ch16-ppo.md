# Chapter 16: Proximal Policy Optimization (PPO)

## Core Idea
PPO answers the same question as TRPO — how do you take the biggest possible improvement
step without stepping so far that you cause performance collapse — but with **first-order
methods and a few tricks** instead of a complex second-order method. It is significantly
simpler to implement and empirically seems to perform at least as well.

## Quick Facts
- **On-policy.**
- Works with **discrete or continuous** action spaces.
- **Supports MPI parallelization.**
- Two variants exist; Spinning Up implements and documents **PPO-Clip**, the primary variant
  used at OpenAI.

## Frameworks Introduced
- **The two PPO variants:**
  - **PPO-Penalty** approximately solves a KL-constrained update like TRPO, but **penalizes
    the KL-divergence in the objective** instead of making it a hard constraint, and
    **automatically adjusts the penalty coefficient** over training so it stays appropriately
    scaled.
  - **PPO-Clip** has **no KL term in the objective and no constraint at all.** It relies on
    specialized **clipping in the objective function** to remove the incentive for the new
    policy to get far from the old.

- **The PPO-Clip objective.** Update by
  `theta_{k+1} = argmax_theta E_{s,a ~ pi_theta_k}[ L(s,a,theta_k,theta) ]`, typically with
  **multiple steps of (usually minibatch) SGD**. The published form:
  ```
  L = min( ratio * A,  clip(ratio, 1-eps, 1+eps) * A )
  where ratio = pi_theta(a|s) / pi_theta_k(a|s)
  ```
  and `eps` is a small hyperparameter roughly saying how far the new policy may go.

- **The simplified equivalent form** (this is the version Spinning Up actually implements,
  and it is much easier to reason about):
  ```
  L = min( ratio * A,  g(eps, A) )
  where g(eps, A) =  (1 + eps) * A   if A >= 0
                     (1 - eps) * A   if A <  0
  ```

## Worked Example
**Why clipping removes the incentive to move far — the two cases.**

**Advantage positive.** The term reduces to `min(ratio, 1+eps) * A`. Because `A > 0`, the
objective increases as the action becomes more likely, i.e. as `pi_theta(a|s)` increases.
But the `min` caps how much. Once `pi_theta(a|s) > (1+eps) * pi_theta_k(a|s)`, the min kicks
in and the term hits a ceiling of `(1+eps) * A`. **The new policy does not benefit by going
far away from the old policy.**

**Advantage negative.** The term reduces to `max(ratio, 1-eps) * A`. Because `A < 0`, the
objective increases as the action becomes *less* likely, i.e. as `pi_theta(a|s)` decreases.
The `max` caps how much: once `pi_theta(a|s) < (1-eps) * pi_theta_k(a|s)`, it hits a ceiling
of `(1-eps) * A`. **Again: the new policy does not benefit by going far away from the old.**

So **clipping serves as a regularizer by removing incentives for the policy to change
dramatically**, and `eps` corresponds to how far the new policy can go while still profiting
from the objective.

**The honest caveat, and Spinning Up's answer.** Clipping goes a long way toward reasonable
updates, but **it is still possible to end up with a new policy too far from the old**, and
different PPO implementations use a variety of tricks to stave this off. Spinning Up uses a
particularly simple one: **early stopping — if the mean KL-divergence of the new policy from
the old grows beyond a threshold, stop taking gradient steps.** Note that this reintroduces a
KL measurement into an algorithm defined by not having one; the clip is the incentive
mechanism, the KL check is the safety net.

## Reference Tables

The PPO-Clip loop, as a diff against VPG's six steps (ch14):

| Step | VPG | PPO-Clip |
|------|-----|----------|
| 1-3 | Collect trajectories, rewards-to-go, advantage estimates | identical |
| 4-5 | Estimate `ghat_k`, single ascent step | **Maximize the PPO-Clip objective, typically via multiple steps of stochastic gradient ascent with Adam** |
| 6 | Fit `V_phi` by MSE regression on `Rhat_t` | identical |

The key structural difference from VPG and TRPO: **multiple gradient steps per batch of data**,
which is where the sample-efficiency gain comes from and why the policy needs restraining at all.

| Relevant paper | Why it is on the list |
|----------------|----------------------|
| Schulman et al. 2017, *Proximal Policy Optimization Algorithms* | The original PPO paper |
| Schulman et al. 2016, *High Dimensional Continuous Control Using GAE* | Spinning Up's PPO uses GAE for the policy gradient |
| Heess et al. 2017, *Emergence of Locomotion Behaviours in Rich Environments* | Large-scale empirical analysis of behaviors learned by PPO agents in complex environments — though it uses PPO-Penalty, not PPO-Clip |

## Exploration vs. Exploitation
Identical to VPG and TRPO: stochastic policy, on-policy sampling, decaying randomness, local
optima as the failure mode.

## Mental Models
- **PPO trades a hard guarantee for implementability.** TRPO enforces the trust region;
  PPO removes the *incentive* to leave it. That is a weaker statement, and PPO's practical
  dominance says the weaker statement is usually enough.
- **The clip is one-sided per case.** It only ever caps the *beneficial* direction. It never
  penalizes moving the wrong way — it just stops paying you for moving further the right way.
- Careful with terminology: **ch9 notes PPO is often called a policy gradient algorithm,
  though this is slightly inaccurate** — it maximizes a surrogate objective rather than
  following `grad J` directly.

## Anti-patterns
- **Implementing PPO-Clip and calling the result PPO without saying which variant.** Two
  public implementations named "PPO" (ModularRL, rllab) implement PPO-**Penalty**; comparing
  against them without noticing is a real reproduction hazard the docs explicitly flag.
- **Relying on the clip alone at large step counts.** More SGD steps per batch means more
  opportunity to drift; that is precisely why the early-stopping KL check exists.
- **Tuning `eps` as if it were a learning rate.** It bounds policy change per update; the
  number of SGD steps and the learning rate interact with it.

## Key Takeaways
1. Same goal as TRPO, first-order machinery: simpler to implement, at least as good empirically.
2. PPO-Clip (no KL term, no constraint) is the OpenAI default and Spinning Up's implementation.
3. The simplified `g(eps, A)` form makes the mechanism obvious: a ceiling in the profitable
   direction, in both the positive- and negative-advantage cases.
4. Clipping is an incentive change, not a guarantee — Spinning Up backs it with KL early stopping.
5. Multiple minibatch SGD steps per batch is the structural difference from VPG and TRPO.

## Connects To
- **Ch 15**: TRPO's hard constraint, the thing PPO replaces.
- **Ch 9**: the surrogate-objective framing and why "policy gradient algorithm" is imprecise here.
- **Ch 12**: Exercise 1.2 asks you to implement the MLP diagonal Gaussian policy for PPO.
- **Ch 13**: use OpenAI Baselines' PPO, not this one, for research comparisons.
