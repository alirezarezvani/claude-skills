#!/usr/bin/env python3
"""score_aggregator.py — validate rubric scores, compute the grade, gate the suggestions.

The scoring agent judges each sampled transcript against the two rubrics in
scorers/ and writes a scores file (labels + reasons only — never numbers).
This script owns all arithmetic and refuses scoring theater:

  * every sampled session must be scored, and only sampled sessions may be
    scored (an entry for an unsampled session is a fabrication and fails);
  * labels must come from the rubric label tables — the numeric score is
    derived here, so an agent cannot inflate it;
  * every label needs a substantive reason (>= 20 chars);
  * every suggestion must cite at least one sampled session id, so proposals
    trace to observed evidence, not generic best practice;
  * zero suggestions is a valid, reportable success.

Emits report.json for render_report.py.

Usage:
    python score_aggregator.py --inventory RUN/inventory.json --emit-template   # skeleton for the agent to fill
    python score_aggregator.py --inventory RUN/inventory.json --scores RUN/session_scores.json
    python score_aggregator.py --inventory RUN/inventory.json --scores RUN/session_scores.json \
        --suggestions RUN/suggestions.json --out RUN/report.json
    python score_aggregator.py --sample --output json

Exit codes: 0 aggregated clean, 2 aggregated with warnings, 3 bad input,
4 validation failure (nothing written).

Stdlib only. No ML/LLM calls. Derived from warpdotdev/common-skills
skill-doctor (MIT); the aggregation math is upstream Step 3, made mechanical.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Label -> score tables. These mirror scorers/efficiency.md and
# scorers/code-quality.md exactly; if a rubric changes, change both together.
EFFICIENCY_LABELS = {
    "highly_efficient": 1.0,
    "mostly_efficient": 0.8,
    "mostly_inefficient": 0.4,
    "highly_inefficient": 0.2,
}
CODE_QUALITY_LABELS = {
    "approve": 1.0,
    "block": 0.2,
    "insufficient_evidence": 0.5,
}
WEIGHTS = {"efficiency": 0.5, "code_quality": 0.35, "skill_coverage": 0.15}
MIN_REASON_CHARS = 20
GRADES = [
    (0.97, "A+"), (0.93, "A"), (0.90, "A-"),
    (0.87, "B+"), (0.83, "B"), (0.80, "B-"),
    (0.77, "C+"), (0.73, "C"), (0.70, "C-"),
    (0.60, "D"), (0.0, "F"),
]


def grade_for(score):
    for threshold, letter in GRADES:
        if score >= threshold:
            return letter
    return "F"


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Validate skill-doctor rubric scores, compute the grade, gate the suggestions.")
    p.add_argument("--inventory", help="inventory.json from collect_sessions.py")
    p.add_argument("--scores", help="session_scores.json written by the scoring agent")
    p.add_argument("--suggestions", help="suggestions.json written by the drafting agent (optional)")
    p.add_argument("--out", help="where to write report.json (default: next to the inventory)")
    p.add_argument("--emit-template", action="store_true",
                   help="print a scores-file skeleton for the sampled sessions and exit")
    p.add_argument("--output", choices=("text", "json"), default="text", help="summary format on stdout")
    p.add_argument("--sample", action="store_true", help="run on built-in sample data (demo/smoke test)")
    return p.parse_args(argv)


def load_json(path, what):
    try:
        return json.loads(Path(path).expanduser().read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: could not read {what} at {path}: {exc}", file=sys.stderr)
        return None


def sampled_sessions(inventory):
    return [s for s in inventory.get("sessions", []) if s.get("sampled")]


def emit_template(inventory):
    template = {
        "top_findings": ["", "", ""],
        "sessions": [
            {
                "session_id": s["meta"]["id"],
                "harness": s.get("harness", ""),
                "efficiency": {"label": "<one of: " + " | ".join(EFFICIENCY_LABELS) + ">",
                               "reason": ""},
                "code_quality": {"label": "<one of: " + " | ".join(CODE_QUALITY_LABELS) + ">",
                                 "reason": ""},
            }
            for s in sampled_sessions(inventory)
        ],
    }
    print(json.dumps(template, indent=2))


def validate(inventory, scores, suggestions):
    """Return (errors, warnings, per_session) — errors block, warnings don't."""
    errors, warnings = [], []
    sampled = {s["meta"]["id"]: s for s in sampled_sessions(inventory)}
    entries = scores.get("sessions")
    if not isinstance(entries, list):
        return (["scores file has no 'sessions' list"], warnings, {})

    per_session = {}
    sids_with_errors = set()
    for i, entry in enumerate(entries):
        sid = entry.get("session_id")
        if not sid:
            errors.append(f"scores entry {i} has no session_id")
            continue
        if sid not in sampled:
            errors.append(f"score for '{sid}' rejected: not a sampled session (fabricated or stale id)")
            continue
        if sid in per_session:
            errors.append(f"duplicate score entry for '{sid}'")
            continue
        errors_before = len(errors)
        record = {}
        for scorer, table in (("efficiency", EFFICIENCY_LABELS), ("code_quality", CODE_QUALITY_LABELS)):
            block = entry.get(scorer)
            if not isinstance(block, dict):
                errors.append(f"'{sid}': missing {scorer} block")
                continue
            label = block.get("label")
            if label not in table:
                errors.append(f"'{sid}': {scorer} label '{label}' is not in the rubric table "
                              f"({', '.join(table)})")
                continue
            reason = (block.get("reason") or "").strip()
            if len(reason) < MIN_REASON_CHARS:
                errors.append(f"'{sid}': {scorer} reason is too thin "
                              f"({len(reason)} chars < {MIN_REASON_CHARS}) — cite specifics from the transcript")
                continue
            record[scorer] = {"label": label, "score": table[label], "reason": reason}
        if len(errors) > errors_before:
            sids_with_errors.add(sid)
        if len(record) == 2:
            if (record["code_quality"]["label"] == "insufficient_evidence"
                    and sampled[sid].get("stats", {}).get("has_code_edits")):
                warnings.append(f"'{sid}': insufficient_evidence despite detected code edits — "
                                "confirm the transcript truly hid the diff")
            per_session[sid] = record

    # Exact-id tracking, not substring matching against error text: one session
    # id being a prefix of another must not suppress its never-scored error.
    for sid in sampled:
        if sid not in per_session and sid not in sids_with_errors:
            errors.append(f"sampled session '{sid}' was never scored")

    findings = scores.get("top_findings")
    if not isinstance(findings, list) or not [f for f in findings if isinstance(f, str) and f.strip()]:
        errors.append("top_findings must contain at least one non-empty finding")

    for i, sug in enumerate(suggestions.get("suggestions", [])):
        where = f"suggestion {i} ({sug.get('skill') or 'unnamed'})"
        for field in ("skill", "change", "evidence"):
            if not (sug.get(field) or "").strip():
                errors.append(f"{where}: missing '{field}'")
        cited = sug.get("sessions") or []
        if not cited:
            errors.append(f"{where}: cites no session — suggestions must trace to a scored session")
        for sid in cited:
            if sid not in sampled:
                errors.append(f"{where}: cites '{sid}', which is not a sampled session")
        if not (sug.get("diff") or "").strip():
            errors.append(f"{where}: no diff — draft the edit (full content counts as the diff for a new skill)")

    return errors, warnings, per_session


def aggregate(inventory, scores, suggestions, per_session, warnings):
    sampled = sampled_sessions(inventory)
    n = len(sampled)
    eff_scores = [per_session[s["meta"]["id"]]["efficiency"]["score"] for s in sampled]
    cq_scores = [per_session[s["meta"]["id"]]["code_quality"]["score"] for s in sampled
                 if per_session[s["meta"]["id"]]["code_quality"]["label"] != "insufficient_evidence"]
    efficiency = sum(eff_scores) / n if n else 0.0
    if cq_scores:
        code_quality = sum(cq_scores) / len(cq_scores)
    else:
        code_quality = 0.5
        if n:
            warnings.append("no session had enough evidence for code quality; using the neutral 0.5")
    skills_found = inventory.get("stats", {}).get("skills_found", 0)
    covered = sum(1 for s in sampled if s.get("skills_used"))
    skill_coverage = (covered / n) if (n and skills_found) else 0.0
    overall = (WEIGHTS["efficiency"] * efficiency
               + WEIGHTS["code_quality"] * code_quality
               + WEIGHTS["skill_coverage"] * skill_coverage)

    st = inventory.get("stats", {})
    report = {
        "title": "Agent Skill Report",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "harness": inventory.get("harness", "mixed"),
        "handle": inventory.get("repo_name", ""),
        "stats": {
            "sessions_analyzed": n,
            "sessions_scanned": st.get("session_records_in_window", 0),
            "skills_found": skills_found,
            "skills_used": st.get("skills_used", 0),
            "window_days": inventory.get("window_days", 45),
        },
        "scores": {
            "efficiency": round(efficiency, 4),
            "code_quality": round(code_quality, 4),
            "skill_coverage": round(skill_coverage, 4),
            "overall": round(overall, 4),
        },
        "grade": grade_for(overall),
        "top_findings": [f.strip() for f in scores.get("top_findings", []) if isinstance(f, str) and f.strip()][:5],
        "suggestions": suggestions.get("suggestions", []),
        "session_scores": {
            sid: {scorer: {"label": rec[scorer]["label"], "reason": rec[scorer]["reason"]}
                  for scorer in rec}
            for sid, rec in sorted(per_session.items())
        },
        "warnings": warnings,
    }
    if not report["suggestions"]:
        warnings.append("no suggestion cleared the filing bar this window — that is a valid outcome, "
                        "and the report says so")
    return report


SAMPLE_INVENTORY = {
    "generated_at": "2026-01-15T10:05:00+00:00",
    "harness": "claude",
    "repo_name": "sample-repo",
    "window_days": 45,
    "stats": {"session_records_in_window": 9, "sessions_in_repo": 4,
              "sessions_considered": 2, "sessions_sampled": 2,
              "skills_found": 1, "skills_used": 1},
    "sessions": [
        {"harness": "claude", "sampled": True, "skills_used": ["sample-skill"],
         "meta": {"id": "sample-session-1"}, "stats": {"has_code_edits": True}},
        {"harness": "claude", "sampled": True, "skills_used": [],
         "meta": {"id": "sample-session-2"}, "stats": {"has_code_edits": False}},
    ],
}
SAMPLE_SCORES = {
    "top_findings": [
        "Files were re-read verbatim in 1 of 2 sessions before any edit was attempted",
        "The only skill installed fired in half the sampled sessions; the other half matched its trigger wording but never invoked it",
    ],
    "sessions": [
        {"session_id": "sample-session-1",
         "efficiency": {"label": "mostly_efficient",
                        "reason": "One duplicated read of src/parse.py before the fix; no knock-on rework after."},
         "code_quality": {"label": "approve",
                          "reason": "Single-line format-string fix matches the surrounding style and the test passed first run."}},
        {"session_id": "sample-session-2",
         "efficiency": {"label": "highly_efficient",
                        "reason": "One read answered the question directly with no redundant steps."},
         "code_quality": {"label": "insufficient_evidence",
                          "reason": "Read-only question; no diff was produced in this session."}},
    ],
}
SAMPLE_SUGGESTIONS = {
    "suggestions": [
        {"skill": "sample-skill",
         "change": "Add a preflight step: read the failing test output before opening the implementation file.",
         "evidence": "sample-session-1 re-read src/parse.py twice before locating the format string the test named directly.",
         "sessions": ["sample-session-1"],
         "proposed_path": "proposed/sample-skill/SKILL.md",
         "diff": "--- a/SKILL.md\n+++ b/SKILL.md\n@@ -3,2 +3,3 @@\n # sample-skill\n+1. Read the failing test output first; it usually names the file and line.\n Fix the bug.\n"},
    ],
}


def main(argv=None):
    args = parse_args(argv)
    if args.sample:
        inventory, scores, suggestions = SAMPLE_INVENTORY, SAMPLE_SCORES, SAMPLE_SUGGESTIONS
        out_path = Path(args.out).expanduser() if args.out else None
    else:
        if not args.inventory:
            print("error: --inventory is required (or use --sample)", file=sys.stderr)
            return 3
        inventory = load_json(args.inventory, "inventory")
        if inventory is None:
            return 3
        if args.emit_template:
            emit_template(inventory)
            return 0
        if not args.scores:
            print("error: --scores is required (use --emit-template to get the skeleton)", file=sys.stderr)
            return 3
        scores = load_json(args.scores, "scores")
        if scores is None:
            return 3
        suggestions = {"suggestions": []}
        if args.suggestions:
            suggestions = load_json(args.suggestions, "suggestions")
            if suggestions is None:
                return 3
        out_path = (Path(args.out).expanduser() if args.out
                    else Path(args.inventory).expanduser().parent / "report.json")

    errors, warnings, per_session = validate(inventory, scores, suggestions)
    if errors:
        payload = {"status": "validation_failed", "errors": errors, "warnings": warnings}
        if args.output == "json":
            print(json.dumps(payload, indent=2))
        else:
            print("VALIDATION FAILED — report.json not written")
            for e in errors:
                print(f"  error: {e}")
            for w in warnings:
                print(f"  warning: {w}")
        return 4

    report = aggregate(inventory, scores, suggestions, per_session, warnings)
    if out_path:
        out_path.write_text(json.dumps(report, indent=2))
        try:
            os.chmod(out_path, 0o600)
        except OSError:
            pass

    if args.output == "json":
        print(json.dumps({"status": "ok", "report": str(out_path) if out_path else None,
                          "grade": report["grade"], "scores": report["scores"],
                          "suggestions": len(report["suggestions"]),
                          "warnings": warnings}, indent=2))
    else:
        print(f"grade:        {report['grade']} (overall {report['scores']['overall']:.2f})")
        for k in ("efficiency", "code_quality", "skill_coverage"):
            print(f"{k + ':':16}{report['scores'][k]:.2f}")
        print(f"suggestions:  {len(report['suggestions'])}")
        for w in warnings:
            print(f"warning:      {w}")
        if out_path:
            print(f"report:       {out_path}")
    return 2 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
