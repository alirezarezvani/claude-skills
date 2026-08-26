# Chapter 3: Algorithms — What's Included and Why

## Core Idea
The six algorithms (VPG, TRPO, PPO, DDPG, TD3, SAC) are not a survey; they are two
lineages of ideas, each starting from a foundational algorithm and progressively fixing
its defining weakness, culminating in PPO and SAC.

## Frameworks Introduced
- **The two lineages**:
  - **On-policy line: VPG to TRPO to PPO.** Each step buys back sample efficiency without
    giving up the stability that comes from directly optimizing the objective you care about.
  - **Off-policy line: DDPG to TD3 and SAC.** Each step mitigates the brittleness that comes
    from optimizing a Bellman self-consistency condition instead of performance itself.
  - When to use: placing any new algorithm you read about. Ask which line it is on and which
    weakness of its predecessor it claims to fix.

- **The central trade-off the lineup exposes**: on-policy algorithms *directly optimize the
  objective you care about* — policy performance — and it works out mathematically that
  you need on-policy data to compute the updates, so they cannot reuse old data. Off-policy
  algorithms exploit the Bellman optimality equations, which hold for *any* transition data,
  so they reuse everything — but satisfying Bellman's equations well carries **no guarantee**
  of good policy performance.
  - How: choose the family by which risk you can afford. Stability with a sample budget, or
    sample efficiency with a tuning budget.

- **The standard two-file code template**: every implementation splits into an *algorithm
  file* (experience buffer class, then one function that runs the algorithm) and a *core
  file* (utilities, the actor-critic constructors, the MLP actor-critic).
  - When to use: reading any Spinning Up algorithm, or structuring your own.

## Key Concepts
- **On-policy**: each update uses only data collected by the most recent version of the policy.
- **Off-policy**: each update can use data collected at any point in training, however the
  agent was exploring at the time.
- **MLP actor-critic**: all six use non-recurrent multi-layer-perceptron actor-critics, which
  makes them suitable for fully-observed, non-image-based environments (e.g. Gym MuJoCo) and
  unsuitable, as shipped, for partial observability or pixels.
- **Sample efficiency**: how much environment interaction is needed to reach a performance level.
- **Deterministic policy gradients**: the theory (2014) that made DDPG possible — much younger
  than the policy gradient theory behind VPG, whose core elements go back to the late 80s.

## Reference Tables

| Algorithm | Family | Policy | Action spaces | Parallel (MPI) | PyTorch | TF1 |
|-----------|--------|--------|---------------|----------------|---------|-----|
| VPG | On-policy | Stochastic | Discrete + continuous | Yes | Yes | Yes |
| TRPO | On-policy | Stochastic | Discrete + continuous | Yes | No | Yes |
| PPO | On-policy | Stochastic | Discrete + continuous | Yes | Yes | Yes |
| DDPG | Off-policy | Deterministic | Continuous only | No | Yes | Yes |
| TD3 | Off-policy | Deterministic | Continuous only | No | Yes | Yes |
| SAC | Off-policy | Stochastic | Continuous only (as shipped) | No | Yes | Yes |

## Code Examples
The PyTorch algorithm function, in order — the template every implementation follows:

```
1) Logger setup
2) Random seed setting
3) Environment instantiation
4) Build the actor-critic module via the `actor_critic` function passed in as an argument
5) Instantiate the experience buffer
6) Set up callable loss functions that also return algorithm-specific diagnostics
7) Make PyTorch optimizers
8) Set up model saving through the logger
9) Set up an update function: one epoch of optimization, or one step of descent
10) Main loop:  a) run the agent in the environment
                b) periodically update parameters per the algorithm's main equations
                c) log key performance metrics and save the agent
```

The TF1 version is the same shape with four graph-construction steps inserted (placeholders,
actor-critic graph, loss/diagnostic graph, training ops) and a session step.

## Mental Models
- Read the lineup as **"progressions of ideas from the recent history of the field"**, not as
  a menu. VPG predates deep RL entirely; DDPG's theory is from 2014.
- Treat **PPO and SAC as the two defaults** — they are close to state of the art on
  reliability and sample efficiency among policy-learning algorithms.
- Think of the `actor_critic` argument as the seam: the algorithm function is fixed, the
  network construction is injected. That is also where the ch12 silent bug lives.

## Anti-patterns
- **Reaching for DDPG on a discrete action space.** DDPG, TD3 and the shipped SAC are
  continuous-only. The max over actions is why (see ch17).
- **Expecting these to work on Atari or partially-observed tasks as shipped**: MLP,
  non-recurrent, non-image.
- **Picking an algorithm by recency**: TD3 and SAC were published roughly concurrently; SAC
  is not a successor to TD3, it is a parallel branch that borrowed the clipped double-Q trick.

## Key Takeaways
1. Two families, one trade-off: directly optimize performance (on-policy, stable, sample-hungry)
   or exploit Bellman (off-policy, sample-efficient, no performance guarantee).
2. PPO and SAC are the practical end points of each line.
3. Continuous-only for the whole off-policy line, as implemented here.
4. Every implementation is two files and the same ten-step function; learn the template once.
5. TRPO has no PyTorch implementation in Spinning Up.

## Connects To
- **Ch 8**: the full taxonomy this lineup is a slice of.
- **Ch 14-19**: one chapter per algorithm, in lineage order.
- **Ch 12**: the exercises that make the on-policy/off-policy distinction concrete.
