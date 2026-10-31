#!/usr/bin/env python3
"""Read one recorded agent run as numbered steps, and walk back from any step to why it happened.

Answers "what did the agent do", "what changed config.yaml" and "why did it
run that" from the recording rather than from anyone's memory of it. Each
step shows the tool, its target, how it ended (exit code, error) and where
that came from. Secrets are redacted in all output.

Views
  (default)        every step: prompts, the agent's words, tool calls with outcome
  --files          every file the run wrote, deleted, moved or read, by step, and
                   whether the agent ever named it in its own text (SILENT if not)
  --why STEP       the causal chain behind one step, each edge labelled:
                     recorded  the harness wrote it down (the call, its result,
                               the agent's words in the same message, ordering)
                     inferred  derived now by a named rule (prior-write, read-before-
                               write, retry-after-failure, target-seen-in-output)
                   Report the two separately. An inferred edge is a lead, not a fact.

Filters (default view): --file PATH, --grep TEXT, --errors, --tools, --around STEP

Exit codes
  0  printed
  2  the filter matched nothing in this run (the answer is not in this trace)
  3  bad input (no such session or step)

Examples
  trace_timeline.py --latest --errors
  trace_timeline.py --trace ~/.claude/projects/-work-shop/abc.jsonl --files
  trace_timeline.py --session abc123 --why 9
  trace_timeline.py --sample --why 9
"""
import argparse
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trace_core as core  # noqa: E402

EXIT = {"OK": 0, "NO_MATCH": 2, "BAD_INPUT": 3}
WRITE_KINDS = ("write", "delete", "move")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__.split("\n\n", 1)[1])
    core.add_source_args(p)
    v = p.add_argument_group("view")
    v.add_argument("--files", action="store_true", help="file-effects table with SILENT flags")
    v.add_argument("--why", type=int, metavar="STEP", help="causal chain behind this step")
    v.add_argument("--file", metavar="PATH", help="only steps that touch this path (suffix match)")
    v.add_argument("--grep", metavar="TEXT", help="only steps whose text or target contains TEXT")
    v.add_argument("--errors", action="store_true", help="only failed tool calls")
    v.add_argument("--tools", action="store_true", help="only tool calls (hide prose)")
    v.add_argument("--around", type=int, metavar="STEP", help="only steps within --context of STEP")
    v.add_argument("--context", type=int, default=4, help="steps either side for --around (default 4)")
    p.add_argument("--output", choices=("text", "json"), default="text")
    p.add_argument("--sample", action="store_true", help="run against a built-in fictional session")
    return p


def outcome(s):
    if s.role != "tool":
        return ""
    if s.status == "no-result":
        return "NO RESULT (interrupted or still running)"
    if s.exit_code is not None:
        warn = "  BUT OUTPUT REPORTS FAILURE (exit is the last command's)" if s.output_fail and s.exit_code == 0 else ""
        return f"exit {s.exit_code} [{s.exit_basis}]{warn}"
    return "ERROR [recorded]" if s.status == "error" else "ok [recorded]"


def touches(s, path, cwd):
    return any(core.path_matches(e.path, path, cwd) for e in s.effects) or (
        s.role == "tool" and path.lstrip("./") in s.target)


def mentioned(path, texts):
    base = os.path.basename(path)
    return any(path in t or (base and base in t) for t in texts)


# --------------------------------------------------------------------------- views

def file_table(sess):
    """SILENT = changed, and the agent never named the file in its own text after the change."""
    said = [(s.n, s.text) for s in sess.steps if s.role == "assistant"]
    rows = {}
    for s in sess.tool_steps:
        for e in s.effects:
            r = rows.setdefault(e.path, {"path": e.path, "events": []})
            r["events"].append({"step": s.n, "kind": e.kind, "basis": e.basis, "rule": e.rule,
                                "tool": s.tool, "status": s.status})
    out = []
    for r in rows.values():
        wrote = [ev["step"] for ev in r["events"] if ev["kind"] in WRITE_KINDS]
        after = [t for n, t in said if wrote and n > wrote[0]]
        r["named_by_agent_after_change"] = bool(wrote) and mentioned(r["path"], after)
        r["silent"] = bool(wrote) and not r["named_by_agent_after_change"]
        out.append(r)
    out.sort(key=lambda r: (not r["silent"], r["events"][0]["step"]))
    return out


def why(sess, n):
    steps = {s.n: s for s in sess.steps}
    target = steps.get(n)
    if target is None:
        return None
    edges = []
    prior = [s for s in sess.steps if s.n < n]
    tools_before = [s for s in prior if s.role == "tool"]
    # recorded: the call and its result
    if target.role == "tool":
        edges.append({"basis": "recorded", "edge": "call->result",
                      "detail": f"{target.tool} {target.target[:120]} -> {outcome(target)}"})
        if target.stated:
            edges.append({"basis": "recorded", "edge": "stated-reason",
                          "detail": f"agent wrote in the same message: \"{target.stated[-300:].strip()}\"",
                          "note": "the agent's claim at the time, not proof of the cause"})
    last_user = next((s for s in reversed(prior) if s.role == "user" and not s.text.lstrip().startswith("<")), None)
    if last_user:
        edges.append({"basis": "recorded", "edge": "after-prompt", "step": last_user.n,
                      "detail": f"last user message before it: \"{last_user.text[:200]}\"",
                      "note": "ordering is recorded; that the prompt caused the step is not"})
    if target.role == "tool":
        tgt_paths = [e.path for e in target.effects]
        # inferred: what this step overwrote, and what the agent had read of it
        for p in tgt_paths:
            hist = [(s, e) for s in tools_before for e in s.effects if e.path == p]
            writes = [(s, e) for s, e in hist if e.kind in WRITE_KINDS]
            reads = [(s, e) for s, e in hist if e.kind == "read"]
            if writes:
                s, e = writes[-1]
                edges.append({"basis": "inferred", "edge": "prior-write", "step": s.n, "rule": "prior-write",
                              "detail": f"{p} was last written at step {s.n} ({s.tool}, {e.basis}: {e.rule}); step {n} changes that version"})
            if reads:
                s, e = reads[-1]
                edges.append({"basis": "inferred", "edge": "read-before-write", "step": s.n, "rule": "read-before-write",
                              "detail": f"the agent read {p} at step {s.n} ({e.basis}); what it saw there is in that step's result"})
            elif any(e.kind in WRITE_KINDS for e in target.effects if e.path == p):
                edges.append({"basis": "inferred", "edge": "unread-write", "rule": "no-read-before-write",
                              "detail": f"no earlier read of {p} in this run: it was changed without being looked at here"})
        # inferred: a failure just before, which this step may be reacting to
        for s in reversed(tools_before[-3:]):
            recovered = any(t.n > s.n and t.tool == s.tool and t.target == s.target and t.status == "ok" and not t.output_fail
                            for t in tools_before)
            if (s.status == "error" or s.output_fail) and not recovered:
                edges.append({"basis": "inferred", "edge": "retry-after-failure", "step": s.n, "rule": "failure-within-3-steps",
                              "detail": f"step {s.n} failed just before ({s.tool} {s.target[:80]} -> {outcome(s)}): {first_line(s.text)}"})
                break
        # inferred: an earlier tool output that named this step's target
        names = {os.path.basename(p) for p in tgt_paths if p and os.path.basename(p)}
        for s in reversed(tools_before):
            if any(e.path in tgt_paths for e in s.effects):
                continue          # a step that touched the file names it in its own result
            hit = next((nm for nm in names if nm and core.re.search(
                r"(?<![\w.-])" + core.re.escape(nm) + r"(?![\w-])", s.text)), None)
            if hit:
                edges.append({"basis": "inferred", "edge": "target-seen-in-output", "step": s.n, "rule": "target-seen-in-output",
                              "detail": f"{hit} appeared in the output of step {s.n} ({s.tool} {s.target[:60]})"})
                break
    # what followed: did anything later depend on or undo it?
    after = []
    if target.role == "tool":
        for p in [e.path for e in target.effects]:
            for s in sess.tool_steps:
                if s.n > n:
                    for e in s.effects:
                        if e.path == p:
                            after.append({"step": s.n, "kind": e.kind, "basis": e.basis, "tool": s.tool})
    return {"step": target.as_dict(), "edges": edges, "later_effects_on_same_files": after[:10]}


def first_line(text):
    for line in (text or "").splitlines():
        if line.strip() and not core.EXIT_RE.match(line):
            return line.strip()[:160]
    return ""


# --------------------------------------------------------------------------- output

def print_step(s):
    if s.role == "tool":
        effs = "; ".join(f"{e.kind} {e.path} [{e.basis}]" for e in s.effects if e.kind in WRITE_KINDS)
        line = f"  #{s.n:<4} {s.tool}: {s.target[:110]}  -> {outcome(s)}"
        print(line)
        if effs:
            print(f"         changes: {effs}")
        if s.status == "error" or s.output_fail:
            hit = core.FAIL_TEXT.search(s.text)
            line = s.text[hit.start():].splitlines()[0] if hit else first_line(s.text)
            print(f"         output: {line.strip()[:160]}")
    else:
        who = "USER " if s.role == "user" else "AGENT"
        text = " ".join(s.text.split())
        print(f"  #{s.n:<4} {who}: {text[:200]}{'...' if len(text) > 200 else ''}")


def run(args):
    try:
        sess = core.resolve_session(args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"trace_timeline: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    head = f"Run {sess.id} [{sess.harness}]  {sess.started} -> {sess.ended}  cwd {sess.cwd}\n  source: {sess.path}"
    red = ", ".join(f"{k} x{v}" for k, v in sess.redactions.items())

    if args.why is not None:
        res = why(sess, args.why)
        if res is None:
            print(f"trace_timeline: no step {args.why} (this run has {len(sess.steps)})", file=sys.stderr)
            return EXIT["BAD_INPUT"]
        if args.output == "json":
            print(json.dumps({"session": sess.summary(), **res}, indent=2))
            return EXIT["OK"]
        print(head)
        print(f"\nWhy step {args.why}?")
        print_step(next(s for s in sess.steps if s.n == args.why))
        for basis in ("recorded", "inferred"):
            group = [e for e in res["edges"] if e["basis"] == basis]
            print(f"\n  {basis.upper()} ({len(group)})")
            if not group:
                print("    none")
            for e in group:
                rule = f" rule={e['rule']}" if "rule" in e else ""
                print(f"    - {e['edge']}{rule}: {e['detail']}")
                if e.get("note"):
                    print(f"      ({e['note']})")
        if res["later_effects_on_same_files"]:
            later = ", ".join(f"#{a['step']} {a['kind']} [{a['basis']}]" for a in res["later_effects_on_same_files"])
            print(f"\n  LATER on the same file(s): {later}")
        print("\n  Answer from RECORDED first; name any INFERRED edge as inferred, with its rule.")
        return EXIT["OK"]

    if args.files:
        table = file_table(sess)
        if args.output == "json":
            print(json.dumps({"session": sess.summary(), "files": table}, indent=2))
            return EXIT["OK"] if table else EXIT["NO_MATCH"]
        print(head)
        silent = sum(1 for r in table if r["silent"])
        print(f"\nFiles: {len(table)} touched, {sum(1 for r in table if any(e['kind'] in WRITE_KINDS for e in r['events']))} changed, {silent} SILENT (changed, never named by the agent)")
        for r in table:
            flag = "SILENT " if r["silent"] else "       "
            evs = ", ".join(f"#{e['step']} {e['kind']}[{e['basis'][0]}]" + ("!" if e["status"] == "error" else "") for e in r["events"])
            print(f"  {flag}{r['path']}  {evs}")
        print("\n  [r] recorded by the tool call  [i] inferred from shell text  ! the call failed")
        return EXIT["OK"] if table else EXIT["NO_MATCH"]

    steps = sess.steps
    filtered = bool(args.file or args.grep or args.errors or args.tools or args.around is not None)
    if args.tools:
        steps = [s for s in steps if s.role == "tool"]
    if args.errors:
        steps = [s for s in steps if s.role == "tool" and (s.status == "error" or s.output_fail)]
    if args.file:
        steps = [s for s in steps if touches(s, args.file, sess.cwd)]
    if args.grep:
        g = args.grep.lower()
        steps = [s for s in steps if g in (s.target + " " + s.text).lower()]
    if args.around is not None:
        steps = [s for s in steps if abs(s.n - args.around) <= args.context]
    if args.output == "json":
        print(json.dumps({"session": sess.summary(), "steps": [s.as_dict() for s in steps]}, indent=2))
    else:
        print(head)
        tools = sess.tool_steps
        print(f"  {len(sess.steps)} steps, {len(tools)} tool calls, {sum(1 for s in tools if s.status == 'error' or s.output_fail)} failed or reported failures"
              + (f", redacted: {red}" if red else ""))
        print()
        for s in steps:
            print_step(s)
        if filtered and not steps:
            print("  (nothing in this run matches; the answer is not in this trace)")
    return EXIT["NO_MATCH"] if filtered and not steps else EXIT["OK"]


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample:
        with tempfile.TemporaryDirectory() as d:
            args.trace = core.write_sample(d)
            return run(args)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
