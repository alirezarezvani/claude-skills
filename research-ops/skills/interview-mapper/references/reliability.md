# Why it's built this way — the evidence base

The skill is designed from research findings (2023–2025). Briefly, why each mechanism exists.

## Verbatim ≠ support (two orthogonal tests)
A quote may be verbatim in the source, yet the conclusion may not follow from it. Empirically: a system with
verbatim quotes scored only 0.033 on entailment; up to 57% of LLM quotes are "post-rationalization"
(the model leans on its own knowledge and back-fills the quote afterward). That's why S2 checks both
verbatim (script) and support (judge model).
Sources: ALCE (EMNLP'23), "Correctness is not Faithfulness in RAG" (SIGIR ICTIR'25).

## Quotes — "regeneration", not extraction
~7.7% of generated quotes aren't found verbatim in the original; many have fillers removed and
punctuation changed, which alters the meaning. Hence `verify_quotes.py`: normalization + fuzzy + a coverage
threshold, not "trust" in the model. Omissions are more dangerous than fabrications (omission 3.45% vs hallucination 1.47%)
→ a mandatory omission check.
Sources: Learning Analytics (CEUR), npj Digital Medicine 2025 (via uintent).

## Multiple runs + consensus
Correct conclusions converge across runs, errors are scattered (self-consistency: +6–18% on benchmarks,
ICLR'23). Multi-agent debate reduces hallucinations (ICML'24). But consensus for open text is
AGREEMENT, not an exact match (Universal Self-Consistency), so `consensus.py` votes
by label and doesn't count paraphrase wordings as disagreement.

## Flag for a human, not an auto-judge
A single LLM judge is unreliable: flip-rate up to 56%, systematic biases (position, length, self-
preference). So disputed cells are NOT decided automatically — they go to a human. This is confirmed
directly on the qual task: "human-in-the-loop necessary"; escalating rare/disputed codes to an expert raises
κ with little manual editing (LAK'26).

## Star model + re-grounding
Multi-turn dialogue accumulates error (~30% in HalluHard), "the model believes itself". So each run is a
fresh context, with the transcript fed anew rather than the chat history.

## Latent constructs — the LLM's limit
On context-heavy codes (tone, intent, power, eNPS) κ drops almost to 0, whereas on
surface ones (sentiment) κ is 0.91–0.95. That's why analytical labels are honestly marked as
candidates for a human.
Sources: PERC'25, AI&Society 2025, mental-health TA (2507.08002).

## Implementation precedents (reuse, don't reinvent)
- **LLMCode**: exact → Levenshtein<5 → rapidfuzz ratio≥90, transfer the annotation onto the verbatim original; unsalvageable — discard.
- **DeTAILS**: not verbatim — discard.
- **Deterministic Quoting**: don't trust the quote text, take it by reference.
Our `verify_quotes.py` is a hybrid: it fixes (fuzzy transfer) + flags/discards + logs everything transparently.

## Threshold calibration on synthetic data (2026-07, re-measured 2026-08 after the difflib fix)

Gold set: `evals/gold/` — 52 labelled cases per language, 6 distortion classes
(exact / noise / truncation / splice / paraphrase / hallucination).
Run: `calibrate_threshold.py`, threshold grid 70–98 (step 2) × coverage {0.4, 0.5, 0.6, 0.7}.

**Current run.** RU: F1 = 1.00 on the 70–88 plateau (P=1.00, R=1.00), then recall drops
(90–96 → 0.97, 98 → 0.91). EN: F1 = 1.00 on the 70–90 plateau, then 92 → 0.98, 94 → 0.97, 96 → 0.95,
98 → 0.90. Coverage across 0.4–0.7 changes no figure in either language — on this gold set LCS coverage
is not a discriminator. Precision is 1.00 across the whole grid in both languages: no false confirmations
under any combination, all the spread comes from recall.
**Defaults 88 / 0.6 are kept** — they sit inside the plateau in both languages.

### What it was before the fix (and why the numbers changed)
The previous calibration gave RU F1=0.89 at threshold 88 (R=0.79) and recorded difflib as "structurally
unreliable": the score of one and the same noisy quote swung 0–96 depending on its position in the text.
The cause turned out not to be difflib as such, but two defects in `fuzzy_score`:

1. `SequenceMatcher` was called with `autojunk` at its default. On strings longer than 200 characters the
   heuristic marks as "junk" any character occurring in more than 1% of positions — for natural text that
   is the space and the frequent letters. Matching then falls apart unpredictably.
2. The window for the second comparison was sized by the longest matched block. A single dropped word
   splits the quote into two blocks, so the quote was compared against half of itself.

With `autojunk=False` and a window sized by the quote: on the org-mapping-vmdi fixture (40 verbatim quotes
with one word dropped) the median score goes 7.9 → 96.8 and 0/40 → 40/40 pass threshold 88; the control
hallucination is still rejected (5.7 → 40.0, below threshold). The unit-test case that previously scored
≈87 on difflib and forced the threshold down to 85 now scores 94.3 — exactly the score that used to be
attributed to rapidfuzz. There is no separate fuzzy backend in the skill, and none is needed.

Honest caveats: synthetic ≠ real interviews (the distortions are constructed, not harvested from a real
model); a 1.00 plateau across the whole 70–88/90 range means the gold set holds no cases near the decision
boundary, i.e. it is no longer sensitive to the threshold — that is a caveat about the set, not proof that
88 is optimal. The "verbatim but does not support the thesis" class is absent here — that is entailment,
caught by `check_support.py`, not by a verbatim threshold. Before trusting this on your own data, calibrate
on your own gold set (`references/validation.md`) and stock it with near-miss cases, or the calibration
measures nothing.
