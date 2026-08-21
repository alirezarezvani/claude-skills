#!/usr/bin/env python3
"""Price the write path of an agent memory system, not just the query path.

The Stanford characterization (arXiv:2606.06448) found that for LLM-mediated
memory systems, construction energy exceeds total query-phase energy across 300
queries. Everyone watches query latency because the user feels it; the bill is
paid at construction, which the user never sees.

This tool splits a memory workload into its construction and query phases,
computes cost per *correct* answer (never accuracy alone), and reports the
amortization ratio -- how many queries each constructed record has to serve
before the write that produced it pays for itself.

Deterministic arithmetic only. No LLM calls, no network, stdlib only.

Exit codes:
    0  profile produced, no blocking finding
    2  actionable finding (write-path dominant, under-amortized, or
       construction co-located with latency-sensitive queries)
    3  invalid input
"""

import argparse
import json
import sys

# Cost split beyond which construction is judged to dominate the lifecycle.
WRITE_DOMINANT_SHARE = 0.50

# Below this many queries per constructed record, the write path has not been
# amortized (Stanford recommendation 4: exploit reuse; recommendation 6: match
# the cost split to the workload's query arrival pattern).
MIN_AMORTIZATION_QUERIES = 10.0

SAMPLE_SPEC = {
    "name": "support-agent-memory (structure-augmented RAG)",
    "construction": {
        "records_per_day": 400,
        "prompt_tokens_per_record": 12000,
        "output_tokens_per_record": 800,
        "embedding_tokens_per_record": 12000,
        "colocated_with_queries": True,
    },
    "query": {
        "queries_per_day": 1200,
        "prompt_tokens_per_query": 2400,
        "output_tokens_per_query": 300,
        "embedding_tokens_per_query": 40,
    },
    "pricing_usd_per_mtok": {
        "prompt": 3.0,
        "output": 15.0,
        "embedding": 0.02,
    },
    "accuracy": 0.72,
}


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def _number(container: dict, key: str, where: str, *, default=None) -> float:
    if key not in container:
        if default is not None:
            return float(default)
        _fail(f"missing required field '{key}' in {where}")
    value = container[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail(f"field '{key}' in {where} must be a number, got {type(value).__name__}")
    if value < 0:
        _fail(f"field '{key}' in {where} must be >= 0, got {value}")
    return float(value)


def _phase_cost(
    prompt_tokens: float,
    output_tokens: float,
    embedding_tokens: float,
    pricing: dict,
) -> dict:
    """Cost of one phase, in USD, broken out by token class."""
    per_mtok = 1_000_000.0
    prompt_cost = prompt_tokens / per_mtok * pricing["prompt"]
    output_cost = output_tokens / per_mtok * pricing["output"]
    embedding_cost = embedding_tokens / per_mtok * pricing["embedding"]
    return {
        "prompt_tokens": round(prompt_tokens, 2),
        "output_tokens": round(output_tokens, 2),
        "embedding_tokens": round(embedding_tokens, 2),
        "prompt_usd": round(prompt_cost, 6),
        "output_usd": round(output_cost, 6),
        "embedding_usd": round(embedding_cost, 6),
        "total_usd": round(prompt_cost + output_cost + embedding_cost, 6),
    }


def profile(spec: dict) -> dict:
    if not isinstance(spec, dict):
        _fail("spec must be a JSON object")

    construction = spec.get("construction")
    query = spec.get("query")
    if not isinstance(construction, dict):
        _fail("spec must contain a 'construction' object")
    if not isinstance(query, dict):
        _fail("spec must contain a 'query' object")

    pricing_raw = spec.get("pricing_usd_per_mtok", {})
    if not isinstance(pricing_raw, dict):
        _fail("'pricing_usd_per_mtok' must be an object")
    pricing = {
        "prompt": _number(pricing_raw, "prompt", "pricing_usd_per_mtok", default=3.0),
        "output": _number(pricing_raw, "output", "pricing_usd_per_mtok", default=15.0),
        "embedding": _number(
            pricing_raw, "embedding", "pricing_usd_per_mtok", default=0.02
        ),
    }

    records = _number(construction, "records_per_day", "construction")
    queries = _number(query, "queries_per_day", "query")

    build = _phase_cost(
        records * _number(construction, "prompt_tokens_per_record", "construction"),
        records * _number(construction, "output_tokens_per_record", "construction"),
        records
        * _number(
            construction, "embedding_tokens_per_record", "construction", default=0
        ),
        pricing,
    )
    read = _phase_cost(
        queries * _number(query, "prompt_tokens_per_query", "query"),
        queries * _number(query, "output_tokens_per_query", "query"),
        queries * _number(query, "embedding_tokens_per_query", "query", default=0),
        pricing,
    )

    total = build["total_usd"] + read["total_usd"]
    build_share = build["total_usd"] / total if total > 0 else 0.0

    accuracy = spec.get("accuracy")
    if accuracy is None:
        _fail(
            "spec must contain 'accuracy' (0-1). Cost per correct answer is the "
            "whole point -- a quality number without a cost number is the "
            "measurement this tool exists to refuse."
        )
    accuracy = float(accuracy)
    if not 0.0 < accuracy <= 1.0:
        _fail(f"'accuracy' must be in (0, 1], got {accuracy}")

    cost_per_query = total / queries if queries > 0 else 0.0
    cost_per_correct = cost_per_query / accuracy
    amortization = queries / records if records > 0 else float("inf")
    colocated = bool(construction.get("colocated_with_queries", False))

    findings = []
    if build_share > WRITE_DOMINANT_SHARE:
        findings.append(
            {
                "code": "WRITE_PATH_DOMINANT",
                "severity": "high",
                "detail": (
                    f"Construction is {build_share:.0%} of daily spend "
                    f"(${build['total_usd']:.2f} build vs "
                    f"${read['total_usd']:.2f} query). The cost you tuned is not "
                    "the cost you pay."
                ),
                "action": (
                    "Cut construction tokens before touching retrieval: batch "
                    "writes, dedup before extraction, or drop to a cheaper "
                    "construction model."
                ),
            }
        )
    if amortization < MIN_AMORTIZATION_QUERIES:
        findings.append(
            {
                "code": "UNDER_AMORTIZED",
                "severity": "high",
                "detail": (
                    f"Each constructed record serves only {amortization:.1f} "
                    f"queries (floor {MIN_AMORTIZATION_QUERIES:.0f}). You are "
                    "paying to remember things nobody asks about."
                ),
                "action": (
                    "Write less, or write later: build memory lazily on second "
                    "access rather than eagerly on every session."
                ),
            }
        )
    if colocated:
        findings.append(
            {
                "code": "CONSTRUCTION_COLOCATED",
                "severity": "medium",
                "detail": (
                    "Construction shares a scheduler with latency-sensitive "
                    "queries. Construction is prefill-heavy, so a large write "
                    "stalls exactly the query a user is waiting on."
                ),
                "action": (
                    "Treat construction as a background job with admission "
                    "control: rate-limit, batch, or defer it off the "
                    "latency-sensitive path."
                ),
            }
        )

    # The verdict names the actual dominant problem, so it can never disagree
    # with the findings list below it.
    codes = {f["code"] for f in findings}
    if "WRITE_PATH_DOMINANT" in codes:
        verdict = "WRITE-PATH-DOMINANT"
    elif "UNDER_AMORTIZED" in codes:
        verdict = "UNDER-AMORTIZED"
    elif "CONSTRUCTION_COLOCATED" in codes:
        verdict = "NEEDS-SCHEDULING-FIX"
    elif build_share < 0.15:
        verdict = "QUERY-DOMINANT"
    else:
        verdict = "BALANCED"

    return {
        "name": spec.get("name", "unnamed memory system"),
        "verdict": verdict,
        "daily_cost_usd": {
            "construction": build["total_usd"],
            "query": read["total_usd"],
            "total": round(total, 6),
            "construction_share": round(build_share, 4),
        },
        "construction_phase": build,
        "query_phase": read,
        "quality_and_cost": {
            "accuracy": accuracy,
            "cost_per_query_usd": round(cost_per_query, 6),
            "cost_per_correct_answer_usd": round(cost_per_correct, 6),
            "note": (
                "Never quote accuracy without cost per correct answer. Two "
                "systems at identical accuracy can differ by more than an "
                "order of magnitude on this number."
            ),
        },
        "amortization": {
            "queries_per_constructed_record": (
                round(amortization, 2) if amortization != float("inf") else None
            ),
            "floor": MIN_AMORTIZATION_QUERIES,
        },
        "findings": findings,
    }


def render(report: dict) -> str:
    lines = []
    lines.append(f"MEMORY COST PROFILE - {report['name']}")
    lines.append("=" * 68)
    lines.append(f"VERDICT: {report['verdict']}")
    lines.append("")

    cost = report["daily_cost_usd"]
    lines.append("Daily cost split")
    lines.append("-" * 68)
    lines.append(
        f"  construction  ${cost['construction']:>10.2f}  "
        f"({cost['construction_share']:.0%} of total)"
    )
    lines.append(
        f"  query         ${cost['query']:>10.2f}  "
        f"({1 - cost['construction_share']:.0%} of total)"
    )
    lines.append(f"  total         ${cost['total']:>10.2f}")
    lines.append("")

    qc = report["quality_and_cost"]
    lines.append("Quality AND cost (never one without the other)")
    lines.append("-" * 68)
    lines.append(f"  accuracy                    {qc['accuracy']:.1%}")
    lines.append(f"  cost per query              ${qc['cost_per_query_usd']:.6f}")
    lines.append(
        f"  cost per CORRECT answer     ${qc['cost_per_correct_answer_usd']:.6f}"
    )
    lines.append("")

    amort = report["amortization"]
    if amort["queries_per_constructed_record"] is not None:
        lines.append(
            f"Amortization: {amort['queries_per_constructed_record']} queries per "
            f"constructed record (floor {amort['floor']:.0f})"
        )
        lines.append("")

    if report["findings"]:
        lines.append(f"Findings ({len(report['findings'])})")
        lines.append("-" * 68)
        for finding in report["findings"]:
            lines.append(f"  [{finding['severity'].upper()}] {finding['code']}")
            lines.append(f"    {finding['detail']}")
            lines.append(f"    -> {finding['action']}")
            lines.append("")
    else:
        lines.append("No blocking findings. Re-run when volume or pricing changes.")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Profile the construction (write) and query (read) phases of an "
            "agent memory system, and report cost per correct answer."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  memory_cost_profiler.py --sample\n"
            "  memory_cost_profiler.py --spec workload.json\n"
            "  memory_cost_profiler.py --sample --output json\n"
        ),
    )
    # Not required=True: argparse enforces a required group during
    # parse_args(), which made --print-sample-spec unreachable on its own.
    # Validated explicitly after the print-and-exit branch instead.
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--spec", help="path to a memory workload spec JSON file")
    source.add_argument(
        "--sample",
        action="store_true",
        help="profile the built-in sample workload (no input file needed)",
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
        help="print the sample spec JSON and exit (use as a template)",
    )
    args = parser.parse_args()

    if args.print_sample_spec:
        print(json.dumps(SAMPLE_SPEC, indent=2))
        return 0

    if not (args.spec or args.sample):
        parser.error(
            "one of --spec, --sample, or --print-sample-spec is required"
        )

    if args.sample:
        spec = SAMPLE_SPEC
    else:
        try:
            with open(args.spec, "r", encoding="utf-8") as handle:
                spec = json.load(handle)
        except FileNotFoundError:
            _fail(f"spec file not found: {args.spec}")
        except json.JSONDecodeError as exc:
            _fail(f"spec file is not valid JSON: {exc}")

    report = profile(spec)

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render(report))

    return 2 if report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
