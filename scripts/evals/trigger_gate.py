#!/usr/bin/env python3
"""Trigger-rate gate: a new or re-described skill must fire on held-out prompts, and never on its near miss.

Claude picks a skill from its name and description alone, so only a change to one of those can
change whether it fires. The gate looks at the SKILL.md files a branch changes against its base,
keeps the ones whose name or description changed (or that are new), and runs each through
`claude -p` the way scripts/evals/run_evals.py does: only the skill's own plugin loaded, an
empty folder, a throwaway config dir, hooks off.

The exam is held out. Prompts come from the BASE branch's cases/heldout_cases.json (falling back
to cases/trigger_cases.json), which were written from the description before this change, so a
branch cannot tune its own exam. A skill with no case at base gets one drafted at run time: from
its base description when it had one, otherwise (a new skill) from its new description.

Rules, per skill (2 positive prompts + 1 near miss, --runs repeats each):
  FALSE_FIRE  it fired on the near-miss prompt at least once                    -> fail
  BELOW_FLOOR new skill fired on fewer than --min-rate of the positive runs      -> fail
  REGRESSED   changed skill's rate fell more than --max-drop below the base
              description's rate on the same prompts, measured in the same run  -> fail
A skill that fails is measured once more and judged on the pooled runs, because single trigger
runs are noisy (0/2 one run, 2/2 the next). A skill the gate could not measure (a run errored, or it
fell past --max-skills or --budget) is reported NOT_MEASURED and fails the gate with exit 3.

Exit codes: 0 pass or nothing to measure, 1 at least one skill failed, 2 usage error, 3 at least
one skill was not measured (runs errored, budget or --max-skills ran out). 3 also fails the check:
an unmeasured skill has not passed.

Usage:
  python3 scripts/evals/trigger_gate.py --base origin/dev --plan     # what would run, no model calls
  python3 scripts/evals/trigger_gate.py --base origin/dev --out gate-out
"""
import argparse
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
import tempfile

from common import REPO, Budget, _frontmatter, fired, inventory, run_claude

MIRRORS = (".gemini/", ".codex/", ".vibe/", ".hermes/", ".claude/")
NO_HOOKS = ["--settings", json.dumps({"disableAllHooks": True})]
COST_PER_RUN = 0.08


def git(*args, check=True):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, check=check).stdout


def show(rev, path):
    out = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else None


def frontmatter_text(text):
    """(name, description) from SKILL.md text, via the same parser the inventory uses."""
    fd, tmp = tempfile.mkstemp(suffix=".md")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    try:
        return _frontmatter(tmp)
    finally:
        os.unlink(tmp)


def changed_skills(base, head):
    """Installable skills whose name or description differs between merge-base and head."""
    mb = git("merge-base", base, head).strip()
    files = git("diff", "--name-only", "--diff-filter=AMR", f"{mb}..{head}", "--", "*SKILL.md").split()
    files = [f for f in files if not f.startswith(MIRRORS)]
    inv = inventory()
    by_real = {os.path.realpath(os.path.join(REPO, r["path"])): r for r in inv}
    by_key = {(r["name"], r["description"]): r for r in inv}
    rows, notes = {}, []
    for f in files:
        abs_f = os.path.join(REPO, f)
        if not os.path.exists(abs_f):
            continue
        head_fm = _frontmatter(abs_f)
        old = show(mb, f)
        if old is not None and frontmatter_text(old) == head_fm:
            continue  # body-only edit: cannot change triggering
        row = by_real.get(os.path.realpath(os.path.dirname(abs_f))) or by_key.get(head_fm)
        if not row:
            notes.append(f"`{f}`: not in any marketplace plugin, not measured")
            continue
        rows[row["path"]] = row
    return mb, [rows[k] for k in sorted(rows)], notes


def base_cases(mb):
    cases = {}
    for name in ("trigger_cases.json", "heldout_cases.json"):  # heldout wins
        text = show(mb, f"scripts/evals/cases/{name}")
        if text:
            try:
                cases.update(json.loads(text))
            except ValueError:
                pass
    return cases


def prepare(rows, mb, worktree, model):
    """Attach base info and a held-out case to each changed skill. Drafts cases it lacks."""
    cases = base_cases(mb)
    to_draft = []
    for r in rows:
        base_md = os.path.join(worktree, r["path"], "SKILL.md")
        base_plugin = os.path.join(worktree, r["plugin_dir"], ".claude-plugin", "plugin.json")
        r["is_new"] = not (os.path.exists(base_md) and os.path.exists(base_plugin))
        r["base_name"] = None if r["is_new"] else _frontmatter(base_md)[0]
        if r["path"] in cases:
            c = cases[r["path"]]
            r["case"] = dict(pos=c["pos"], neg=c["neg"])
            r["case_source"] = "base heldout/trigger cases"
        else:
            desc = r["description"] if r["is_new"] else _frontmatter(base_md)[1]
            to_draft.append(dict(path=r["path"], name=r["base_name"] or r["name"], description=desc))
            r["case_source"] = "drafted from the " + ("new" if r["is_new"] else "base") + " description"
    if to_draft:
        from generate_trigger_cases import draft
        try:
            got, _ = draft(to_draft, model)
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as e:
            got = {}
            for r in rows:
                if "case" not in r:
                    r["draft_error"] = str(e)
        for r in rows:
            c = got.get(r["path"]) if "case" not in r else None
            if c and len(c.get("pos", [])) == 2 and c.get("neg"):
                r["case"] = dict(pos=c["pos"], neg=c["neg"])
                r["drafted_case"] = r["case"]
    return rows


def jobs_for(r, worktree, runs, rnd):
    prompts = [("pos", i, q) for i, q in enumerate(r["case"]["pos"])] + [("neg", 0, r["case"]["neg"])]
    arms = [("head", os.path.join(REPO, r["plugin_dir"]), r["name"])]
    if not r["is_new"]:
        arms.append(("base", os.path.join(worktree, r["plugin_dir"]), r["base_name"]))
    for arm, plugin_dir, name in arms:
        for kind, i, q in prompts:
            for rep in range(runs):
                yield dict(skill=r["path"], plugin=r["plugin"], arm=arm, plugin_dir=plugin_dir, name=name,
                           kind=kind, i=i, rep=rep, round=rnd, prompt=q)


def run_job(j, args, budget):
    if budget.exhausted:
        return dict(j, status="skipped")
    cwd = tempfile.mkdtemp(prefix="cc-gate-cwd-")
    key = f"{j['skill'].replace('/', '__')}__{j['arm']}__{j['kind']}{j['i']}__r{j['round']}{j['rep']}"
    t = run_claude(j["prompt"], os.path.join(args.out, "transcripts", key + ".jsonl"), cwd=cwd,
                   plugin_dirs=[j["plugin_dir"]], model=args.model, max_turns=2, max_budget=0.5, extra=NO_HOOKS)
    shutil.rmtree(cwd, ignore_errors=True)
    budget.add(t["cost"])
    exact, _ = fired(t["skills"], j["name"], j["plugin"])
    return dict(j, status="error" if t["error"] and not t["skills"] else "ok", exact=exact, fired=t["skills"],
                cost=t["cost"], transcript=key + ".jsonl", error=t["error"], error_detail=t.get("error_detail", ""))


def tally(runs, arm):
    rs = [x for x in runs if x["arm"] == arm]
    pos = [x for x in rs if x["kind"] == "pos" and x["status"] == "ok"]
    neg = [x for x in rs if x["kind"] == "neg" and x["status"] == "ok"]
    return dict(pos=sum(x["exact"] for x in pos), pos_total=len(pos), neg_fires=sum(x["exact"] for x in neg),
                neg_total=len(neg), skipped=sum(x["status"] == "skipped" for x in rs),
                errors=sum(x["status"] == "error" for x in rs))


def judge(r, runs, args):
    h = tally(runs, "head")
    b = tally(runs, "base") if not r["is_new"] else None
    r["head"], r["base"] = h, b
    if h["skipped"] or (b and b["skipped"]):
        return "NOT_MEASURED", "budget ran out before every run started"
    if not h["pos_total"] or (b and not b["pos_total"]) or h["errors"] or (b and b["errors"]):
        n = h["errors"] + (b["errors"] if b else 0)
        return "NOT_MEASURED", f"{n} run(s) errored (see the errors below)"
    rate = h["pos"] / h["pos_total"]
    if h["neg_fires"]:
        return "FALSE_FIRE", f"fired on the near-miss prompt {h['neg_fires']}/{h['neg_total']}"
    if r["is_new"]:
        if rate < args.min_rate:
            return "BELOW_FLOOR", f"fired {h['pos']}/{h['pos_total']}, floor is {args.min_rate:.0%}"
        return "PASS", f"fired {h['pos']}/{h['pos_total']}"
    base_rate = b["pos"] / b["pos_total"]
    if rate < base_rate - args.max_drop - 1e-9:
        return "REGRESSED", f"fired {h['pos']}/{h['pos_total']} vs {b['pos']}/{b['pos_total']} with the base description"
    return "PASS", f"fired {h['pos']}/{h['pos_total']} vs {b['pos']}/{b['pos_total']} with the base description"


def run_round(rows, worktree, args, budget, rnd):
    jobs = [j for r in rows for j in jobs_for(r, worktree, args.runs, rnd)]
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        return list(ex.map(lambda j: run_job(j, args, budget), jobs))


def render(res):
    lines = ["## Trigger-rate gate", ""]
    if not res["skills"] and not res["not_measured"]:
        lines.append("No skill name or description changed, nothing to measure.")
    else:
        lines += [f"Base `{res['merge_base'][:8]}`, model `{res['model']}`, {res['runs']} runs per prompt per round, "
                  f"spent ${res['spent']:.2f}.", "",
                  "| Skill | New? | Verdict | Detail | Exam |", "|---|---|---|---|---|"]
        for s in res["skills"]:
            lines.append(f"| `{s['path']}` | {'yes' if s['is_new'] else 'no'} | **{s['verdict']}** | {s['detail']} "
                         f"| {s['case_source']} |")
        for p in res["not_measured"]:
            lines.append(f"| `{p}` | | NOT_MEASURED | over --max-skills | |")
    errs = {}
    for r in res["runs_detail"]:
        if r.get("status") == "error":
            errs.setdefault(f"{r.get('error')}: {r.get('error_detail') or '(no detail)'}", 0)
            errs[f"{r.get('error')}: {r.get('error_detail') or '(no detail)'}"] += 1
    if errs:
        lines += ["", "**Runs that errored** (a run that errors measures nothing, so the gate fails):", ""]
        lines += [f"- {n}x `{e}`" for e, n in sorted(errs.items(), key=lambda kv: -kv[1])[:5]]
        if any("401" in e or "authenticate" in e.lower() for e in errs):
            lines += ["", "**Auth failed.** The CI token is missing, wrong or expired. A maintainer runs "
                      "`claude setup-token` and stores the new token as the repo secret `CLAUDE_CODE_OAUTH_TOKEN`; "
                      "subscription tokens expire, so this recurs."]
    for n in res["notes"]:
        lines.append(f"\n- {n}")
    failed = [s for s in res["skills"] if s["verdict"] in FAILING]
    if failed:
        lines += ["", "**How to fix:** say what the skill is for in the user's words (\"Use whenever the user ...\" "
                  "with 2-4 situations); for a false fire, narrow the description so it no longer claims the near-miss "
                  "job. The exam prompts and transcripts are in the workflow artifact. Recipe: "
                  "`scripts/evals/README.md`."]
    drafted = {s["path"]: s["drafted_case"] for s in res["skills"] if s.get("drafted_case")}
    if drafted:
        lines += ["", "<details><summary>Drafted exam cases (review and add to "
                  "<code>scripts/evals/cases/heldout_cases.json</code> in a later PR)</summary>", "", "```json",
                  json.dumps(drafted, indent=1, ensure_ascii=False), "```", "</details>"]
    return "\n".join(lines) + "\n"


FAILING = ("FALSE_FIRE", "BELOW_FLOOR", "REGRESSED")
# A skill the gate could not measure has not passed it: failing open let PR #1111 through with 12 of
# 12 skills unmeasured because every claude run errored on the runner.
UNMEASURED = ("NOT_MEASURED",)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="origin/dev", help="branch or commit to compare against (default origin/dev)")
    ap.add_argument("--head", default="HEAD", help="commit under test; must be checked out (default HEAD)")
    ap.add_argument("--runs", type=int, default=2, help="repeats per prompt per round (default 2)")
    ap.add_argument("--min-rate", type=float, default=0.5, help="positive fire rate a new skill needs (default 0.5)")
    ap.add_argument("--max-drop", type=float, default=0.25,
                    help="largest allowed fall in fire rate vs the base description (default 0.25, one run in four)")
    ap.add_argument("--max-skills", type=int, default=20, help="skills measured per run (default 20)")
    ap.add_argument("--budget", type=float, default=30.0, help="stop starting runs past this many USD (default 30)")
    ap.add_argument("--model", default="sonnet", help="model under test (default sonnet)")
    ap.add_argument("--jobs", type=int, default=6, help="parallel claude processes (default 6)")
    ap.add_argument("--out", default="gate-out", help="output folder (default gate-out/)")
    ap.add_argument("--plan", action="store_true", help="list what would be measured and the cost; no model calls")
    args = ap.parse_args()
    if git("rev-parse", "HEAD").strip() != git("rev-parse", args.head).strip():
        sys.exit("--head must be the checked-out commit")

    mb, rows, notes = changed_skills(args.base, args.head)
    measured, over = rows[:args.max_skills], [r["path"] for r in rows[args.max_skills:]]
    est = len(measured) * 3 * args.runs * 2 * COST_PER_RUN
    print(f"{len(rows)} skill(s) with a new or changed name/description; measuring {len(measured)}, "
          f"estimate ${est:.2f} (cap ${args.budget:.2f})")
    for r in measured:
        print(f"  {r['path']}")
    for p in over:
        print(f"  {p} (over --max-skills, not measured)")
    if args.plan:
        if os.environ.get("GITHUB_OUTPUT"):
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write(f"skills={len(measured)}\n")
        return 0

    os.makedirs(os.path.join(args.out, "transcripts"), exist_ok=True)
    budget = Budget(args.budget)
    worktree = tempfile.mkdtemp(prefix="cc-gate-base-")
    results = []
    try:
        if measured:
            git("worktree", "add", "--detach", worktree, mb)
            measured = prepare(measured, mb, worktree, args.model)
            for r in measured:
                if "case" not in r:
                    r["verdict"], r["detail"] = "NOT_MEASURED", "no exam case and drafting one failed" + (f": {r['draft_error']}" if r.get("draft_error") else "")
            todo = [r for r in measured if "case" in r]
            runs = run_round(todo, worktree, args, budget, 0)
            for r in todo:
                r["verdict"], r["detail"] = judge(r, [x for x in runs if x["skill"] == r["path"]], args)
            retry = [r for r in todo if r["verdict"] in FAILING]
            if retry:  # confirm on a second round and judge the pooled runs
                runs += run_round(retry, worktree, args, budget, 1)
                for r in retry:
                    r["verdict"], r["detail"] = judge(r, [x for x in runs if x["skill"] == r["path"]], args)
                    r["detail"] += " (pooled over 2 rounds)"
            results = runs
    finally:
        subprocess.run(["git", "-C", REPO, "worktree", "remove", "--force", worktree], capture_output=True)
        shutil.rmtree(worktree, ignore_errors=True)

    keep = ("path", "name", "plugin", "is_new", "case_source", "case", "drafted_case", "verdict", "detail", "head", "base")
    res = dict(merge_base=mb, model=args.model, runs=args.runs, min_rate=args.min_rate, max_drop=args.max_drop,
               spent=round(budget.spent, 4), skills=[{k: r.get(k) for k in keep} for r in measured],
               not_measured=over, notes=notes, runs_detail=results)
    with open(os.path.join(args.out, "gate.json"), "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
    md = render(res)
    with open(os.path.join(args.out, "gate.md"), "w") as f:
        f.write(md)
    print(md)
    if any(s["verdict"] in FAILING for s in res["skills"]):
        return 1
    if over or any(s["verdict"] in UNMEASURED for s in res["skills"]):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
