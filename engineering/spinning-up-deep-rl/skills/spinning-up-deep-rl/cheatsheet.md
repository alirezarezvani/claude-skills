# Cheatsheet

Decision rules, thresholds and tells from Spinning Up. One page; keep it beside you.

## Which algorithm?

| If | Then | Because |
|----|------|---------|
| Discrete actions | PPO (or VPG to learn) | DDPG, TD3 and shipped SAC are continuous-only |
| Continuous, stability matters most | PPO | Directly optimizes performance; on-policy is stable |
| Continuous, sample efficiency matters most | SAC, else TD3 | Off-policy data reuse; both are research-grade here |
| You are learning the field | VPG first, then DQN, A2C, PPO, DDPG | Simplest first; complexity added gradually |
| You need a research baseline for TRPO/PPO | OpenAI Baselines, not Spinning Up | Spinning Up's on-policy trio omits observation normalization and normalized value targets |
| You need a research baseline for DDPG/TD3/SAC | Spinning Up is fine | Roughly at parity with best reported results |
| Partial observability or pixels | None of these as shipped | All six are non-recurrent MLP actor-critics |

## Debugging a run that does not learn

1. **Assume it is a bug, not the hyperparameters.** Bad hyperparameters degrade performance;
   if yours resemble the paper's, they are probably not the cause.
2. **Check tensor shapes.** A `[N]` vs `[N,1]` mismatch is broadcast-compatible, raises
   nothing, and silently corrupts the Bellman backup into an `[N,N]` matrix.
3. **Check what your loss is computed on** — wrong equation, wrong distribution, or data
   piped to the wrong place are the three usual causes.
4. **Do not read the policy-gradient loss as a health signal.** Only average return means
   anything; the loss can go to negative infinity while performance craters.
5. **Instrument more.** Mean/std/min/max of returns, episode lengths and value estimates;
   objective losses; exploration parameters (policy entropy, epsilon). Watch videos too.
6. **Test in more than one environment** once results look promising — code can work in one
   environment despite a breaking bug.

## Thresholds and defaults

| Quantity | Value | Source |
|----------|-------|--------|
| Debug-stage turnaround target | **under 5 minutes** locally | Ch 10 |
| Random seeds, minimum | **3** | Ch 10 |
| Random seeds, thorough | **10 or more** | Ch 10, Ch 13 |
| Debug environments | CartPole-v0, InvertedPendulum-v0, FrozenLake-v0, HalfCheetah-v2 at 100-250 steps | Ch 10 |
| From-scratch implementation size | ~250-300 lines; no-frills VPG ~80 | Ch 10 |
| On-policy benchmark network | (64, 32), tanh | Ch 13 |
| Off-policy benchmark network | (256, 256), relu | Ch 13 |
| On-policy batch | 4000 env steps per update | Ch 13 |
| Off-policy minibatch | 100 per gradient step | Ch 13 |
| TD3 `policy_delay` | 2 | Ch 18 |
| Polyak `rho` | in (0,1), usually close to 1 | Ch 17 |
| Benchmark length | 3M timesteps, 5 MuJoCo envs | Ch 13 |
| Plot smoothing used in the book | 11-epoch window | Ch 13 |

## Choosing a research frame

| Frame | Scope | Wraps up in | Main risk |
|-------|-------|-------------|-----------|
| Improve an existing approach | Narrow | A few months | Tweaks fail and you have no signal on what next |
| Unsolved benchmark | Broad | Months to a year-plus | May need a breakthrough; long time, no progress |
| New problem setting | Open-ended | Unbounded | You must design the benchmark too; cannot go looking for these |

## Rigor checklist before reporting

- [ ] Baseline tuned **as much as** your own method. Never handicap it.
- [ ] All else held equal (e.g. comparable parameter counts across architecture variants).
- [ ] At least 3 seeds, ideally 10 or more; plot mean and std dev.
- [ ] Final runs launched fresh and **precommitted** — not the best or most interesting runs.
- [ ] One ablation per design decision, so each claim is separately supported.
- [ ] Checked the idea has not already been published.

## Tells and smells

- **A learning curve with no seed band** is telling you less than it looks like.
- **`AverageEpRet` on an off-policy algorithm** is the noisy behavior policy, not performance.
  Use the plotter's `Performance` alias.
- **Evaluating SAC without `--deterministic`** measures the wrong policy.
- **A model-based agent that scores well but behaves badly** is exploiting model bias — the
  same shape as a policy exploiting Q-function errors.
- **"Fits the Bellman equation well"** carries no guarantee of good policy performance.
- **A single missing `squeeze`** in a critic is the archetype of silent failure.
- **A paper's full trick list** is usually more than strictly necessary — try simplifications.
- **A library abstraction** is good for reuse across algorithms and a cost when learning one.

## Quick commands

```bash
python -m spinup.run ppo --env Walker2d-v2 --exp_name walker --seed 0 10 20
python -m spinup.run test_policy data/walker/walker_s0        # add -d for SAC
python -m spinup.run plot data/walker                          # prefix autocompletes
python -m spinup.run [algo] --help                             # every kwarg is a flag
```
