# Chapter 10: Spinning Up as a Deep RL Researcher

## Core Idea
Joshua Achiam's curriculum for becoming a deep RL researcher, in four stages: build the
right background, learn by writing your own implementations, develop a research project
through one of three idea frames, and hold yourself to experimental standards strict enough
that a positive result means something.

## Frameworks Introduced
- **The Right Background** (four items, all prerequisites, none optional):
  - **Math**: from probability and statistics — random variables, Bayes' theorem, chain rule
    of probability, expected values, standard deviations, importance sampling. From
    multivariate calculus — gradients, and optionally Taylor series expansions.
  - **General deep learning**: standard architectures (MLP, vanilla RNN, LSTM, GRU, conv
    layers, resnets, attention), regularizers (weight decay, dropout), normalization (batch,
    layer, weight norm), optimizers (SGD, momentum SGD, Adam), and the reparameterization trick.
  - **One deep learning library**, well enough to confidently implement a simple supervised
    learning program.
  - **RL concepts and terminology**: states, actions, trajectories, policies, rewards, value
    functions, action-value functions. Optionally, monotonic improvement theory (the basis
    for advanced policy gradient algorithms) and classical RL algorithms.

- **Learn by Doing** — the core of the essay, in eight rules:
  1. **Write your own implementations**, aiming for the **shortest correct implementation** of
     each. By far the best way to build both understanding and performance intuitions.
  2. **Simplicity is critical.** Implement the simplest algorithms first and add complexity
     gradually. Starting with too many moving parts means weeks lost to debugging — a common
     failure mode for newcomers. If you are stuck in it, drop to a simpler algorithm and
     return later.
  3. **Which algorithms, in roughly this order**: VPG (REINFORCE), DQN, A2C (the synchronous
     A3C), PPO (clipped objective), DDPG. The simplest versions are a few hundred lines
     (ballpark 250-300); a no-frills VPG is about 80. Write single-threaded before parallel,
     but do parallelize at least one.
  4. **Focus on understanding, because broken RL code almost always fails silently** — the
     code runs fine and the agent simply never learns. Usually something is computed with the
     wrong equation, on the wrong distribution, or piped to the wrong place. Sometimes the
     only way to find it is to read the code critically, knowing exactly what it should do.
  5. **What to look for in papers**: scour ablation analyses (they tell you which parameters
     and subroutines actually matter, which is what you need to diagnose bugs) and
     supplementary material (network architectures, optimization hyperparameters — align your
     implementation to these to improve your odds of getting it working).
  6. **But do not overfit to paper details.** Papers often prescribe more tricks than are
     strictly necessary. The original DDPG paper suggests a complex architecture, an
     initialization scheme and batch normalization; none are strictly necessary and some of
     the best DDPG results use simpler networks. The original A3C uses asynchronous updates
     from actor-learners; synchronous updates work about as well.
  7. **Do not overfit to existing implementations either.** RL libraries make abstraction
     choices that are good for code reuse across algorithms but unnecessary if you are
     writing one algorithm for one use case.
  8. **Iterate fast in simple environments.** CartPole-v0, InvertedPendulum-v0, FrozenLake-v0,
     HalfCheetah-v2 with a short horizon (100 or 250 steps, not the full 1000).
     **Ideal debug-stage turnaround: under 5 minutes on your local machine.** These runs need
     no special hardware and run fine on CPUs. Do not attempt Atari or Humanoid before the
     simplest toy task works.

- **Three idea-generation frames** — the frame you pick shapes the project's scope and risk:

  | Frame | What it is | Scope | Main risk |
  |-------|-----------|-------|-----------|
  | **1. Improving on an existing approach** | Incrementalism: performance gains in an established setting by tweaking an existing algorithm. Reimplementing prior work exposes where it is brittle. Most accessible to novices, still worthwhile at any level | Narrow, wraps up in a few months | Your tweaks may simply fail to improve it, and then the project is over with no signal on what to do next |
  | **2. Focusing on unsolved benchmarks** | Succeed at a task nobody has solved. You may try a wide variety of methods, prior and invented | Broad, several months to a year-plus | The benchmark may be unsolvable without a substantial breakthrough; easy to spend a long time with no progress. Even failure usually yields insights that seed the next project |
  | **3. Creating a new problem setting** | An entirely different conceptual problem nobody has studied; you will have to design the benchmark too | Open-ended | Enormous challenge — but great benchmarks move the whole field forward. These problems come up when they come up; hard to go looking for them |

- **Doing Rigorous Research in RL** — four standards, each closing a specific way a result
  can look real and not be:
  1. **Set up fair comparisons.** If you implement your baseline from scratch, spend **as much
     time tuning the baseline as tuning your own algorithm.** Hold all else equal even when
     the methods differ substantially — e.g. keep parameter counts approximately equal when
     investigating architecture variants. **Under no circumstances handicap the baseline.**
     RL baselines are strong, and consistent wins over them are hard.
  2. **Remove stochasticity as a confounder.** Run everything for many random seeds — **at
     least 3, and 10 or more to be thorough.** Deep RL is fairly brittle with respect to seed;
     two different groups of seeds can produce learning curves so different they look like
     they come from different distributions.
  3. **Run high-integrity experiments.** Do not report the best or most interesting runs.
     Launch **new, final experiments** for every method being compared and **precommit to
     reporting whatever comes out.** This enforces a weak form of preregistration: the tuning
     stage produces your hypotheses, the final runs produce your conclusions.
  4. **Check each claim separately — run an ablation analysis.** Any proposed method has
     several key design decisions, and the claim "these collectively help" is really a bundle
     of separate claims. Systematically swap or remove each one to attribute credit correctly.
     This lets you state each claim with a measure of confidence and strengthens the whole work.

## Key Concepts
- **Silent failure**: the defining property of broken RL code. It runs; the agent just never learns.
- **Measure everything**: instrument heavily. The author's own list — mean/std/min/max of
  cumulative rewards, episode lengths and value function estimates, plus the objective losses
  and any exploration parameters (mean policy entropy for stochastic policy optimization,
  current epsilon for epsilon-greedy). **Also watch videos of your agent** periodically; it
  gives insights nothing else does. You cannot tell it is broken if you cannot see it breaking.
- **Assume there is a bug.** Spend a lot of effort searching for bugs before tweaking
  hyperparameters. Bad hyperparameters can significantly degrade performance, but if yours
  are similar to those in papers and standard implementations, they are probably not the issue.
- **Test in more than one environment**: sometimes code works in one environment despite a
  breaking bug, so re-verify once results look promising.
- **Avoid reinventing the wheel**: before investing, check thoroughly that the idea has not
  been done. But do not let the risk push you into planting flags with not-quite-finished
  research or over-claiming partial work. Complete, thorough investigations are what counts.
- **Scale when things work**: after the simplest environments pass, move to harder ones —
  experiments now take hours to a couple of days, and specialized hardware (a beefy GPU, a
  32-core machine) or cloud resources start to be worth it.

## Anti-patterns
- **Tuning hyperparameters to fix a bug.** It is usually a bug.
- **Debugging in a hard environment.** If turnaround exceeds a few minutes at the debug stage,
  you are working in the wrong environment.
- **Starting with the complex algorithm.** The predicted outcome is weeks lost.
- **Reporting your best run.** That is the failure the precommitment rule exists to stop.
- **Under-tuning the baseline** — the most common way to manufacture a positive result without
  intending to.
- **Fewer than 3 seeds.** With deep RL's seed sensitivity, a single-seed result carries
  almost no information.
- **Bundling claims.** Without ablations you cannot say which of your design decisions did
  the work — including, possibly, none of them.

## Key Takeaways
1. Implement from scratch, simplest first, shortest correct version, single-threaded before parallel.
2. Broken RL code fails silently — so instrumentation and critical reading, not error messages,
   are your debugging tools.
3. Debug loops under five minutes in toy environments; scale only after correctness.
4. Read papers for ablations and supplementary material, but do not adopt every trick.
5. Pick an idea frame deliberately: incremental (narrow, fast, may dead-end), unsolved
   benchmark (broad, slow, insight-rich even in failure), or new problem setting (rare, huge).
6. Rigor is four things: a fully-tuned baseline, many seeds, precommitted final runs, and
   per-claim ablations.
7. These habits are worth keeping past the learning stage; they accelerate research.

## Connects To
- **Ch 1**: the code design philosophy that makes the reference implementations readable.
- **Ch 4**: the `--seed 0 10 20` flag that operationalizes the multi-seed rule.
- **Ch 11**: the key papers list, the recommended starting point for literature exploration.
- **Ch 12**: the exercises — Problem Set 2 is entirely about silent failure modes.
- **Ch 13**: the benchmarks, run at 10 seeds — the standard this chapter asks for.
