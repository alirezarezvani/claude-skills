#!/usr/bin/env python3
"""Shared trace parser for agent-run-forensics. Imported by the three CLIs; not a CLI itself.

Reads the recordings coding agents already keep on disk and normalises them to
one list of numbered steps:

  Claude Code   ~/.claude/projects/<project>/<session>.jsonl  (also `claude -p
                --output-format stream-json` output, which uses session_id)
  Codex CLI     ~/.codex/sessions/**/rollout-*.jsonl           (best effort)

Every fact carries where it came from:

  recorded   the harness wrote it down when it happened: the tool call, its
             arguments, its result, is_error, "Exit code N", the file path an
             Edit/Write tool was given, the assistant's own words at the time.
  inferred   derived now by a named rule, for example a shell command whose
             text contains `sed -i` is inferred to have written that file.

Nothing here calls the network or a model. Secret-shaped strings are redacted
before any text leaves this module, and there is no switch to turn that off.
"""
from __future__ import annotations

import json
import os
import re
import shlex
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

MAX_FILE_BYTES = 64 * 1024 * 1024
RESULT_KEEP = 4000          # characters of each tool result kept in memory
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "str_replace_based_edit_tool"}
READ_TOOLS = {"Read", "NotebookRead"}
SEARCH_TOOLS = {"Grep", "Glob", "LS"}
SHELL_TOOLS = {"Bash", "shell", "local_shell", "exec_command", "container.exec", "BashOutput"}

# --------------------------------------------------------------------------- redaction

REDACTION_PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?(?:-----END [A-Z ]*PRIVATE KEY-----|$)")),
    ("aws-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("stripe-key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}")),
    ("google-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("npm-token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}")),
    ("bearer-token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._+/=-]{16,}")),
    ("url-credential", re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s/'\"@:]+:[^\s'\"@/]+@")),
    ("env-secret", re.compile(
        r"(?i)\b([A-Z0-9_]*(?:API_?KEY|SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL)S?)(\s*[=:]\s*)['\"]?[^\s'\"]{8,}")),
]


def redact(text: str, counter: dict | None = None) -> str:
    """Replace secret-shaped substrings with [REDACTED:<label>]. Always on."""
    if not text:
        return text
    for label, pattern in REDACTION_PATTERNS:
        def _sub(m, _label=label):
            if "[REDACTED:" in m.group(0):
                return m.group(0)
            if counter is not None:
                counter[_label] = counter.get(_label, 0) + 1
            if _label == "env-secret":
                return m.group(1) + m.group(2) + f"[REDACTED:{_label}]"
            return f"[REDACTED:{_label}]"
        text = pattern.sub(_sub, text)
    return text


# --------------------------------------------------------------------------- data model

@dataclass
class Effect:
    path: str
    kind: str        # write | read | delete | move
    basis: str       # recorded | inferred
    rule: str        # what recorded it, or the rule that inferred it


@dataclass
class Step:
    n: int
    ts: str | None
    role: str                 # user | assistant | tool
    tool: str | None = None
    call_id: str | None = None
    target: str = ""          # file path, command or query, redacted
    text: str = ""            # user/assistant text, or the tool result, redacted
    args: dict = field(default_factory=dict)
    status: str = ""          # ok | error | no-result | "" for text steps
    exit_code: int | None = None
    exit_basis: str = ""      # recorded | inferred | ""
    effects: list = field(default_factory=list)
    turn: int = 0             # index of the assistant message that issued it
    stated: str = ""          # assistant text in the same message (its reason at the time)
    output_fail: bool = False  # exited 0, but its output reports failures (e.g. `pytest | tail`)

    def as_dict(self) -> dict:
        d = {
            "step": self.n, "ts": self.ts, "role": self.role, "tool": self.tool,
            "target": self.target, "status": self.status or None,
            "exit_code": self.exit_code, "exit_basis": self.exit_basis or None,
            "effects": [vars(e) for e in self.effects],
        }
        if self.output_fail:
            d["output_reports_failure"] = True
        if self.role != "tool":
            d["text"] = self.text
        else:
            d["result"] = self.text[:600]
            if self.stated:
                d["stated_reason"] = self.stated[:400]
        return d


@dataclass
class Session:
    id: str
    path: str
    harness: str
    cwd: str | None = None
    started: str | None = None
    ended: str | None = None
    subagent: bool = False
    steps: list = field(default_factory=list)
    redactions: dict = field(default_factory=dict)

    @property
    def tool_steps(self):
        return [s for s in self.steps if s.role == "tool"]

    def summary(self) -> dict:
        tools = self.tool_steps
        written = sorted({e.path for s in tools for e in s.effects if e.kind in ("write", "delete", "move")})
        first_user = next((s.text for s in self.steps if s.role == "user" and not s.text.lstrip().startswith("<")), "")
        return {
            "session": self.id, "harness": self.harness, "path": self.path, "cwd": self.cwd,
            "started": self.started, "ended": self.ended, "subagent": self.subagent,
            "tool_calls": len(tools), "errors": sum(1 for s in tools if s.status == "error" or s.output_fail),
            "files_written": written, "first_prompt": first_user[:160],
            "redactions": self.redactions,
        }


# --------------------------------------------------------------------------- helpers

FAIL_TEXT = re.compile(r"(^FAILED\b|^FAIL: |^ERROR: |^Traceback \(most recent|\b[1-9]\d* failed\b|\(failures=\d+|\(errors=\d+)", re.M)
EXIT_RE = re.compile(r"^\s*(?:Exit code|exit code:?|Process exited with code)\s*(-?\d+)", re.I | re.M)


def block_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for b in content:
            if isinstance(b, dict):
                if b.get("type") == "text" and isinstance(b.get("text"), str):
                    out.append(b["text"])
                elif b.get("type") == "image":
                    out.append("[image]")
            elif isinstance(b, str):
                out.append(b)
        return "\n".join(out)
    if content is None:
        return ""
    return str(content)


INJECTED_MARKERS = ("<system-reminder>", "<command-name>", "<local-command-stdout>",
                    "<command-message>", "Caveat: The messages below", "[Request interrupted")


def looks_injected(text: str) -> bool:
    head = text.lstrip()[:200]
    return any(head.startswith(m) or m in head for m in INJECTED_MARKERS)


def norm_path(p: str, cwd: str | None) -> str:
    if not p:
        return p
    p = p.strip().strip("'\"")
    if cwd and not os.path.isabs(p) and not p.startswith("~"):
        p = os.path.normpath(os.path.join(cwd, p))
    return os.path.normpath(p) if p.startswith("/") else p


def path_matches(effect_path: str, query: str, cwd: str | None) -> bool:
    """A query matches a path if it equals it, or is a suffix at a path boundary."""
    if not effect_path or not query:
        return False
    q = query.strip()
    full_q = norm_path(q, cwd) if cwd else q
    if effect_path == full_q or effect_path == q:
        return True
    q2 = q.lstrip("./")
    return effect_path.endswith("/" + q2) or effect_path == q2


# Shell commands whose text implies a file effect. Each is a named rule, and every
# effect it produces is labelled inferred: the recording holds the command, not
# the filesystem change.


HEREDOC_RE = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1[^\n]*\n.*?\n\s*\2\s*(?=\n|$)", re.S)


def strip_heredocs(command: str) -> str:
    """Drop heredoc bodies: their text is data for the command, not shell syntax."""
    return HEREDOC_RE.sub(lambda m: "<<HEREDOC ", command)


def _tokenize(command: str):
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        return list(lex)
    except ValueError:
        return command.split()


SEPARATORS = {";", "&&", "||", "|", "&", "(", ")", ";;", "\n"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>"}


def shell_effects(command: str, cwd: str | None) -> list:
    effects = []
    if not command:
        return effects
    segments, cur = [], []
    tokens = _tokenize(strip_heredocs(command).replace("\n", " ; "))
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in REDIRECTS:
            if cur and isinstance(cur[-1], str) and cur[-1].isdigit():
                cur.pop()
            target = tokens[i + 1] if i + 1 < len(tokens) else ""
            if target and not target.startswith(("/dev/", "&")) and target not in SEPARATORS:
                cur.append(("redirect", target))
            i += 2
            continue
        if tok in (">&", "<", "<<", "<<<", "<&"):
            if cur and isinstance(cur[-1], str) and cur[-1].isdigit():
                cur.pop()
            i += 2
            continue
        if tok in SEPARATORS:
            segments.append(cur)
            cur = []
        else:
            cur.append(tok)
        i += 1
    segments.append(cur)
    for words in segments:
        for w in [w for w in words if isinstance(w, tuple)]:
            effects.append(Effect(norm_path(w[1], cwd), "write", "inferred", "shell-redirect"))
        words = [w for w in words if not isinstance(w, tuple)]
        if words and words[0] in ("cd", "pushd") and len(words) > 1:
            cwd = norm_path(words[1], cwd) if not words[1].startswith("~") else words[1]
            continue
        while words and (re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0]) or words[0] in ("sudo", "command", "time", "env")):
            words = words[1:]
        if not words:
            continue
        cmd, rest = os.path.basename(words[0]), words[1:]
        plain = [w for w in rest if not w.startswith("-")]
        if cmd == "tee":
            for w in plain:
                effects.append(Effect(norm_path(w, cwd), "write", "inferred", "shell-tee"))
        elif cmd in ("sed", "perl") and any(w.startswith("-i") or w == "--in-place" or (cmd == "perl" and w.startswith("-") and "i" in w) for w in rest):
            if cmd == "sed" and "-e" in rest:
                scripts = {rest[k + 1] for k, w in enumerate(rest[:-1]) if w == "-e"}
                files = [w for w in plain if w not in scripts]
            else:
                files = plain[1:]
            for w in files:
                effects.append(Effect(norm_path(w, cwd), "write", "inferred", f"shell-{cmd}-inplace"))
        elif cmd in ("rm", "unlink", "shred"):
            for w in plain:
                effects.append(Effect(norm_path(w, cwd), "delete", "inferred", "shell-rm"))
        elif cmd == "mv" and len(plain) >= 2:
            for w in plain[:-1]:
                effects.append(Effect(norm_path(w, cwd), "move", "inferred", "shell-mv-source"))
            effects.append(Effect(norm_path(plain[-1], cwd), "write", "inferred", "shell-mv-dest"))
        elif cmd in ("cp", "install", "rsync") and len(plain) >= 2:
            effects.append(Effect(norm_path(plain[-1], cwd), "write", "inferred", f"shell-{cmd}-dest"))
        elif cmd in ("touch", "truncate", "mkdir"):
            for w in plain:
                if not w.isdigit():
                    effects.append(Effect(norm_path(w, cwd), "write", "inferred", f"shell-{cmd}"))
        elif cmd == "git" and rest:
            sub = rest[0]
            args = [w for w in rest[1:] if not w.startswith("-")]
            if sub in ("checkout", "restore") and ("--" in rest or sub == "restore"):
                after = [w for w in rest[rest.index("--") + 1:]] if "--" in rest else args
                for w in after:
                    effects.append(Effect(norm_path(w, cwd), "write", "inferred", f"git-{sub}-discards"))
            elif sub == "reset" and "--hard" in rest:
                effects.append(Effect(norm_path(".", cwd), "write", "inferred", "git-reset-hard"))
            elif sub == "clean" and any(w.startswith("-") and "f" in w for w in rest):
                effects.append(Effect(norm_path(".", cwd), "delete", "inferred", "git-clean"))
            elif sub == "rm":
                for w in args:
                    effects.append(Effect(norm_path(w, cwd), "delete", "inferred", "git-rm"))
            elif sub == "mv" and len(args) >= 2:
                effects.append(Effect(norm_path(args[0], cwd), "move", "inferred", "git-mv-source"))
                effects.append(Effect(norm_path(args[-1], cwd), "write", "inferred", "git-mv-dest"))
            elif sub == "stash" and (not args or args[0] in ("push", "save")):
                effects.append(Effect(norm_path(".", cwd), "write", "inferred", "git-stash-reverts-tree"))
        elif cmd in ("cat", "head", "tail", "less", "wc", "grep", "rg"):
            for w in plain[-3:]:
                if "/" in w or re.search(r"\.[A-Za-z0-9]{1,6}$", w):
                    effects.append(Effect(norm_path(w, cwd), "read", "inferred", f"shell-{cmd}"))
    # de-duplicate
    seen, out = set(), []
    for e in effects:
        key = (e.path, e.kind, e.rule)
        if e.path and key not in seen:
            seen.add(key)
            out.append(e)
    return out


def patch_effects(patch: str, cwd: str | None) -> list:
    """Codex apply_patch payloads name their files; those effects are recorded."""
    out = []
    for m in re.finditer(r"^\*\*\* (Add|Update|Delete) File: (.+)$", patch or "", re.M):
        kind = {"Add": "write", "Update": "write", "Delete": "delete"}[m.group(1)]
        out.append(Effect(norm_path(m.group(2).strip(), cwd), kind, "recorded", "apply_patch"))
    for m in re.finditer(r"^\*\*\* Move to: (.+)$", patch or "", re.M):
        out.append(Effect(norm_path(m.group(1).strip(), cwd), "write", "recorded", "apply_patch-move"))
    return out


def tool_target_and_effects(name: str, args: dict, cwd: str | None) -> tuple:
    a = args if isinstance(args, dict) else {}
    fp = a.get("file_path") or a.get("notebook_path") or a.get("path") or ""
    if name in EDIT_TOOLS:
        p = norm_path(fp, cwd)
        return p, [Effect(p, "write", "recorded", f"{name}.file_path")]
    if name in READ_TOOLS:
        p = norm_path(fp, cwd)
        return p, [Effect(p, "read", "recorded", f"{name}.file_path")]
    if name in SEARCH_TOOLS:
        q = a.get("pattern") or ""
        return f"{q} {fp}".strip(), []
    if name in SHELL_TOOLS or "command" in a or "cmd" in a:
        cmd = a.get("command") or a.get("cmd") or ""
        if isinstance(cmd, list):
            cmd = " ".join(str(c) for c in cmd)
            if cmd.startswith(("bash -lc ", "bash -c ")):
                cmd = cmd.split(" ", 2)[2]
        wd = a.get("workdir") or a.get("cwd") or cwd
        return str(cmd), shell_effects(str(cmd), wd)
    if name == "apply_patch":
        patch = a.get("input") or a.get("patch") or ""
        effs = patch_effects(patch, cwd)
        return ", ".join(e.path for e in effs), effs
    if name == "Skill":
        return str(a.get("skill") or ""), []
    if name in ("Task", "Agent"):
        return str(a.get("description") or a.get("subagent_type") or ""), []
    if name in ("WebFetch", "WebSearch"):
        return str(a.get("url") or a.get("query") or ""), []
    if fp:
        return norm_path(fp, cwd), []
    try:
        return json.dumps(a, ensure_ascii=False)[:200], []
    except (TypeError, ValueError):
        return str(a)[:200], []


# --------------------------------------------------------------------------- parsers

def _read_lines(path: Path):
    with open(path, "rb") as fh:
        raw = fh.read(MAX_FILE_BYTES).decode("utf-8", errors="replace")
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(obj, dict):
            yield obj


def detect_harness(path: Path) -> str:
    for i, obj in enumerate(_read_lines(path)):
        if obj.get("type") in ("session_meta", "response_item", "event_msg", "turn_context"):
            return "codex"
        if obj.get("sessionId") or obj.get("session_id") or obj.get("type") in ("user", "assistant", "system"):
            return "claude"
        if i > 20:
            break
    return "claude"


def parse_session(path, include_text: bool = True) -> Session | None:
    path = Path(path).expanduser()
    try:
        harness = detect_harness(path)
        return _parse_codex(path) if harness == "codex" else _parse_claude(path)
    except OSError:
        return None


def _finish_tool(step: Step, result_text: str, is_error, counter: dict):
    step.text = redact(result_text[:RESULT_KEEP], counter)
    m = EXIT_RE.search(result_text[:300])
    if m:
        step.exit_code, step.exit_basis = int(m.group(1)), "recorded"
        step.status = "ok" if step.exit_code == 0 else "error"
    elif is_error is True:
        step.status = "error"
    elif is_error is False:
        step.status = "ok"
        if step.tool in SHELL_TOOLS:
            # Claude Code sets is_error on a non-zero exit, so false means exit 0.
            step.exit_code, step.exit_basis = 0, "recorded"
    else:
        step.status = "ok"
    if step.status == "ok" and step.tool in SHELL_TOOLS and FAIL_TEXT.search(result_text[:RESULT_KEEP]):
        step.output_fail = True
    if step.status == "error":
        # A failed Edit/Write did not write; keep the effect but mark it.
        for e in step.effects:
            if e.kind == "write" and e.basis == "recorded":
                e.rule += " (tool reported error: not applied)"


def _harness_diff(step: Step, tur):
    """Claude Code attaches `bashEditDiff` when a shell command changed a file it was
    tracking. That is the harness's own record, so it upgrades an inferred write."""
    if not isinstance(tur, dict):
        return
    files = (tur.get("bashEditDiff") or {}).get("files") if isinstance(tur.get("bashEditDiff"), dict) else None
    for f in files or []:
        fp = f.get("filePath") if isinstance(f, dict) else None
        if not fp:
            continue
        for e in step.effects:
            if e.path == fp and e.kind == "write":
                e.basis, e.rule = "recorded", "harness bashEditDiff (shell text: " + e.rule + ")"
                break
        else:
            step.effects.append(Effect(fp, "write", "recorded", "harness bashEditDiff"))


def _parse_claude(path: Path) -> Session | None:
    sess = Session(id=path.stem, path=str(path), harness="claude-code")
    pending: dict = {}
    seen_msg_ids: dict = {}
    n = 0
    turn = 0
    got_any = False
    for obj in _read_lines(path):
        ts = obj.get("timestamp")
        sid = obj.get("sessionId") or obj.get("session_id")
        if sid and sess.id == path.stem:
            sess.id = sid + (f"-{obj['agentId']}" if obj.get("agentId") else "")
        if obj.get("cwd") and not sess.cwd:
            sess.cwd = obj["cwd"]
        if obj.get("type") == "system" and obj.get("subtype") == "init" and obj.get("cwd"):
            sess.cwd = sess.cwd or obj["cwd"]
        if obj.get("isSidechain"):
            sess.subagent = True
        if ts:
            sess.started = sess.started or ts
            sess.ended = ts
        msg = obj.get("message")
        if obj.get("type") not in ("user", "assistant") or not isinstance(msg, dict):
            continue
        got_any = True
        role = msg.get("role") or obj["type"]
        content = msg.get("content")
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content or ""}]
        if role == "assistant":
            mid = msg.get("id") or obj.get("uuid")
            if mid not in seen_msg_ids:
                turn += 1
                seen_msg_ids[mid] = turn
            this_turn = seen_msg_ids[mid]
        else:
            this_turn = turn
        stated_parts = []
        for b in blocks:
            if not isinstance(b, dict):
                continue
            bt = b.get("type")
            if bt == "text":
                text = b.get("text") or ""
                if not isinstance(text, str) or not text.strip() or looks_injected(text):
                    continue
                n += 1
                sess.steps.append(Step(n, ts, role, text=redact(text[:RESULT_KEEP], sess.redactions), turn=this_turn))
                if role == "assistant":
                    stated_parts.append(text)
            elif bt == "tool_use":
                name = str(b.get("name") or "unknown")
                args = b.get("input") if isinstance(b.get("input"), dict) else {}
                target, effects = tool_target_and_effects(name, args, obj.get("cwd") or sess.cwd)
                n += 1
                st = Step(n, ts, "tool", tool=name, call_id=b.get("id"),
                          target=redact(str(target)[:500], sess.redactions), args=args,
                          effects=effects, turn=this_turn, status="no-result")
                # the assistant's words in this same message, recorded at the time
                same = [s.text for s in sess.steps if s.role == "assistant" and s.turn == this_turn]
                st.stated = " ".join(same)[-600:]
                sess.steps.append(st)
                if st.call_id:
                    pending[st.call_id] = st
            elif bt == "tool_result":
                st = pending.pop(b.get("tool_use_id"), None)
                if st is None:
                    continue
                _finish_tool(st, block_text(b.get("content")), b.get("is_error"), sess.redactions)
                _harness_diff(st, obj.get("toolUseResult"))
    if not got_any:
        return None
    return sess


def _parse_codex(path: Path) -> Session | None:
    sess = Session(id=path.stem, path=str(path), harness="codex")
    pending: dict = {}
    n = 0
    turn = 0
    got_any = False
    for obj in _read_lines(path):
        ts = obj.get("timestamp")
        if ts:
            sess.started = sess.started or ts
            sess.ended = ts
        typ = obj.get("type")
        p = obj.get("payload") if isinstance(obj.get("payload"), dict) else obj
        if typ == "session_meta":
            sess.id = p.get("id") or sess.id
            sess.cwd = p.get("cwd") or sess.cwd
            continue
        if typ == "turn_context":
            sess.cwd = sess.cwd or p.get("cwd")
            continue
        if typ != "response_item":
            continue
        got_any = True
        pt = p.get("type")
        if pt == "message":
            role = p.get("role")
            if role not in ("user", "assistant"):
                continue
            text = "\n".join(c.get("text", "") for c in p.get("content") or [] if isinstance(c, dict))
            if not text.strip() or looks_injected(text) or text.lstrip().startswith(("<environment_context>", "<user_instructions>")):
                continue
            if role == "assistant":
                turn += 1
            n += 1
            sess.steps.append(Step(n, ts, role, text=redact(text[:RESULT_KEEP], sess.redactions), turn=turn))
        elif pt in ("function_call", "custom_tool_call", "local_shell_call"):
            name = p.get("name") or ("local_shell" if pt == "local_shell_call" else "unknown")
            raw = p.get("arguments") if pt == "function_call" else p.get("input")
            if pt == "local_shell_call":
                args = (p.get("action") or {})
            elif isinstance(raw, str):
                try:
                    args = json.loads(raw)
                    if not isinstance(args, dict):
                        args = {"input": raw}
                except (json.JSONDecodeError, ValueError):
                    args = {"input": raw}
            else:
                args = raw if isinstance(raw, dict) else {}
            target, effects = tool_target_and_effects(name, args, sess.cwd)
            turn += 1
            n += 1
            st = Step(n, ts, "tool", tool=name, call_id=p.get("call_id") or p.get("id"),
                      target=redact(str(target)[:500], sess.redactions), args=args,
                      effects=effects, turn=turn, status="no-result")
            prev = [s.text for s in sess.steps[-2:] if s.role == "assistant"]
            st.stated = " ".join(prev)[-600:]
            sess.steps.append(st)
            if st.call_id:
                pending[st.call_id] = st
        elif pt in ("function_call_output", "custom_tool_call_output", "local_shell_call_output"):
            st = pending.pop(p.get("call_id"), None)
            if st is None:
                continue
            out = p.get("output")
            text, code = "", None
            if isinstance(out, dict):
                text = str(out.get("content") or out.get("output") or "")
            elif isinstance(out, str):
                text = out
                try:
                    o = json.loads(out)
                    if isinstance(o, dict):
                        text = str(o.get("output", text))
                        code = (o.get("metadata") or {}).get("exit_code")
                except (json.JSONDecodeError, ValueError):
                    pass
            _finish_tool(st, text, None, sess.redactions)
            if isinstance(code, int):
                st.exit_code, st.exit_basis = code, "recorded"
                st.status = "ok" if code == 0 else "error"
                st.output_fail = st.output_fail and code == 0
    return sess if got_any else None


# --------------------------------------------------------------------------- discovery

def parse_since(value: str | None):
    if not value:
        return None
    m = re.fullmatch(r"(\d+)\s*([hdw])", value.strip())
    if m:
        n, unit = int(m.group(1)), m.group(2)
        delta = {"h": timedelta(hours=n), "d": timedelta(days=n), "w": timedelta(weeks=n)}[unit]
        return datetime.now(timezone.utc) - delta
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        raise ValueError(f"--since must be like 36h, 7d, 2w or an ISO date, got {value!r}")


def parse_ts(ts: str | None):
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def default_homes():
    claude = Path(os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude").expanduser()
    codex = Path(os.environ.get("CODEX_HOME") or "~/.codex").expanduser()
    return claude, codex


def candidate_files(claude_home: Path, codex_home: Path, include_subagents: bool, since=None):
    files = []
    proj = claude_home / "projects"
    if proj.is_dir():
        files += proj.glob("*/*.jsonl")
        if include_subagents:
            files += proj.glob("*/*/subagents/*.jsonl")
    for sub in ("sessions", "archived_sessions"):
        d = codex_home / sub
        if d.is_dir():
            files += d.rglob("rollout-*.jsonl")
    out = []
    for f in files:
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, timezone.utc)
        except OSError:
            continue
        if since and mtime < since:
            continue
        out.append((mtime, f))
    out.sort(reverse=True)
    return [f for _, f in out]


def default_repo(start: str | None = None) -> str:
    """The git top level of the current directory, or the directory itself."""
    start = os.path.realpath(start or os.getcwd())
    d = start
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return start
        d = parent


def repo_matches(cwd: str | None, repo: str | None) -> bool:
    if not repo:
        return True
    if not cwd:
        return False
    a, b = os.path.realpath(cwd), os.path.realpath(repo)
    return a == b or a.startswith(b.rstrip("/") + "/")


def resolve_session(args) -> Session:
    """--trace PATH, --session ID (prefix ok) or --latest, shared by the CLIs."""
    if getattr(args, "trace", None):
        sess = parse_session(args.trace)
        if sess is None:
            raise FileNotFoundError(f"no readable session records in {args.trace}")
        return sess
    claude_home = Path(args.claude_home).expanduser()
    codex_home = Path(args.codex_home).expanduser()
    files = candidate_files(claude_home, codex_home, include_subagents=True)
    if getattr(args, "session", None):
        for f in files:
            if f.stem.startswith(args.session) or args.session in f.stem:
                sess = parse_session(f)
                if sess:
                    return sess
        for f in files:   # the id inside the file can differ from the filename
            sess = parse_session(f)
            if sess and sess.id.startswith(args.session):
                return sess
        raise FileNotFoundError(f"no session matching {args.session!r} under {claude_home} or {codex_home}")
    repo = default_repo(getattr(args, "repo", None))
    for f in files:
        sess = parse_session(f)
        if sess and not sess.subagent and repo_matches(sess.cwd, repo):
            return sess
    raise FileNotFoundError(f"no session recorded for {repo} under {claude_home} or {codex_home}")


def add_source_args(p):
    claude, codex = default_homes()
    src = p.add_argument_group("which run")
    src.add_argument("--trace", metavar="PATH", help="a session JSONL file (Claude Code or Codex)")
    src.add_argument("--session", metavar="ID", help="session id or prefix; searched under the homes below")
    src.add_argument("--latest", action="store_true", help="newest main session recorded for --repo (default)")
    src.add_argument("--repo", metavar="DIR", help="repo whose sessions --latest considers (default: cwd)")
    src.add_argument("--claude-home", default=str(claude), help=f"default {claude}")
    src.add_argument("--codex-home", default=str(codex), help=f"default {codex}")


# --------------------------------------------------------------------------- sample

def sample_records() -> list:
    """A small fictional Claude Code session used by every --sample flag.

    The story: asked to add retries, the agent edits client.py, fails a test,
    rewrites config.yaml with `sed -i` without saying so, gets the tests green,
    then edits client.py once more and reports "tests pass, config untouched".
    """
    sid, cwd = "sample-0001-forensics", "/work/shop-api"
    recs = []
    t = [0]

    def ts():
        t[0] += 1
        return f"2026-10-30T14:{t[0]:02d}:00Z"

    def user(text):
        recs.append({"type": "user", "sessionId": sid, "cwd": cwd, "timestamp": ts(),
                     "message": {"role": "user", "content": text}})

    def asst(mid, text=None, tool=None):
        content = []
        if text:
            content.append({"type": "text", "text": text})
        if tool:
            content.append({"type": "tool_use", "id": tool[0], "name": tool[1], "input": tool[2]})
        recs.append({"type": "assistant", "sessionId": sid, "cwd": cwd, "timestamp": ts(),
                     "message": {"id": mid, "role": "assistant", "content": content}})

    def result(tid, text, err=False):
        recs.append({"type": "user", "sessionId": sid, "cwd": cwd, "timestamp": ts(),
                     "message": {"role": "user", "content": [
                         {"type": "tool_result", "tool_use_id": tid, "content": text, "is_error": err}]}})

    user("Add retries with backoff to the HTTP client and make sure the tests pass.")
    asst("m1", "I'll read the client and its config first.", ("t1", "Read", {"file_path": "/work/shop-api/src/client.py"}))
    result("t1", "import requests\n\ndef fetch(url):\n    return requests.get(url, timeout=TIMEOUT)\n")
    asst("m2", None, ("t2", "Read", {"file_path": "/work/shop-api/config.yaml"}))
    result("t2", "timeout: 30\nretries: 0\napi_token: sk-ant-api03-FAKEFAKEFAKEFAKEFAKE00\n")
    asst("m3", "Adding a retry loop around requests.get.", ("t3", "Edit", {
        "file_path": "/work/shop-api/src/client.py", "old_string": "return requests.get", "new_string": "for i in range(RETRIES): ..."}))
    result("t3", "The file /work/shop-api/src/client.py has been updated.")
    asst("m4", None, ("t4", "Bash", {"command": "pytest -q tests/test_client.py"}))
    result("t4", "Exit code 1\nFAILED tests/test_client.py::test_retry_count - assert 0 == 3\n1 failed, 4 passed", True)
    asst("m5", "The test expects 3 retries; the config says 0. Setting it.", ("t5", "Bash", {
        "command": "sed -i 's/retries: 0/retries: 3/; s/timeout: 30/timeout: 5/' config.yaml"}))
    result("t5", "")
    asst("m6", None, ("t6", "Bash", {"command": "pytest -q tests/test_client.py"}))
    result("t6", "5 passed in 0.41s")
    asst("m7", "Tidying the backoff constant.", ("t7", "Edit", {
        "file_path": "/work/shop-api/src/client.py", "old_string": "BACKOFF = 1", "new_string": "BACKOFF = 0.5 * 2 ** i"}))
    result("t7", "The file /work/shop-api/src/client.py has been updated.")
    asst("m8", "Done. Retries with backoff are in src/client.py, the tests pass, and I didn't change config.yaml.")
    user("Why did the request timeout drop to 5 seconds in production?")
    return recs


def write_sample(tmpdir) -> str:
    p = Path(tmpdir) / "sample-0001-forensics.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in sample_records()) + "\n", encoding="utf-8")
    return str(p)


if __name__ == "__main__":
    import argparse
    import sys
    import tempfile
    ap = argparse.ArgumentParser(description="Shared trace parser for agent-run-forensics (a library; "
                                 "use trace_finder.py, trace_timeline.py or claim_checker.py). "
                                 "With --trace or --sample, prints the parsed steps as JSON.")
    ap.add_argument("--trace", help="parse this session JSONL")
    ap.add_argument("--sample", action="store_true", help="parse the built-in fictional session")
    ap.add_argument("--output", choices=("json",), default="json")
    a = ap.parse_args()
    if not a.trace and not a.sample:
        ap.print_help()
        sys.exit(0)
    with tempfile.TemporaryDirectory() as d:
        sess = parse_session(a.trace or write_sample(d))
        if sess is None:
            print("no readable session records", file=sys.stderr)
            sys.exit(3)
        print(json.dumps({"session": sess.summary(), "steps": [st.as_dict() for st in sess.steps]}, indent=2))
