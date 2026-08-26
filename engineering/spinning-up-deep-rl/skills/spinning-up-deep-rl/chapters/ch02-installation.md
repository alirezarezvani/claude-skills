# Chapter 2: Installation

## Core Idea
Spinning Up needs Python 3, OpenAI Gym and OpenMPI, on Linux or OSX; MuJoCo is optional
but is the de facto benchmarking standard, and everything in the book works without it on
the free Classic Control and Box2D environments.

## Frameworks Introduced
- **Install then immediately verify with a real training run**: the install is not confirmed
  by a successful `pip install`, it is confirmed by an agent visibly learning.
  - When to use: every fresh environment, before debugging anything else.
  - How: run the install test below, then watch the policy and plot the curve. Three
    commands, three different subsystems (training, rendering, plotting) verified.

## Key Concepts
- **OpenMPI**: the message-passing library used for the parallelized (on-policy) algorithms.
  Installed with `apt-get install libopenmpi-dev` on Ubuntu, `brew install openmpi` on Mac.
- **MuJoCo**: a proprietary physics engine; free to trial and free for full-time students,
  otherwise paid. The de facto standard for benchmarking continuous-control deep RL.
- **mujoco-py**: the Python bindings that let Gym use MuJoCo.
- **Classic Control / Box2D**: Gym environment families that are completely free and
  sufficient to get started.
- **Editable install**: `pip install -e .` from the cloned repo, so edits to the algorithm
  files take effect without reinstalling — the intended workflow for a repo you are meant
  to read and modify.

## Code Examples
Environment and dependencies:

```bash
conda create -n spinningup python=3.6
conda activate spinningup

# Ubuntu
sudo apt-get update && sudo apt-get install libopenmpi-dev
# Mac OS X (requires Homebrew)
brew install openmpi

git clone https://github.com/openai/spinningup.git
cd spinningup
pip install -e .
```

Verify the install (roughly 10 minutes; leave it running and keep reading):

```bash
python -m spinup.run ppo --hid "[32,32]" --env LunarLander-v2 \
    --exp_name installtest --gamma 0.999
python -m spinup.run test_policy data/installtest/installtest_s0
python -m spinup.run plot data/installtest/installtest_s0
```

Optional MuJoCo, after following the mujoco-py README and obtaining a license:

```bash
pip install gym[mujoco,robotics]
python -m spinup.run ppo --hid "[32,32]" --env Walker2d-v2 --exp_name mujocotest
```

## Reference Tables

| Requirement | Status | Notes |
|-------------|--------|-------|
| Python 3 | Required | Anaconda recommended; the docs pin 3.6 |
| OpenAI Gym | Required | Installed by `pip install -e .`, MuJoCo envs excluded |
| OpenMPI | Required | Needed for the MPI-parallelized on-policy algorithms |
| Linux / OSX | Required | Windows unsupported and untested; one community workaround exists |
| MuJoCo | Optional | Proprietary, licensed; preferred because of benchmarking convention |

## Anti-patterns
- **Skipping the install test** and then debugging an algorithm that was never installed
  correctly. The install test costs ten unattended minutes.
- **Treating a MuJoCo licence as a prerequisite for learning RL**: Classic Control and Box2D
  are free and adequate for everything up to benchmarking.
- **Fighting package management ad hoc**: the docs go out of their way to point at conda
  explainers, because "I just installed this thing but it says it's not found" is the
  predicted failure, not an unusual one.

## Key Takeaways
1. Install is Python 3 + Gym + OpenMPI, plus optional MuJoCo; Linux or OSX only.
2. `pip install -e .` (editable) because you are expected to modify the code.
3. Verification means an actual short PPO run, a rendered policy and a plot.
4. Not having MuJoCo blocks benchmarking, not learning.

## Connects To
- **Ch 4**: `python -m spinup.run` is the entry point every later chapter uses.
- **Ch 13**: the benchmarks that make MuJoCo the convention.
- **Ch 20**: the MPI utilities that OpenMPI enables.
