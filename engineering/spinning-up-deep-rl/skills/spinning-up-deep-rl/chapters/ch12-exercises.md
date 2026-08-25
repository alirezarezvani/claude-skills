# Chapter 12: Exercises

## Core Idea
Two problem sets with opposite purposes: Problem Set 1 makes you write the mathematical
core of three algorithms, and Problem Set 2 makes you **watch RL code fail silently** and
find out why — because that is the skill the essay says decides whether you can do this work.

## Frameworks Introduced
- **Problem Set 1: Basics of Implementation** — you are given everything except the math.
  - **1.1 Gaussian Log-Likelihood.** Write a function taking means, log stds and samples,
    returning the log likelihoods. Auto-checked against a known-good implementation on a
    batch of random inputs. The formula is the one in ch7.
  - **1.2 Policy for PPO.** Implement an MLP diagonal Gaussian policy. Auto-checked by
    running 20 epochs on InvertedPendulum-v2 (3-5 minutes). **Bar for success: average score
    over 500 in the last 5 epochs, or 1000 (the maximum) in the last 5.**
  - **1.3 Computation Graph for TD3.** You are given the entire TD3 algorithm *except* the
    loss functions and the intermediate calculations for them. Find "YOUR CODE HERE".
    No automatic checking. Evaluated on HalfCheetah-v2, InvertedPendulum-v2 and one other
    MuJoCo environment of your choosing, with smaller networks ([128,128]), max episode
    length 150, 10 epochs, roughly 10 minutes. **Anecdotal targets within 10 epochs:
    HalfCheetah over 300, InvertedPendulum maxing out at 150.** `--use_soln` runs Spinning
    Up's TD3 instead of yours.

- **Problem Set 2: Algorithm Failure Modes** — the point is the failure, not the fix.
  - **2.1 Value Function Fitting in TRPO.** Compare `train_v_iters=80` against
    `train_v_iters=0` on Hopper-v2, three seeds each, 250 epochs, 4000 steps per epoch.
    **Result: the difference is substantial. With a trained value function the agent makes
    quick progress; with an untrained one it gets stuck early on.** Few factors affect policy
    gradient performance more drastically than the quality of the value function used for
    advantage estimation.
  - **2.2 Silent Bug in DDPG.** Run DDPG with and without a planted bug, three seeds each,
    six runs, ~10 minutes each; plot and compare. Then, **without looking at DDPG's `core.py`**,
    work out what the bug is.

## Worked Example
**The 2.2 bug, and why it is the most instructive page in the book.**

The correct and bugged actor-critic differ in exactly one thing: whether the Q-function
output is squeezed.

```python
# Correct
def forward(self, obs, act):
    q = self.q(torch.cat([obs, act], dim=-1))
    return torch.squeeze(q, -1)   # Critical to ensure q has right shape.

# Bugged
def forward(self, obs, act):
    return self.q(torch.cat([obs, act], dim=-1))   # shape [batch, 1], not [batch]
```

The TF1 version is the same defect: the correct code squeezes to shape `[batch size]`, the
bugged code leaves shape `[batch size, 1]`.

Why that one missing squeeze destroys learning — look at the DDPG graph:

```python
backup = tf.stop_gradient(r_ph + gamma*(1-d_ph)*q_pi_targ)
pi_loss = -tf.reduce_mean(q_pi)
q_loss  = tf.reduce_mean((q - backup)**2)
```

`r_ph` and `d_ph` have shape `[batch size]`. The backup line was written assuming it adds
tensors of the same shape. But it will also happily add tensors of *different* shapes as long
as they are broadcast-compatible — and `[batch size]` and `[batch size, 1]` are compatible,
with results that are not what you expect:

```
x has shape [5], y has shape [5,1]
x * y  ->  shape [5,5]
x + y  ->  shape [5,5]
```

Adding or multiplying a shape-`[5]` tensor by a shape-`[5,1]` tensor returns a shape-`[5,5]`
tensor. So when the Q-functions are not squeezed, `q_pi_targ` has shape `[batch size, 1]`,
the backup becomes a `[batch, batch]` matrix, and the whole Q-loss is meaningless. **Nothing
raises. Nothing warns. The run completes. The agent just learns worse.**

This is ch10's "broken RL code almost always fails silently" reduced to a single missing
`squeeze`. The **Bonus** question is worth sitting with: *are there any choices of
hyperparameters which would have hidden the effects of the bug?*

## Anti-patterns
- **Looking at `core.py` before attempting 2.2.** The exercise is diagnostic practice; the
  answer is worth less than the search.
- **Broadcast-compatible shapes as an implicit contract.** The lesson generalizes far past
  DDPG: any elementwise op between a `[N]` and an `[N,1]` tensor is a silent bug waiting.
  Assert shapes.
- **Skipping Problem Set 2 because it produces no code.** 2.1 produces no code at all and is
  still one of the most decision-relevant results in the book.

## Key Takeaways
1. Problem Set 1 is math-in-code: Gaussian log-likelihood, a PPO policy, TD3's losses.
2. 1.1 and 1.2 self-check; 1.3 does not, and is evaluated on visible learning progress.
3. 2.1: a badly-fit value function does not degrade a policy gradient agent gracefully — it
   gets stuck early.
4. 2.2: one missing `squeeze` silently corrupts the Bellman backup through broadcasting.
5. The challenges past the problem sets are: reimplement algorithms from scratch (ch10), and
   attempt OpenAI's standing Requests for Research.

## Connects To
- **Ch 7**: the diagonal Gaussian log-likelihood formula that Exercise 1.1 asks for.
- **Ch 9**: why the value function baseline quality drives policy gradient performance (2.1).
- **Ch 17 and Ch 18**: the DDPG graph and the TD3 losses the exercises operate on.
- **Ch 10**: "broken RL code almost always fails silently" — Problem Set 2 is the proof.
