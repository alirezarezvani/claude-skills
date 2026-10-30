#!/usr/bin/env python3
"""Draft trigger cases for skills that have none, using Claude, into cases/trigger_cases.json.

Each case is two realistic prompts that should fire the skill (without naming it) and one
near-miss prompt from an adjacent topic that should not. Drafts are data for review, not
ground truth: read the diff before committing, and fix any case where the "near miss" is
really the skill's job. Existing cases are never overwritten unless --force is given.

Maintainer tool, run by hand (it spends API budget, about $0.01 per skill):
  python3 scripts/evals/generate_trigger_cases.py --limit 20
  python3 scripts/evals/generate_trigger_cases.py --skills engineering/skills/rag-architect --force
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import tempfile

from common import CASES, inventory, load_cases

PROMPT = """You write trigger-eval cases for Claude Code skills. A skill is picked by the model
only from its name and description, so the eval asks: does it fire on realistic requests, and
stay quiet on a near miss?

For EACH skill below write:
- "pos": two prompts a real user would type that this skill should handle. Do not name the
  skill or quote its trigger phrases verbatim. Make one short and casual, one specific with
  concrete details (numbers, file names, context). Ask for the work, not for a skill.
- "neg": one near-miss prompt from an adjacent topic that shares vocabulary with the skill but
  is NOT its job (a different task a nearby skill or plain Claude should handle). It must not be
  something the description says the skill does.

Return ONLY a JSON object mapping each skill path to {"pos": [str, str], "neg": str}. No prose.

Skills:
"""


def draft(batch, model):
    listing = "\n".join(f"- path: {r['path']}\n  name: {r['name']}\n  description: {r['description']}" for r in batch)
    cfg = tempfile.mkdtemp(prefix="cc-gen-cfg-")
    env = dict(os.environ, CLAUDE_CONFIG_DIR=cfg, CLAUDE_CODE_SYNC_PLUGINS="0")
    env.pop("CLAUDECODE", None)
    out = subprocess.run(["claude", "-p", PROMPT + listing, "--output-format", "json", "--model", model,
                          "--max-turns", "1", "--no-session-persistence", "--disable-slash-commands"],
                         capture_output=True, text=True, env=env, cwd=cfg, timeout=600)
    res = json.loads(out.stdout)
    text = res.get("result", "")
    start, end = text.find("{"), text.rfind("}")
    cases = json.loads(text[start:end + 1])
    return cases, res.get("total_cost_usd", 0.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills", help="comma-separated skill paths (default: every skill without cases)")
    ap.add_argument("--limit", type=int, default=0, help="draft at most N skills")
    ap.add_argument("--batch", type=int, default=12, help="skills per model call")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--force", action="store_true", help="overwrite existing cases")
    args = ap.parse_args()

    cases = load_cases("trigger_cases.json")
    inv = inventory()
    if args.skills:
        want = set(args.skills.split(","))
        todo = [r for r in inv if r["path"] in want]
    else:
        todo = [r for r in inv if args.force or r["path"] not in cases]
    if args.limit:
        todo = todo[:args.limit]
    batches = [todo[i:i + args.batch] for i in range(0, len(todo), args.batch)]
    spent = 0.0
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        for batch, fut in zip(batches, [ex.submit(draft, b, args.model) for b in batches]):
            try:
                got, cost = fut.result()
            except (ValueError, KeyError, subprocess.TimeoutExpired) as e:
                print(f"batch starting {batch[0]['path']} failed: {e}")
                continue
            spent += cost
            for r in batch:
                c = got.get(r["path"])
                if c and len(c.get("pos", [])) == 2 and c.get("neg"):
                    cases[r["path"]] = dict(name=r["name"], plugin=r["plugin"], pos=c["pos"], neg=c["neg"],
                                            origin="generated")
                else:
                    print(f"no usable case for {r['path']}")
    os.makedirs(CASES, exist_ok=True)
    with open(os.path.join(CASES, "trigger_cases.json"), "w") as f:
        json.dump(dict(sorted(cases.items())), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{len(todo)} drafted, {len(cases)} skills with cases, ${spent:.2f} spent")


if __name__ == "__main__":
    main()
