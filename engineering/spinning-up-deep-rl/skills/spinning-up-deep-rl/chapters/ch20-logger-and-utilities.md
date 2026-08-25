# Chapter 20: Logger, MPI Tools and Run Utils

## Core Idea
The three utility modules are the only code shared between algorithms — logging (which is
also model saving and config recording), MPI data-parallelism, and ExperimentGrid — and
each has a small fixed usage pattern worth memorizing.

## Frameworks Introduced
- **`Logger` and `EpochLogger`.** `Logger` carries the basic functionality: saving
  diagnostics, hyperparameter configurations, the state of a training run, and the trained
  model. `EpochLogger` adds a thin layer that makes it easy to track the **average, standard
  deviation, min and max** of a diagnostic over each epoch **and across MPI workers**.
  **All Spinning Up algorithm implementations use an EpochLogger.**
  - The three-call pattern: **`store`** accumulates values into internal state,
    **`log_tabular`** computes the statistics over everything stored, **`dump_tabular`**
    writes to file and stdout. **The internal state is wiped clean after `log_tabular`,
    to prevent leakage into the next epoch's statistics.**

- **The MPI + PyTorch pattern** — three steps, in this order:
  1. At the beginning of the training script, call **`setup_pytorch_for_mpi()`**. This is the
     fix for a real problem: each separate process's PyTorch instance tries to grab too many
     threads and they clobber each other.
  2. After constructing a PyTorch module, call **`sync_params(module)`**.
  3. During gradient descent, call **`mpi_avg_grads`** after the backward pass and before the
     optimizer step.
  - The two main ingredients are therefore **syncing parameters** and **averaging gradients
    before they are used by the adaptive optimizer** — the order matters, because averaging
    after the optimizer step would give each worker a different adaptive state.

- **ExperimentGrid** — a tool for hyperparameter ablations, based on but simpler than rllab's
  VariantGenerator. `eg.add(param_name, values, shorthand, in_name)` then
  `eg.run(thunk, **run_kwargs)`; `ExperimentGrid.run` uses `call_experiment` to launch the
  thunk. See ch4 for the full usage.

## Code Examples
The EpochLogger statistic pattern:

```python
from spinup.utils.logx import EpochLogger
epoch_logger = EpochLogger()
for i in range(10):
    epoch_logger.store(Test=i)
epoch_logger.log_tabular('Test', with_min_and_max=True)
epoch_logger.dump_tabular()
```

```
-------------------------------------
|     AverageTest |             4.5 |
|         StdTest |            2.87 |
|         MaxTest |               9 |
|         MinTest |               0 |
-------------------------------------
```

The MPI gradient-averaging step, in place:

```python
optimizer.zero_grad()
loss = compute_loss(module)
loss.backward()
mpi_avg_grads(module)   # averages gradient buffers across MPI processes
optimizer.step()
```

## Reference Tables

| Module | Contents |
|--------|----------|
| `spinup.utils.logx` | `Logger`, `EpochLogger` |
| `spinup.utils.mpi_tools` | Core MPI utilities |
| `spinup.utils.mpi_pytorch` | `setup_pytorch_for_mpi`, `sync_params`, `mpi_avg_grads` |
| `spinup.utils.mpi_tf` | AdamOptimizer across MPI processes. **Explicitly "a bit hacky"** — for something more sophisticated and general-purpose, the docs point to horovod |
| `spinup.utils.run_utils` | `ExperimentGrid`, `call_experiment`, `setup_logger_kwargs` |
| `spinup.utils.plot` | The plotter (documented in ch6) |

## Anti-patterns
- **Calling `mpi_avg_grads` after `optimizer.step()`.** The averaging must happen before the
  adaptive optimizer consumes the gradients, or workers diverge in optimizer state.
- **Skipping `setup_pytorch_for_mpi()`.** The thread-clobbering problem it fixes is a real
  performance failure, not a theoretical one.
- **Expecting `log_tabular` to be idempotent.** It wipes the accumulated state; calling it
  twice for the same key in one epoch gives you statistics over nothing.
- **Reaching for `mpi_tf` as a general distributed-training solution.** The docs say to use
  horovod instead if you need something serious.

## Key Takeaways
1. `store` / `log_tabular` / `dump_tabular` is the whole logger interface, and the state
   resets on `log_tabular`.
2. `EpochLogger` aggregates across MPI workers as well as across an epoch.
3. MPI PyTorch is three calls in a fixed order: setup, sync params, average grads before step.
4. The logger is also the model-saving and config-recording path (ch5).
5. `mpi_tf` is acknowledged as hacky; horovod is the recommended alternative.

## Connects To
- **Ch 4**: ExperimentGrid usage and the CLI it backs.
- **Ch 5**: the outputs the logger writes — `progress.txt`, `config.json`, the save directories.
- **Ch 6**: the plotter, which reads what `dump_tabular` writes.
- **Ch 2**: OpenMPI, the system dependency all of this rests on.
