#!/usr/bin/env python3
"""Turn a close checklist into a dependency-ordered calendar with a critical path.

Most close checklists are a flat list sorted by habit. The close actually runs
as a dependency graph: accruals wait on the sub-ledger cut-off, consolidation
waits on intercompany, flux review waits on everything. A flat list hides the
one chain of tasks that sets the close date, so teams speed up the wrong work.

Input JSON:
  {"period": "2026-10", "close_start": "2026-11-02", "target_wd": 5, "holidays": ["2026-11-11"],
   "tasks": [{"id": "ap-cutoff", "name": "AP cut-off", "owner": "Dana", "reviewer": "Lee",
              "duration_days": 1, "depends_on": [], "deadline_wd": 2, "key_control": false}]}

Durations are in workdays (0.5 = half a day). WD1 is the first business day of
the close. Scheduling assumes each task starts as soon as its predecessors
finish, then checks whether the people can actually carry that load.

Checks:
  C1 [BLOCKER] task without an owner
  C2 [BLOCKER] planned close finishes after target_wd (the critical path is shown)
  C3 [WARN]    task finishes after its own deadline_wd
  C4 [WARN]    an owner is booked for more than one day of work on the same workday
  C5 [BLOCKER] key control with no reviewer, or reviewed by its own preparer
  C6 [WARN]    one person owns more than half of the critical path (key-person risk)
Unknown dependencies and cycles are invalid input (exit 3).

Deterministic, stdlib only, no network.

Exit codes:
    0  on track
    2  warnings
    3  invalid input (unknown dependency, cycle, bad field)
    4  blocker
"""

import argparse
import datetime as dt
import json
import math
import sys
from collections import defaultdict

EPS = 1e-9

SAMPLE = {
    "period": "2026-10", "close_start": "2026-11-02", "target_wd": 5, "holidays": [],
    "tasks": [
        {"id": "ap-cutoff", "name": "AP cut-off and invoice accrual", "owner": "Dana", "duration_days": 1, "depends_on": []},
        {"id": "ar-cutoff", "name": "AR cut-off and billing", "owner": "Sam", "duration_days": 1, "depends_on": []},
        {"id": "payroll", "name": "Payroll accrual", "owner": "Dana", "duration_days": 0.5, "depends_on": []},
        {"id": "bank-rec", "name": "Bank reconciliations", "owner": "Sam", "reviewer": "Lee", "duration_days": 1,
         "depends_on": ["ar-cutoff"], "key_control": True, "deadline_wd": 2},
        {"id": "accruals", "name": "Accruals and prepaids", "owner": "Dana", "reviewer": "Dana", "duration_days": 1,
         "depends_on": ["ap-cutoff", "payroll"], "key_control": True},
        {"id": "fixed-assets", "name": "Depreciation run", "owner": "Priya", "duration_days": 0.5, "depends_on": ["ap-cutoff"]},
        {"id": "interco", "name": "Intercompany matching and eliminations", "owner": "Dana", "duration_days": 1.5,
         "depends_on": ["accruals", "bank-rec"], "deadline_wd": 3},
        {"id": "consolidation", "name": "Consolidation and FX translation", "owner": "Lee", "duration_days": 1,
         "depends_on": ["interco", "fixed-assets"]},
        {"id": "flux", "name": "Flux review", "owner": "Lee", "reviewer": "CFO", "duration_days": 1,
         "depends_on": ["consolidation"], "key_control": True},
        {"id": "reporting", "name": "Management reporting pack", "owner": "", "duration_days": 0.5, "depends_on": ["flux"]},
    ],
}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def topo_order(tasks):
    ids = {t["id"] for t in tasks}
    for t in tasks:
        for d in t.get("depends_on", []):
            if d not in ids:
                _fail(f"task '{t['id']}' depends on unknown task '{d}'")
    indeg = {t["id"]: len(t.get("depends_on", [])) for t in tasks}
    children = defaultdict(list)
    for t in tasks:
        for d in t.get("depends_on", []):
            children[d].append(t["id"])
    ready = sorted(i for i, n in indeg.items() if n == 0)
    order = []
    while ready:
        cur = ready.pop(0)
        order.append(cur)
        for c in sorted(children[cur]):
            indeg[c] -= 1
            if indeg[c] == 0:
                ready.append(c)
    if len(order) != len(tasks):
        _fail("dependency cycle among: " + ", ".join(sorted(i for i, n in indeg.items() if n > 0)))
    return order, children


def workday_dates(start, count, holidays):
    dates, day = [], start
    while len(dates) < count:
        if day.weekday() < 5 and day.isoformat() not in holidays:
            dates.append(day)
        day += dt.timedelta(days=1)
    return dates


def plan(spec):
    tasks = spec.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        _fail("spec needs a non-empty 'tasks' list")
    seen = set()
    for t in tasks:
        if not t.get("id") or t["id"] in seen:
            _fail(f"every task needs a unique id (problem at {t.get('id')!r})")
        seen.add(t["id"])
        if not isinstance(t.get("duration_days", 0), (int, float)) or t.get("duration_days", 0) < 0:
            _fail(f"task '{t['id']}': duration_days must be a non-negative number")
    by_id = {t["id"]: t for t in tasks}
    order, children = topo_order(tasks)

    es, ef = {}, {}
    for i in order:
        t = by_id[i]
        es[i] = max((ef[d] for d in t.get("depends_on", [])), default=0.0)
        ef[i] = es[i] + float(t.get("duration_days", 0))
    finish = max(ef.values())
    lf, ls = {}, {}
    for i in reversed(order):
        lf[i] = min((ls[c] for c in children[i]), default=finish)
        ls[i] = lf[i] - float(by_id[i].get("duration_days", 0))
    critical = [i for i in order if ls[i] - es[i] < EPS]
    # trace one critical chain from the last-finishing task backwards
    chain, cur = [], max(critical, key=lambda i: ef[i])
    while cur:
        chain.append(cur)
        preds = [d for d in by_id[cur].get("depends_on", []) if d in critical and abs(ef[d] - es[cur]) < EPS]
        cur = preds[0] if preds else None
    chain.reverse()

    wd = lambda x: max(1, math.ceil(x - EPS))
    findings = []
    target = spec.get("target_wd")
    close_wd = wd(finish)
    if target is not None and close_wd > target:
        findings.append(("C2", "BLOCKER", f"close finishes WD{close_wd}, target WD{target}; critical path: {' -> '.join(chain)}"))
    for i in order:
        t = by_id[i]
        if not str(t.get("owner", "")).strip():
            findings.append(("C1", "BLOCKER", f"'{i}' has no owner"))
        if t.get("deadline_wd") is not None and wd(ef[i]) > t["deadline_wd"]:
            findings.append(("C3", "WARN", f"'{i}' finishes WD{wd(ef[i])}, deadline WD{t['deadline_wd']}"))
        if t.get("key_control"):
            rv = str(t.get("reviewer", "")).strip()
            if not rv:
                findings.append(("C5", "BLOCKER", f"key control '{i}' has no reviewer"))
            elif rv == str(t.get("owner", "")).strip():
                findings.append(("C5", "BLOCKER", f"key control '{i}' is reviewed by its own preparer ({rv})"))

    load = defaultdict(lambda: defaultdict(float))
    for i in order:
        owner = str(by_id[i].get("owner", "")).strip()
        if not owner:
            continue
        s, e = es[i], ef[i]
        day = math.floor(s)
        while day < e - EPS:
            overlap = min(e, day + 1) - max(s, day)
            load[owner][day + 1] += overlap
            day += 1
    for owner, days in sorted(load.items()):
        over = [f"WD{d} ({v:.1f}d)" for d, v in sorted(days.items()) if v > 1 + EPS]
        if over:
            findings.append(("C4", "WARN", f"{owner} is over-booked on {', '.join(over)}; the plan is not achievable as staffed"))

    crit_total = sum(float(by_id[i].get("duration_days", 0)) for i in chain) or 1
    share = defaultdict(float)
    for i in chain:
        share[str(by_id[i].get("owner", "")).strip() or "(none)"] += float(by_id[i].get("duration_days", 0))
    for owner, d in share.items():
        if owner != "(none)" and d / crit_total > 0.5:
            findings.append(("C6", "WARN", f"{owner} owns {d / crit_total:.0%} of the critical path"))

    dates = []
    if spec.get("close_start"):
        try:
            start = dt.date.fromisoformat(spec["close_start"])
        except ValueError:
            _fail("close_start must be YYYY-MM-DD")
        dates = workday_dates(start, max(close_wd, target or 0) + 1, set(spec.get("holidays", [])))

    schedule = []
    for i in sorted(order, key=lambda x: (es[x], x)):
        t = by_id[i]
        row = {"id": i, "name": t.get("name", i), "owner": t.get("owner", ""), "start_wd": math.floor(es[i] + EPS) + 1,
               "finish_wd": wd(ef[i]), "slack_days": round(ls[i] - es[i], 2), "critical": i in critical}
        if dates:
            row["finish_date"] = dates[row["finish_wd"] - 1].isoformat()
        schedule.append(row)

    order_sev = {"BLOCKER": 0, "WARN": 1}
    findings.sort(key=lambda f: (order_sev[f[1]], f[0]))
    sev = [f[1] for f in findings]
    verdict, code = ("BLOCKED", 4) if "BLOCKER" in sev else (("AT_RISK", 2) if sev else ("ON_TRACK", 0))
    return {"verdict": verdict, "period": spec.get("period"), "close_wd": close_wd, "target_wd": target,
            "close_date": dates[close_wd - 1].isoformat() if dates else None, "critical_path": chain,
            "findings": [{"id": i, "severity": s, "message": m} for i, s, m in findings], "schedule": schedule}, code


def render(r):
    head = f"Close plan {r['period'] or ''}: {r['verdict']} - finishes WD{r['close_wd']}"
    if r["target_wd"]:
        head += f" (target WD{r['target_wd']})"
    if r["close_date"]:
        head += f", {r['close_date']}"
    out = [head, f"  critical path: {' -> '.join(r['critical_path'])}"]
    out += [f"  [{f['severity']}] {f['id']}: {f['message']}" for f in r["findings"]]
    out.append(f"  {'task':<16} {'owner':<8} {'start':>5} {'finish':>6} {'slack':>6}")
    for s in r["schedule"]:
        out.append(f"  {s['id']:<16} {s['owner'] or '-':<8} {'WD' + str(s['start_wd']):>5} {'WD' + str(s['finish_wd']):>6} "
                   f"{s['slack_days']:>6}{'  *critical' if s['critical'] else ''}")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Order close tasks by dependencies, find the critical path, and check owners, reviewers, deadlines and load.")
    p.add_argument("--plan", help="close plan JSON (see module docstring)")
    p.add_argument("--sample", action="store_true", help="run on an embedded sample close plan")
    p.add_argument("--print-sample", action="store_true", help="print the sample plan JSON and exit")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    if a.print_sample:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if a.sample:
        spec = SAMPLE
    elif a.plan:
        try:
            with open(a.plan, encoding="utf-8") as fh:
                spec = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            _fail(f"cannot read {a.plan}: {exc}")
    else:
        p.error("give --plan, or --sample")
    report, code = plan(spec)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
