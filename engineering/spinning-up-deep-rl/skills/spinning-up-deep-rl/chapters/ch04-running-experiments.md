# Chapter 4: Running Experiments

## Core Idea
`spinup/run.py` turns every keyword argument of every algorithm into a command-line flag,
and turns a list of values for a flag into a series of experiments — so hyperparameter
sweeps and multi-seed runs are one command, not a script.

## Frameworks Introduced
- **One flag per kwarg**: if `kwarg` is a valid keyword argument of an algorithm function,
  `--kwarg` sets it. `python -m spinup.run [algo] --help` prints the docstring readout.
  - How: `python -m spinup.run [algo name] [experiment flags]`.

- **Multiple values means multiple experiments**: providing more than one value for an
  argument launches one experiment per combination, **in series**. They do not run in
  parallel because a single experiment already soaks up enough resources that concurrency
  buys no speedup.
  - When to use: seed sweeps (the ch10 rigor requirement) and hyperparameter ablations.

- **ExperimentGrid**: the in-script equivalent, based on but simpler than rllab's
  VariantGenerator. `spinup.run` uses one under the hood.
  - How: `eg.add(param_name, values, shorthand, in_name)` then `eg.run(thunk, **run_kwargs)`.
    `in_name` forces a parameter into the experiment name even when it does not vary.
  - Difference from the CLI: no shortcut kwargs — you must write `ac_kwargs:hidden_sizes`,
    not `hid`.

- **Shorthand-driven save directories**: results land in
  `data_dir/[outer_prefix]exp_name[suffix]/[inner_prefix]exp_name[suffix]_s[seed]`.
  The suffix encodes only the hyperparameters that *differ across the launched experiments*,
  and never the seed — so runs that differ only by seed group into the same folder, which is
  exactly what the plotter needs to average over seeds.

## Key Concepts
- **`--env` / `--env_name`**: a Gym environment name, converted internally into the `env_fn`
  callable every algorithm actually takes.
- **`--hid` / `--act`**: shortcut flags for `ac_kwargs:hidden_sizes` and `ac_kwargs:activation`,
  valid for all current algorithms.
- **`--cpu` / `--num_cpu`**: launch with this many MPI-connected processes; `auto` uses all
  available. Raises an error for algorithms that do not support parallelization.
- **`--dt` / `--datestamp`**: put timestamps in the save directory names.
- **User-supplied shorthand**: square brackets after a flag, e.g. `--hid[h]`, control the
  directory-name abbreviation. Without one, a shorthand is derived automatically
  (`clip_ratio` becomes `cli`).
- **`eval()` passthrough**: flag values pass through `eval()` before use, so you can name
  functions and objects directly, e.g. `--act torch.nn.ELU`.
- **Dict kwargs**: `--key:v1 value_1 --key:v2 value_2` instead of `--key dict(v1=..., v2=...)`.

## Code Examples
The quickstart, with every flag doing something distinct:

```bash
python -m spinup.run ppo --exp_name ppo_ant --env Ant-v2 --clip_ratio 0.1 0.2 \
    --hid[h] [32,32] [64,32] --act torch.nn.Tanh --seed 0 10 20 --dt \
    --data_dir path/to/data
```

Choosing the backend explicitly:

```bash
python -m spinup.run ppo_pytorch --env Walker2d-v2 --exp_name walker
python -m spinup.run ppo_tf1     --env Walker2d-v2 --exp_name walker
# bare `ppo` reads spinup/user_config.py for the default backend
```

From a script:

```python
from spinup import ppo_pytorch as ppo
import gym
env_fn = lambda: gym.make('LunarLander-v2')
ac_kwargs = dict(hidden_sizes=[64, 64])
logger_kwargs = dict(output_dir='path/to/output_dir', exp_name='experiment_name')
ppo(env_fn=env_fn, ac_kwargs=ac_kwargs, steps_per_epoch=5000, epochs=250,
    logger_kwargs=logger_kwargs)
```

ExperimentGrid, from `spinup/examples/pytorch/bench_ppo_cartpole.py`:

```python
from spinup.utils.run_utils import ExperimentGrid
from spinup import ppo_pytorch
import torch

eg = ExperimentGrid(name='ppo-pyt-bench')
eg.add('env_name', 'CartPole-v0', '', True)
eg.add('seed', [10*i for i in range(args.num_runs)])
eg.add('epochs', 10)
eg.add('steps_per_epoch', 4000)
eg.add('ac_kwargs:hidden_sizes', [(32,), (64,64)], 'hid')
eg.add('ac_kwargs:activation', [torch.nn.Tanh, torch.nn.ReLU], '')
eg.run(ppo_pytorch, num_cpu=args.cpu)
```

## Worked Example
`python -m spinup.run ddpg_tf1 --env Hopper-v2 --hid[h] [300] [128,128] --act tf.nn.tanh tf.nn.relu`

Two `hid` values times two `act` values is four experiments, run in series, producing four
suffixes:

```
_h128-128_ac-actrelu
_h128-128_ac-acttanh
_h300_ac-actrelu
_h300_ac-acttanh
```

`h` came from the user-supplied `[h]`; `ac-act` was derived automatically from the true flag
name `ac_kwargs:activation`. Add `--seed 0 10 20` and you get twelve runs in four folders —
three seeds grouped per configuration, which is the grouping the plotter averages over.

## Anti-patterns
- **Running the per-algorithm files directly** (`spinup/algos/BACKEND/ALGO/ALGO.py`). The
  command-line support there is vestigial, takes a different argument set, and is explicitly
  not the recommended way to run experiments.
- **Using ZShell without escaping square brackets**: ZShell treats them as special characters
  and Spinning Up uses them for both list values and shorthands.
- **One seed.** RL algorithms have high variance; the flag exists so you use it (ch10 asks
  for at least 3, ideally 10 or more).
- **Expecting parallel experiment launches.** Sweeps run in series by design.

## Key Takeaways
1. Every kwarg is a flag; every list of flag values is a sweep.
2. Sweeps run in series; MPI parallelism is per-experiment via `--cpu`, and only for
   algorithms that support it.
3. Save-directory suffixes encode only the varying hyperparameters, never the seed — that
   grouping is what makes multi-seed plotting work.
4. `ExperimentGrid` is the scripted form and loses only the shortcut kwargs.
5. Values go through `eval()`, so activations and other objects can be named on the command line.

## Connects To
- **Ch 5**: what the directories those flags create actually contain.
- **Ch 6**: the plotter, which consumes this directory structure and its autocompletion.
- **Ch 10**: why multi-seed runs are a rigor requirement, not a convenience.
- **Ch 20**: `ExperimentGrid`, `call_experiment` and `setup_logger_kwargs` in Run Utils.
