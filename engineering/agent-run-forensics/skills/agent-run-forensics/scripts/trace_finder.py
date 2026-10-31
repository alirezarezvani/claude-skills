#!/usr/bin/env python3
"""Find the recorded agent run a question is about, before anyone answers it.

"Which session deleted the migrations folder?", "what ran last night?", "did
anything touch config.yaml this week?" - each needs a trace, and this finds it.
It lists the Claude Code and Codex sessions recorded on this machine, newest
first, filtered by repo, time window, a file a session touched, or text in its
commands, and prints the ids to pass to trace_timeline.py and claim_checker.py.

Sources (read-only; nothing is uploaded, nothing is written):
  ~/.claude/projects/*/*.jsonl          Claude Code (CLAUDE_CONFIG_DIR respected)
  ~/.codex/sessions/**/rollout-*.jsonl  Codex CLI (CODEX_HOME respected)

Exit codes
  0  one or more sessions match
  2  no session matches: there is no trace, so do not answer from memory
  3  bad input (unknown flag value, unreadable --trace)

Examples
  trace_finder.py --since 2d
  trace_finder.py --touched config.yaml --since 7d
  trace_finder.py --grep "rm -rf" --all-repos --since 1w
  trace_finder.py --sample
"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trace_core as core  # noqa: E402

EXIT = {"FOUND": 0, "NONE": 2, "BAD_INPUT": 3}


def build_parser():
    claude, codex = core.default_homes()
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog=__doc__.split("\n\n", 1)[1])
    p.add_argument("--repo", help="only sessions whose working dir is in this repo (default: cwd)")
    p.add_argument("--all-repos", action="store_true", help="ignore --repo and list every project")
    p.add_argument("--since", help="only sessions active in this window: 36h, 7d, 2w or an ISO date")
    p.add_argument("--touched", metavar="PATH", help="only sessions that wrote, deleted or read this path (suffix match)")
    p.add_argument("--writes-only", action="store_true", help="with --touched: ignore reads")
    p.add_argument("--grep", metavar="TEXT", help="only sessions whose tool calls or prompts contain this text")
    p.add_argument("--errors", action="store_true", help="only sessions with a failed tool call")
    p.add_argument("--subagents", action="store_true", help="include subagent transcripts")
    p.add_argument("--limit", type=int, default=15, help="max sessions to list (default 15)")
    p.add_argument("--trace", action="append", metavar="PATH", help="search these JSONL files instead of the homes")
    p.add_argument("--claude-home", default=str(claude))
    p.add_argument("--codex-home", default=str(codex))
    p.add_argument("--output", choices=("text", "json"), default="text")
    p.add_argument("--sample", action="store_true", help="run against a built-in fictional session")
    return p


def matches(sess, args, since):
    hits = []
    if since:
        end = core.parse_ts(sess.ended) or core.parse_ts(sess.started)
        if end and end < since:
            return None
    tools = sess.tool_steps
    if args.errors and not any(s.status == "error" for s in tools):
        return None
    if args.touched:
        kinds = ("write", "delete", "move") if args.writes_only else ("write", "delete", "move", "read")
        for s in tools:
            for e in s.effects:
                if e.kind in kinds and core.path_matches(e.path, args.touched, sess.cwd):
                    hits.append({"step": s.n, "tool": s.tool, "effect": e.kind, "path": e.path,
                                 "basis": e.basis, "rule": e.rule})
                    break
        if not hits:
            return None
    if args.grep:
        needle = args.grep.lower()
        found = []
        for s in sess.steps:
            hay = (s.target if s.role == "tool" else s.text).lower()
            if needle in hay:
                found.append({"step": s.n, "role": s.role, "tool": s.tool,
                              "excerpt": (s.target if s.role == "tool" else s.text)[:120]})
        if not found:
            return None
        hits.extend(found[:5])
    return hits


def run(args):
    try:
        since = core.parse_since(args.since)
    except ValueError as exc:
        print(f"trace_finder: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    if args.trace:
        files = [Path(t).expanduser() for t in args.trace]
        missing = [str(f) for f in files if not f.is_file()]
        if missing:
            print(f"trace_finder: not a file: {', '.join(missing)}", file=sys.stderr)
            return EXIT["BAD_INPUT"]
    else:
        files = core.candidate_files(Path(args.claude_home).expanduser(), Path(args.codex_home).expanduser(),
                                     args.subagents, since)
    repo = None if (args.all_repos or args.trace) else core.default_repo(args.repo)
    rows = []
    for f in files:
        sess = core.parse_session(f)
        if sess is None or (sess.subagent and not args.subagents):
            continue
        if repo and not core.repo_matches(sess.cwd, repo):
            continue
        hits = matches(sess, args, since)
        if hits is None:
            continue
        row = sess.summary()
        row["matches"] = hits
        rows.append(row)
        if len(rows) >= args.limit:
            break
    rows.sort(key=lambda r: r.get("ended") or "", reverse=True)
    verdict = "FOUND" if rows else "NONE"
    if args.output == "json":
        print(json.dumps({"verdict": verdict, "repo": repo, "sources_scanned": len(files), "sessions": rows}, indent=2))
    else:
        scope = repo or "all repos"
        print(f"Trace finder: {verdict}  ({len(rows)} session(s) in {scope}, {len(files)} file(s) scanned)")
        if not rows:
            print("  No recorded run matches. Say so; do not reconstruct what happened from memory.")
        for r in rows:
            print(f"\n  {r['session']}  [{r['harness']}]  {r['started']} -> {r['ended']}")
            print(f"    cwd: {r['cwd']}   tool calls: {r['tool_calls']}   failed: {r['errors']}")
            if r["first_prompt"]:
                print(f"    first prompt: {r['first_prompt']}")
            if r["files_written"]:
                shown = r["files_written"][:6]
                more = len(r["files_written"]) - len(shown)
                print(f"    wrote: {', '.join(shown)}" + (f" (+{more} more)" if more > 0 else ""))
            for h in r["matches"][:5]:
                if "effect" in h:
                    print(f"    step {h['step']}: {h['effect']} {h['path']} via {h['tool']} [{h['basis']}: {h['rule']}]")
                else:
                    print(f"    step {h['step']} ({h['tool'] or h['role']}): {h['excerpt']}")
            print(f"    next: trace_timeline.py --trace {r['path']}")
    return EXIT[verdict]


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample:
        with tempfile.TemporaryDirectory() as d:
            args.trace = [core.write_sample(d)]
            if not args.touched and not args.grep:
                args.touched = "config.yaml"
                args.writes_only = True
            return run(args)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
