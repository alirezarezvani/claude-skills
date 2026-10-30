#!/usr/bin/env python3
"""Turn a run's results.json into a Markdown summary and fold it into the running scoreboard.

The scoreboard keeps the latest result per skill plus a short verdict history, so a nightly
rotation adds up to a library-wide picture and a skill that used to fire and now stays silent
shows up as a regression.

Usage:
  python3 scripts/evals/report.py eval-out/results.json                       # summary to stdout
  python3 scripts/evals/report.py eval-out/results.json --scoreboard board/   # also update board/
"""
import argparse
import json
import os

HISTORY = 10


def pct(a, b):
    return f"{a}/{b}" if b else "-"


def merge(board, res):
    trig, beh = board.setdefault("trigger", {}), board.setdefault("behaviour", {})
    regressions = []
    for s in res["trigger"]:
        if s["verdict"] in ("INCOMPLETE", "ERROR"):
            continue
        prev = trig.get(s["skill"], {})
        hist = (prev.get("history", []) + [[res["date"], s["verdict"]]])[-HISTORY:]
        if prev.get("verdict") == "FIRES" and s["verdict"] in ("SILENT", "PLUGIN_ONLY"):
            regressions.append(f"trigger: `{s['skill']}` was FIRES on {prev['date']}, now {s['verdict']}")
        if s["false_fire"] and not prev.get("false_fire"):
            regressions.append(f"trigger: `{s['skill']}` now fires on its near-miss prompt")
        trig[s["skill"]] = dict(date=res["date"], model=res["model"], scenario=res["scenario"], verdict=s["verdict"],
                                pos=pct(s["pos_exact"], s["pos_total"]), plugin_pos=pct(s["pos_plugin"], s["pos_total"]),
                                false_fire=s["false_fire"], history=hist)
    for s in res["behaviour"]:
        if s["verdict"] == "INCOMPLETE":
            continue
        prev = beh.get(s["case"], {})
        if "delta" in prev and s["delta"] < prev["delta"]:
            regressions.append(f"behaviour: `{s['case']}` lift fell from {prev['delta']:+d} to {s['delta']:+d}")
        beh[s["case"]] = dict(date=res["date"], model=res["model"], skill=s["skill"], verdict=s["verdict"],
                              with_=pct(s["with_passed"], s["total"]), without=pct(s["without_passed"], s["total"]),
                              delta=s["delta"], skill_fired=s["skill_fired"],
                              history=(prev.get("history", []) + [[res["date"], s["delta"]]])[-HISTORY:])
    board["updated"] = res["date"]
    return regressions


def run_summary(res, regressions):
    lines = [f"# Skill evals, {res['date']}", "",
             f"Model `{res['model']}`, scenario `{res['scenario']}`, {res['runs']} run(s) per trigger prompt, "
             f"{res['claude_version']}. Spent ${res['spent']:.2f} of ${res['budget']:.2f}"
             + (" (budget reached, some runs skipped)." if res["stopped_early"] else "."), ""]
    if regressions:
        lines += ["## Regressions", ""] + [f"- {r}" for r in regressions] + [""]
    if res["trigger"]:
        lines += ["## Trigger", "", "| Skill | Verdict | Fired (exact) | Fired (plugin) | Near miss fired | Cost |",
                  "|---|---|---|---|---|---|"]
        for s in res["trigger"]:
            lines.append(f"| `{s['skill']}` | {s['verdict']} | {pct(s['pos_exact'], s['pos_total'])} | "
                         f"{pct(s['pos_plugin'], s['pos_total'])} | {pct(s['neg_fires'], s['neg_total'])} | ${s['cost']:.2f} |")
        lines.append("")
    if res["behaviour"]:
        lines += ["## Behaviour (with skill vs without)", "",
                  "| Case | Verdict | With | Without | Skill fired | Cost |", "|---|---|---|---|---|---|"]
        for s in res["behaviour"]:
            lines.append(f"| `{s['case']}` | {s['verdict']} | {pct(s['with_passed'] or 0, s['total'])} | "
                         f"{pct(s['without_passed'] or 0, s['total'])} | {'yes' if s['skill_fired'] else 'no'} | ${s['cost']:.2f} |")
        lines.append("")
    return "\n".join(lines)


def board_summary(board):
    trig, beh = board.get("trigger", {}), board.get("behaviour", {})
    counts = {}
    for v in trig.values():
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    lines = [f"# Skill eval scoreboard (updated {board.get('updated')})", "",
             "Latest result per skill from the nightly rotation. Verdicts: FIRES (exact skill fired on at least "
             "75% of realistic prompts), FLAKY (some), PLUGIN_ONLY (a sibling skill or command from the same plugin "
             "fired), SILENT (nothing fired). Behaviour LIFTS means the answer with the skill passed more "
             "assertions than without it.", "",
             "Trigger: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + f" ({len(trig)} skills evaluated)",
             "", "## Behaviour", "", "| Case | Verdict | With | Without | Date |", "|---|---|---|---|---|"]
    for k, v in sorted(beh.items()):
        lines.append(f"| `{k}` | {v['verdict']} | {v['with_']} | {v['without']} | {v['date']} |")
    lines += ["", "## Trigger", "", "| Skill | Verdict | Fired | Near miss fired | Date | History |", "|---|---|---|---|---|---|"]
    order = {"SILENT": 0, "PLUGIN_ONLY": 1, "FLAKY": 2, "FIRES": 3}
    for k, v in sorted(trig.items(), key=lambda kv: (order.get(kv[1]["verdict"], 9), kv[0])):
        hist = " ".join(h[1][0] for h in v["history"])
        lines.append(f"| `{k}` | {v['verdict']} | {v['pos']} | {'yes' if v['false_fire'] else 'no'} | {v['date']} | {hist} |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", help="results.json written by run_evals.py")
    ap.add_argument("--scoreboard", help="folder holding scoreboard.json and SCOREBOARD.md to update")
    args = ap.parse_args()
    res = json.load(open(args.results))
    board, regressions = {}, []
    if args.scoreboard:
        path = os.path.join(args.scoreboard, "scoreboard.json")
        if os.path.exists(path):
            board = json.load(open(path))
        regressions = merge(board, res)
        os.makedirs(args.scoreboard, exist_ok=True)
        with open(path, "w") as f:
            json.dump(board, f, indent=1, sort_keys=True)
        with open(os.path.join(args.scoreboard, "SCOREBOARD.md"), "w") as f:
            f.write(board_summary(board))
    print(run_summary(res, regressions))


if __name__ == "__main__":
    main()
