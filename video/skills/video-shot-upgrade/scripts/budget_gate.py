#!/usr/bin/env python3
"""budget_gate.py — the spend gate between a quote and a generated shot.

A ledger (spend.v1 JSON) walks every upgrade through four states and refuses
each step that would spend credits the user did not agree to:

  quote    every request has a provider price; the total fits the cap (the
           lower of the brief's budget_credits and --cap) and the balance.
           Prints the exact sentence the user has to say yes to.
  approve  records the yes. The credits named must equal the quoted total,
           and quotes older than --max-age minutes must be refreshed first.
  reserve  run immediately before each generate call. Refused unless the
           batch is approved and the shot was never reserved before: a
           reserved shot with no known outcome may already be charged, so it
           is never sent again on its own (the timeout rule).
  record   the job id and later the outcome (completed / failed / unknown).
           Only a failed shot can be released for one new reserve, and only
           with --release-failed, which is the user's second yes.

Nothing here calls a provider. The agent calls the MCP; this file is the
memory of what was quoted, approved and sent, so a resumed session cannot
pay twice.

Exit codes: 0 ok, 2 bad input, 3 missing quotes or ledger, 4 refused.

Examples:
  budget_gate.py --sample
  budget_gate.py quote --requests film/requests.json --quotes film/quotes.json \\
      --brief film/brief.json --cap 30 --balance 120 --ledger film/spend.json
  budget_gate.py approve --ledger film/spend.json --credits 20
  budget_gate.py reserve --ledger film/spend.json --shot s2
  budget_gate.py record  --ledger film/spend.json --shot s2 --job-id 1b2c... --status submitted
  budget_gate.py status  --ledger film/spend.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

COMMITTED = {"reserved", "submitted", "completed", "unknown"}


class GateError(Exception):
    def __init__(self, msg: str, code: int = 4):
        super().__init__(msg)
        self.code = code


def now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def load(path: Path) -> dict:
    if not path.exists():
        raise GateError(f"no ledger at {path}; run the quote step first", 3)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "spend.v1":
        raise GateError(f"{path} is not a spend.v1 ledger", 2)
    return data


def save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".spend-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
    os.replace(tmp, path)


def log(ledger: dict, event: str, **kw) -> None:
    ledger.setdefault("events", []).append({"at": now().isoformat(), "event": event, **kw})


def committed(ledger: dict) -> float:
    return round(sum(s["credits"] for s in ledger["shots"].values() if s["state"] in COMMITTED), 3)


def cmd_quote(args) -> dict:
    req = json.loads(Path(args.requests).read_text(encoding="utf-8"))
    quotes = json.loads(Path(args.quotes).read_text(encoding="utf-8"))
    brief = json.loads(Path(args.brief).read_text(encoding="utf-8")) if args.brief else {}
    if req.get("schema") != "requests.v1":
        raise GateError("--requests must be a requests.v1 file from provider_adapter.py", 2)
    if brief and not brief.get("upgrade_allowed", False):
        raise GateError("the brief says upgrade_allowed: false; ask the user before any generation")
    ids = [r["id"] for r in req["requests"]]
    if args.only:
        wanted = [i.strip() for i in args.only.split(",") if i.strip()]
        unknown = set(wanted) - set(ids)
        if unknown:
            raise GateError(f"--only names unknown shots: {sorted(unknown)}", 2)
        ids = [i for i in ids if i in wanted]
    missing = [i for i in ids if i not in quotes or not isinstance(quotes[i], dict) or quotes[i].get("credits") is None]
    if missing:
        raise GateError(f"no price for {', '.join(missing)}; call the quote tool for each and add "
                        f"{{\"<id>\": {{\"credits\": n, \"quote_ref\": \"...\"}}}} to the quotes file", 3)
    caps = [c for c in (brief.get("budget_credits"), args.cap) if c is not None]
    if not caps:
        raise GateError("no cap: set budget_credits in the brief or pass --cap", 3)
    cap = float(min(caps))
    shots, total = {}, 0.0
    for r in req["requests"]:
        if r["id"] not in ids:
            continue
        q = quotes[r["id"]]
        credits = float(q["credits"])
        if credits < 0:
            raise GateError(f"{r['id']}: negative price", 2)
        total += credits
        shots[r["id"]] = {"credits": credits, "quote_ref": q.get("quote_ref"), "state": "quoted",
                          "generated_duration": r["generated_duration"], "job_id": None, "plate": None}
    total = round(total, 3)
    if args.max_shots and len(shots) > args.max_shots:
        raise GateError(f"{len(shots)} shots quoted but --max-shots is {args.max_shots}; pass --only to pick them")
    if total > cap + 1e-9:
        drop, over = [], total - cap
        for sid, s in sorted(shots.items(), key=lambda kv: -kv[1]["credits"]):
            if over <= 1e-9:
                break
            drop.append(sid)
            over -= s["credits"]
        raise GateError(f"OVER BUDGET: {total:g} credits quoted, cap {cap:g}. Cheapest way under: drop "
                        f"{', '.join(drop)} (keep them as motion graphics), pick a cheaper model or lower resolution")
    if args.balance is not None and total > args.balance + 1e-9:
        raise GateError(f"balance {args.balance:g} credits is below the {total:g} quoted; the user must top up "
                        f"{total - args.balance:g} or drop shots")
    ledger = {
        "schema": "spend.v1", "title": req.get("title"), "provider": req.get("provider"), "model": req.get("model"),
        "cap": cap, "balance_at_quote": args.balance, "total_quoted": total, "quoted_at": now().isoformat(),
        "state": "quoted", "approved_credits": None, "approved_at": None, "shots": shots, "events": [],
        "approval_sentence": f"yes, spend {total:g} credits on {len(shots)} shot(s) "
                             f"({', '.join(shots)}) with {req.get('provider')} {req.get('model')}",
    }
    log(ledger, "quoted", total=total, cap=cap)
    save(Path(args.ledger), ledger)
    return ledger


def cmd_approve(args) -> dict:
    path = Path(args.ledger)
    ledger = load(path)
    if ledger["state"] != "quoted":
        raise GateError(f"ledger is {ledger['state']}, not quoted; quote again for a new batch")
    age = now() - datetime.fromisoformat(ledger["quoted_at"])
    if age > timedelta(minutes=args.max_age):
        raise GateError(f"quotes are {int(age.total_seconds() // 60)} min old (limit {args.max_age}); prices move, quote again")
    if abs(float(args.credits) - ledger["total_quoted"]) > 1e-9:
        raise GateError(f"the yes was for {args.credits:g} credits but {ledger['total_quoted']:g} were quoted; "
                        f"show the user the quoted total and ask again")
    ledger.update(state="approved", approved_credits=ledger["total_quoted"], approved_at=now().isoformat())
    log(ledger, "approved", credits=ledger["total_quoted"], said=args.said)
    save(path, ledger)
    return ledger


def cmd_reserve(args) -> dict:
    path = Path(args.ledger)
    ledger = load(path)
    shot = ledger["shots"].get(args.shot)
    if shot is None:
        raise GateError(f"{args.shot} is not in this batch", 2)
    if ledger["state"] != "approved":
        raise GateError(f"batch is {ledger['state']}: no generate call before the user's yes is recorded")
    if shot["state"] != "quoted":
        if shot["state"] == "unknown":
            raise GateError(f"{args.shot} was sent and its outcome is unknown; it may be charged. Poll the job "
                            f"({shot['job_id'] or 'no id recorded'}) instead of resubmitting")
        raise GateError(f"{args.shot} is already {shot['state']}; one quote buys one generate call")
    if committed(ledger) + shot["credits"] > ledger["approved_credits"] + 1e-9:
        raise GateError("this call would pass the approved total")
    shot["state"] = "reserved"
    log(ledger, "reserved", shot=args.shot, credits=shot["credits"])
    save(path, ledger)
    return ledger


def cmd_record(args) -> dict:
    path = Path(args.ledger)
    ledger = load(path)
    shot = ledger["shots"].get(args.shot)
    if shot is None:
        raise GateError(f"{args.shot} is not in this batch", 2)
    if args.release_failed:
        if shot["state"] != "failed":
            raise GateError(f"only a failed shot can be released; {args.shot} is {shot['state']}")
        shot.update(state="quoted", job_id=None)
        log(ledger, "released", shot=args.shot, note="user approved one more attempt")
        save(path, ledger)
        return ledger
    if shot["state"] == "quoted":
        raise GateError(f"{args.shot} was never reserved; run reserve before the generate call")
    allowed = {"reserved": {"submitted", "unknown", "failed"},
               "submitted": {"completed", "failed", "unknown"},
               "unknown": {"completed", "failed", "submitted"}}
    if args.status not in allowed.get(shot["state"], set()):
        raise GateError(f"{args.shot}: cannot go from {shot['state']} to {args.status}", 2)
    shot["state"] = args.status
    if args.job_id:
        shot["job_id"] = args.job_id
    if args.plate:
        shot["plate"] = args.plate
    if args.charged is not None:
        shot["charged"] = args.charged
    log(ledger, args.status, shot=args.shot, job_id=shot["job_id"])
    if all(s["state"] in ("completed", "failed") for s in ledger["shots"].values()):
        ledger["state"] = "closed"
    save(path, ledger)
    return ledger


def summary(ledger: dict) -> str:
    lines = [f"{ledger['provider']} / {ledger['model']}: {ledger['state']}, quoted {ledger['total_quoted']:g} "
             f"of cap {ledger['cap']:g}, committed {committed(ledger):g}"]
    for sid, s in ledger["shots"].items():
        lines.append(f"  {sid:>6}  {s['credits']:g} cr  {s['state']:<9} job={s['job_id'] or '-'}  plate={s['plate'] or '-'}")
    if ledger["state"] == "quoted":
        lines.append(f"ask the user, and wait for: \"{ledger['approval_sentence']}\"")
    return "\n".join(lines)


def run_sample() -> int:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "req.json").write_text(json.dumps({"schema": "requests.v1", "title": "sample", "provider": "higgsfield",
                                                "model": "magi_2", "requests": [
                                                    {"id": "s2", "generated_duration": 4}, {"id": "s4", "generated_duration": 4}]}))
        (d / "q.json").write_text(json.dumps({"s2": {"credits": 10, "quote_ref": "quote:a"}, "s4": {"credits": 10, "quote_ref": "quote:b"}}))
        (d / "brief.json").write_text(json.dumps({"upgrade_allowed": True, "budget_credits": 60}))
        base = dict(requests=str(d / "req.json"), quotes=str(d / "q.json"), brief=str(d / "brief.json"),
                    ledger=str(d / "spend.json"), only=None, max_shots=None)
        steps = [
            ("quote, cap 15 -> refused", cmd_quote, dict(base, cap=15, balance=None)),
            ("quote, cap 30, balance 0.5 -> refused", cmd_quote, dict(base, cap=30, balance=0.5)),
            ("quote, cap 30", cmd_quote, dict(base, cap=30, balance=100)),
            ("reserve before yes -> refused", cmd_reserve, dict(ledger=base["ledger"], shot="s2")),
            ("approve 25 (wrong total) -> refused", cmd_approve, dict(ledger=base["ledger"], credits=25, max_age=60, said=None)),
            ("approve 20", cmd_approve, dict(ledger=base["ledger"], credits=20, max_age=60, said="yes, spend 20")),
            ("reserve s2", cmd_reserve, dict(ledger=base["ledger"], shot="s2")),
            ("record s2 timeout -> unknown", cmd_record, dict(ledger=base["ledger"], shot="s2", status="unknown",
                                                             job_id=None, plate=None, charged=None, release_failed=False)),
            ("reserve s2 again -> refused", cmd_reserve, dict(ledger=base["ledger"], shot="s2")),
        ]
        for label, fn, kw in steps:
            try:
                fn(argparse.Namespace(**kw))
                print(f"ok       {label}")
            except GateError as exc:
                print(f"refused  {label}: {exc}")
        print(summary(load(Path(base["ledger"]))))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Spend gate for generated shots: quote, approve, reserve, record.")
    ap.add_argument("--sample", action="store_true", help="Walk the gate through a sample batch, refusals included.")
    sub = ap.add_subparsers(dest="cmd")
    q = sub.add_parser("quote", help="Check quotes against the cap and balance; write the ledger.")
    q.add_argument("--requests", required=True)
    q.add_argument("--quotes", required=True, help='JSON {"<shot id>": {"credits": n, "quote_ref": "..."}}')
    q.add_argument("--brief", help="brief.json (budget_credits, upgrade_allowed).")
    q.add_argument("--cap", type=float, help="Hard credit cap for this batch (the lower of this and budget_credits wins).")
    q.add_argument("--balance", type=float, help="The provider balance read just now.")
    q.add_argument("--only", help="Comma-separated shot ids to put in this batch.")
    q.add_argument("--max-shots", type=int, help="Refuse a batch with more shots than this (capped tests).")
    q.add_argument("--ledger", required=True)
    a = sub.add_parser("approve", help="Record the user's yes to the quoted total.")
    a.add_argument("--ledger", required=True)
    a.add_argument("--credits", type=float, required=True, help="The total the user said yes to.")
    a.add_argument("--said", help="The user's words, for the record.")
    a.add_argument("--max-age", type=int, default=60, help="Minutes a quote stays valid (default 60).")
    r = sub.add_parser("reserve", help="Run right before one generate call.")
    r.add_argument("--ledger", required=True)
    r.add_argument("--shot", required=True)
    rc = sub.add_parser("record", help="Record a job id or outcome.")
    rc.add_argument("--ledger", required=True)
    rc.add_argument("--shot", required=True)
    rc.add_argument("--status", choices=["submitted", "completed", "failed", "unknown"])
    rc.add_argument("--job-id")
    rc.add_argument("--plate", help="Path of the downloaded plate (completed).")
    rc.add_argument("--charged", type=float, help="Credits the provider actually charged, if it says.")
    rc.add_argument("--release-failed", action="store_true", help="Allow one new attempt for a failed shot (needs a new yes).")
    s = sub.add_parser("status", help="Print the ledger.")
    s.add_argument("--ledger", required=True)
    for p in (q, a, r, rc, s):
        p.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()
    if args.sample or not args.cmd:
        return run_sample()
    if args.cmd == "record" and not args.release_failed and not args.status:
        print("error: record needs --status or --release-failed", file=sys.stderr)
        return 2
    try:
        if args.cmd == "status":
            ledger = load(Path(args.ledger))
        else:
            ledger = {"quote": cmd_quote, "approve": cmd_approve, "reserve": cmd_reserve, "record": cmd_record}[args.cmd](args)
    except GateError as exc:
        print(("REFUSED " if exc.code == 4 else "error: ") + str(exc), file=sys.stderr)
        return exc.code
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(ledger, indent=2) if args.output == "json" else summary(ledger))
    return 0


if __name__ == "__main__":
    sys.exit(main())
