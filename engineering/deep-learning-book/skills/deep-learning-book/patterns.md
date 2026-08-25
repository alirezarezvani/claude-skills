# Patterns

Recurring techniques from the book, stated as instruments with their trade-offs. Each names the
chapter that develops it.

## Derive the loss from the output distribution (ch03, ch06)

Choose what p(y|x) is, then take its negative log. Gaussian → MSE, Bernoulli → binary
cross-entropy, categorical → cross-entropy, Laplace → MAE, mixture → mixture density loss.
**Trade-off:** none — this is strictly better than picking a loss by habit. **Failure mode it
prevents:** MSE on bounded, count-valued or heavily skewed targets.

## Work in log-space (ch04)

Sums of logs instead of products of probabilities; stabilized softmax and `log_softmax` rather
than hand-rolled exp/normalize. **Trade-off:** slightly more care at implementation time.
**Prevents:** silent underflow, NaN losses, and inf logits.

## Train-error-first triage (ch11, ch05)

Read training error before deciding anything. High training error → capacity or optimization is
the bottleneck; more data will not help. Low training error with high validation error → data or
regularization. **Trade-off:** requires honest, non-leaky splits. **Prevents:** the most expensive
common mistake, which is collecting data to fix underfitting.

## Overfit a tiny subset as a smoke test (ch11)

Take 10–50 examples and drive training loss to ~0. If you cannot, you have a bug — not a hard
problem. **Trade-off:** minutes. **Prevents:** weeks of tuning around a broken data pipeline,
a wrong loss reduction, or a detached gradient.

## Random search over grid search (ch11)

With more than about two hyperparameters, random search finds better configurations for the same
budget because it does not spend trials re-testing unimportant dimensions. **Trade-off:** results
are less tidy to tabulate. **Prevents:** exponential waste in dimensions that do not matter.

## Regularize in cost order (ch07)

More real data → augmentation with label-preserving transforms → early stopping → weight decay →
dropout → architecture change. Add one at a time and measure the train/val gap after each.
**Trade-off:** slower than stacking everything. **Prevents:** an unattributable result you cannot
tune.

## Parameter sharing over parameter penalties (ch07, ch09)

When a real invariance exists, encode it structurally (convolution, weight tying) rather than
penalizing a free parameter into behaving. **Trade-off:** the prior is hard — wrong invariance
means a wrong model, with no way for data to override it. **Prevents:** paying for capacity you
then have to regularize away.

## Diagnose by gradient behaviour (ch08, ch04)

Gradient norm exploding → clip. Norm large, loss flat → ill-conditioning; use momentum, an
adaptive optimizer, or normalization. Norm near zero with high loss → saturation or dead units;
check initialization and activations. Loss NaN → numerics before modelling. **Trade-off:**
requires instrumentation. **Prevents:** changing the architecture to fix an optimizer problem.

## Tune learning rate and schedule before optimizer family (ch08)

The schedule usually dominates the choice among SGD/Adam variants. **Trade-off:** none. **Prevents:**
optimizer-shopping while the real problem is a step size two orders of magnitude off.

## Name what prevents the identity map (ch14)

Every autoencoder needs an answer: bottleneck, sparsity penalty, input corruption, or Jacobian
contraction. **Trade-off:** each constraint defines a different notion of useful.
**Prevents:** an overcomplete autoencoder that learns a copy and reports a low loss.

## Escape the partition function deliberately (ch18, ch16)

Four routes: sample the negative phase (CD/PCD), sidestep Z algebraically (pseudolikelihood,
score matching), learn around it (NCE), or estimate it for evaluation only (AIS). **Trade-off:**
each optimizes a different objective, so they are not interchangeable. **Prevents:** discovering
mid-project that your undirected model cannot be trained or compared.

## Pick your generative failure mode (ch20, ch03)

Likelihood-based objectives cover modes and blur. Adversarial objectives sharpen and drop modes.
This follows from KL direction, so it is a design choice, not bad luck. **Trade-off:** you must
decide which error your application tolerates. **Prevents:** treating blurriness as a bug to be
tuned away.

## Evaluate representations by transfer, not reconstruction (ch15, ch14)

Linear probes and downstream task performance. **Trade-off:** needs a downstream task.
**Prevents:** optimizing reconstruction error into a code that memorized the input.

## Report Monte Carlo estimates with error bars (ch17)

Standard error and a mixing diagnostic, always. **Trade-off:** more reporting.
**Prevents:** a confidently unimodal answer from a chain that never left its starting mode.
