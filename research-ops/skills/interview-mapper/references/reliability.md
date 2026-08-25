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

## Threshold calibration on synthetic data (2026-07)

Gold set: `evals/gold/` — 52 labeled cases per language, 6 distortion classes
(exact / noise / truncation / splice / paraphrase / hallucination).
Run: `calibrate_threshold.py`, grid of threshold 70–98 (step 2) x coverage {0.4, 0.5, 0.6, 0.7}.

Result: coverage in the 0.4–0.7 range doesn't affect P/R/F1 for either language — on this
gold set, LCS coverage turned out not to be a discriminator with the difflib backend. On
threshold: RU has a F1=0.90 plateau across 70–82, with the default of 88 giving F1=0.89
(P=1.00, R=0.79); the best point wins by only 0.01. EN has a F1=1.00 plateau across 70–88,
and the default of 88 already sits inside that plateau (F1=1.00, P=1.00, R=1.00). Both gains
are below the 0.03 bar → **the 88/0.6 defaults are left unchanged**. Precision is 1.00 on both
languages across the whole grid — no false confirmations at any combination; the spread comes
entirely from recall (noise class).
A caveat for EN: the F1=1.00 plateau across 70–88 with unchanged P/R signals that the EN
gold set is not sensitive enough to the threshold (no cases near the decision boundary) —
not proof that 88 is optimal.

**The threshold depends on the backend.** Calibration was run on the difflib fallback
(rapidfuzz wasn't installed). difflib matches the quote against the whole text, and
SequenceMatcher's autojunk heuristic on texts >200 characters makes scores unstable for
noisy quotes: the same degree of ASR noise yields ~90 in one spot and ~0 in another,
depending on position. On our own gold set the noise class showed a score spread from 0 to
96 for verbatim (is_verbatim=true) quotes — reproduced directly by calling `fuzzy_score()`
in this session. Separately, on a synthetic quote with one word dropped, difflib scored ≈79
(cut by the 88 threshold); rapidfuzz isn't installed in this environment, and its score on
the same pair wasn't re-verified in this session — per a note from a prior calibration
session it was noticeably higher and more stable (on the order of ≈94, passing the
threshold), but that figure isn't re-measured here and is offered as a reference point, not
a fact of the current run. On difflib the gap between verbatim (≈84–100 for most cases) and
non-verbatim is so large that the exact threshold value barely affects precision — but recall
on the noise class is unpredictable and depends on the specific text, not just the degree of
distortion. With rapidfuzz installed (recommended for real work) the noise class behaves
differently — recalibrate on your own backend.

Honest caveats: synthetic data ≠ real interviews (the distortions are constructed, not
collected from a real model); the class "verbatim but doesn't support the claim" isn't
represented here — that's entailment, caught by check_support.py, not the verbatim
threshold. Before trusting this on your own data — calibrate on your own gold set
(references/validation.md).
