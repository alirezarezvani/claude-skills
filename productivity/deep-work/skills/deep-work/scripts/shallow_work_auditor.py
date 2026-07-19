#!/usr/bin/env python3
"""shallow_work_auditor.py — Classify tasks deep vs shallow and audit the shallow share against a budget.

Encodes Cal Newport's shallow-work budget discipline:

  1. Every task is classified DEEP or SHALLOW by keyword heuristics on its name:
       shallow signals: email, inbox, slack, status, standup, meeting, expense, invoice,
                        scheduling, calendar, admin, paperwork, timesheet, errand, triage
       deep signals:    write, draft, design, code, build, research, analyze, study,
                        architect, prototype, prove, strategy, model
     A tie (or no signal at all) counts as SHALLOW — depth must be claimed deliberately.
     Override any task with an explicit :deep or :shallow suffix; the suffix always wins.
  2. The shallow share of total hours is compared against --budget percent (default 50 —
     the top of Newport's 30-50 percent band for most knowledge roles).
  3. For every shallow item, the forcing question is printed:
       "How long would it take to train a smart recent graduate to do this?"
     Months of training -> it is probably deep; days or weeks -> it is shallow. Batch it,
     delegate it, or say no to it.

Verdicts:
  WITHIN-BUDGET  (exit 0)  shallow share <= budget
  OVER-BUDGET    (exit 2)  shallow share  > budget — cut, batch, or delegate before planning the day

NO LLM CALLS. Deterministic keyword scoring. Identical inputs, identical verdict.

Exit codes:
  0  WITHIN-BUDGET
  1  usage / input error (bad task spec)
  2  OVER-BUDGET

Usage:
    python shallow_work_auditor.py --task "Write investor update:60" \\
        --task "Email triage:45" --task "Analyze churn cohort:90:deep" --budget 50
    python shallow_work_auditor.py --sample
    python shallow_work_auditor.py --sample --json
"""

import argparse
import json
import re
import sys
from typing import Any, Dict, List

SHALLOW_KEYWORDS = [
    "email", "inbox", "slack", "status", "standup", "meeting", "expense", "invoice",
    "scheduling", "schedule", "calendar", "admin", "paperwork", "timesheet", "errand",
    "triage",
]
DEEP_KEYWORDS = [
    "write", "writing", "draft", "design", "code", "coding", "program", "build",
    "research", "analyze", "analysis", "study", "architect", "prototype", "prove",
    "strategy", "model",
]

FORCING_QUESTION = ('How long would it take to train a smart recent graduate to do "{name}"? '
                    "Days or weeks -> shallow: batch it, delegate it, or say no.")


def parse_task(spec: str) -> Dict[str, Any]:
    """Accepts "name:minutes" (heuristic classifies) or "name:minutes:deep|shallow" (override)."""
    parts = spec.rsplit(":", 2)
    override = None
    if len(parts) == 3 and parts[2].strip().lower() in ("deep", "shallow"):
        name, minutes_s, override = parts[0], parts[1], parts[2].strip().lower()
    else:
        parts = spec.rsplit(":", 1)
        if len(parts) != 2:
            raise ValueError(f'task must be "name:minutes[:deep|shallow]", got: {spec!r}')
        name, minutes_s = parts
    name, minutes_s = name.strip(), minutes_s.strip()
    if not name:
        raise ValueError(f"task name is empty in: {spec!r}")
    if not minutes_s.isdigit() or int(minutes_s) <= 0:
        raise ValueError(f"task minutes must be a positive integer in: {spec!r}")
    return {"name": name, "minutes": int(minutes_s), "override": override}


def classify(name: str) -> Dict[str, Any]:
    lowered = name.lower()
    deep_hits = [k for k in DEEP_KEYWORDS if re.search(rf"\b{re.escape(k)}\b", lowered)]
    shallow_hits = [k for k in SHALLOW_KEYWORDS if re.search(rf"\b{re.escape(k)}\b", lowered)]
    if len(deep_hits) > len(shallow_hits):
        mode, why = "deep", f"deep signals: {', '.join(deep_hits)}"
    elif shallow_hits:
        mode, why = "shallow", f"shallow signals: {', '.join(shallow_hits)}"
    else:
        mode, why = "shallow", "no signal — unclassified counts as shallow; claim :deep explicitly if wrong"
    return {"mode": mode, "why": why}


def audit(tasks: List[Dict[str, Any]], budget_pct: float) -> Dict[str, Any]:
    items = []
    for t in tasks:
        if t["override"]:
            mode, why = t["override"], f"explicit :{t['override']} override"
        else:
            c = classify(t["name"])
            mode, why = c["mode"], c["why"]
        item = {"name": t["name"], "minutes": t["minutes"], "mode": mode, "why": why}
        if mode == "shallow":
            item["forcing_question"] = FORCING_QUESTION.format(name=t["name"])
        items.append(item)

    total = sum(i["minutes"] for i in items)
    shallow_min = sum(i["minutes"] for i in items if i["mode"] == "shallow")
    deep_min = total - shallow_min
    share = round(100.0 * shallow_min / total, 1) if total else 0.0
    verdict = "WITHIN-BUDGET" if share <= budget_pct else "OVER-BUDGET"
    return {
        "items": items,
        "total_minutes": total,
        "deep_minutes": deep_min,
        "shallow_minutes": shallow_min,
        "shallow_share_pct": share,
        "budget_pct": budget_pct,
        "verdict": verdict,
        "headline": (
            f"Shallow work is {share}% of the day against a {budget_pct:.0f}% budget. "
            + ("Within budget — protect the deep hours you just earned."
               if verdict == "WITHIN-BUDGET"
               else "Over budget — cut, batch, or delegate shallow items before planning the day.")
        ),
    }


def render_human(r: Dict[str, Any]) -> str:
    out: List[str] = []
    out.append("Shallow-Work Audit (deep vs shallow, share vs budget)")
    out.append("=" * 64)
    out.append("")
    out.append("| Task | Min | Mode | Basis |")
    out.append("|------|-----|------|-------|")
    for i in r["items"]:
        out.append(f"| {i['name']} | {i['minutes']} | {i['mode'].upper()} | {i['why']} |")
    out.append("")
    out.append(f"  Deep {r['deep_minutes']} min · Shallow {r['shallow_minutes']} min · "
               f"Shallow share {r['shallow_share_pct']}% vs budget {r['budget_pct']:.0f}%")
    out.append("")
    out.append(f"  VERDICT: {r['verdict']}")
    out.append(f"  {r['headline']}")
    shallow_items = [i for i in r["items"] if i["mode"] == "shallow"]
    if shallow_items:
        out.append("")
        out.append("  The forcing question, per shallow item:")
        for i in shallow_items:
            out.append(f"    - {i['forcing_question']}")
    return "\n".join(out)


SAMPLE_TASKS = [
    "Write investor update:60",
    "Analyze churn cohort:90:deep",
    "Email triage:45",
    "Slack catch-up:30",
    "Expense report:20",
    "Team scheduling:15",
]


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Classify tasks deep vs shallow and audit the shallow share against a budget.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=("Exit codes:\n"
                "  0  WITHIN-BUDGET — shallow share <= --budget\n"
                "  1  usage / input error\n"
                "  2  OVER-BUDGET — shallow share > --budget; cut, batch, or delegate first"),
    )
    p.add_argument("--task", action="append", default=[],
                   help='Repeatable: "name:minutes" (heuristic) or "name:minutes:deep|shallow" (override)')
    p.add_argument("--budget", type=float, default=50.0,
                   help="Shallow budget as percent of total time (default 50 — top of the 30-50 band)")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of the table")
    p.add_argument("--sample", action="store_true", help="Run the embedded sample task list")
    args = p.parse_args(argv)

    if args.sample:
        args.task = SAMPLE_TASKS
    if not args.task:
        p.print_help()
        print("\nerror: at least one --task is required (or --sample)", file=sys.stderr)
        return 1
    if not 0 < args.budget <= 100:
        print("error: --budget must be in (0, 100]", file=sys.stderr)
        return 1
    try:
        tasks = [parse_task(s) for s in args.task]
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    result = audit(tasks, args.budget)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_human(result))
    return 0 if result["verdict"] == "WITHIN-BUDGET" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
