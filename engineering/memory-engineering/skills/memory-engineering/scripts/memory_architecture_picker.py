#!/usr/bin/env python3
"""Pick which memory cost to pay on purpose -- there is no best system.

The Stanford characterization (arXiv:2606.06448) evaluated ten memory systems
across four paradigm families and found no single system wins on construction
time, query latency, and accuracy at once. So this tool never returns "best".
It returns the family that fits the stated constraints and names, explicitly,
the cost that choice makes you pay.

The four families, and the taxonomy axes they are scored on (construction,
storage, retrieval, mutability):

  long_context        Paradigm I   -- keep raw history in the window
  flat_rag            Paradigm II  -- BM25 / embedding retrieval over chunks
  structured_rag      Paradigm III -- GraphRAG / Mem0-style extraction
  agentic             Paradigm IV  -- Letta / MIRIX-style agentic control flow

When the top two families score within AMBIGUITY_MARGIN of each other, the tool
refuses to pick and names the one question that would break the tie.

Deterministic scoring only. No LLM calls, no network, stdlib only.

Exit codes:
    0  a single family fits the constraints
    2  ambiguous -- two families tie; a tie-breaking question is printed
    3  invalid input
    4  no family satisfies a hard constraint
"""

import argparse
import json
import sys

AMBIGUITY_MARGIN = 0.06

# Per-family profile. Scores are 0-1 where higher is better on that axis.
# Values encode the qualitative ordering reported in the Stanford
# characterization, not measurements from any one deployment.
FAMILIES = {
    "long_context": {
        "label": "Paradigm I - Long-context memory",
        "examples": "raw history in the context window",
        "build_cheapness": 1.00,  # no construction at all
        "query_speed": 0.25,  # quadratic attention over the whole history
        "recall_quality": 0.55,  # strong within window, cliff-edge outside it
        "scales_with_volume": 0.10,  # hard context ceiling
        "mutability": 0.20,  # cannot selectively update or delete
        "cost_you_pay": (
            "Query latency and a hard ceiling. Cheap to build because there is "
            "no write path, but cost grows quadratically with history and "
            "prefix caching collapses across sessions."
        ),
        "kills_it": "history that outgrows the context window",
    },
    "flat_rag": {
        "label": "Paradigm II - Flat RAG memory",
        "examples": "BM25, EmbedRAG",
        "build_cheapness": 0.85,  # indexing only, no LLM in the write path
        "query_speed": 0.80,
        "recall_quality": 0.55,  # blunt: no relation between chunks
        "scales_with_volume": 0.85,
        "mutability": 0.75,  # re-index a document, but no fact-level edit
        "cost_you_pay": (
            "Precision. Builds almost instantly and stays cheap, but retrieval "
            "is blunt -- it returns chunks that mention the topic, not the "
            "fact that answers the question."
        ),
        "kills_it": "questions whose answer spans several documents",
    },
    "structured_rag": {
        "label": "Paradigm III - Structure-augmented RAG",
        "examples": "GraphRAG, Mem0, HippoRAG v2",
        "build_cheapness": 0.25,  # LLM-mediated extraction on every write
        "query_speed": 0.90,  # small, pre-distilled payload at query time
        "recall_quality": 0.85,
        "scales_with_volume": 0.70,
        "mutability": 0.80,  # fact-level update and delete
        "cost_you_pay": (
            "Construction. Answers fast because the thinking already happened "
            "at write time -- which is exactly why the write path can cost "
            "more than every query it will ever serve."
        ),
        "kills_it": "a write budget that cannot absorb an LLM call per record",
    },
    "agentic": {
        "label": "Paradigm IV - Agentic control flow",
        "examples": "Letta, MIRIX, A-Mem",
        "build_cheapness": 0.10,  # multi-step agent loop per write
        "query_speed": 0.45,  # unbounded LLM-mediated retrieval loop
        "recall_quality": 0.90,
        "scales_with_volume": 0.45,  # footprint compounds as the store grows
        "mutability": 0.95,  # the agent can rewrite its own memory
        "cost_you_pay": (
            "Everything except recall. Highest energy per correct answer in "
            "the Stanford run, worst-case query latency is unbounded without "
            "an explicit cap, and footprint compounds as the store grows."
        ),
        "kills_it": "a hard p99 latency SLO, or an unbounded footprint budget",
    },
}

# Which constraint drives which axis, and how heavily.
WEIGHTS = {
    "query_latency_sensitivity": ("query_speed", 0.28),
    "build_budget_pressure": ("build_cheapness", 0.26),
    "recall_need": ("recall_quality", 0.24),
    "volume_growth": ("scales_with_volume", 0.12),
    "mutability_need": ("mutability", 0.10),
}

LEVELS = {"low": 0.15, "medium": 0.5, "high": 1.0}

# Keyed by the two tied families. Lookup normalizes the pair with sorted(), so
# these keys are normalized too -- see the guard below. Authored in whatever
# order reads naturally; order is not significant.
_TIE_BREAKERS_RAW = {
    ("flat_rag", "structured_rag"): (
        "Does a correct answer usually require joining facts that live in "
        "different sessions? If yes, pay for structured extraction. If a single "
        "well-retrieved chunk normally answers it, stay flat."
    ),
    ("structured_rag", "agentic"): (
        "Does your memory need to correct itself without a human in the loop? "
        "If yes, go agentic and cap its retrieval loop. If a human reviews "
        "corrections, structured extraction is cheaper for the same recall."
    ),
    ("long_context", "flat_rag"): (
        "Will the history exceed the context window within your planning "
        "horizon? If yes, build the retrieval path now -- migrating later costs "
        "a full re-index. If not, raw context is free."
    ),
    ("long_context", "structured_rag"): (
        "Is the value in the raw transcript or in the facts extracted from it? "
        "If a human would summarize before reusing it, extract at write time."
    ),
}

# Normalize every key to its sorted form, because the lookup below sorts the
# tied pair. Without this, a key authored in the other order is unreachable and
# the tool silently falls back to the generic question -- no error, just a worse
# answer. This repo has no test suite, so the collision check runs at import.
TIE_BREAKERS = {}
for _pair, _question in _TIE_BREAKERS_RAW.items():
    _key = tuple(sorted(_pair))
    if _key in TIE_BREAKERS:
        raise AssertionError(
            f"duplicate tie-breaker for {_key} after normalization -- two "
            "entries describe the same family pair"
        )
    TIE_BREAKERS[_key] = _question
del _pair, _question, _key

SAMPLE_CONSTRAINTS = {
    "name": "customer-support agent, 18-month retention",
    "query_latency_sensitivity": "high",
    "build_budget_pressure": "medium",
    "recall_need": "high",
    "volume_growth": "high",
    "mutability_need": "medium",
    "hard_constraints": {
        "max_p99_query_ms": 1500,
        "context_window_tokens": 200000,
        "expected_history_tokens": 4000000,
    },
}


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def _level(constraints: dict, key: str) -> float:
    raw = constraints.get(key, "medium")
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        value = float(raw)
        if not 0.0 <= value <= 1.0:
            _fail(f"'{key}' as a number must be in [0, 1], got {value}")
        return value
    if not isinstance(raw, str) or raw.lower() not in LEVELS:
        _fail(f"'{key}' must be one of {sorted(LEVELS)} or a number in [0, 1]")
    return LEVELS[raw.lower()]


def _hard_constraint_kills(family, hard):
    """Return a disqualifying reason, or None if the family survives."""
    window = hard.get("context_window_tokens")
    history = hard.get("expected_history_tokens")
    if family == "long_context" and window and history and history > window:
        return (
            f"expected history ({history:,} tokens) exceeds the context window "
            f"({window:,} tokens) -- raw context cannot hold it"
        )

    p99 = hard.get("max_p99_query_ms")
    if family == "agentic" and p99 and p99 < 3000:
        return (
            f"p99 budget of {p99} ms cannot absorb an uncapped agentic "
            "retrieval loop"
        )
    if family == "long_context" and p99 and p99 < 1000:
        return (
            f"p99 budget of {p99} ms cannot absorb quadratic attention over "
            "full history"
        )
    return None


def pick(constraints: dict) -> dict:
    if not isinstance(constraints, dict):
        _fail("constraints must be a JSON object")

    hard = constraints.get("hard_constraints", {})
    if not isinstance(hard, dict):
        _fail("'hard_constraints' must be an object")

    levels = {key: _level(constraints, key) for key in WEIGHTS}

    scored = []
    disqualified = []
    for name, profile in FAMILIES.items():
        reason = _hard_constraint_kills(name, hard)
        if reason:
            disqualified.append(
                {"family": name, "label": profile["label"], "reason": reason}
            )
            continue
        score = 0.0
        breakdown = {}
        for constraint_key, (axis, weight) in WEIGHTS.items():
            contribution = levels[constraint_key] * weight * profile[axis]
            breakdown[axis] = round(contribution, 4)
            score += contribution
        scored.append(
            {
                "family": name,
                "label": profile["label"],
                "examples": profile["examples"],
                "score": round(score, 4),
                "breakdown": breakdown,
                "cost_you_pay": profile["cost_you_pay"],
                "kills_it": profile["kills_it"],
            }
        )

    if not scored:
        return {
            "name": constraints.get("name", "unnamed workload"),
            "verdict": "NO-VIABLE-FAMILY",
            "ranked": [],
            "disqualified": disqualified,
            "recommendation": None,
            "tie_breaker": None,
        }

    scored.sort(key=lambda item: item["score"], reverse=True)
    winner = scored[0]

    tie_breaker = None
    verdict = "RECOMMENDED"
    if len(scored) > 1:
        runner_up = scored[1]
        gap = winner["score"] - runner_up["score"]
        if gap < AMBIGUITY_MARGIN:
            verdict = "AMBIGUOUS"
            pair = tuple(sorted([winner["family"], runner_up["family"]]))
            tie_breaker = {
                "between": [winner["label"], runner_up["label"]],
                "gap": round(gap, 4),
                "question": TIE_BREAKERS.get(
                    pair,
                    "Which cost hurts you more in production: a slow write path "
                    "or a blunt retrieval result? Answer that and the choice "
                    "resolves.",
                ),
            }

    return {
        "name": constraints.get("name", "unnamed workload"),
        "verdict": verdict,
        "ranked": scored,
        "disqualified": disqualified,
        "recommendation": None if verdict == "AMBIGUOUS" else winner,
        "tie_breaker": tie_breaker,
    }


def render(result: dict) -> str:
    lines = []
    lines.append(f"MEMORY ARCHITECTURE - {result['name']}")
    lines.append("=" * 68)
    lines.append(f"VERDICT: {result['verdict']}")
    lines.append("")

    if result["verdict"] == "NO-VIABLE-FAMILY":
        lines.append("Every family was disqualified by a hard constraint.")
        lines.append("Relax a hard constraint, or split the workload in two.")
        lines.append("")
    elif result["recommendation"]:
        rec = result["recommendation"]
        lines.append(f"Use: {rec['label']}  ({rec['examples']})")
        lines.append("")
        lines.append("The cost you are choosing to pay:")
        lines.append(f"  {rec['cost_you_pay']}")
        lines.append("")
        lines.append(f"What would kill this choice: {rec['kills_it']}")
        lines.append("")
    else:
        tie = result["tie_breaker"]
        lines.append(f"Too close to call ({tie['gap']:.3f} apart):")
        for label in tie["between"]:
            lines.append(f"  - {label}")
        lines.append("")
        lines.append("Answer this before picking:")
        lines.append(f"  {tie['question']}")
        lines.append("")

    if result["ranked"]:
        lines.append("Ranked")
        lines.append("-" * 68)
        for index, item in enumerate(result["ranked"], start=1):
            lines.append(f"  {index}. {item['label']:<42} {item['score']:.4f}")
        lines.append("")

    if result["disqualified"]:
        lines.append("Disqualified by hard constraints")
        lines.append("-" * 68)
        for item in result["disqualified"]:
            lines.append(f"  {item['label']}")
            lines.append(f"    {item['reason']}")
        lines.append("")

    lines.append(
        "No family wins on build cost, query speed, and accuracy at once.\n"
        "This is a choice of which cost to pay, not a ranking of quality."
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Recommend an agent memory paradigm from stated constraints, and "
            "name the cost that choice makes you pay."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  memory_architecture_picker.py --sample\n"
            "  memory_architecture_picker.py --constraints workload.json\n"
            "  memory_architecture_picker.py --sample --output json\n"
        ),
    )
    # Not required=True: argparse enforces a required group during
    # parse_args(), which made --print-sample-spec unreachable on its own.
    # Validated explicitly after the print-and-exit branch instead.
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--constraints", help="path to a constraints JSON file")
    source.add_argument(
        "--sample",
        action="store_true",
        help="run against the built-in sample constraints",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="output format (default: text)",
    )
    parser.add_argument(
        "--print-sample-spec",
        action="store_true",
        help="print the sample constraints JSON and exit (use as a template)",
    )
    args = parser.parse_args()

    if args.print_sample_spec:
        print(json.dumps(SAMPLE_CONSTRAINTS, indent=2))
        return 0

    if not (args.constraints or args.sample):
        parser.error(
            "one of --constraints, --sample, or --print-sample-spec is required"
        )

    if args.sample:
        constraints = SAMPLE_CONSTRAINTS
    else:
        try:
            with open(args.constraints, "r", encoding="utf-8") as handle:
                constraints = json.load(handle)
        except FileNotFoundError:
            _fail(f"constraints file not found: {args.constraints}")
        except json.JSONDecodeError as exc:
            _fail(f"constraints file is not valid JSON: {exc}")

    result = pick(constraints)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render(result))

    if result["verdict"] == "NO-VIABLE-FAMILY":
        return 4
    if result["verdict"] == "AMBIGUOUS":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
