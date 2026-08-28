# Chapter 5: Experiment Outputs

## Core Idea
Every run saves four things — a config record, a TSV of training metrics, the trained
model, and a pickled copy of the environment — and only one of them (`config.json`) is
ever meant to be read by hand.

## Frameworks Introduced
- **Tools, not files**: `test_policy` loads from `pyt_save/` or `tf1_save/`, the plotter
  interprets `progress.txt`. Those are the correct interfaces. `config.json` is the only
  file you should ever open yourself, and only to remember what you ran.
  - When to use: any time you are tempted to parse a save directory manually.

- **Watch, then measure**: `test_policy` renders the agent so you can see behavior that no
  scalar metric would have shown you; `-nr` drops rendering when you only want the numbers.

## Key Concepts
- **`progress.txt`**: tab-separated records of every metric the logger recorded, e.g. `Epoch`,
  `AverageEpRet`.
- **`config.json`**: as-complete-as-possible dict of the args and kwargs used to launch the run.
  Record-keeping only — launching an experiment from a config file is not supported.
- **`vars.pkl`**: algorithm state; currently used only to save a copy of the environment.
- **`pyt_save/model.pt`**: a pickled PyTorch `nn.Module`; loading restores an ActorCritic
  object with an `act` method.
- **`tf1_save/`**: `variables/`, `model_info.pkl` (key-to-tensor-name map) and `saved_model.pb`.
  Renamed from `simple_save/` on 2020-01-30.
- **`DEFAULT_DATA_DIR`**: set in `spinup/user_config.py`; defaults to `spinningup/data`.

## Reference Tables

| File | Contents |
|------|----------|
| `pyt_save/` | PyTorch only. Everything needed to restore the agent and value functions |
| `tf1_save/` | TF1 only. SavedModel plus the key-to-tensor map |
| `config.json` | The launch args and kwargs. Non-serializable values become strings |
| `progress.txt` | TSV of logged metrics across training |
| `vars.pkl` | Pickled environment copy; may be empty if the env cannot be pickled |

`test_policy` flags:

| Flag | Default | Does |
|------|---------|------|
| `-l L`, `--len=L` | 0 | Max episode length; 0 means no maximum |
| `-n N`, `--episodes=N` | 100 | Number of test episodes |
| `-nr`, `--norender` | off | Print returns and lengths only; much faster |
| `-i I`, `--itr=I` | -1 | Which saved snapshot; -1 is latest (see below) |
| `-d`, `--deterministic` | off | **SAC only.** Use the deterministic mean policy |

## Code Examples
```bash
python -m spinup.run test_policy path/to/output_directory
```

When the environment failed to pickle and `test_policy` raises `AssertionError: Environment
not found!`, rebuild it by hand:

```python
from spinup.utils.test_policy import load_policy_and_env, run_policy
import your_env
_, get_action = load_policy_and_env('/path/to/output_directory')
env = your_env.make()
run_policy(env, get_action)
```

To keep snapshots from many points in training (off by default — algorithms overwrite the
most recent one), change the line present in every algorithm:

```python
logger.save_state({'env': env}, None)      # default: one snapshot, overwritten
logger.save_state({'env': env}, epoch)     # keep per-epoch snapshots
```

and then set `save_freq` to something reasonable — at the default of 1 you flood the output
directory with one folder per epoch.

## Anti-patterns
- **Forgetting `-d` when evaluating SAC.** SAC trains a stochastic policy but the correct
  evaluation policy is the deterministic mean. Without the flag you are measuring the wrong
  thing, and the flag is used for no other algorithm.
- **Expecting to resume training.** Spinning Up implementations have no way to resume a
  partially-trained agent.
- **Trying to relaunch from `config.json`.** It is a record, not an input.
- **Assuming `vars.pkl` has your environment.** Gym Box2D environments in older Gym versions
  are known to fail to pickle, leaving it empty.

## Key Takeaways
1. Four artifacts per run; use the tools for three of them and read only `config.json` by hand.
2. SAC evaluation requires `--deterministic`; every other algorithm ignores it.
3. Multi-snapshot saving is a two-line change plus a `save_freq` you must set deliberately.
4. Environment pickling can silently fail — the recovery path is rebuilding the env in Python.
5. No resume support; a killed run is a lost run.

## Connects To
- **Ch 4**: the flags that create these directories.
- **Ch 6**: `progress.txt` is what the plotter reads.
- **Ch 19**: why SAC's evaluation policy differs from its training policy.
- **Ch 20**: the EpochLogger that writes all of this.
