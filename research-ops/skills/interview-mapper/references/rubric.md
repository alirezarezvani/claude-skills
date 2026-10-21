# Rubric for comparing mappings (human ↔ AI, run ↔ run)

A single tool. Freeze it before the runs, don't change it mid-way.

Applies to any of the 16 lenses, not just org-mapping-VMDI: divergence codes `[F]/[O]/[I]/[R]` are lens-agnostic, and the number and names of cells come from the current lens's template (`templates/<lens>.md`) — e.g., K1–K7 for `candidate`, its own codes for `usability`.

## Unit
Each cell of the chosen lens (e.g., 18 for org mapping, K1–K7 for candidate). We score by coverage + flag divergences.

## Coverage scale (1–5)
- **5** — complete: all key facts/names/numbers + quote, no errors.
- **4** — nearly complete: 1 minor omission.
- **3** — partial: the meaning is caught, specifics lost.
- **2** — weak: only the theme, details confused/missing.
- **1** — failure: theme not covered / gross error / hallucination.

## Types of divergence
- **[F]** factual error (name, number, attribution; often — a trace of transcription distortion).
- **[O]** omission (was in the source, didn't make it into the cell).
- **[I]** reinterpretation (the conclusion doesn't rest on the respondent's words).
- **[R]** frame mismatch (theme assigned to the wrong column / different level of generalization).

## What to record
**Run↔run (Experiment 1, proofreading effect/variance):** did the cell shift, the type, did the CONCLUSION change (not the wording). Bottom line — the share of cells where the meaning moved.

**Human↔AI (Experiment 2):** for each cell, the winner (human/AI/parity) + the loser's divergence type. Separately: where the AI hallucinates, where the human didn't make the analytical conclusion.

## Per-cell Δ
Aggregate Δ by cell of the CURRENT lens, as in the "FINAL COMPARISON" template. The number and names of cells come from the lens template (`templates/<lens>.md`), not fixed.

| Cell | Avg. Δ AI↔Human | Main divergences/agreements |
|---|---|---|
| cell code … cell code | average over the cell | cells with Δ≤2 — where AI and human diverged the most |

This shows in which cells the AI is reliable (Δ≈4–5) and where a human is needed (Δ≤2 — usually latent).

**Example (org-mapping-VMDI):** for the VMDI codebook, cells group into blocks:

| Block | Avg. Δ AI↔Human | Main divergences/agreements |
|---|---|---|
| Block 1 … Block 6 | average over the block's codes | codes with Δ≤2 — where AI and human diverged the most |

This is one specific implementation (latent for VMDI is usually eNPS, recognition culture, forecast), not the only possible table shape.

## Honesty rule
The score in a human↔AI comparison is set by a **human, blind** (not knowing which is AI). "Parity 5/5", assigned by the AI itself by comparing texts, is not a blind score — mark it as such.

## Separate variance from effect
A single A/B run confuses "proofreading effect" and "the model's run-to-run variance". To separate them strictly —
≥3 runs of each version, measure which cells flip with the transcript UNCHANGED (that is the variance).

## Sources
- Cohen, J. — *A Coefficient of Agreement for Nominal Scales* (Educational and Psychological Measurement, 1960) — the origin of chance-corrected inter-rater agreement, the logic behind scoring "run vs run" divergence rather than raw disagreement.
- Landis, J. R. & Koch, G. G. — *The Measurement of Observer Agreement for Categorical Data* (Biometrics, 1977) — benchmark bands for interpreting agreement strength, informing what counts as a "divergence" worth flagging.
- Krippendorff, K. — *Content Analysis: An Introduction to Its Methodology* (SAGE, 4th ed., 2018) — alpha reliability and the general discipline of a fixed, pre-registered coding scheme (freeze the rubric before the runs).
- McDonald, N., Schoenebeck, S. & Forte, A. — *Reliability and Inter-rater Reliability in Qualitative Research: Norms and Guidelines for CSCW and HCI Practice* (CSCW 2019) — blind, independent scoring as the norm this rubric enforces.
- Saldaña, J. — *The Coding Manual for Qualitative Researchers* (SAGE, 4th ed., 2021) — divergence typology (omission, reinterpretation, frame mismatch) mirrors the "types of code drift" literature.
