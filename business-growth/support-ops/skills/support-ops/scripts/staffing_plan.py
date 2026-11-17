#!/usr/bin/env python3
"""How many support agents each interval needs, for live and async channels.

Live channels (phone, chat): Erlang C. Given arrivals per hour, average handle
time (AHT) and a service-level goal (e.g. 80% answered within 60 s), finds the
smallest number of agents on line that meets the goal without pushing
occupancy above --max-occupancy, then grosses it up for shrinkage (breaks,
training, meetings, absence) to the number to schedule.

Async channels (email, web form): workload. Agents = arrivals x AHT / 3600,
plus enough extra to drain any --backlog within --drain-hours, grossed up for
shrinkage. Erlang C does not apply: an email does not abandon after 60 s.

Chat agents handling several sessions at once: pass --concurrency; AHT is then
divided by it, which is an approximation (concurrent chats are slower each).

Input: --arrivals and --aht for one interval, or --intervals CSV with columns
interval, arrivals (per hour) [, aht_s]. Optional column staffed compares the
plan with the roster.

Exit codes: 0 plan meets the goal (and the roster, if given), 2 roster short in
at least one interval, 3 bad input. Deterministic, stdlib only, no network.
"""
import argparse
import csv
import json
import math
import sys

EXIT = {"OK": 0, "SHORT": 2, "BAD_INPUT": 3}
SAMPLE = [  # interval, chats per hour, staffed
    ("08:00", 40, 6), ("09:00", 95, 11), ("10:00", 130, 14), ("11:00", 140, 14),
    ("12:00", 110, 10), ("13:00", 120, 12), ("14:00", 105, 12), ("15:00", 80, 9), ("16:00", 50, 7),
]


def erlang_c(agents, load):
    """Probability an arrival waits (Erlang C), computed via Erlang B for stability."""
    if agents <= load:
        return 1.0
    b = 1.0
    for k in range(1, agents + 1):
        b = load * b / (k + load * b)
    return agents * b / (agents - load * (1 - b))


def service_level(agents, load, aht_s, t_s):
    if agents <= load:
        return 0.0
    pw = erlang_c(agents, load)
    return 1 - pw * math.exp(-(agents - load) * t_s / aht_s)


def asa(agents, load, aht_s):
    if agents <= load:
        return math.inf
    return erlang_c(agents, load) * aht_s / (agents - load)


def live_agents(arrivals_h, aht_s, sl, t_s, max_occ):
    load = arrivals_h * aht_s / 3600.0
    if load == 0:
        return 0, load
    n = max(1, math.ceil(load))
    while True:
        if service_level(n, load, aht_s, t_s) >= sl and load / n <= max_occ:
            return n, load
        n += 1
        if n > 100000:
            raise ValueError("no feasible staffing; check inputs")


def plan(rows, mode, sl, t_s, shrink, max_occ, conc, backlog, drain_h, default_aht):
    out = []
    short = False
    per_drain = (backlog * default_aht / 3600.0) / drain_h if backlog else 0.0
    for r in rows:
        aht = r.get("aht_s") or default_aht
        eff_aht = aht / conc
        if mode == "live":
            n, load = live_agents(r["arrivals"], eff_aht, sl, t_s, max_occ)
            got_sl = service_level(n, load, eff_aht, t_s) if n else 1.0
            wait = asa(n, load, eff_aht) if n else 0.0
            item = {"interval": r["interval"], "arrivals_per_h": r["arrivals"], "erlangs": round(load, 2),
                    "on_line": n, "service_level": round(got_sl, 3), "asa_s": round(wait, 1),
                    "occupancy": round(load / n, 3) if n else 0.0}
        else:
            work = r["arrivals"] * eff_aht / 3600.0 + per_drain
            n = math.ceil(work / max_occ) if work else 0
            item = {"interval": r["interval"], "arrivals_per_h": r["arrivals"], "work_hours_per_h": round(work, 2),
                    "on_line": n, "occupancy": round(work / n, 3) if n else 0.0}
        item["scheduled"] = math.ceil(n / (1 - shrink)) if n else 0
        if r.get("staffed") is not None:
            item["staffed"] = r["staffed"]
            item["gap"] = r["staffed"] - item["scheduled"]
            if item["gap"] < 0:
                short = True
        out.append(item)
    return out, short


def read_rows(path):
    with open(path, encoding="utf-8-sig") as fh:
        rdr = csv.DictReader(fh)
        if not rdr.fieldnames or not {"interval", "arrivals"} <= set(rdr.fieldnames):
            raise ValueError("--intervals CSV needs columns interval, arrivals [, aht_s, staffed]")
        rows = []
        for i, r in enumerate(rdr, 2):
            try:
                row = {"interval": r["interval"], "arrivals": float(r["arrivals"])}
                if (r.get("aht_s") or "").strip():
                    row["aht_s"] = float(r["aht_s"])
                if (r.get("staffed") or "").strip():
                    row["staffed"] = int(float(r["staffed"]))
            except ValueError:
                raise ValueError(f"row {i}: non-numeric value")
            if row["arrivals"] < 0 or row.get("aht_s", 1) <= 0:
                raise ValueError(f"row {i}: arrivals must be >= 0 and aht_s > 0")
            rows.append(row)
    if not rows:
        raise ValueError("no intervals")
    return rows


def render(res):
    a = res["assumptions"]
    head = (f"Staffing plan ({res['mode']}): {res['verdict']}  - goal {a['service_level']:.0%} in {a['target_s']:g}s, "
            if res["mode"] == "live" else f"Staffing plan ({res['mode']}): {res['verdict']}  - ")
    out = [head + f"AHT {a['aht_s']:g}s, shrinkage {a['shrinkage']:.0%}, max occupancy {a['max_occupancy']:.0%}"
           + (f", concurrency {a['concurrency']:g}" if a["concurrency"] != 1 else ""), ""]
    for i in res["intervals"]:
        extra = f"SL {i['service_level']:.0%} ASA {i['asa_s']:.0f}s" if res["mode"] == "live" else f"work {i['work_hours_per_h']}h/h"
        roster = f"  staffed {i['staffed']} ({i['gap']:+d})" if "staffed" in i else ""
        out.append(f"  {i['interval']:>8s}  {i['arrivals_per_h']:>6g}/h  on line {i['on_line']:>3d}  schedule {i['scheduled']:>3d}  occ {i['occupancy']:.0%}  {extra}{roster}")
    out.append("")
    out.append(f"Peak to schedule: {max(i['scheduled'] for i in res['intervals'])}; agent-hours to schedule: {sum(i['scheduled'] for i in res['intervals'])}")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 plan ok, 2 roster short, 3 bad input.")
    ap.add_argument("--mode", choices=["live", "async"], default="live", help="live = phone/chat (Erlang C), async = email/form (workload)")
    ap.add_argument("--arrivals", type=float, help="contacts per hour (single interval)")
    ap.add_argument("--intervals", help="CSV: interval, arrivals [, aht_s, staffed]")
    ap.add_argument("--aht", type=float, help="average handle time in seconds (talk/chat + wrap-up)")
    ap.add_argument("--service-level", type=float, default=0.8, help="share answered within --target-s (live; default 0.8)")
    ap.add_argument("--target-s", type=float, default=60, help="answer-time target in seconds (live; default 60)")
    ap.add_argument("--shrinkage", type=float, default=0.3, help="share of paid time not on queue (default 0.3)")
    ap.add_argument("--max-occupancy", type=float, default=0.85, help="cap on time busy while on line (default 0.85)")
    ap.add_argument("--concurrency", type=float, default=1.0, help="simultaneous chats per agent (default 1)")
    ap.add_argument("--backlog", type=int, default=0, help="async: tickets already waiting")
    ap.add_argument("--drain-hours", type=float, default=8, help="async: hours to clear --backlog (default 8)")
    ap.add_argument("--sample", action="store_true", help="run a built-in chat day with a roster")
    ap.add_argument("--output", "--format", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            rows = [{"interval": i, "arrivals": float(n), "staffed": s} for i, n, s in SAMPLE]
            aht, conc = a.aht or 420.0, a.concurrency if a.concurrency != 1 else 2.0
        else:
            if a.aht is None or a.aht <= 0:
                raise ValueError("--aht (seconds, > 0) is required")
            aht, conc = a.aht, a.concurrency
            if a.intervals:
                rows = read_rows(a.intervals)
            elif a.arrivals is not None and a.arrivals >= 0:
                rows = [{"interval": "interval", "arrivals": a.arrivals}]
            else:
                raise ValueError("give --arrivals N or --intervals FILE (or --sample)")
        if not 0 < a.service_level < 1 or a.target_s <= 0:
            raise ValueError("--service-level must be in (0,1) and --target-s > 0")
        if not 0 <= a.shrinkage < 1 or not 0 < a.max_occupancy <= 1 or conc < 1 or a.drain_hours <= 0:
            raise ValueError("--shrinkage in [0,1), --max-occupancy in (0,1], --concurrency >= 1, --drain-hours > 0")
        intervals, short = plan(rows, a.mode, a.service_level, a.target_s, a.shrinkage, a.max_occupancy, conc, a.backlog, a.drain_hours, aht)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    res = {"verdict": "SHORT" if short else "OK", "mode": a.mode,
           "assumptions": {"aht_s": aht, "service_level": a.service_level, "target_s": a.target_s, "shrinkage": a.shrinkage,
                           "max_occupancy": a.max_occupancy, "concurrency": conc},
           "intervals": intervals}
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
