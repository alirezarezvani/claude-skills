# Chapter 13: Benchmarks for Spinning Up Implementations

## Core Idea
All six algorithms were benchmarked for 3M timesteps across five MuJoCo environments at
10 seeds each — and the results carry an explicit, unusual disclosure about which
implementations are research-grade and which are not.

## Frameworks Introduced
- **The parity disclosure — the single most decision-relevant paragraph in the chapter:**
  - **DDPG, TD3 and SAC are roughly at parity with the best reported results** for those
    algorithms. **You can use them for research purposes.**
  - **VPG, TRPO and PPO are overall a bit weaker than the best reported results**, because
    the implementations omit standard tricks — specifically **observation normalization** and
    **normalized value regression targets**. **For research comparisons, use the TRPO or PPO
    implementations from OpenAI Baselines instead.**
  - When to use: before citing any Spinning Up number, or before using one of these as a
    baseline in a paper (which ch10 says you must tune as hard as your own method).

- **Report performance with its measurement definition attached.** The two families are not
  measured the same way, and saying "return" without saying which is a category error:
  - **On-policy**: the average trajectory return across the batch collected at each epoch —
    i.e. the exploring policy, measured continuously.
  - **Off-policy**: measured **once every 10,000 steps** by running the deterministic policy
    (or, for SAC, the **mean** policy) **without action noise** for **ten trajectories**, and
    reporting the average return over those test trajectories.

## Reference Tables

Benchmark setup:

| Parameter | On-policy (VPG, TRPO, PPO) | Off-policy (DDPG, TD3, SAC) |
|-----------|---------------------------|----------------------------|
| Network architecture | (64, 32), tanh units | (256, 256), relu units |
| Batch | 4000 environment steps per batch update | Minibatches of 100 per gradient step |
| Performance metric | Average batch trajectory return per epoch | Deterministic/mean policy, no noise, 10 trajectories every 10k steps |
| Research-grade? | No — use Baselines for TRPO/PPO | Yes |

Common to all:

| Setting | Value |
|---------|-------|
| Environments | HalfCheetah-v3, Hopper-v3, Walker2d-v3, Swimmer-v3, Ant-v3 (MuJoCo Gym suite) |
| Timesteps | 3M |
| Random seeds | 10 per experiment |
| Plot content | Solid line = mean over seeds; shaded = std dev over seeds |
| Smoothing | Averaged over a window of 11 epochs |
| Other hyperparameters | Left at Spinning Up defaults; see each algorithm page |

Both PyTorch and TF1 versions were benchmarked in every environment, plus dedicated
head-to-head PyTorch-vs-TF1 pages for VPG, PPO, DDPG, TD3 and SAC. (TRPO has no PyTorch
implementation, so it has no head-to-head page.)

## Mental Models
- **Reporting mean and std dev over 10 seeds *as shaded bands* is the visual form of ch10's
  "remove stochasticity as a confounder."** A benchmark plot without a seed band is telling
  you less than it appears to.
- **The architecture split is itself a finding**: on-policy at (64, 32)/tanh and off-policy
  at (256, 256)/relu is the convention these algorithm families settled into, not an
  arbitrary choice, and copying the wrong family's defaults is a real source of bad results.
- **Honest self-assessment is a feature of the resource**, not a caveat. A benchmarks page
  that names which of its own implementations you should not use is doing the reader's
  ch10 rigor work for them.

## Anti-patterns
- **Using Spinning Up's PPO or TRPO as a paper baseline.** The page says explicitly to use
  Baselines for those. Under-powered baselines are the ch10 failure of "handicapping the
  baseline," even when it is unintentional.
- **Comparing an on-policy `AverageEpRet` against an off-policy `AverageTestEpRet`** as if
  they were the same quantity. Use the plotter's `Performance` alias (ch6), which resolves
  per family.
- **Reading a single-seed curve as a result.** These plots are 10 seeds precisely because
  fewer is not informative.

## Key Takeaways
1. 3M timesteps, five MuJoCo environments, 10 seeds, both backends.
2. DDPG, TD3, SAC: research-usable. VPG, TRPO, PPO: educational only — use Baselines.
3. The weakness is attributed to two named omissions: observation normalization and
   normalized value regression targets.
4. On-policy and off-policy performance are different measurements, not different numbers
   of the same measurement.
5. Architecture defaults differ by family: (64,32)/tanh on-policy, (256,256)/relu off-policy.

## Connects To
- **Ch 1**: "reasonably good" — this chapter is the quantification of that phrase.
- **Ch 6**: the `Performance` alias, which exists because of the metric split described here.
- **Ch 10**: the seed and fair-baseline standards this benchmark actually meets.
- **Ch 14-19**: per-algorithm hyperparameter defaults referenced as "left at default settings."
