# Chapter 1: Introduction

## Core Idea
Spinning Up exists to be the missing middle step between "I want to work on deep RL"
and "I can implement and evaluate a deep RL algorithm" — the field has no standard
textbook, papers omit the design details that decide whether code works, and production
RL libraries hide the algorithm inside framework abstractions.

## Frameworks Introduced
- **The missing middle step**: the gap Spinning Up fills, between high-level awareness
  (what topics exist, why they matter) and the ability to transmute an algorithm into code.
  - When to use: deciding whether a resource teaches you deep RL or merely describes it.
  - How: judge a resource on whether it closes the theory-to-code gap. Papers give theory
    and omit details; libraries give code that hides the algorithm. Neither closes it alone.

- **Code Design Philosophy** (the four rules the implementations obey):
  - **As simple as possible while still being reasonably good.** Not state of the art;
    good enough to reach roughly the intended performance.
  - **Highly consistent with each other**, so understanding one makes the next painless.
  - **Almost completely self-contained** — virtually no shared code between algorithms
    except logging, saving, loading and MPI utilities. You can study one algorithm without
    following a chain of dependencies.
  - **Patterned to come as close to pseudocode as possible**, minimizing the theory-code gap.
  - How: when reading or writing RL code, prefer the version you can read top to bottom
    over the version that reuses the most code. Reuse is an engineering virtue that is a
    pedagogical cost.

- **Minimize tricks and minimize differences**: the implementations deliberately omit
  tricks present in the original papers (e.g. the regularization terms in the original
  Soft Actor-Critic code, observation normalization in all algorithms) and deliberately
  remove gratuitous differences between similar algorithms (DDPG, TD3 and SAC all run
  gradient updates after fixed intervals of environment interaction, so they compare cleanly).
  - When to use: any time you are comparing two algorithms and want the comparison to be
    about the algorithms rather than about their implementation choices.

## Key Concepts
- **Deep RL**: reinforcement learning (learning to solve tasks by trial and error) combined
  with deep learning.
- **Reasonably good**: achieves roughly the intended performance but does not necessarily
  match the best reported results in the literature on every task.
- **Maintenance mode**: Spinning Up's current status. Breaking bugs get repaired; no major
  new features are planned.
- **The Rosetta Stone goal**: the motivation for the January 2020 PyTorch update — the same
  algorithm expressed in two neural network libraries so the algorithm is separable from the
  library.

## Mental Models
- Think of an RL library's abstraction layer as a **tax on learning**: good for code reuse
  between algorithms, unnecessary if you are writing one algorithm for one use case.
- Use "**can I read this algorithm without opening another file?**" as the test of whether
  an implementation is written to be learned from.
- Think of the resource landscape as **two failure modes**: papers that obscure key design
  details, and public implementations that are hard to read. Spinning Up targets both.

## Anti-patterns
- **Using Spinning Up's implementations for scientific benchmarking comparisons**: they are
  "reasonably good," not best-reported. See ch13 for which ones are at parity (DDPG, TD3, SAC)
  and which are not (VPG, TRPO, PPO). Use OpenAI Baselines for TRPO/PPO research comparisons.
- **Assuming an educational implementation is a research implementation**: the omitted tricks
  (observation normalization, normalized value regression targets) are exactly what separates
  the two.
- **Treating deep RL as engineering-only**: the material explicitly serves people from
  professions with no connection to engineering or computer science who nonetheless need to
  make informed decisions about the technology.

## Worked Example
Support history, read as a record of what the community actually asked for after release:

| Date | Event |
|------|-------|
| Nov 8, 2018 | Initial release, followed by three weeks of high-bandwidth support |
| April 2019 | Six-month internal review of community feedback |
| Jan 2020 | The PyTorch update ships |
| Future | No major updates planned |

The April 2019 review surfaced exactly three requests, in priority order:
1. **Implementations in other neural network libraries** — enough people had written their
   own PyTorch ports (Fired Up, Spinning Up Basic, Torching Up) that a "Rosetta Stone for
   deep RL" became the top priority. This one shipped.
2. **Open source RL environments** (e.g. PyBullet) for benchmarks, examples and exercises,
   to avoid the proprietary MuJoCo dependency. Did not ship.
3. **More algorithms**, especially Deep Q-Networks. Did not ship.

The lesson for anyone building an educational resource: the community's top request was not
more content, it was the same content expressed in the framework they already use.

## Key Takeaways
1. The barrier to entry in deep RL is not intelligence or math; it is that theory and code
   are documented in separate places and neither is written to connect to the other.
2. Self-contained beats DRY when the reader is trying to learn the algorithm.
3. Consistency across implementations is a teaching feature: differences that remain are
   real algorithmic differences.
4. "Reasonably good" is a deliberate, stated performance target — check ch13 before citing
   any Spinning Up number as a benchmark.
5. Deep RL is central to AI safety work in OpenAI's framing; the resource exists partly as
   a recruiting and capability-building pipeline for that.

## Connects To
- **Ch 3**: which algorithms were chosen and why, and the code template they all share.
- **Ch 10**: the essay on becoming a researcher — the practice counterpart to this chapter's
  philosophy.
- **Ch 13**: the benchmark numbers that qualify "reasonably good."
