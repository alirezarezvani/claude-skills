# Validation and calibration (T1) — before trusting the conclusions

The skill is assembled from research; the thresholds are calibrated on synthetic data only (`reliability.md`) and accuracy on real data hasn't been measured. Before "production" use — run this stage. Otherwise you're building on sand.

## What we calibrate
Thresholds in the scripts are hyperparameters, not truth:
- `verify_quotes.py`: fuzzy `--threshold` (default 88), `--min-coverage` (0.6).
- `score_insights.py`: triangulation `--k` (3), watchlist `--severe` (4).
The only threshold documented in the primary sources is difflib 0.6; the rest is practice. Calibrate on your own data.

## Calibrating the verbatim threshold
1. Assemble a **gold-set** manually: 15–40 examples `{"quote":"…","is_verbatim":true/false}`.
   - true: the quote is really in the source (including with ASR noise).
   - false: a fabrication OR a heavy "regeneration" (words removed such that the meaning shifted).
   - **The most valuable are near-misses**: real quotes with fillers/punctuation removed (regenerations). On easy fabrications any threshold gives F1=1.0 and calibrates nothing.
2. `python scripts/calibrate_threshold.py --transcript T.txt --gold gold.json [--prefer-precision]`
3. Take the recommended threshold. For mapping, **precision** usually matters more (fewer false "verified" quotes) → `--prefer-precision`.

## Mini-eval skill vs baseline (qualitative)
The full eval cycle — via skill-creator. The minimum for a sanity check:
1. Take 2–3 transcripts.
2. Run the task twice: with this skill and without (baseline).
3. Compare via `references/rubric.md` (coverage 1–5 + divergence types). The score is set by a human, blind.
4. Look not only at the bottom line, but also at: the share of rejected quotes, the number of council flags, the caught omissions.
Test prompts — in `evals/evals.json`.

## Separate variance from effect (important!)
A single A/B run confuses "proofreading effect" and "the model's run-to-run variance". To separate them:
- run ONE transcript version 3–5 times, count which Layer 2 cells flip with the text unchanged — that's pure variance;
- only then compare raw vs proofread. The difference beyond variance = the proofreading effect.

## Honest status
- n<k interviews → synthesis yields no insights, only watchlist. Don't pass it off as a pattern.
- gold-set <15 examples → the threshold is approximate.
- Latent labels (eNPS, etc.) are unstable by nature — calibration doesn't fix it, only the council + a human.

## Pilot on a real interview (breaking the closed loop)

The fixtures, the gold set and the distortions in this repo were written by the same model that later does the
mapping. Such an eval checks internal consistency, not whether the skill works on live speech: real ASR breaks
differently from constructed noise, and a real respondent talks longer and messier. Until a pilot is run, the
honest status line is "not validated on real data", not "F1 = 1.00".

The minimal pilot — one interview, one person, half a day:

1. Take a REAL transcript (not tidied up for looks) and a human mapping made with the same lens, independently
   and BEFORE the skill run. No human version — make it first, or there is nothing to compare against; knowing
   the AI's output spoils the baseline irreversibly.
2. Run S1–S2 in full. Record three numbers: the share of `rejected` quotes, the number of `dangerous` verdicts
   from `check_support.py`, and the number of omissions found on the counterfactual pass.
3. `compare_to_gold.py` → a blind review blank. The 1–5 scores from `references/rubric.md` are set by a human
   who cannot see which side is the AI's.
4. Run S3 on the unstable cells and check: are the flagged cells the ones the human also considers disputed? A
   match says the council works; a mismatch says instability is being caught in the wrong place.
5. Separately, eyeball the `rejected` quotes. Each one is either a genuine fabrication (the skill did its job)
   or a correct quote cut by the threshold (a recall miss). The second case feeds calibration directly: those
   quotes are exactly the near-miss cases the synthetic gold set lacks.

What counts as a failed pilot: a `rejected` share above ~15% while the quotes check out by eye (the threshold
does not suit your data); `dangerous` verdicts the human does not confirm (the judge is noisy); an average Δ
below 4 on Layer 1 (facts are not being extracted — the lens does not fit the material, and thresholds are not
the issue).

## Sources
- Powers, D. M. W. — *Evaluation: From Precision, Recall and F-Measure to ROC, Informedness, Markedness and Correlation* (Journal of Machine Learning Technologies, 2011) — the precision/recall/F1 sweep `calibrate_threshold.py` runs against the gold-set.
- Krippendorff, K. — *Content Analysis: An Introduction to Its Methodology* (SAGE, 4th ed., 2018) — reliability calibration against a labeled set before trusting an automated coder.
- Cohen, J. — *A Coefficient of Agreement for Nominal Scales* (Educational and Psychological Measurement, 1960) — chance-corrected agreement, the same family of statistic the variance-vs-effect separation borrows from.
- Landis, J. R. & Koch, G. G. — *The Measurement of Observer Agreement for Categorical Data* (Biometrics, 1977) — interpreting how "good" a calibrated threshold's agreement actually is.
- Guest, G., Bunce, A. & Johnson, L. — *How Many Interviews Are Enough?* (Field Methods, 2006) — honesty about small samples, mirrored here in "n<k → watchlist, not insight."
