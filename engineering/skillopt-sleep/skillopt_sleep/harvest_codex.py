"""SkillOpt-Sleep Codex Desktop session harvesting.

Reads Codex Desktop archived session JSONL files and normalizes them into
``SessionDigest`` records without copying developer/system instructions, tool
arguments, or raw tool outputs.
"""
from __future__ import annotations

import os
import re
from typing import Any, Dict, Iterable, List, Optional

from skillopt_sleep.harvest import (
    _detect_feedback,
    _is_meta_prompt,
    _iter_jsonl,
    _project_matches,
)
from skillopt_sleep.staging import _SECRET_PATTERNS
from skillopt_sleep.types import SessionDigest


def _payload(rec: Dict[str, Any]) -> Dict[str, Any]:
    payload = rec.get("payload")
    return payload if isinstance(payload, dict) else {}


def _timestamp(rec: Dict[str, Any], payload: Dict[str, Any]) -> str:
    for value in (
        payload.get("timestamp"),
        rec.get("timestamp"),
        payload.get("started_at"),
        payload.get("completed_at"),
    ):
        if isinstance(value, str) and value:
            return value
    return ""


def _text_from_any(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if item.get("type") == "text" and item.get("text"):
                    parts.append(str(item["text"]))
                elif item.get("text"):
                    parts.append(str(item["text"]))
        return "\n".join(parts)
    if isinstance(content, dict):
        if content.get("text"):
            return str(content["text"])
        if content.get("content"):
            return _text_from_any(content["content"])
    return ""


def _strip_codex_meta(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""
    if stripped.startswith("<codex_internal_context"):
        return ""
    if stripped.startswith("<environment_context"):
        return ""
    if stripped.startswith("# AGENTS.md instructions") or "--- project-doc ---" in stripped:
        for marker in ("</environment_context>", "</INSTRUCTIONS>"):
            idx = stripped.rfind(marker)
            if idx == -1:
                continue
            tail = stripped[idx + len(marker):].strip()
            if tail and not tail.startswith("<"):
                return tail
        return ""
    return stripped


def _sanitize_text(text: str) -> str:
    sanitized = _strip_codex_meta(text).replace("\x00", "").strip()
    if not sanitized or _is_meta_prompt(sanitized):
        return ""
    for pattern, replacement in _SECRET_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized


def _sanitize_tool_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", name)[:80]


def _tool_name(payload: Dict[str, Any]) -> str:
    payload_type = payload.get("type")
    name = payload.get("name")
    if isinstance(name, str) and name:
        return _sanitize_tool_name(name)
    if payload_type == "exec_command_end":
        return "exec_command"
    if payload_type == "patch_apply_end":
        return "apply_patch"
    if payload_type == "web_search_call":
        return "web_search"
    if payload_type == "tool_search_call":
        return "tool_search"
    if isinstance(payload_type, str) and payload_type.endswith("_tool_call"):
        return _sanitize_tool_name(payload_type)
    return ""


def _dedup(xs: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def digest_codex_archived_session(path: str, project: str = "") -> Optional[SessionDigest]:
    """Build a ``SessionDigest`` from one Codex Desktop archived session."""
    session_id = os.path.splitext(os.path.basename(path))[0]
    started = ""
    ended = ""
    session_project = ""
    user_prompts: List[str] = []
    assistant_finals: List[str] = []
    tools: List[str] = []
    feedback: List[str] = []
    n_user = 0
    n_asst = 0

    for rec in _iter_jsonl(path):
        payload = _payload(rec)
        payload_type = payload.get("type")
        ts = _timestamp(rec, payload)
        if ts:
            if not started:
                started = ts
            ended = ts
        cwd = payload.get("cwd")
        if isinstance(cwd, str) and cwd:
            if not session_project:
                session_project = cwd
            if project and _project_matches(cwd, "invoked", project):
                session_project = cwd

        role = payload.get("role")
        text = ""
        output_role = ""
        if payload_type == "user_message":
            text = _text_from_any(payload.get("message"))
            output_role = "user"
        elif payload_type == "agent_message":
            text = _text_from_any(payload.get("message"))
            output_role = "assistant"
        elif payload_type == "message" and role in {"user", "assistant"}:
            text = _text_from_any(payload.get("content"))
            output_role = str(role)
        else:
            tool = _tool_name(payload)
            if tool:
                tools.append(tool)
            continue

        sanitized = _sanitize_text(text)
        if not sanitized:
            continue
        if output_role == "user":
            n_user += 1
            user_prompts.append(sanitized)
            feedback.extend(_detect_feedback(sanitized))
        elif output_role == "assistant":
            n_asst += 1
            assistant_finals.append(sanitized)

    if project and not _project_matches(session_project or "", "invoked", project):
        return None
    if n_user == 0 and n_asst == 0:
        return None

    return SessionDigest(
        session_id=session_id,
        project=session_project,
        started_at=started,
        ended_at=ended,
        user_prompts=user_prompts,
        assistant_finals=assistant_finals[-5:],
        tools_used=_dedup(tools),
        files_touched=[],
        feedback_signals=feedback,
        n_user_turns=n_user,
        n_assistant_turns=n_asst,
        raw_path=path,
    )


def harvest_codex(
    archived_sessions_dir: str,
    *,
    scope: Any = "all",
    invoked_project: str = "",
    since_iso: Optional[str] = None,
    limit: int = 0,
) -> List[SessionDigest]:
    """Walk ``~/.codex/archived_sessions`` and return matching digests."""
    digests: List[SessionDigest] = []
    if not os.path.isdir(archived_sessions_dir):
        return digests

    paths = [
        os.path.join(archived_sessions_dir, fn)
        for fn in os.listdir(archived_sessions_dir)
        if fn.endswith(".jsonl")
    ]
    paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)

    project_hint = invoked_project if scope == "invoked" else ""
    for path in paths:
        digest = digest_codex_archived_session(path, project=project_hint)
        if digest is None:
            continue
        if not _project_matches(digest.project or "", scope, invoked_project):
            continue
        if since_iso and digest.ended_at and digest.ended_at < since_iso:
            continue
        digests.append(digest)
        if limit and len(digests) >= limit:
            break
    return digests
