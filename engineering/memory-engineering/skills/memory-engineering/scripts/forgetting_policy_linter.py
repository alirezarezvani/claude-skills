#!/usr/bin/env python3
"""Refuse a memory design that has no forgetting policy.

This is the gate. Everything else in this skill measures a memory system; this
one blocks it.

Stanford's characterization found that none of the ten evaluated memory systems
prunes or forgets by default, so footprint grows monotonically -- and at 1M
tokens, footprint already varies by up to 9x across systems. Growth slope, not
starting size, is what bankrupts a long-lived agent.

Two rules are non-negotiable, and either one failing fails the whole design:

  F1  an explicit forgetting rule must exist (TTL, capacity bound, or decay)
  F4  contradictions must be SURFACED to a human, never auto-merged

F4 is not fussiness. Two memories that disagree may both have been true in
different contexts. A system that silently merges them destroys the only
evidence that the conflict existed.

The remaining checks (F2, F3, F5-F8) degrade the verdict to CONDITIONAL rather
than failing it.

Deterministic policy audit. No LLM calls, no network, stdlib only.

Exit codes:
    0  PASS        -- forgetting is designed
    2  CONDITIONAL -- forgetting exists but the controls around it are thin
    3  invalid input
    4  FAIL        -- no forgetting rule, or contradictions are auto-merged
"""

import argparse
import json
import sys

# Recognized `forgetting.rule` values. Anything outside this set is treated as
# no rule at all -- see _check_forgetting_rule.
KNOWN_FORGETTING_RULES = {"ttl", "capacity", "decay", "none", "never", ""}

VALID_CONTRADICTION_POLICIES = {"surface", "surface_to_human", "flag", "escalate"}
AUTO_MERGE_POLICIES = {"auto_merge", "newest_wins", "overwrite", "last_write_wins"}

SAMPLE_POLICY = {
    "name": "support-agent memory store",
    "forgetting": {
        "rule": "ttl",
        "ttl_days": 365,
        "max_records": 50000,
        "decay": "none",
    },
    "dedup_on_write": True,
    "consolidation": {"enabled": True, "cadence": "weekly"},
    "contradiction_policy": "surface",
    "scope": {"read": ["support-agents"], "write": ["memory-writer-service"]},
    "audit_trail": {"timestamp": True, "source_attribution": True},
    "rollback": {"supported": True, "delete_path": "api"},
    "growth_monitoring": {"tracks_slope": False, "baseline_only": True},
}

FAILING_SAMPLE = {
    "name": "naive vector store (the default everyone ships)",
    "forgetting": {"rule": "none"},
    "dedup_on_write": False,
    "consolidation": {"enabled": False},
    "contradiction_policy": "newest_wins",
    "scope": {},
    "audit_trail": {},
    "rollback": {"supported": False},
    "growth_monitoring": {},
}


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def _check_forgetting_rule(policy: dict) -> dict:
    """F1 -- pass only on a concrete, named forgetting mechanism.

    This check is allowlist-based on purpose. An earlier version failed only
    when `rule` was literally "none"/""/"never" and inferred PASS from what the
    rule was *not*, so a typo ("asdf") or a declared-but-unconfigured rule
    ("ttl" with ttl_days omitted) fell through to PASS with an empty mechanism
    list -- the blocking gate this whole skill is built around, defeated by a
    misspelling. PASS is now unreachable unless a mechanism is actually found.
    """
    forgetting = policy.get("forgetting") or {}
    if not isinstance(forgetting, dict):
        _fail("'forgetting' must be an object")

    rule = str(forgetting.get("rule", "none")).lower().strip()

    ttl_days = forgetting.get("ttl_days")
    has_ttl = isinstance(ttl_days, (int, float)) and not isinstance(
        ttl_days, bool
    ) and ttl_days > 0

    capacity = forgetting.get("max_records") or forgetting.get("max_bytes")
    has_capacity = isinstance(capacity, (int, float)) and not isinstance(
        capacity, bool
    ) and capacity > 0

    decay = str(forgetting.get("decay", "none")).lower().strip()
    has_decay = rule == "decay" or decay not in {"none", ""}

    mechanisms = []
    if has_ttl:
        mechanisms.append(f"TTL {ttl_days}d")
    if has_capacity:
        mechanisms.append(f"capacity bound ({capacity})")
    if has_decay:
        mechanisms.append("relevance decay")

    if mechanisms:
        return {
            "id": "F1",
            "name": "explicit forgetting rule",
            "status": "PASS",
            "blocking": True,
            "detail": "Forgetting is designed: " + ", ".join(mechanisms) + ".",
            "fix": None,
        }

    # No mechanism found. Say precisely why, so a typo is not mistaken for a
    # deliberate "we decided not to forget".
    if rule not in KNOWN_FORGETTING_RULES:
        detail = (
            f"Unrecognized forgetting rule {rule!r}. Recognized values are "
            f"{sorted(KNOWN_FORGETTING_RULES)}. An unrecognized rule is treated "
            "as no rule -- a misspelling must never read as a policy."
        )
    elif rule in {"ttl", "capacity", "decay"}:
        detail = (
            f"Rule is declared as {rule!r} but carries no usable parameter "
            "(ttl_days > 0, max_records/max_bytes > 0, or a decay setting). "
            "A declared rule with nothing configured forgets exactly as much "
            "as no rule at all."
        )
    else:
        detail = (
            "No TTL, no capacity bound, no decay. The store only grows. This "
            "is the default behaviour of every system Stanford evaluated, and "
            "it is the one thing that makes a long-lived agent unaffordable."
        )

    return {
        "id": "F1",
        "name": "explicit forgetting rule",
        "status": "FAIL",
        "blocking": True,
        "detail": detail,
        "fix": (
            "Pick one before the store gets big: a TTL (ttl_days), a hard "
            "record/byte cap with an eviction order, or a relevance decay that "
            "expires unreferenced records."
        ),
    }


def _check_contradictions(policy: dict) -> dict:
    raw = str(policy.get("contradiction_policy", "")).lower().strip()
    if raw in AUTO_MERGE_POLICIES:
        return {
            "id": "F4",
            "name": "contradictions surfaced, never auto-merged",
            "status": "FAIL",
            "blocking": True,
            "detail": (
                f"Contradiction policy is '{raw}', which resolves conflicts "
                "silently. Two memories that disagree may both have been true "
                "in different contexts; auto-merging destroys the evidence "
                "that the conflict existed."
            ),
            "fix": (
                "Change the policy to surface the conflict to a human with "
                "both versions and their sources. The system surfaces, the "
                "human decides."
            ),
        }
    if raw not in VALID_CONTRADICTION_POLICIES:
        return {
            "id": "F4",
            "name": "contradictions surfaced, never auto-merged",
            "status": "FAIL",
            "blocking": True,
            "detail": (
                f"No contradiction policy declared (got '{raw or 'nothing'}'). "
                "Undeclared means whatever the storage layer does by default, "
                "which is almost always last-write-wins."
            ),
            "fix": (
                "Declare 'contradiction_policy': 'surface' and build the "
                "surfacing path before the store holds conflicting facts."
            ),
        }
    return {
        "id": "F4",
        "name": "contradictions surfaced, never auto-merged",
        "status": "PASS",
        "blocking": True,
        "detail": f"Contradiction policy is '{raw}' -- a human resolves conflicts.",
        "fix": None,
    }


def _simple_check(
    check_id: str, name: str, ok: bool, detail_ok: str, detail_bad: str, fix: str
) -> dict:
    return {
        "id": check_id,
        "name": name,
        "status": "PASS" if ok else "WARN",
        "blocking": False,
        "detail": detail_ok if ok else detail_bad,
        "fix": None if ok else fix,
    }


def lint(policy: dict) -> dict:
    if not isinstance(policy, dict):
        _fail("policy must be a JSON object")

    scope = policy.get("scope") or {}
    audit = policy.get("audit_trail") or {}
    rollback = policy.get("rollback") or {}
    consolidation = policy.get("consolidation") or {}
    growth = policy.get("growth_monitoring") or {}

    checks = [
        _check_forgetting_rule(policy),
        _simple_check(
            "F2",
            "dedup at write time",
            bool(policy.get("dedup_on_write")),
            "Duplicates are collapsed on the way in.",
            "No write-time dedup. Duplicates let a stale copy outrank a corrected one.",
            "Hash or fingerprint each record at write and collapse near-matches.",
        ),
        _simple_check(
            "F3",
            "consolidation / compaction",
            bool(consolidation.get("enabled")),
            f"Consolidation runs ({consolidation.get('cadence', 'cadence unspecified')}).",
            "Nothing compacts many small records into fewer dense ones.",
            "Schedule a consolidation pass that merges related records into one denser record.",
        ),
        _check_contradictions(policy),
        _simple_check(
            "F5",
            "read and write scope",
            bool(scope.get("read")) and bool(scope.get("write")),
            "Read and write scopes are both named.",
            "Read scope, write scope, or both are undeclared -- anything can write anything.",
            "Name who may read and who may write. An org-wide store should usually be read-only.",
        ),
        _simple_check(
            "F6",
            "audit trail",
            bool(audit.get("timestamp")) and bool(audit.get("source_attribution")),
            "Every write carries a timestamp and a source.",
            "Writes are not fully attributed, so a wrong memory cannot be traced to its origin.",
            "Record timestamp plus source attribution on every write.",
        ),
        _simple_check(
            "F7",
            "rollback and delete path",
            bool(rollback.get("supported")),
            "Earlier versions can be restored and records can be deleted.",
            "No rollback. A wrong memory persists into every future session that reads it.",
            "Add a restore path and a hard-delete path you can invoke without a migration.",
        ),
        _simple_check(
            "F8",
            "growth-slope monitoring",
            bool(growth.get("tracks_slope")),
            "Growth slope is tracked, not just current size.",
            "Only baseline size is watched. Slope, not starting size, is what bankrupts the store.",
            "Track footprint over time and alert on the slope, per Stanford recommendation 9.",
        ),
    ]

    blocking_failures = [c for c in checks if c["blocking"] and c["status"] == "FAIL"]
    warnings = [c for c in checks if c["status"] == "WARN"]

    if blocking_failures:
        verdict = "FAIL"
        exit_code = 4
        summary = (
            "This design does not forget on purpose. "
            + " ".join(f"{c['id']} failed." for c in blocking_failures)
        )
    elif warnings:
        verdict = "CONDITIONAL"
        exit_code = 2
        summary = (
            f"Forgetting is designed, but {len(warnings)} control"
            f"{'s are' if len(warnings) != 1 else ' is'} missing around it."
        )
    else:
        verdict = "PASS"
        exit_code = 0
        summary = "Forgetting is designed and the controls around it are in place."

    return {
        "name": policy.get("name", "unnamed memory design"),
        "verdict": verdict,
        "exit_code": exit_code,
        "summary": summary,
        "passed": sum(1 for c in checks if c["status"] == "PASS"),
        "total": len(checks),
        "checks": checks,
    }


def render(report: dict) -> str:
    lines = []
    lines.append(f"FORGETTING POLICY LINT - {report['name']}")
    lines.append("=" * 68)
    lines.append(f"VERDICT: {report['verdict']}  ({report['passed']}/{report['total']} checks pass)")
    lines.append(f"{report['summary']}")
    lines.append("")

    for check in report["checks"]:
        blocking = " [BLOCKING]" if check["blocking"] else ""
        lines.append(
            f"  {check['status']}  {check['id']}  {check['name']}{blocking}"
        )
        lines.append(f"        {check['detail']}")
        if check["fix"]:
            lines.append(f"        -> {check['fix']}")
        lines.append("")

    if report["verdict"] == "FAIL":
        lines.append(
            "Blocked. A storer optimizes what a system remembers; a memory\n"
            "engineer optimizes what it forgets. Fix the blocking checks before\n"
            "this design goes near real volume."
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a memory design against eight forgetting-policy checks. "
            "Fails the design if it has no forgetting rule or auto-merges "
            "contradictions."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  forgetting_policy_linter.py --sample\n"
            "  forgetting_policy_linter.py --sample-failing\n"
            "  forgetting_policy_linter.py --policy design.json --output json\n"
        ),
    )
    # Not required=True: argparse enforces a required group during
    # parse_args(), which made --print-sample-spec unreachable on its own.
    # Validated explicitly after the print-and-exit branch instead.
    source = parser.add_mutually_exclusive_group(required=False)
    source.add_argument("--policy", help="path to a memory design policy JSON file")
    source.add_argument(
        "--sample",
        action="store_true",
        help="lint the built-in passing sample policy",
    )
    source.add_argument(
        "--sample-failing",
        action="store_true",
        help="lint a policy with no forgetting rule (shows what the gate blocks)",
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
        help="print the sample policy JSON and exit (use as a template)",
    )
    args = parser.parse_args()

    if args.print_sample_spec:
        print(json.dumps(SAMPLE_POLICY, indent=2))
        return 0

    if not (args.policy or args.sample or args.sample_failing):
        parser.error(
            "one of --policy, --sample, --sample-failing, or --print-sample-spec is required"
        )

    if args.sample:
        policy = SAMPLE_POLICY
    elif args.sample_failing:
        policy = FAILING_SAMPLE
    else:
        try:
            with open(args.policy, "r", encoding="utf-8") as handle:
                policy = json.load(handle)
        except FileNotFoundError:
            _fail(f"policy file not found: {args.policy}")
        except json.JSONDecodeError as exc:
            _fail(f"policy file is not valid JSON: {exc}")

    report = lint(policy)

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render(report))

    return report["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
