#!/usr/bin/env python3
"""Measure whether a Claude Code rollout is being used, without reading anyone's prompts.

A rollout that is never measured ends in one of two stories: "everyone loves
it" (from the three enthusiasts) or "nobody uses it" (from the licence bill).
This script turns local session transcripts into counts a team can compare.

Two modes:

  member mode   each developer runs it on their own machine over
                ~/.claude/projects/*/*.jsonl and gets a summary of COUNTS:
                sessions, active days, prompts, tool calls by kind, skills and
                slash commands used, CLI versions. No prompt text, file
                content, or tool input other than a skill or command NAME is
                ever read into the output. --anonymize hashes project names.

  team mode     --merge combines the members' JSON summaries and classifies
                the rollout stage:
                  PILOT      under 25% of seats active in the window
                  SPREADING  25-60% active
                  EMBEDDED   60%+ active and the median active member uses it
                             on 3+ days a week
                  STALLED    under 25% active six or more weeks after launch

Collecting the summaries is a team decision: share the JSON, never the
transcripts, which are plaintext and can contain secrets that tools read.

Deterministic, stdlib only, no network.

Exit codes:
    0  report produced
    2  rollout STALLED
    3  invalid input
"""

import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import re
import statistics
import sys
from collections import Counter

CMD_RE = re.compile(r"<command-name>/?([A-Za-z0-9:_-]+)</command-name>")

SAMPLE_MEMBERS = [
    {"member": "dev-a", "window_days": 28, "sessions": 41, "active_days": 17, "user_prompts": 388,
     "tool_calls": {"builtin": 2210, "mcp": 140, "skill": 22}, "top_skills": {"code-review": 9},
     "slash_commands": {"compact": 12}, "versions": {"2.1.306": 41}, "projects": 3},
    {"member": "dev-b", "window_days": 28, "sessions": 12, "active_days": 6, "user_prompts": 70,
     "tool_calls": {"builtin": 410, "mcp": 0, "skill": 1}, "top_skills": {}, "slash_commands": {},
     "versions": {"2.1.250": 12}, "projects": 1},
    {"member": "dev-c", "window_days": 28, "sessions": 0, "active_days": 0, "user_prompts": 0,
     "tool_calls": {"builtin": 0, "mcp": 0, "skill": 0}, "top_skills": {}, "slash_commands": {},
     "versions": {}, "projects": 0},
]


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def _ts(value):
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def _text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def member_summary(root, days, today, member, anonymize):
    since = dt.datetime.combine(today - dt.timedelta(days=days), dt.time.min, tzinfo=dt.timezone.utc)
    sessions, active_days, versions, projects = set(), set(), Counter(), set()
    prompts, tools, skills, commands = 0, Counter(), Counter(), Counter()
    files = glob.glob(os.path.join(root, "*", "*.jsonl"))
    for path in files:
        project = os.path.basename(os.path.dirname(path))
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = _ts(rec.get("timestamp", ""))
            if ts is None or ts.tzinfo is None or ts < since or rec.get("isSidechain"):
                continue
            kind = rec.get("type")
            if kind not in ("user", "assistant"):
                continue
            sessions.add(rec.get("sessionId"))
            active_days.add(ts.date().isoformat())
            projects.add(project)
            msg = rec.get("message") or {}
            content = msg.get("content")
            if kind == "user" and not rec.get("isMeta"):
                is_tool_result = isinstance(content, list) and any(
                    isinstance(b, dict) and b.get("type") == "tool_result" for b in content)
                if not is_tool_result:
                    text = _text_of(content)
                    m = CMD_RE.search(text)
                    if m:
                        commands[m.group(1)] += 1
                    elif text.strip():
                        prompts += 1
            if kind == "assistant" and isinstance(content, list):
                for b in content:
                    if not isinstance(b, dict) or b.get("type") != "tool_use":
                        continue
                    name = str(b.get("name", ""))
                    if name == "Skill":
                        tools["skill"] += 1
                        skill = (b.get("input") or {}).get("skill")
                        if skill:
                            skills[str(skill)] += 1
                    elif name.startswith("mcp__"):
                        tools["mcp"] += 1
                    else:
                        tools["builtin"] += 1
    # CLI version per session (first seen)
    seen = set()
    for path in files:
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            sid = rec.get("sessionId")
            if sid in sessions and sid not in seen and rec.get("version"):
                seen.add(sid)
                versions[rec["version"]] += 1
    name = member
    if anonymize:
        name = hashlib.sha256(member.encode()).hexdigest()[:10]
    return {"member": name, "window_days": days, "sessions": len(sessions), "active_days": len(active_days),
            "user_prompts": prompts, "tool_calls": {k: tools.get(k, 0) for k in ("builtin", "mcp", "skill")},
            "top_skills": dict(skills.most_common(10)), "slash_commands": dict(commands.most_common(10)),
            "versions": dict(versions), "projects": len(projects)}


def team_report(members, seats, weeks_since_launch):
    if not members:
        _fail("no member summaries to merge")
    seats = seats or len(members)
    window = max(m.get("window_days", 28) for m in members)
    active = [m for m in members if m.get("active_days", 0) > 0]
    share = len(active) / seats
    days_per_week = [m["active_days"] / (m.get("window_days", 28) / 7) for m in active]
    median_dpw = statistics.median(days_per_week) if days_per_week else 0.0
    if share >= 0.6 and median_dpw >= 3:
        stage = "EMBEDDED"
    elif share >= 0.25:
        stage = "SPREADING"
    elif weeks_since_launch is not None and weeks_since_launch >= 6:
        stage = "STALLED"
    else:
        stage = "PILOT"
    skills, versions, commands = Counter(), Counter(), Counter()
    tools = Counter()
    for m in members:
        skills.update(m.get("top_skills", {}))
        versions.update(m.get("versions", {}))
        commands.update(m.get("slash_commands", {}))
        tools.update(m.get("tool_calls", {}))
    total_tool = sum(tools.values()) or 1
    newest = max(versions, key=lambda v: [int(x) if x.isdigit() else 0 for x in v.split(".")]) if versions else None
    behind = sum(c for v, c in versions.items() if v != newest)
    return {
        "stage": stage, "seats": seats, "members_reporting": len(members), "active_members": len(active),
        "active_share": round(share, 3), "median_active_days_per_week": round(median_dpw, 2), "window_days": window,
        "sessions_total": sum(m.get("sessions", 0) for m in members),
        "tool_mix": {k: round(v / total_tool, 3) for k, v in tools.items()},
        "top_skills": dict(skills.most_common(10)), "top_slash_commands": dict(commands.most_common(10)),
        "cli_versions": dict(versions), "sessions_not_on_newest_version": behind,
        "inactive_members": [m["member"] for m in members if m.get("active_days", 0) == 0],
    }


def render_team(r):
    out = [f"Rollout stage: {r['stage']}",
           f"  {r['active_members']}/{r['seats']} seats active in {r['window_days']} days ({r['active_share']:.0%}); "
           f"median active member uses it {r['median_active_days_per_week']} days/week",
           f"  sessions {r['sessions_total']}; tool mix " + ", ".join(f"{k} {v:.0%}" for k, v in r["tool_mix"].items())]
    if r["top_skills"]:
        out.append("  skills used: " + ", ".join(f"{k} ({v})" for k, v in r["top_skills"].items()))
    else:
        out.append("  skills used: none - shared skills are not being picked up")
    if r["sessions_not_on_newest_version"]:
        out.append(f"  {r['sessions_not_on_newest_version']} sessions ran an older CLI version: {r['cli_versions']}")
    if r["inactive_members"]:
        out.append(f"  inactive: {', '.join(r['inactive_members'])}")
    return "\n".join(out)


def render_member(m):
    t = m["tool_calls"]
    return "\n".join([
        f"Member summary ({m['member']}, last {m['window_days']} days) - counts only, no prompt text",
        f"  sessions {m['sessions']}, active days {m['active_days']}, prompts {m['user_prompts']}, projects {m['projects']}",
        f"  tool calls: builtin {t['builtin']}, mcp {t['mcp']}, skill {t['skill']}",
        f"  skills: {m['top_skills'] or 'none'}   slash commands: {m['slash_commands'] or 'none'}",
        f"  CLI versions: {m['versions'] or 'none'}",
        "  Share the --output json form of this summary, never the transcripts."])


def main():
    p = argparse.ArgumentParser(description="Privacy-safe Claude Code adoption counts per member, and a team rollout stage from merged summaries.")
    p.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"), help="transcripts root (default ~/.claude/projects)")
    p.add_argument("--days", type=int, default=28, help="window in days (default 28)")
    p.add_argument("--member", default=os.environ.get("USER", "me"), help="label for this member's summary")
    p.add_argument("--anonymize", action="store_true", help="hash the member label")
    p.add_argument("--today", help="override today's date (YYYY-MM-DD)")
    p.add_argument("--merge", nargs="+", help="team mode: member summary JSON files to combine")
    p.add_argument("--seats", type=int, help="licensed seats (default: number of summaries)")
    p.add_argument("--weeks-since-launch", type=int, help="enables the STALLED verdict")
    p.add_argument("--sample", action="store_true", help="team mode on embedded sample summaries")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()

    if a.sample or a.merge:
        members = SAMPLE_MEMBERS if a.sample else []
        for path in a.merge or []:
            try:
                with open(path, encoding="utf-8") as fh:
                    data = json.load(fh)
            except (OSError, json.JSONDecodeError) as exc:
                _fail(f"cannot read {path}: {exc}")
            members.extend(data if isinstance(data, list) else [data])
        report = team_report(members, a.seats or (4 if a.sample else None), a.weeks_since_launch or (7 if a.sample else None))
        print(json.dumps(report, indent=2) if a.output == "json" else render_team(report))
        return 2 if report["stage"] == "STALLED" else 0

    if not os.path.isdir(a.projects_dir):
        _fail(f"no transcripts directory at {a.projects_dir}")
    today = dt.date.today()
    if a.today:
        try:
            today = dt.date.fromisoformat(a.today)
        except ValueError:
            p.error("--today must be YYYY-MM-DD")
    summary = member_summary(a.projects_dir, a.days, today, a.member, a.anonymize)
    print(json.dumps(summary, indent=2) if a.output == "json" else render_member(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
