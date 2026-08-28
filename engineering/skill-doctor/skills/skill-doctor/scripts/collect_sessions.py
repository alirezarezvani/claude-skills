#!/usr/bin/env python3
"""collect_sessions.py — harvest local Claude Code / Codex sessions for skill-doctor scoring.

Scans Claude Code project-history JSONL and Codex rollout JSONL, discovers the
skills installed in the target repo, detects which sessions actually used which
skills, redacts secrets, and emits:

  <out>/inventory.json        - skills, per-session stats, sampling decisions
  <out>/transcripts/<id>.md   - condensed, redacted transcripts for sampled sessions

Everything runs locally; nothing is uploaded. Every transcript line passes
through the secret redactor before it touches disk, and the output directory
is created 0700 with 0600 files.

Derived from warpdotdev/common-skills skill-doctor (MIT, (c) Denver
Technologies, Inc.) — see the plugin README for the numbered deviations.

Usage:
    python collect_sessions.py --out ./skill-doctor-run
    python collect_sessions.py --harness claude --days 30 --max-sessions 8
    python collect_sessions.py --sample                # synthetic demo, touches no real history
    python collect_sessions.py --sample --output json

Exit codes: 0 collected (even when 0 sessions matched — the inventory says so),
3 bad input (an explicitly requested source is missing).

Stdlib only. No ML/LLM calls.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_MSG_CHARS = 1500
MAX_TOOL_CHARS = 500
MAX_TRANSCRIPT_ENTRIES = 160
TRANSCRIPT_HEAD = 100
TRANSCRIPT_TAIL = 40

CODE_EDIT_HINTS = ("apply_patch", "*** Begin Patch", "edit_file", "create_file", "str_replace", "write_file")
CLAUDE_CODE_EDIT_TOOLS = {"Edit", "MultiEdit", "NotebookEdit", "Write"}

# ---------------------------------------------------------------------------
# Secret redaction — applied to every transcript entry before it is written.
# Ordered: more specific token shapes first so e.g. sk-ant- wins over sk-.
# ---------------------------------------------------------------------------
REDACTION_PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----(?:.|\n)*?(?:-----END [A-Z ]*PRIVATE KEY-----|\Z)")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("stripe-key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}\b")),
    ("bearer-token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._+/=-]{16,}")),
    ("connection-string", re.compile(r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqps?)://[^\s'\"]+:[^\s'\"@]+@[^\s'\"]+")),
    ("url-credential", re.compile(r"(?i)([?&](?:token|key|secret|access_token|api_key|apikey|sig)=)[^&\s'\"]+")),
    ("env-secret", re.compile(r"(?i)\b([A-Z0-9_]*(?:API_?KEY|SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL)S?)(\s*[=:]\s*)['\"]?[^\s'\"]{8,}")),
]


def redact_secrets(text, counter=None):
    """Replace secret-shaped substrings with [REDACTED:<label>] markers."""
    if not text:
        return text
    for label, pattern in REDACTION_PATTERNS:
        def _sub(match, _label=label):
            # A broader pattern (e.g. env-secret) re-matching an already-redacted
            # value would just stack markers; leave prior redactions alone.
            if "[REDACTED:" in match.group(0):
                return match.group(0)
            if counter is not None:
                counter[_label] = counter.get(_label, 0) + 1
            groups = match.groups()
            if groups and groups[0] is not None:
                return groups[0] + (groups[1] if len(groups) > 1 and groups[1] else "") + f"[REDACTED:{_label}]"
            return f"[REDACTED:{_label}]"
        text = pattern.sub(_sub, text)
    return text


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Harvest local Claude Code / Codex sessions for skill-doctor scoring.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:")[1] if "Usage:" in __doc__ else None,
    )
    p.add_argument("--harness", choices=("auto", "all", "claude", "codex"), default="auto",
                   help="session source (default: auto — scan every locally available source)")
    p.add_argument("--claude-home", default=os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude"),
                   help="Claude Code config dir (default: CLAUDE_CONFIG_DIR or ~/.claude)")
    p.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", "~/.codex"),
                   help="Codex home (default: CODEX_HOME or ~/.codex)")
    p.add_argument("--repo", default=None, help="repo to scope to (default: git root of cwd, else cwd)")
    p.add_argument("--include-global-skills", action="store_true",
                   help="also discover skills outside the repo (~/.claude/skills, ~/.agents/skills, ~/.codex/skills)")
    p.add_argument("--days", type=int, default=45, help="only consider sessions modified in the last N days (default 45)")
    p.add_argument("--max-sessions", type=int, default=12, help="max sessions to sample for scoring (default 12)")
    p.add_argument("--per-skill", type=int, default=3, help="max sampled sessions per skill (default 3)")
    p.add_argument("--no-skill", type=int, default=4, help="max sampled sessions that used no skill (default 4)")
    p.add_argument("--skills-dir", action="append", default=[], help="extra skills directory to scan (repeatable)")
    p.add_argument("--include-subagents", action="store_true", help="include subagent/sidechain sessions")
    p.add_argument("--strict-repo", action="store_true",
                   help="only include sessions whose cwd resolves inside the repo "
                        "(disables the worktree/basename fallback, which can match an unrelated repo of the same name)")
    p.add_argument("--out", default=None, help="output directory (default: a fresh dir under the system temp dir)")
    p.add_argument("--output", choices=("text", "json"), default="text", help="summary format on stdout")
    p.add_argument("--sample", action="store_true",
                   help="run on built-in synthetic sessions instead of real history (demo/smoke test)")
    return p.parse_args(argv)


def resolve_repo(repo_arg):
    if repo_arg:
        return Path(repo_arg).expanduser().resolve()
    try:
        res = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            return Path(res.stdout.strip()).resolve()
    except (subprocess.TimeoutExpired, OSError):
        pass
    return Path.cwd().resolve()


def secure_mkdir(path):
    path.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path, 0o700)
    except OSError:
        pass


def secure_write(path, text):
    path.write_text(text)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def discover_skills(repo, codex_home, extra_dirs, include_global):
    """Find installed skills: classic skill roots plus this-repo plugin layouts."""
    roots = [
        repo / ".agents" / "skills",
        repo / ".claude" / "skills",
        repo / ".codex" / "skills",
    ]
    if include_global:
        roots += [
            codex_home / "skills",
            Path.home() / ".agents" / "skills",
            Path.home() / ".claude" / "skills",
        ]
    roots += [Path(d).expanduser() for d in extra_dirs]

    skills = {}

    def add_skill(skill_md):
        name = skill_md.parent.name
        if name in skills:
            return
        try:
            text = skill_md.read_text(errors="replace")
        except OSError:
            return
        desc = ""
        m = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        if m:
            desc = m.group(1).strip().strip("\"'")[:300]
        skills[name] = {
            "name": name,
            "path": str(skill_md),
            "description": desc,
            "bytes": skill_md.stat().st_size,
            "modified_at": datetime.fromtimestamp(skill_md.stat().st_mtime, tz=timezone.utc).isoformat(),
        }

    for root in roots:
        if not root.is_dir():
            continue
        for skill_md in sorted(root.glob("*/SKILL.md")):
            add_skill(skill_md)
        # Marketplace-plugin layout: <root>/<plugin>/skills/<skill>/SKILL.md
        for skill_md in sorted(root.glob("*/skills/*/SKILL.md")):
            add_skill(skill_md)
    return skills


def find_session_files(root, patterns, cutoff):
    files = []
    for pattern in patterns:
        for f in root.rglob(pattern) if root.is_dir() else []:
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            except OSError:
                continue
            if mtime >= cutoff:
                files.append((mtime, f))
    files.sort(key=lambda t: (t[0], str(t[1])), reverse=True)
    return files


def truncate(text, limit):
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + f" …[truncated {len(text) - limit} chars]"


def extract_text(content):
    if isinstance(content, str):
        return content
    parts = []
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict):
                t = block.get("text") or block.get("content") or ""
                if isinstance(t, str) and t:
                    parts.append(t)
            elif isinstance(block, str):
                parts.append(block)
    return "\n".join(parts)


def looks_injected(text):
    head = text.lstrip()[:80]
    return head.startswith("<") and any(
        tag in head
        for tag in ("environment_context", "user_instructions", "ENVIRONMENT", "system-reminder",
                    "permissions", "collaboration_mode", "recommended_plugins", "turn_context")
    )


COMMAND_NAME_RE = re.compile(r"<command-name>/?([\w:-]+)</command-name>")


def new_stats():
    return {"user_turns": 0, "assistant_turns": 0, "tool_calls": 0,
            "repeated_tool_calls": 0, "error_outputs": 0}


def parse_claude_session(path, skill_names, include_subagents):
    """Normalize one Claude Code JSONL session to the shared transcript shape."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read(MAX_FILE_BYTES).decode("utf-8", errors="replace")
    except OSError:
        return None

    meta = {}
    stats = new_stats()
    entries = []
    seen_calls = {}
    seen_assistant_messages = set()
    call_args_text = []
    used_tool_names = set()
    skills_used = set()
    first_ts = last_ts = None
    is_sidechain = False

    for line in raw.splitlines():
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        ts = obj.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts

        if obj.get("isSidechain"):
            is_sidechain = True
            if not include_subagents:
                return None

        if not meta and obj.get("sessionId"):
            session_id = obj.get("sessionId")
            agent_id = obj.get("agentId")
            meta = {
                "id": f"{session_id}-{agent_id}" if agent_id else session_id,
                "cwd": obj.get("cwd"),
                "started_at": ts,
                "originator": "claude-code",
                "thread_source": "subagent" if obj.get("isSidechain") else None,
                "cli_version": obj.get("version"),
            }
        elif meta:
            meta["cwd"] = meta.get("cwd") or obj.get("cwd")
            meta["started_at"] = meta.get("started_at") or ts

        record_type = obj.get("type")
        message = obj.get("message")
        if record_type not in ("user", "assistant") or not isinstance(message, dict):
            continue

        role = message.get("role") or record_type
        content = message.get("content")
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}]
        has_user_text = False

        if role == "assistant":
            message_id = message.get("id") or obj.get("uuid")
            if message_id and message_id not in seen_assistant_messages:
                seen_assistant_messages.add(message_id)
                stats["assistant_turns"] += 1

        for block in blocks:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text":
                text = block.get("text")
                if not isinstance(text, str) or not text:
                    continue
                # Slash-command invocations arrive as harness-injected user text;
                # mine them for skill usage before the injection filter drops them.
                for cmd in COMMAND_NAME_RE.findall(text):
                    base = cmd.split(":")[-1]
                    if cmd in skill_names:
                        skills_used.add(cmd)
                    elif base in skill_names:
                        skills_used.add(base)
                if looks_injected(text):
                    continue
                if role == "user":
                    has_user_text = True
                    entries.append(("user", truncate(text, MAX_MSG_CHARS)))
                elif role == "assistant":
                    entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
            elif block_type == "tool_use":
                stats["tool_calls"] += 1
                name = str(block.get("name") or "unknown")
                args = block.get("input") or {}
                args_text = args if isinstance(args, str) else json.dumps(args, ensure_ascii=False)
                key = hashlib.sha1((name + args_text).encode()).hexdigest()
                seen_calls[key] = seen_calls.get(key, 0) + 1
                if seen_calls[key] > 1:
                    stats["repeated_tool_calls"] += 1
                call_args_text.append(args_text)
                used_tool_names.add(name)
                if name == "Skill" and isinstance(args, dict):
                    skill_name = str(args.get("skill") or "")
                    base = skill_name.split(":")[-1]
                    if skill_name in skill_names:
                        skills_used.add(skill_name)
                    elif base in skill_names:
                        skills_used.add(base)
                entries.append((f"tool:{name}", truncate(args_text, MAX_TOOL_CHARS)))
            elif block_type == "tool_result":
                result = extract_text(block.get("content"))
                low = result[:2000].lower()
                if block.get("is_error") or "error" in low or "failed" in low or "traceback" in low:
                    stats["error_outputs"] += 1
                entries.append(("output", truncate(result, MAX_TOOL_CHARS)))

        if role == "user" and has_user_text:
            stats["user_turns"] += 1

    if not meta:
        meta = {"id": path.stem, "cwd": None, "started_at": first_ts,
                "originator": "claude-code",
                "thread_source": "subagent" if is_sidechain else None}
    elif is_sidechain:
        meta["thread_source"] = "subagent"

    args_blob = "\n".join(call_args_text)
    skills_used.update(
        name for name in skill_names
        if f"skills/{name}/" in args_blob or f"{name}/SKILL.md" in args_blob
    )
    stats["first_ts"] = first_ts
    stats["last_ts"] = last_ts
    stats["has_code_edits"] = (
        bool(used_tool_names & CLAUDE_CODE_EDIT_TOOLS)
        or any(hint in args_blob for hint in CODE_EDIT_HINTS)
    )
    return meta, stats, entries, sorted(skills_used)


def parse_codex_session(path, skill_names, include_subagents):
    """Normalize one Codex rollout JSONL session to the shared transcript shape."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read(MAX_FILE_BYTES).decode("utf-8", errors="replace")
    except OSError:
        return None

    meta = {}
    stats = new_stats()
    entries = []
    seen_calls = {}
    call_args_text = []
    first_ts = last_ts = None

    for line in raw.splitlines():
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        ltype = obj.get("type")
        payload = obj.get("payload") or {}
        if not isinstance(payload, dict):
            continue
        ts = obj.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts

        if ltype == "session_meta":
            meta = {
                "id": payload.get("id") or payload.get("session_id") or path.stem,
                "cwd": payload.get("cwd"),
                "started_at": payload.get("timestamp"),
                "originator": payload.get("originator"),
                "thread_source": payload.get("thread_source"),
            }
            source = payload.get("source")
            is_subagent = payload.get("thread_source") == "subagent" or (
                isinstance(source, dict) and "subagent" in source
            )
            if is_subagent and not include_subagents:
                return None
        elif ltype == "event_msg":
            ptype = payload.get("type")
            if ptype == "user_message":
                stats["user_turns"] += 1
            elif ptype == "agent_message":
                stats["assistant_turns"] += 1
        elif ltype == "response_item":
            ptype = payload.get("type")
            if ptype == "message":
                role = payload.get("role")
                text = extract_text(payload.get("content"))
                if not text:
                    continue
                if role == "user":
                    if looks_injected(text):
                        continue
                    entries.append(("user", truncate(text, MAX_MSG_CHARS)))
                elif role == "assistant":
                    entries.append(("assistant", truncate(text, MAX_MSG_CHARS)))
            elif ptype in ("function_call", "custom_tool_call", "local_shell_call"):
                stats["tool_calls"] += 1
                name = payload.get("name") or ptype
                args = payload.get("arguments") or payload.get("input") or ""
                if not isinstance(args, str):
                    args = json.dumps(args)
                key = hashlib.sha1((name + args).encode()).hexdigest()
                seen_calls[key] = seen_calls.get(key, 0) + 1
                if seen_calls[key] > 1:
                    stats["repeated_tool_calls"] += 1
                call_args_text.append(args)
                entries.append((f"tool:{name}", truncate(args, MAX_TOOL_CHARS)))
            elif ptype in ("function_call_output", "custom_tool_call_output"):
                out = payload.get("output") or ""
                if not isinstance(out, str):
                    out = json.dumps(out)
                low = out[:2000].lower()
                if "error" in low or "failed" in low or "traceback" in low:
                    stats["error_outputs"] += 1
                entries.append(("output", truncate(out, MAX_TOOL_CHARS)))

    if not meta:
        meta = {"id": path.stem, "cwd": None, "started_at": first_ts}

    # A skill counts as used only when a tool call actually touched it: the raw
    # session text is unusable because Codex injects the installed-skill list
    # into every session preamble.
    args_blob = "\n".join(call_args_text)
    skills_used = sorted(
        name for name in skill_names
        if f"skills/{name}/" in args_blob or f"{name}/SKILL.md" in args_blob
    )
    stats["first_ts"] = first_ts
    stats["last_ts"] = last_ts
    stats["has_code_edits"] = any(h in args_blob for h in CODE_EDIT_HINTS)
    return meta, stats, entries, skills_used


def render_transcript(meta, stats, skills_used, entries, redaction_counter):
    lines = [
        f"# Session {meta.get('id')}",
        f"- cwd: {meta.get('cwd')}",
        f"- started: {meta.get('started_at') or stats.get('first_ts')}",
        f"- skills detected: {', '.join(skills_used) or '(none)'}",
        f"- stats: {stats['user_turns']} user turns, {stats['assistant_turns']} assistant turns, "
        f"{stats['tool_calls']} tool calls ({stats['repeated_tool_calls']} repeated), "
        f"{stats['error_outputs']} error-ish outputs, code edits: {stats['has_code_edits']}",
        "",
        "## Condensed transcript",
        "",
    ]
    shown = entries
    if len(entries) > MAX_TRANSCRIPT_ENTRIES:
        omitted = len(entries) - TRANSCRIPT_HEAD - TRANSCRIPT_TAIL
        shown = (entries[:TRANSCRIPT_HEAD]
                 + [("note", f"[... {omitted} entries omitted ...]")]
                 + entries[-TRANSCRIPT_TAIL:])
    for role, text in shown:
        lines.append(f"[{role}] {redact_secrets(text, redaction_counter)}")
        lines.append("")
    return "\n".join(lines)


def repo_match_mode(cwd, repo):
    """How a session's recorded cwd relates to the target repo.

    Returns "path" when cwd resolves inside the repo root (a certain match),
    "name" when only the worktree/basename heuristic matches (the directory
    name equals the repo's — this can false-positive on an unrelated repo that
    shares the name, so callers record it and --strict-repo disables it), or
    None for no match.
    """
    if not cwd:
        return None
    p = Path(cwd)
    try:
        if p.resolve().is_relative_to(repo):
            return "path"
    except (OSError, ValueError):
        pass
    if p.name == repo.name or repo.name in p.parts:
        return "name"
    return None


# ---------------------------------------------------------------------------
# --sample fixtures: two tiny synthetic sessions, one with a planted secret.
# ---------------------------------------------------------------------------
def sample_sessions(repo):
    fixed_ts = "2026-01-15T10:00:00Z"
    s1 = {
        "harness": "claude",
        "meta": {"id": "sample-session-1", "cwd": str(repo), "started_at": fixed_ts,
                 "originator": "claude-code", "thread_source": None},
        "stats": {"user_turns": 2, "assistant_turns": 3, "tool_calls": 6,
                  "repeated_tool_calls": 2, "error_outputs": 1,
                  "first_ts": fixed_ts, "last_ts": fixed_ts, "has_code_edits": True},
        "skills_used": ["sample-skill"],
        "file": "(synthetic)",
        "repo_match": "path",
        "modified_at": fixed_ts,
        "_entries": [
            ("user", "Fix the failing date parser test"),
            ("tool:Read", '{"file_path": "src/parse.py"}'),
            ("tool:Read", '{"file_path": "src/parse.py"}'),
            ("assistant", "Re-read the same file twice, then patched the format string."),
            ("output", "export OPENAI_API_KEY=sk-abcdefghijklmnopqrstuv1234 loaded from .env"),
            ("tool:Edit", '{"file_path": "src/parse.py", "old_string": "%Y/%m/%d", "new_string": "%Y-%m-%d"}'),
            ("output", "1 passed"),
        ],
    }
    s2 = {
        "harness": "claude",
        "meta": {"id": "sample-session-2", "cwd": str(repo), "started_at": fixed_ts,
                 "originator": "claude-code", "thread_source": None},
        "stats": {"user_turns": 1, "assistant_turns": 2, "tool_calls": 3,
                  "repeated_tool_calls": 0, "error_outputs": 0,
                  "first_ts": fixed_ts, "last_ts": fixed_ts, "has_code_edits": False},
        "skills_used": [],
        "file": "(synthetic)",
        "repo_match": "path",
        "modified_at": fixed_ts,
        "_entries": [
            ("user", "What does the release script do?"),
            ("tool:Read", '{"file_path": "scripts/release.sh"}'),
            ("assistant", "It tags the commit and pushes the tag; no publish step."),
        ],
    }
    skills = {"sample-skill": {
        "name": "sample-skill", "path": str(repo / ".claude/skills/sample-skill/SKILL.md"),
        "description": "Synthetic skill used by the --sample fixture.",
        "bytes": 0, "modified_at": fixed_ts,
    }}
    return skills, [s1, s2]


def sample_and_write(sessions, skills, args, out_dir, transcripts_dir):
    """Newest-first sampling: up to --per-skill sessions per skill, then --no-skill without one."""
    sessions.sort(key=lambda s: (s["modified_at"], s["meta"]["id"]), reverse=True)
    for s in sessions:
        s["_key"] = f"{s['harness']}:{s['meta']['id']}"

    sampled_keys = set()
    per_skill_count = {name: 0 for name in skills}
    for s in sessions:
        if len(sampled_keys) >= args.max_sessions:
            break
        for name in s["skills_used"]:
            if per_skill_count.get(name, 0) < args.per_skill:
                per_skill_count[name] = per_skill_count.get(name, 0) + 1
                sampled_keys.add(s["_key"])
                break
    no_skill_taken = 0
    for s in sessions:
        if len(sampled_keys) >= args.max_sessions or no_skill_taken >= args.no_skill:
            break
        if not s["skills_used"] and s["_key"] not in sampled_keys:
            sampled_keys.add(s["_key"])
            no_skill_taken += 1

    redaction_counter = {}
    for s in sessions:
        sid = s["meta"]["id"]
        s["sampled"] = s["_key"] in sampled_keys
        if s["sampled"]:
            tpath = transcripts_dir / f"{s['harness']}-{sid}.md"
            secure_write(tpath, render_transcript(s["meta"], s["stats"], s["skills_used"],
                                                  s["_entries"], redaction_counter))
            s["transcript_path"] = str(tpath)
        del s["_entries"]
        del s["_key"]
    return sampled_keys, redaction_counter


def main(argv=None):
    args = parse_args(argv)
    claude_home = Path(args.claude_home).expanduser()
    codex_home = Path(args.codex_home).expanduser()
    if args.out:
        out_dir = Path(args.out).expanduser()
    else:
        out_dir = Path(tempfile.mkdtemp(prefix="skill-doctor-"))
    transcripts_dir = out_dir / "transcripts"
    secure_mkdir(out_dir)
    secure_mkdir(transcripts_dir)

    repo = resolve_repo(args.repo)
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)

    sessions = []
    in_repo_count = 0
    scanned_count = 0
    sources = {}

    if args.sample:
        skills, sessions = sample_sessions(repo)
        sources["sample"] = {"records_in_window": len(sessions)}
        scanned_count = in_repo_count = len(sessions)
    else:
        skills = discover_skills(repo, codex_home, args.skills_dir, args.include_global_skills)

        requested_claude = args.harness in ("auto", "all", "claude")
        claude_projects = claude_home / "projects"
        if requested_claude and claude_projects.is_dir():
            candidates = list(claude_projects.glob("*/*.jsonl"))
            if args.include_subagents:
                candidates.extend(claude_projects.glob("*/*/subagents/*.jsonl"))
            claude_files = []
            for path in candidates:
                try:
                    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                except OSError:
                    continue
                if mtime >= cutoff:
                    claude_files.append((mtime, path))
            claude_files.sort(key=lambda t: (t[0], str(t[1])), reverse=True)
            sources["claude"] = {"home": str(claude_home), "records_in_window": len(claude_files)}
            scanned_count += len(claude_files)
            for mtime, path in claude_files:
                parsed = parse_claude_session(path, skills.keys(), args.include_subagents)
                if parsed is None:
                    continue
                meta, stats, entries, skills_used = parsed
                match = repo_match_mode(meta.get("cwd"), repo)
                if match is None or (args.strict_repo and match != "path"):
                    continue
                in_repo_count += 1
                if stats["assistant_turns"] < 1 or stats["tool_calls"] < 1:
                    continue
                sessions.append({"harness": "claude", "meta": meta, "stats": stats,
                                 "skills_used": skills_used, "file": str(path),
                                 "repo_match": match,
                                 "modified_at": mtime.isoformat(), "_entries": entries})
        elif args.harness == "claude":
            print(f"error: Claude Code project history not found at {claude_projects}", file=sys.stderr)
            return 3

        requested_codex = args.harness in ("auto", "all", "codex")
        if requested_codex and codex_home.is_dir():
            codex_files = find_session_files(codex_home / "sessions", ["rollout-*.jsonl"], cutoff)
            codex_files += find_session_files(codex_home / "archived_sessions", ["rollout-*.jsonl"], cutoff)
            codex_files.sort(key=lambda t: (t[0], str(t[1])), reverse=True)
            sources["codex"] = {"home": str(codex_home), "records_in_window": len(codex_files)}
            scanned_count += len(codex_files)
            for mtime, path in codex_files:
                parsed = parse_codex_session(path, skills.keys(), args.include_subagents)
                if parsed is None:
                    continue
                meta, stats, entries, skills_used = parsed
                match = repo_match_mode(meta.get("cwd"), repo)
                if match is None or (args.strict_repo and match != "path"):
                    continue
                in_repo_count += 1
                if stats["assistant_turns"] < 1 or stats["tool_calls"] < 1:
                    continue
                sessions.append({"harness": "codex", "meta": meta, "stats": stats,
                                 "skills_used": skills_used, "file": str(path),
                                 "repo_match": match,
                                 "modified_at": mtime.isoformat(), "_entries": entries})
        elif args.harness == "codex":
            print(f"error: Codex home not found at {codex_home}", file=sys.stderr)
            return 3

        if not sources:
            print("error: no Claude Code project history or Codex home found; "
                  "pass --claude-home/--codex-home, or --sample for a demo run", file=sys.stderr)
            return 3

    sampled_keys, redaction_counter = sample_and_write(sessions, skills, args, out_dir, transcripts_dir)

    skill_usage = {name: 0 for name in skills}
    for s in sessions:
        for name in s["skills_used"]:
            skill_usage[name] += 1

    inventory = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "harness": next(iter(sources)) if len(sources) == 1 else "mixed",
        "sources": sources,
        "repo": str(repo),
        "repo_name": repo.name,
        "window_days": args.days,
        "skills": sorted(skills.values(), key=lambda x: x["name"]),
        "skill_usage": skill_usage,
        "redactions": redaction_counter,
        "stats": {
            "session_records_in_window": scanned_count,
            "sessions_in_repo": in_repo_count,
            "sessions_considered": len(sessions),
            "sessions_sampled": len(sampled_keys),
            "skills_found": len(skills),
            "skills_used": sum(1 for v in skill_usage.values() if v > 0),
            "sessions_matched_by_name_only": sum(1 for s in sessions if s.get("repo_match") == "name"),
        },
        "sessions": sessions,
    }
    secure_write(out_dir / "inventory.json", json.dumps(inventory, indent=2))

    st = inventory["stats"]
    if args.output == "json":
        summary = {"out_dir": str(out_dir), "inventory": str(out_dir / "inventory.json"),
                   "transcripts_dir": str(transcripts_dir), "sources": sorted(sources),
                   "redactions": sum(redaction_counter.values()), "stats": st}
        print(json.dumps(summary, indent=2))
    else:
        print(f"repo:               {repo}")
        print(f"sources:            {', '.join(sources)}")
        print(f"skills found:       {st['skills_found']} ({st['skills_used']} used in window)")
        print(f"sessions in window: {st['session_records_in_window']} records, "
              f"{st['sessions_in_repo']} in repo, {st['sessions_considered']} scoreable")
        print(f"sessions sampled:   {st['sessions_sampled']} -> {transcripts_dir}")
        print(f"secrets redacted:   {sum(redaction_counter.values())}")
        if st["sessions_matched_by_name_only"]:
            print(f"note:               {st['sessions_matched_by_name_only']} session(s) matched only by "
                  "directory name (worktree heuristic) — pass --strict-repo to exclude them")
        print(f"inventory:          {out_dir / 'inventory.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
