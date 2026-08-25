# Transcript scoring canon — why rubric-anchored LLM judging works, and where it fails

How skill-doctor's scoring step is designed, and the evidence behind each design
choice. The scoring agent is an LLM judge; everything numeric downstream of it is
deterministic code. This split is the whole architecture.

## 1. LLM-as-judge is reliable enough — when anchored

Zheng et al. showed GPT-4-class judges reach >80% agreement with human experts on
conversation quality — the same level as human-human agreement — but only when the
judgment is structured; free-form "rate this 1–10" drifts badly (source 1). G-Eval
found the same: chain-of-thought judging against explicit criteria beats bare
scoring on summarization benchmarks (source 2). skill-doctor therefore never asks
for a number. The judge picks a **label from a closed table** (four efficiency
labels, three code-quality labels) and must justify it with transcript specifics.

Known judge failure modes the design compensates for:

| Failure mode | Evidence | Countermeasure here |
|---|---|---|
| Score inflation / leniency bias | Zheng et al. §3.3 (source 1) | Labels map to fixed scores in `score_aggregator.py`; the judge cannot emit a number |
| Verbosity bias (longer looks better) | Zheng et al. §3.3 | Transcripts are condensed to a fixed budget before judging |
| Position/order effects | Zheng et al. §3.3 | Each session judged independently, never pairwise |
| Rationale-free verdicts | G-Eval (source 2) | Reasons are mandatory and length-checked (≥ 20 chars, must cite specifics) |
| Judging fabricated work | SWE-bench Verified re-annotation found ~30% of tasks unscoreable as stated (source 3) | Aggregator rejects scores for sessions that were never sampled |

## 2. Verification must be cheaper than generation

Wei's asymmetry-of-verification argument: tasks improve fastest where checking an
answer is much cheaper than producing it (source 4). Grading a finished transcript
against a rubric is exactly that shape — the expensive part (the session) already
happened. This is also why the aggregation is code, not judgment: label-to-score
mapping, weighted means, and coverage fractions are verifiable in one read.

## 3. Mine the benchmark from real usage, not from synthetic tasks

Microsoft's SkillOpt sleep engine established the pattern this repo already
vendors: harvest past session transcripts read-only, mine recurring tasks, and
treat real usage as the evaluation set (source 5). Upstream skill-doctor (source
6) applies the same idea to grading: the sessions that actually ran in this repo
are the only honest benchmark for whether its skills help. Synthetic eval tasks
measure what you imagined; the last 45 days measure what happened.

## 4. Two rubrics, deliberately disjoint

The efficiency rubric scores the **process** (rework, flailing, batching, cost to
the human); the code-quality rubric scores the **artifact** as a senior reviewer
would, explicitly excluding process. The disjointness comes from upstream (source
6) and matches Anthropic's guidance that agent evaluation should separate
trajectory quality from outcome quality (source 7). Keeping them disjoint is what
makes a `highly_efficient` + `block` combination informative: fast path, wrong
artifact — usually a missing check, which is a skill gap.

## 5. Aggregation weights

`overall = 0.5·efficiency + 0.35·code_quality + 0.15·skill_coverage` is carried
from upstream (source 6). Efficiency dominates because it compounds: routine-step
overhead recurs every session until a skill encodes the fix. Coverage is weighted
lowest because it is instrumental — a proxy for whether installed skills fire, not
an end in itself. Confidence: these weights are upstream's editorial choice, not
an empirical fit; treat the sub-scores as the signal and the overall as a headline.

## Sources

1. Zheng, L. et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* arXiv:2306.05685.
2. Liu, Y. et al. (2023). *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment.* arXiv:2303.16634.
3. OpenAI (2024). *Introducing SWE-bench Verified.* openai.com/index/introducing-swe-bench-verified — human re-annotation of a coding benchmark's scoreability.
4. Wei, J. (2025). *Asymmetry of verification and verifier's law.* jasonwei.net blog.
5. microsoft/SkillOpt — `skillopt_sleep` engine (MIT), vendored in this repo at `engineering/skillopt-sleep/`: mine the benchmark from real session history.
6. warpdotdev/common-skills — `skill-doctor` at commit `f3b58c81` (MIT): the upstream rubrics, sampling strategy, and weights this skill rebuilds.
7. Anthropic (2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents — separate the trajectory from the outcome when evaluating agent work.
