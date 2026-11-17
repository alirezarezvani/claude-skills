#!/usr/bin/env python3
"""Decide the next step of a staged (Android) or phased (iOS) rollout.

Compares the new release's crash and ANR numbers with the previous release
(the baseline) and with Google Play's "bad behavior" thresholds, and returns
PROCEED, HOLD or HALT for the current stage.

Input: a CSV with one row per release, the baseline first or marked
release=baseline. Columns (counts, not percentages, so the test is honest):

  release, platform (android|ios), rollout_pct, users,
  crashed_users, anr_users (android, optional), worst_device_crash_pct (optional)

Decision, in order
  HALT     Android user-perceived crash rate >= 1.09% or ANR rate >= 0.47%
           (Play bad-behavior thresholds), or a single phone model >= 8%
  HALT     crash (or ANR) rate is worse than baseline by more than
           --max-regression (relative) AND the difference is significant
           (one-sided two-proportion z-test, p < --alpha)
  HOLD     fewer than --min-users users on the release: not enough data
  HOLD     worse than baseline by more than --max-regression, not yet
           significant: wait for more users before widening
  PROCEED  otherwise: next percentage of the ladder

Ladders: iOS phased release is fixed by Apple at 1, 2, 5, 10, 20, 50, 100%
over seven days and can only be paused (up to 30 days) or released to all;
users can still download the version manually while paused. Android staged
rollout percentages are yours to set; the default ladder here is
1, 5, 10, 20, 50, 100 (change with --ladder).

Exit codes: 0 PROCEED, 2 HOLD, 3 bad input, 4 HALT.
Thresholds verified 2026-11-17. Deterministic, stdlib only, no network.
"""
import argparse
import csv
import io
import json
import math
import sys

RULES_VERIFIED = "2026-11-17"
EXIT = {"PROCEED": 0, "HOLD": 2, "BAD_INPUT": 3, "HALT": 4}
PLAY_CRASH, PLAY_ANR, PLAY_DEVICE = 1.09, 0.47, 8.0
IOS_LADDER = [1, 2, 5, 10, 20, 50, 100]
ANDROID_LADDER = [1, 5, 10, 20, 50, 100]

SAMPLE = """release,platform,rollout_pct,users,crashed_users,anr_users,worst_device_crash_pct
baseline 4.11.0,android,100,412000,1480,1050,2.1
4.12.0,android,5,21800,131,49,3.4
"""


def z_one_sided(x1, n1, x0, n0):
    """p-value that rate1 > rate0 (pooled two-proportion z-test)."""
    if n1 == 0 or n0 == 0:
        return 1.0
    p1, p0 = x1 / n1, x0 / n0
    p = (x1 + x0) / (n1 + n0)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n0))
    if se == 0:
        return 0.0 if p1 > p0 else 1.0
    z = (p1 - p0) / se
    return 0.5 * math.erfc(z / math.sqrt(2))


def to_int(row, key, required=True):
    v = (row.get(key) or "").strip()
    if not v:
        if required:
            raise ValueError(f"missing {key} in row {row.get('release')}")
        return None
    try:
        n = int(float(v))
    except ValueError:
        raise ValueError(f"{key}='{v}' is not a number in row {row.get('release')}")
    if n < 0:
        raise ValueError(f"{key} is negative in row {row.get('release')}")
    return n


def parse(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if len(rows) < 2:
        raise ValueError("need a baseline row and the new release row")
    base = next((r for r in rows if (r.get("release") or "").lower().startswith("baseline")), rows[0])
    new = rows[-1] if rows[-1] is not base else rows[-2]
    out = []
    for r in (base, new):
        d = {
            "release": r.get("release", "").strip(),
            "platform": (r.get("platform") or "").strip().lower(),
            "rollout_pct": float(r.get("rollout_pct") or 0),
            "users": to_int(r, "users"),
            "crashed_users": to_int(r, "crashed_users"),
            "anr_users": to_int(r, "anr_users", False),
            "worst_device_crash_pct": float(r["worst_device_crash_pct"]) if (r.get("worst_device_crash_pct") or "").strip() else None,
        }
        if d["platform"] not in ("android", "ios"):
            raise ValueError(f"platform must be android or ios in row {d['release']}")
        if d["users"] == 0:
            raise ValueError(f"users is 0 in row {d['release']}")
        if d["crashed_users"] > d["users"] or (d["anr_users"] or 0) > d["users"]:
            raise ValueError(f"more affected users than users in row {d['release']}")
        out.append(d)
    return out


def next_step(pct, ladder):
    for step in ladder:
        if step > pct + 1e-9:
            return step
    return None


def decide(base, new, min_users, max_reg, alpha, ladder):
    reasons, verdict = [], "PROCEED"
    rate = lambda x, n: 100.0 * x / n
    metrics = {}
    for name, key in (("crash", "crashed_users"), ("anr", "anr_users")):
        if new[key] is None or base[key] is None:
            continue
        r1, r0 = rate(new[key], new["users"]), rate(base[key], base["users"])
        p = z_one_sided(new[key], new["users"], base[key], base["users"])
        rel = (r1 - r0) / r0 if r0 > 0 else (math.inf if r1 > 0 else 0.0)
        metrics[name] = {"release_pct": round(r1, 3), "baseline_pct": round(r0, 3),
                         "relative_change": None if math.isinf(rel) else round(rel, 3), "p_worse": round(p, 4)}

    def escalate(v, why):
        nonlocal verdict
        order = {"PROCEED": 0, "HOLD": 1, "HALT": 2}
        if order[v] > order[verdict]:
            verdict = v
        reasons.append(f"{v}: {why}")

    if new["platform"] == "android":
        c = metrics.get("crash", {}).get("release_pct")
        a = metrics.get("anr", {}).get("release_pct")
        if c is not None and c >= PLAY_CRASH:
            escalate("HALT", f"user-perceived crash rate {c}% >= Play bad-behavior threshold {PLAY_CRASH}%")
        if a is not None and a >= PLAY_ANR:
            escalate("HALT", f"user-perceived ANR rate {a}% >= Play bad-behavior threshold {PLAY_ANR}%")
        if new["worst_device_crash_pct"] is not None and new["worst_device_crash_pct"] >= PLAY_DEVICE:
            escalate("HALT", f"a phone model at {new['worst_device_crash_pct']}% crash rate >= Play per-device threshold {PLAY_DEVICE}%")
    for name, m in metrics.items():
        rel = m["relative_change"]
        worse = rel is None or rel > max_reg
        if worse and m["p_worse"] < alpha:
            escalate("HALT", f"{name} rate {m['release_pct']}% vs baseline {m['baseline_pct']}% is a significant regression (p={m['p_worse']})")
        elif worse:
            escalate("HOLD", f"{name} rate {m['release_pct']}% vs baseline {m['baseline_pct']}% is worse by more than {int(max_reg * 100)}% but not yet significant (p={m['p_worse']}); wait for more users")
    if new["users"] < min_users:
        escalate("HOLD", f"only {new['users']} users on the release (< {min_users}); not enough data to widen")
    if not metrics:
        escalate("HOLD", "no comparable crash counts")

    step = next_step(new["rollout_pct"], ladder)
    if verdict == "PROCEED":
        action = f"widen to {step}%" if step else "rollout complete"
        if new["platform"] == "ios":
            action = "let the phased release continue" + (f" (next automatic step {step}%)" if step else "")
    elif verdict == "HOLD":
        action = ("pause the phased release (up to 30 days) or leave it on schedule only if the trend is improving"
                  if new["platform"] == "ios" else f"stay at {new['rollout_pct']:g}% and re-run after more users")
    else:
        action = ("pause the phased release and ship a fix; paused versions can still be downloaded manually, so consider removing the build from sale if the crash is severe"
                  if new["platform"] == "ios" else "halt the staged rollout in Play Console, fix, and ship a new version code")
    return {"verdict": verdict, "action": action, "reasons": reasons or ["no threshold or regression triggered"],
            "metrics": metrics, "release": new["release"], "baseline": base["release"],
            "rollout_pct": new["rollout_pct"], "next_step_pct": step, "rules_verified": RULES_VERIFIED}


def render(res):
    out = [f"Rollout gate: {res['verdict']} for {res['release']} at {res['rollout_pct']:g}% (baseline {res['baseline']})",
           f"Action: {res['action']}", ""]
    for name, m in res["metrics"].items():
        rel = "n/a" if m["relative_change"] is None else f"{m['relative_change'] * 100:+.0f}%"
        out.append(f"  {name:5s} {m['release_pct']:.3f}% vs {m['baseline_pct']:.3f}%  ({rel}, p_worse={m['p_worse']})")
    out.append("")
    out += [f"- {r}" for r in res["reasons"]]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 PROCEED, 2 HOLD, 3 bad input, 4 HALT.")
    ap.add_argument("--input", help="CSV with a baseline row and the new release row")
    ap.add_argument("--min-users", type=int, default=1000, help="users needed on the release before widening (default 1000)")
    ap.add_argument("--max-regression", type=float, default=0.25, help="relative worsening tolerated vs baseline (default 0.25 = 25%%)")
    ap.add_argument("--alpha", type=float, default=0.05, help="significance level of the one-sided test (default 0.05)")
    ap.add_argument("--ladder", help="Android percentages, comma-separated (default 1,5,10,20,50,100)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in example")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            text = SAMPLE
        elif a.input:
            with open(a.input, encoding="utf-8") as fh:
                text = fh.read()
        else:
            raise ValueError("give --input FILE or --sample")
        base, new = parse(text)
        if not 0 < a.alpha < 1 or a.max_regression < 0 or a.min_users < 0:
            raise ValueError("--alpha must be in (0,1); --max-regression and --min-users must be >= 0")
        ladder = ANDROID_LADDER
        if new["platform"] == "ios":
            ladder = IOS_LADDER
        elif a.ladder:
            ladder = sorted(float(x) for x in a.ladder.split(","))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    res = decide(base, new, a.min_users, a.max_regression, a.alpha, ladder)
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
