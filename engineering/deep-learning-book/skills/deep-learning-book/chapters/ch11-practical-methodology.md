# Chapter 11: Practical Methodology

**Source chapter (free, official):** https://www.deeplearningbook.org/contents/guidelines.html

## Core Idea

Knowing many algorithms matters less than knowing which one to reach for given a measurement.
This chapter is a workflow: pick a metric, build an end-to-end baseline fast, then let
instrumentation — not intuition — decide whether to add data, capacity, or regularization.

## Frameworks Introduced

- **The design process**: (1) determine goals — the error metric and the target value; (2) build
  a working end-to-end pipeline early; (3) instrument it to find bottlenecks; (4) change one
  thing at a time based on measurement.
- **Choose the metric before the model**: accuracy, precision/recall, F-score, PR/ROC curves,
  coverage. Name the target value and where it came from.
- **Sensible baselines**: pick the standard architecture and optimizer for the data type before
  inventing anything.
- **More data or a bigger model?** — the decision procedure: if training error is high, the model
  or the optimization is the bottleneck (data will not help). If training error is low and test
  error is high, gather more data or regularize.
- **Hyperparameter tuning**: manual (understand what each knob does to effective capacity),
  **grid search** (poor scaling in dimensions), **random search** (better — it does not waste
  trials on unimportant dimensions; Bergstra & Bengio 2012), and model-based/Bayesian.
- **Debugging strategies**: visualize the model's actual predictions and worst cases; fit a tiny
  subset to zero training error; compare backprop against numerical derivatives; monitor
  activation and gradient histograms.

## Mental Models

- Use the **train-error-first rule** as the single most valuable heuristic in the book: high
  training error means "do not collect data yet."
- Treat "**can it overfit 20 examples?**" as the smoke test that separates a bug from a modelling
  limitation. If it cannot, you have a bug.
- Prefer **random search over grid search** whenever the number of hyperparameters exceeds ~2.

## Anti-patterns

- **Tuning many things per experiment** — you learn nothing attributable.
- **Collecting more data to fix underfitting.**
- **Optimizing a proxy metric** whose relationship to the real objective was never checked.
- **Skipping the end-to-end pipeline** in favour of perfecting one component.

## What changed after 2016

The workflow is the most durable material in the book and is now the backbone of MLOps practice.
Additions since: experiment tracking as standard tooling, seeded reproducibility expectations,
Hyperband/ASHA for early-stopping-based search (post-2016), and — for large models — scaling laws
used to *predict* the return on more data or parameters instead of testing empirically at full
size. **Confidence: high.**

## Key Takeaways

1. Write the metric and its target number before writing model code.
2. Ask "is training error high?" before every data or capacity decision.
3. Change one thing per experiment and log it.

## Connects To

- **Ch 5**: the underfit/overfit framing this operationalizes.
- **Ch 7 / Ch 8**: the two toolboxes the workflow selects from.
- **scripts/training_diagnostics.py**: this decision tree, executable.
