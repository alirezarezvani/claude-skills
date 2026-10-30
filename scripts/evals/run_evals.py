#!/usr/bin/env python3
"""Run skill evals with Claude Code and write one results JSON.

Two evals, both run through the real `claude` CLI with the repo's plugins loaded by --plugin-dir:

  trigger    Does the skill fire on realistic prompts, and stay quiet on a near miss?
             Cases: cases/trigger_cases.json (2 positive + 1 near-miss prompt per skill).
             Each prompt runs --runs times, because single runs swing between 0/2 and 2/2.
  behaviour  Does the skill change the answer? The same task runs with the skill's plugin and
             with no plugin, in a fresh copy of a fixture folder, and a blind grader scores both
             transcripts against the case's assertions. Cases: cases/behaviour_cases.json.

Selection: --skills / --cases pick explicitly; otherwise a rotation over all skills with cases,
--count skills a night, offset by the date, so the whole library is covered every
ceil(skills / count) days and the same night always picks the same slice.

Spend: every run passes --max-budget-usd, and no new run starts once --budget is spent.

Usage:
  python3 scripts/evals/run_evals.py --count 15 --out eval-out/          # nightly slice
  python3 scripts/evals/run_evals.py --skills engineering/skills/rag-architect --runs 1
  python3 scripts/evals/run_evals.py --plan --count 15                   # print the slice, run nothing
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import json
import math
import os
import shutil
import subprocess
import tempfile

from common import FIXTURES, Budget, all_plugin_dirs, fired, inventory, load_cases, run_claude, REPO

GRADER = """You are grading an AI assistant's answer against a checklist. You see the user's
task, the tools the assistant called, and its final answer. For each assertion decide whether
the final answer (or the tool calls, where the assertion is about process) clearly satisfies it.
Be strict: vague or partial coverage is a fail. Quote short evidence.

TASK:
{prompt}

TOOLS CALLED (in order):
{tools}

FINAL ANSWER:
{final}

ASSERTIONS:
{assertions}
"""

GRADE_SCHEMA = {
    "type": "object",
    "properties": {"results": {"type": "array", "items": {
        "type": "object",
        "properties": {"assertion": {"type": "string"}, "pass": {"type": "boolean"}, "evidence": {"type": "string"}},
        "required": ["assertion", "pass", "evidence"]}}},
    "required": ["results"],
}


def rotate(items, count, day):
    if not items or count <= 0:
        return []
    if count >= len(items):
        return list(items)
    start = (day.toordinal() * count) % len(items)
    return [items[(start + i) % len(items)] for i in range(count)]


def plan(args):
    inv = {r["path"]: r for r in inventory()}
    trig = load_cases("trigger_cases.json")
    beh = load_cases("behaviour_cases.json")
    day = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    eligible = sorted(p for p in trig if p in inv)
    if args.skills:
        skills = [s.strip().rstrip("/") for s in args.skills.split(",") if s.strip()]
        unknown = [s for s in skills if s not in inv]
        if unknown:
            raise SystemExit(f"not an installable skill: {', '.join(unknown)}")
        trigger = [s for s in skills if s in trig]
        behaviour = [k for k, c in sorted(beh.items()) if c["skill"] in skills]
    else:
        trigger = rotate(eligible, args.count, day)
        behaviour = rotate(sorted(beh), args.behaviour_count, day)
    if args.cases:
        behaviour = [c.strip() for c in args.cases.split(",") if c.strip()]
    cycle = math.ceil(len(eligible) / args.count) if args.count else 0
    return day, inv, trig, beh, trigger, behaviour, cycle


def trigger_jobs(paths, inv, trig, scenario, runs):
    for p in paths:
        c = trig[p]
        prompts = [("pos", i, q) for i, q in enumerate(c["pos"])] + [("neg", 0, c["neg"])]
        for kind, i, q in prompts:
            for rep in range(runs):
                yield dict(skill=p, name=inv[p]["name"], plugin=inv[p]["plugin"], plugin_dir=inv[p]["plugin_dir"],
                           scenario=scenario, kind=kind, i=i, rep=rep, prompt=q)


def run_trigger(job, args, budget, all_dirs):
    if budget.exhausted:
        return dict(job, status="skipped")
    cwd = tempfile.mkdtemp(prefix="cc-eval-cwd-")
    dirs = all_dirs if job["scenario"] == "full" else [os.path.join(REPO, job["plugin_dir"])]
    key = f"{job['skill'].replace('/', '__')}__{job['scenario']}__{job['kind']}{job['i']}__r{job['rep']}"
    t = run_claude(job["prompt"], os.path.join(args.out, "transcripts", key + ".jsonl"), cwd=cwd,
                   plugin_dirs=dirs, model=args.model, max_turns=2, max_budget=0.5)
    shutil.rmtree(cwd, ignore_errors=True)
    budget.add(t["cost"])
    exact, plugin_hit = fired(t["skills"], job["name"], job["plugin"])
    return dict(job, status="error" if t["error"] and not t["skills"] else "ok", error=t["error"],
                fired=t["skills"], exact=exact, plugin_hit=plugin_hit, cost=t["cost"], transcript=key + ".jsonl")


def summarize_trigger(rows):
    out = {}
    for r in rows:
        s = out.setdefault(r["skill"], dict(skill=r["skill"], name=r["name"], plugin=r["plugin"], pos_total=0,
                                             pos_exact=0, pos_plugin=0, neg_total=0, neg_fires=0, errors=0,
                                             skipped=0, cost=0.0))
        s["cost"] += r.get("cost", 0.0)
        if r["status"] == "skipped":
            s["skipped"] += 1
            continue
        if r["status"] == "error":
            s["errors"] += 1
            continue
        if r["kind"] == "pos":
            s["pos_total"] += 1
            s["pos_exact"] += r["exact"]
            s["pos_plugin"] += r["plugin_hit"]
        else:
            s["neg_total"] += 1
            s["neg_fires"] += r["exact"]
    for s in out.values():
        s["cost"] = round(s["cost"], 4)
        if s["skipped"]:
            s["verdict"] = "INCOMPLETE"
        elif not s["pos_total"]:
            s["verdict"] = "ERROR"
        elif s["pos_exact"] / s["pos_total"] >= 0.75:
            s["verdict"] = "FIRES"
        elif s["pos_exact"]:
            s["verdict"] = "FLAKY"
        elif s["pos_plugin"]:
            s["verdict"] = "PLUGIN_ONLY"
        else:
            s["verdict"] = "SILENT"
        s["false_fire"] = s["neg_fires"] > 0
    return sorted(out.values(), key=lambda s: s["skill"])


def grade(case, t, args, budget):
    cfg_cwd = tempfile.mkdtemp(prefix="cc-eval-grade-")
    prompt = GRADER.format(prompt=case["prompt"], tools="\n".join(t["tools"]) or "(none)",
                           final=t["final"] or "(no final answer)",
                           assertions="\n".join(f"- {a}" for a in case["assertions"]))
    env = dict(os.environ, CLAUDE_CONFIG_DIR=cfg_cwd, CLAUDE_CODE_SYNC_PLUGINS="0")
    env.pop("CLAUDECODE", None)
    try:
        out = subprocess.run(["claude", "-p", prompt, "--output-format", "json", "--model", args.grader_model,
                              "--json-schema", json.dumps(GRADE_SCHEMA), "--no-session-persistence",
                              "--disable-slash-commands", "--max-budget-usd", "0.5"],
                             capture_output=True, text=True, env=env, cwd=cfg_cwd, timeout=600)
        res = json.loads(out.stdout)
        budget.add(res.get("total_cost_usd", 0.0))
        results = (res.get("structured_output") or {}).get("results") or []
    except (ValueError, subprocess.TimeoutExpired):
        results = []
    finally:
        shutil.rmtree(cfg_cwd, ignore_errors=True)
    passed = sum(1 for r in results if r.get("pass"))
    return dict(passed=passed, total=len(case["assertions"]), graded=len(results) == len(case["assertions"]),
                results=results)


def run_behaviour(cid, case, arm, args, budget):
    if budget.exhausted:
        return dict(case=cid, arm=arm, status="skipped")
    cwd = os.path.join(tempfile.mkdtemp(prefix="cc-eval-beh-"), "work")
    shutil.copytree(os.path.join(FIXTURES, case["fixture"]), cwd)
    plugin_dir = [os.path.join(REPO, inventory_dir(case))] if arm == "with" else []
    key = f"behaviour__{cid}__{arm}"
    t = run_claude(case["prompt"], os.path.join(args.out, "transcripts", key + ".jsonl"), cwd=cwd,
                   plugin_dirs=plugin_dir, model=args.model, max_turns=25, max_budget=1.0,
                   extra=["--permission-mode", "bypassPermissions"], timeout=1500)
    shutil.rmtree(os.path.dirname(cwd), ignore_errors=True)
    budget.add(t["cost"])
    g = grade(case, t, args, budget)
    return dict(case=cid, arm=arm, status="ok" if g["graded"] else "ungraded", fired=t["skills"], cost=t["cost"],
                transcript=key + ".jsonl", **g)


_INV = {}


def inventory_dir(case):
    if not _INV:
        _INV.update({r["path"]: r for r in inventory()})
    return _INV[case["skill"]]["plugin_dir"]


def summarize_behaviour(rows, beh):
    out = []
    by = {(r["case"], r["arm"]): r for r in rows}
    for cid in sorted({r["case"] for r in rows}):
        w, wo = by.get((cid, "with"), {}), by.get((cid, "without"), {})
        s = dict(case=cid, skill=beh[cid]["skill"], name=beh[cid]["name"], total=len(beh[cid]["assertions"]),
                 with_passed=w.get("passed"), without_passed=wo.get("passed"),
                 skill_fired=bool(w.get("fired")), cost=round(w.get("cost", 0) + wo.get("cost", 0), 4))
        if w.get("status") != "ok" or wo.get("status") != "ok":
            s["verdict"] = "INCOMPLETE"
        else:
            d = s["with_passed"] - s["without_passed"]
            s["delta"] = d
            s["verdict"] = "LIFTS" if d > 0 else "HURTS" if d < 0 else "NO_LIFT"
        out.append(s)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills", help="comma-separated skill paths to run (overrides the rotation)")
    ap.add_argument("--cases", help="comma-separated behaviour case ids to run (overrides the rotation)")
    ap.add_argument("--count", type=int, default=15, help="skills per night in the trigger rotation (default 15)")
    ap.add_argument("--behaviour-count", type=int, default=2, help="behaviour cases per night (default 2)")
    ap.add_argument("--scenario", choices=["targeted", "full"], default="targeted",
                    help="targeted: load only the skill's plugin; full: load every marketplace plugin")
    ap.add_argument("--runs", type=int, default=2, help="repeats per trigger prompt (default 2)")
    ap.add_argument("--model", default="sonnet", help="model under test (default sonnet)")
    ap.add_argument("--grader-model", default="sonnet", help="behaviour grader model (default sonnet)")
    ap.add_argument("--budget", type=float, default=10.0, help="stop starting runs past this many USD (default 10)")
    ap.add_argument("--jobs", type=int, default=6, help="parallel claude processes (default 6)")
    ap.add_argument("--date", help="rotation date, YYYY-MM-DD (default today)")
    ap.add_argument("--out", default="eval-out", help="output folder (default eval-out/)")
    ap.add_argument("--plan", action="store_true", help="print the selection and estimated cost, run nothing")
    args = ap.parse_args()

    day, inv, trig, beh, trigger, behaviour, cycle = plan(args)
    missing = [c for c in behaviour if c not in beh]
    if missing:
        raise SystemExit(f"unknown behaviour case: {', '.join(missing)}")
    n_trig = len(trigger) * 3 * args.runs
    estimate = n_trig * (0.16 if args.scenario == "full" else 0.08) + len(behaviour) * 0.40
    print(f"{day}: {len(trigger)} skills x {3 * args.runs} trigger runs ({args.scenario}), "
          f"{len(behaviour)} behaviour cases; estimate ${estimate:.2f}, cap ${args.budget:.2f}; "
          f"full rotation every {cycle} nights")
    for p in trigger:
        print(f"  trigger   {p}")
    for c in behaviour:
        print(f"  behaviour {c} ({beh[c]['skill']})")
    if args.plan:
        return

    os.makedirs(os.path.join(args.out, "transcripts"), exist_ok=True)
    budget = Budget(args.budget)
    all_dirs = all_plugin_dirs() if args.scenario == "full" else []
    jobs = list(trigger_jobs(trigger, inv, trig, args.scenario, args.runs))
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        beh_futs = [ex.submit(run_behaviour, c, beh[c], arm, args, budget) for c in behaviour for arm in ("with", "without")]
        trig_rows = list(ex.map(lambda j: run_trigger(j, args, budget, all_dirs), jobs))
        beh_rows = [f.result() for f in beh_futs]

    results = dict(date=day.isoformat(), model=args.model, grader_model=args.grader_model, scenario=args.scenario,
                   runs=args.runs, budget=args.budget, spent=round(budget.spent, 4),
                   stopped_early=any(r["status"] == "skipped" for r in trig_rows + beh_rows),
                   claude_version=subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip(),
                   trigger=summarize_trigger(trig_rows), behaviour=summarize_behaviour(beh_rows, beh),
                   trigger_runs=trig_rows, behaviour_runs=beh_rows)
    with open(os.path.join(args.out, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    print(f"spent ${budget.spent:.2f}; wrote {os.path.join(args.out, 'results.json')}")


if __name__ == "__main__":
    main()
