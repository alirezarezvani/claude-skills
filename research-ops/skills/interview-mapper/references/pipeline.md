# Pipeline S1–S4 — in detail

## S1 — Transcript QA
**Goal:** remove factual transcription errors without touching the analysis. Empirically: proofreading fixes names/systems/numbers (Layer 1), not tone/conclusions.

Steps:
1. `number_lines.py input.(txt|docx)` → numbered `*_nl.txt`.
2. Go through the transcript and list distortion candidates:
   - proper names (people, departments, systems, products, exhibitions),
   - numbers (%, tenure, quantities, prices),
   - "garbage"/nonsensical chunks where the ASR clearly broke.
3. For each candidate — tag "which cell it touches" (e.g., system → K5/E4). If none — low priority.
4. Classify the fix:
   - **confident** (context is unambiguous: "KAIS/comiss" → KAMIS) — fix it, log it in `(was → became, type, rationale)`;
   - **disputed** (can't be guessed without audio: a surname, an ambiguous word) — do NOT fix, move to the "disputed, needs audio" section.
5. Save: clean copy `*_proofread_nl.txt` + `proofreading_log.md`.

Mark the fix type: [F] fact, [D] diarization (speaker mixed up).

## S2 — Interpretation + grounding
1. Read the relevant `templates/<lens>.md`.
2. Fill in Layer 1 (1 run). Each cell: conclusion + **verbatim quote** + `LNN`.
3. Assemble `claims.json`: `[{"cell":"K5","claim":"brief thesis","quote":"verbatim","line":22}]`.
4. `verify_quotes.py --transcript *_proofread_nl.txt --claims claims.json --out qcheck.json`.
   - `rejected` → quote not in the source: replace with a verbatim one or drop the thesis.
   - `line_mismatches` → fix the line number.
   - record `verified_share` — you'll need it as the run's weight in S3.
5. Entailment (yourself as judge): for each thesis↔quote pair — "does the quote support the thesis?". No → weaken it / move to "in question".
6. Counterfactual + omission: "what contradicts the conclusions? which fragments aren't covered?" → the "Gaps/contradictions" section.

## S3 — Reliability council (Layer 2)
1. N isolated Layer 2 runs (3 by default), each a fresh subagent, transcript fed anew.
   Format of each: `{"A1":{"label":"NEUTRAL","text":"..."}, ...}`.
2. `consensus.py run1.json run2.json run3.json --weights w1,w2,w3` (weights = the runs' verified_share).
3. Result:
   - `flagged` (labels diverged) → mark the cell `[⚑ disputed]`, send it to a human for blind adjudication;
   - agreeing → `[consensus]`, take the consensus label, take the text from the most grounded run.

## S4 — Final output format
```
# MAPPING: [respondent] · lens [X]
Grounding: verified N/M quotes; rejected K; disputed Layer 2 cells: F

## Layer 1
**[code] | [theme]**
[conclusion]
_«verbatim quote» (L44) — verified_exact_

## Layer 2
**[code] | [theme]** [consensus | ⚑ disputed — human decides]
[LABEL] [conclusion]
_«quote» (L61) — verified_fuzzy · support: yes_

## Gaps and contradictions
- [what's not covered / what contradicts]

## Rejected quotes (transparency)
- [code]: «…» — rejected (not in the source)

## Proofreading log
- [F] was → became (rationale)
- Disputed (needs audio): …
```

## Sources
- Gao, T. et al. — *Enabling Large Language Models to Generate Text with Citations* (ALCE, EMNLP 2023) — attributed generation and citation-verification pattern behind `verify_quotes.py`.
- Saldaña, J. — *The Coding Manual for Qualitative Researchers* (SAGE, 4th ed., 2021) — the two-layer (facts/analysis) coding structure underlying Layer 1 / Layer 2.
- Braun, V. & Clarke, V. — *Using Thematic Analysis in Psychology* (Qualitative Research in Psychology, 2006) — the code-then-interpret sequencing that S2 follows.
- Miles, M. B., Huberman, A. M. & Saldaña, J. — *Qualitative Data Analysis: A Methods Sourcebook* (SAGE, 4th ed., 2020) — the "counterfactual/omission" discipline (what contradicts, what's uncovered) as a bias check.
- Charmaz, K. — *Constructing Grounded Theory* (SAGE, 2nd ed., 2014) — grounding conclusions in verbatim data before allowing interpretation.
