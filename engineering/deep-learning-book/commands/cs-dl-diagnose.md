---
name: "cs-dl-diagnose"
description: "/cs:dl-diagnose — Diagnose a training run against Chapter 11's decision tree: read training error before deciding anything, and never diagnose a NaN as overfitting. Returns a ranked cause, the specific next action, and the chapter that justifies it."
argument-hint: "[what the run is doing — losses, gradient norm, or a description]"
---

# /cs:dl-diagnose — Measurement first, hypothesis second

**Command:** `/cs:dl-diagnose [symptoms]`

Chapter 11's rule, which most teams have backwards: **read training error first.** High
training error means the model or the optimizer is the bottleneck, and more data cannot help.

## Procedure

1. **Collect the instruments.** Ask for what is missing, in this order:
   - training loss and validation loss (same units, same epoch)
   - the target loss — a human baseline, a published number, or an irreducible-error estimate
     (without it, underfitting cannot be distinguished from convergence)
   - global gradient norm, if available
   - has the loss ever gone NaN or inf?
   - can the model drive training loss to ~0 on 10–50 examples? (the smoke test that separates
     a bug from a hard problem)
2. **Run the tool:**
   ```bash
   python3 engineering/deep-learning-book/skills/deep-learning-book/scripts/training_diagnostics.py \
       --train-loss <x> --val-loss <y> --target-loss <z> --grad-norm <g> \
       --tiny-subset-fits yes|no|unknown
   ```
   Exit 4 means not enough instruments — ask for one of the named measurements rather than
   guessing.
3. **Act on finding [1] first.** Rules fire in priority order for a reason: a non-finite loss is
   a numerics failure, not a modelling one, and a model that cannot overfit 20 examples has a
   bug that no hyperparameter will fix.
4. **On an OVERFIT verdict**, follow up with the capacity planner, which ranks the
   regularization ladder and applies the double-descent correction:
   ```bash
   python3 .../capacity_planner.py --params <n> --train-examples <m> \
       --train-error <x> --val-error <y> --applied early-stopping
   ```
5. **On a memory or throughput question**, run `model_arithmetic.py --spec <file>` — it reports
   parameters, FLOPs and activation memory per example, and refuses a stack whose shapes do not
   connect.
6. **Close with the discipline, not just the fix:** change one thing per experiment, log it,
   re-measure the gap.

## Do not

- Skip to the interesting hypothesis before the rules have been read in order.
- Recommend collecting data while training error is high.
- Recommend shrinking an overparameterized model first — see the double-descent caveat in
  `skills/deep-learning-book/references/book_to_2026_delta.md`.
