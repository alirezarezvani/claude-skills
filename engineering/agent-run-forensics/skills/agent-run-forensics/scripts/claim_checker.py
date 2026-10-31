#!/usr/bin/env python3
"""Check what an agent says it did against what the recording shows it did.

A session summary is written from memory, and memory drops exactly the parts
that matter: the test run that failed, the file changed by a shell one-liner,
the edit made after the last green run. Turn each sentence of the summary into
a typed claim and this checks it, step by step, against the trace.

Claim forms (one per --claim, or one per line in --claims-file; # comments ok)
  ran:<text>          a tool call whose command or target contains <text>
  not-run:<text>      no such call
  passed:<text>       the LAST matching shell run exited 0, and no file was changed after it
  failed:<text>       the last matching shell run exited non-zero
  edited:<path>       the run wrote, moved or deleted <path>
  not-edited:<path>   it did not
  read:<path>         the run read <path> before any write to it

Verdicts
  SUPPORTED            the recording shows it
  SUPPORTED_INFERRED   only an inferred effect shows it (shell text such as sed -i)
  STALE                passed: it passed, but files changed after that run
  PARTIAL              passed: exit 0 belongs to a compound line (a|b, a; b, a || b)
                       whose last command is not the one claimed
  CONTRADICTED         the recording shows the opposite
  CONTRADICTED_INFERRED  only an inferred effect contradicts it
  NOT_IN_TRACE         the trace holds no evidence either way
  UNVERIFIABLE         the matching call has no recorded result or exit code

Exit codes
  0  every claim SUPPORTED
  2  something is weaker than supported (inferred, stale, partial, absent): say so
  3  bad input (no session, malformed claim)
  4  at least one claim CONTRADICTED or CONTRADICTED_INFERRED: correct the account first

Examples
  claim_checker.py --latest --claim "passed:pytest" --claim "not-edited:config.yaml"
  claim_checker.py --session abc123 --claims-file claims.txt --output json
  claim_checker.py --sample
"""
import argparse
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trace_core as core  # noqa: E402

EXIT = {"SUPPORTED": 0, "WEAK": 2, "BAD_INPUT": 3, "CONTRADICTED": 4}
KINDS = ("ran", "not-run", "passed", "failed", "edited", "not-edited", "read")
WRITE_KINDS = ("write", "delete", "move")
STRONG = {"SUPPORTED"}
BAD = {"CONTRADICTED", "CONTRADICTED_INFERRED"}
SAMPLE_CLAIMS = ["passed:pytest", "edited:src/client.py", "not-edited:config.yaml", "ran:ruff"]


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__.split("\n\n", 1)[1])
    core.add_source_args(p)
    p.add_argument("--claim", action="append", default=[], metavar="KIND:ARG", help="a typed claim (repeatable)")
    p.add_argument("--claims-file", metavar="FILE", help="one typed claim per line")
    p.add_argument("--output", choices=("text", "json"), default="text")
    p.add_argument("--sample", action="store_true", help="check sample claims against a built-in fictional session")
    return p


def parse_claims(args):
    raw = list(args.claim)
    if args.claims_file:
        with open(args.claims_file, encoding="utf-8") as fh:
            raw += [ln.strip() for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    claims = []
    for r in raw:
        kind, sep, arg = r.partition(":")
        kind = kind.strip().lower()
        if not sep or kind not in KINDS or not arg.strip():
            raise ValueError(f"malformed claim {r!r}: use one of {', '.join(k + ':<arg>' for k in KINDS)}")
        claims.append((kind, arg.strip()))
    if not claims:
        raise ValueError("no claims given (--claim KIND:ARG or --claims-file)")
    return claims


def is_compound_tail_mismatch(command, needle):
    """True when `needle` is not in the last command of a compound shell line."""
    segs = [s.strip() for s in core.re.split(r"\|\||&&|;|\|(?!\|)", core.strip_heredocs(command)) if s.strip()]
    if len(segs) <= 1:
        return False
    tail = segs[-1]
    joined_by_and = "&&" in command and not any(op in command for op in ("||", ";", "|"))
    if joined_by_and:
        return False            # a && b exits 0 only if both did
    return needle.lower() not in tail.lower()


def ev(step, note=""):
    return {"step": step.n, "tool": step.tool, "target": step.target[:140],
            "status": step.status, "exit_code": step.exit_code, "note": note}


def check(sess, kind, arg):
    tools = sess.tool_steps
    needle = arg.lower()
    if kind in ("ran", "not-run"):
        hits = [s for s in tools if needle in s.target.lower()]
        if kind == "ran":
            return ("SUPPORTED", [ev(s) for s in hits[:3]]) if hits else ("NOT_IN_TRACE", [])
        return ("CONTRADICTED", [ev(s, "it did run") for s in hits[:3]]) if hits else ("SUPPORTED", [])

    if kind in ("passed", "failed"):
        runs = [s for s in tools if needle in s.target.lower()]
        if not runs:
            return "NOT_IN_TRACE", []
        last = runs[-1]
        if last.status == "no-result" or (last.exit_code is None and last.status != "error"):
            return "UNVERIFIABLE", [ev(last, "no recorded exit status")]
        ok = last.exit_code == 0 if last.exit_code is not None else last.status == "ok"
        evidence = [ev(s) for s in runs[-3:]]
        if kind == "failed":
            return ("SUPPORTED" if not ok else "CONTRADICTED"), evidence
        if not ok:
            return "CONTRADICTED", evidence + [{"note": f"last run (step {last.n}) did not pass"}]
        if is_compound_tail_mismatch(last.target, arg):
            return "PARTIAL", evidence + [{"note": "exit 0 is the last command's in a compound line, not necessarily this one's"}]
        later = [(s, e) for s in tools if s.n > last.n for e in s.effects
                 if e.kind in WRITE_KINDS and "not applied" not in e.rule]
        if later:
            files = sorted({e.path for _, e in later})
            return "STALE", evidence + [{"note": f"changed after the passing run: {', '.join(files[:5])}",
                                         "steps": sorted({s.n for s, _ in later})}]
        return "SUPPORTED", evidence

    effects = [(s, e) for s in tools for e in s.effects if core.path_matches(e.path, arg, sess.cwd)]
    writes = [(s, e) for s, e in effects if e.kind in WRITE_KINDS and "not applied" not in e.rule]
    if kind in ("edited", "not-edited"):
        rec = [x for x in writes if x[1].basis == "recorded"]
        inf = [x for x in writes if x[1].basis == "inferred"]
        evidence = [ev(s, f"{e.kind} [{e.basis}: {e.rule}]") for s, e in (rec + inf)[:4]]
        if kind == "edited":
            if rec:
                return "SUPPORTED", evidence
            return ("SUPPORTED_INFERRED", evidence) if inf else ("NOT_IN_TRACE", [])
        if rec:
            return "CONTRADICTED", evidence
        return ("CONTRADICTED_INFERRED", evidence) if inf else ("SUPPORTED", [])

    if kind == "read":
        reads = [(s, e) for s, e in effects if e.kind == "read"]
        if not reads:
            return "NOT_IN_TRACE", []
        first_read = reads[0][0].n
        first_write = writes[0][0].n if writes else None
        if first_write is not None and first_write < first_read:
            return "PARTIAL", [ev(reads[0][0], "read"), ev(writes[0][0], "but written before it was read")]
        s, e = reads[0]
        return ("SUPPORTED" if e.basis == "recorded" else "SUPPORTED_INFERRED"), [ev(s, f"read [{e.basis}: {e.rule}]")]
    raise ValueError(kind)


def run(args):
    try:
        claims = parse_claims(args)
        sess = core.resolve_session(args)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"claim_checker: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    results = []
    for kind, arg in claims:
        verdict, evidence = check(sess, kind, arg)
        results.append({"claim": f"{kind}:{arg}", "verdict": verdict, "evidence": evidence})
    verdicts = {r["verdict"] for r in results}
    if verdicts & BAD:
        overall = "CONTRADICTED"
    elif verdicts <= STRONG:
        overall = "SUPPORTED"
    else:
        overall = "WEAK"
    if args.output == "json":
        print(json.dumps({"verdict": overall, "session": sess.summary(), "claims": results}, indent=2))
    else:
        counts = {}
        for r in results:
            counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
        print(f"Claim check: {overall}  ({', '.join(f'{v} {k}' for k, v in sorted(counts.items()))})")
        print(f"  run {sess.id} [{sess.harness}]  {sess.path}")
        for r in results:
            print(f"\n  {r['verdict']:<22} {r['claim']}")
            for e in r["evidence"]:
                if "step" in e:
                    code = f" exit {e['exit_code']}" if e.get("exit_code") is not None else ""
                    print(f"      step {e['step']} {e['tool']}: {e['target'][:90]} [{e['status']}{code}] {e.get('note', '')}")
                else:
                    print(f"      {e['note']}")
        if overall == "CONTRADICTED":
            print("\n  The account contradicts the recording. Correct it, citing the steps, before anything else.")
        elif overall == "WEAK":
            print("\n  Not every claim is backed by a recorded step. Say which are inferred, stale or absent.")
    return EXIT[overall]


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample:
        with tempfile.TemporaryDirectory() as d:
            args.trace = core.write_sample(d)
            if not args.claim and not args.claims_file:
                args.claim = list(SAMPLE_CLAIMS)
            return run(args)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
