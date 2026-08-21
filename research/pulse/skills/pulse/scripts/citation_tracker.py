#!/usr/bin/env python3
"""citation_tracker.py — JSON-backed three-count audit log for pulse runs.

Stdlib-only. Maintains the research-pack convention's three counts:

  - queries sent     (every tool call issued)
  - sources received (every item returned across all queries)
  - sources cited    (every unique URL in the final synthesis)

Session state persists in ~/.pulse_sessions/<session>.json so runs can be
inspected and resumed.

NO LLM CALLS. Pure JSON I/O + counters.

Actions:
  start             Create a new session file
  record_sent       Increment sent count + log the query
  record_received   Increment received count by N
  record_cited      Increment cited count + log the URL
  import_sources    Normalize a local X export and record unique sources
  status            Show current counts + audit summary block
  list              List existing sessions
  close             Finalize the session (set ended_at timestamp)

Usage:
    python citation_tracker.py --action start --session pulse-2026-05-15-claude-code --topic "Claude Code adoption"
    python citation_tracker.py --action record_sent --session pulse-... --query "claude code adoption" --platform reddit
    python citation_tracker.py --action record_received --session pulse-... --count 12 --platform reddit
    python citation_tracker.py --action record_cited --session pulse-... --url "https://reddit.com/..." --platform reddit
    python citation_tracker.py --action import_sources --session pulse-... --input x-search.json --platform x
    python citation_tracker.py --action status --session pulse-...
    python citation_tracker.py --action list
    python citation_tracker.py --action close --session pulse-...
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SESSIONS_DIR = Path.home() / ".pulse_sessions"
IMPORT_PROVIDERS = ("auto", "generic", "x-api-v2", "xquik")

SAMPLE_XQUIK_EXPORT: Dict[str, Any] = {
    "tweets": [
        {
            "id": "100",
            "text": "Public launch feedback",
            "createdAt": "2026-08-20T10:00:00Z",
            "likeCount": 7,
            "retweetCount": 2,
            "replyCount": 1,
            "author": {"id": "10", "username": "example"},
        },
        {
            "id": "100",
            "text": "Public launch feedback",
            "createdAt": "2026-08-20T10:00:00Z",
            "author": {"id": "10", "username": "example"},
        },
        {
            "id": "101",
            "text": "A second public response",
            "created_at": 1787223600,
            "author_username": "second_example",
            "public_metrics": {"like_count": 3, "repost_count": 1},
        },
    ],
    "has_more": False,
    "next_cursor": "",
}


def session_path(name: str) -> Path:
    return SESSIONS_DIR / f"{name}.json"


def load_session(name: str) -> Dict[str, Any]:
    p = session_path(name)
    if not p.exists():
        raise FileNotFoundError(f"Session not found: {name} (looked at {p})")
    return json.loads(p.read_text(encoding="utf-8"))


def save_session(name: str, data: Dict[str, Any]) -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    session_path(name).write_text(json.dumps(data, indent=2), encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def first_value(data: Dict[str, Any], names: Tuple[str, ...]) -> Any:
    for name in names:
        value = data.get(name)
        if value is not None:
            return value
    return None


def parse_timestamp(value: Any) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, timezone.utc)
    if not isinstance(value, str):
        raise ValueError(f"unsupported timestamp {value!r}")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def integer_value(data: Dict[str, Any], names: Tuple[str, ...]) -> int:
    value = first_value(data, names)
    if value is None:
        return 0
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def detect_provider(payload: Any) -> str:
    if isinstance(payload, dict):
        if isinstance(payload.get("tweets"), list):
            return "xquik"
        if isinstance(payload.get("data"), list):
            return "x-api-v2"
    return "generic"


def extract_rows(payload: Any, provider: str) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        if provider == "xquik":
            if not isinstance(payload.get("tweets"), list):
                raise ValueError("Xquik import must contain a tweets array")
            rows = payload["tweets"]
        elif provider == "x-api-v2":
            if not isinstance(payload.get("data"), list):
                raise ValueError("X API v2 import must contain a data array")
            rows = payload["data"]
        elif first_value(payload, ("id", "tweet_id", "tweetId", "id_str")) is not None:
            rows = [payload]
        else:
            key = next(
                (candidate for candidate in ("records", "items", "results", "tweets", "data")
                 if isinstance(payload.get(candidate), list)),
                "",
            )
            if not key:
                raise ValueError("generic import must be a Tweet object, array, or known list container")
            rows = payload[key]
    else:
        raise ValueError("import root must be a JSON object or array")
    return [row for row in rows if isinstance(row, dict)]


def x_api_users(payload: Any) -> Dict[str, Dict[str, Any]]:
    if not isinstance(payload, dict):
        return {}
    includes = payload.get("includes")
    if not isinstance(includes, dict) or not isinstance(includes.get("users"), list):
        return {}
    return {
        str(user["id"]): user
        for user in includes["users"]
        if isinstance(user, dict) and user.get("id") is not None
    }


def normalize_row(row: Dict[str, Any], users: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    tweet_id = first_value(row, ("id", "tweet_id", "tweetId", "id_str"))
    text = first_value(row, ("text", "full_text", "fullText"))
    if tweet_id is None or not isinstance(text, str) or not text.strip():
        return None

    embedded_author = row.get("author") if isinstance(row.get("author"), dict) else {}
    author_id = first_value(row, ("author_id", "authorId")) or first_value(
        embedded_author, ("id", "id_str")
    )
    included_author = users.get(str(author_id), {}) if author_id is not None else {}
    username = first_value(row, ("author_username", "authorUsername", "username"))
    if username is None:
        username = first_value(embedded_author, ("username", "screen_name", "screenName"))
    if username is None:
        username = first_value(included_author, ("username", "screen_name"))

    metrics = row.get("public_metrics") if isinstance(row.get("public_metrics"), dict) else row
    identifier = str(tweet_id)
    source_url = first_value(row, ("url", "permalink", "tweet_url", "tweetUrl"))
    if not source_url:
        account = str(username).lstrip("@") if username else "i/web"
        source_url = f"https://x.com/{account}/status/{identifier}"

    return {
        "id": identifier,
        "url": str(source_url),
        "text": text.strip(),
        "created_at": first_value(row, ("created_at", "createdAt")),
        "author": {
            "id": str(author_id) if author_id is not None else None,
            "username": str(username).lstrip("@") if username else None,
        },
        "metrics": {
            "likes": integer_value(metrics, ("like_count", "likeCount", "favorite_count")),
            "reposts": integer_value(
                metrics, ("repost_count", "retweet_count", "retweetCount")
            ),
            "replies": integer_value(metrics, ("reply_count", "replyCount")),
            "quotes": integer_value(metrics, ("quote_count", "quoteCount")),
            "views": integer_value(metrics, ("view_count", "viewCount", "impression_count")),
            "bookmarks": integer_value(metrics, ("bookmark_count", "bookmarkCount")),
        },
    }


def normalize_export(
    payload: Any,
    provider: str = "auto",
    since: Optional[str] = None,
    until: Optional[str] = None,
) -> Dict[str, Any]:
    selected_provider = detect_provider(payload) if provider == "auto" else provider
    rows = extract_rows(payload, selected_provider)
    users = x_api_users(payload)
    since_at = parse_timestamp(since)
    until_at = parse_timestamp(until)
    if since_at and until_at and since_at >= until_at:
        raise ValueError("--since must be earlier than --until")

    sources: List[Dict[str, Any]] = []
    seen_ids = set()
    duplicates = 0
    filtered = 0
    malformed = 0
    for row in rows:
        source = normalize_row(row, users)
        if source is None:
            malformed += 1
            continue
        if source["id"] in seen_ids:
            duplicates += 1
            continue
        seen_ids.add(source["id"])
        if since_at or until_at:
            try:
                created_at = parse_timestamp(source.get("created_at"))
            except ValueError:
                malformed += 1
                continue
            if created_at is None:
                malformed += 1
                continue
            if since_at and created_at < since_at:
                filtered += 1
                continue
            if until_at and created_at >= until_at:
                filtered += 1
                continue
        sources.append(source)

    return {
        "provider": selected_provider,
        "input_count": len(rows),
        "accepted_count": len(sources),
        "duplicate_count": duplicates,
        "filtered_count": filtered,
        "malformed_count": malformed,
        "sources": sources,
    }


def load_export(path: str) -> Tuple[Any, Dict[str, str]]:
    input_path = Path(path).expanduser()
    try:
        raw = input_path.read_text(encoding="utf-8")
        payload = json.loads(raw)
    except OSError as exc:
        raise ValueError(f"cannot read import: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"import is not valid JSON: {exc}") from exc
    return payload, {
        "input_name": input_path.name,
        "input_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
    }


def action_start(name: str, topic: Optional[str]) -> Dict[str, Any]:
    if session_path(name).exists():
        raise FileExistsError(f"Session already exists: {name}")
    data: Dict[str, Any] = {
        "session": name,
        "topic": topic or "",
        "started_at": now_iso(),
        "ended_at": None,
        "queries_sent": [],
        "sources_received": [],
        "sources_cited": [],
        "source_imports": [],
        "imported_sources": [],
        "counts": {"sent": 0, "received": 0, "cited": 0},
    }
    save_session(name, data)
    return data


def action_record_sent(name: str, query: str, platform: str) -> Dict[str, Any]:
    data = load_session(name)
    data["queries_sent"].append({"query": query, "platform": platform, "at": now_iso()})
    data["counts"]["sent"] += 1
    save_session(name, data)
    return data


def action_record_received(name: str, count: int, platform: str) -> Dict[str, Any]:
    if count < 0:
        raise ValueError("--count cannot be negative")
    data = load_session(name)
    data["sources_received"].append({"count": count, "platform": platform, "at": now_iso()})
    data["counts"]["received"] += count
    save_session(name, data)
    return data


def action_record_cited(name: str, url: str, platform: str) -> Dict[str, Any]:
    data = load_session(name)
    if any(source.get("url") == url for source in data["sources_cited"]):
        return data
    data["sources_cited"].append({"url": url, "platform": platform, "at": now_iso()})
    data["counts"]["cited"] += 1
    save_session(name, data)
    return data


def action_import_sources(
    name: str,
    input_path: str,
    platform: str,
    provider: str,
    since: Optional[str],
    until: Optional[str],
) -> Dict[str, Any]:
    payload, provenance = load_export(input_path)
    report = normalize_export(payload, provider, since, until)
    data = load_session(name)
    imported_sources = data.setdefault("imported_sources", [])
    existing_ids = {source.get("id") for source in imported_sources}
    new_sources = [source for source in report["sources"] if source["id"] not in existing_ids]
    imported_sources.extend(new_sources)
    data.setdefault("source_imports", []).append({
        **provenance,
        "platform": platform,
        "provider": report["provider"],
        "input_count": report["input_count"],
        "accepted_count": len(new_sources),
        "duplicate_count": report["duplicate_count"] + len(report["sources"]) - len(new_sources),
        "filtered_count": report["filtered_count"],
        "malformed_count": report["malformed_count"],
        "at": now_iso(),
    })
    data["sources_received"].append({
        "count": len(new_sources),
        "platform": platform,
        "kind": "local_import",
        "at": now_iso(),
    })
    data["counts"]["received"] += len(new_sources)
    save_session(name, data)
    return data


def action_status(name: str) -> Dict[str, Any]:
    return load_session(name)


def action_close(name: str) -> Dict[str, Any]:
    data = load_session(name)
    if data.get("ended_at") is None:
        data["ended_at"] = now_iso()
        save_session(name, data)
    return data


def action_list() -> List[Dict[str, Any]]:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    out: List[Dict[str, Any]] = []
    for p in sorted(SESSIONS_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            out.append({
                "session": data.get("session", p.stem),
                "topic": data.get("topic", ""),
                "started_at": data.get("started_at", ""),
                "ended_at": data.get("ended_at"),
                "counts": data.get("counts", {}),
            })
        except (OSError, json.JSONDecodeError):
            continue
    return out


def render_status_human(data: Dict[str, Any]) -> str:
    out: List[str] = []
    out.append(f"Session:        {data['session']}")
    out.append(f"Topic:          {data.get('topic', '(unset)')}")
    out.append(f"Started:        {data['started_at']}")
    out.append(f"Ended:          {data.get('ended_at') or '(active)'}")
    out.append("")
    out.append("Three-count audit:")
    c = data["counts"]
    out.append(f"  Sent:         {c['sent']}")
    out.append(f"  Received:     {c['received']}")
    out.append(f"  Cited:        {c['cited']}")
    out.append("")
    # Per-platform breakdown
    by_platform_sent: Dict[str, int] = {}
    for q in data["queries_sent"]:
        by_platform_sent[q["platform"]] = by_platform_sent.get(q["platform"], 0) + 1
    if by_platform_sent:
        out.append("Sent by platform:")
        for plat, n in sorted(by_platform_sent.items(), key=lambda kv: -kv[1]):
            out.append(f"  {plat:<10s} {n}")
    imports = data.get("source_imports", [])
    if imports:
        out.append("Local imports:")
        for item in imports:
            out.append(
                f"  {item.get('input_name', '(unknown)')}: "
                f"{item.get('accepted_count', 0)}/{item.get('input_count', 0)} accepted "
                f"({item.get('provider', 'generic')})"
            )
    out.append("")
    out.append("Audit block (paste in synthesis):")
    parts: List[str] = []
    for plat, n in sorted(by_platform_sent.items(), key=lambda kv: -kv[1]):
        parts.append(f"{plat}: {n}")
    breakdown = " (" + ", ".join(parts) + ")" if parts else ""
    out.append(
        f"  *Audit:* Queries sent: {c['sent']}{breakdown}. "
        f"Sources received: {c['received']}. Sources cited: {c['cited']}. "
        f"Training knowledge: 0 ([Background] excluded from count)."
    )
    return "\n".join(out)


def render_list_human(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "(no sessions found)"
    out: List[str] = []
    out.append(f"{'session':<55s}  {'sent':>4s} {'recv':>4s} {'cited':>5s}  status")
    out.append("-" * 88)
    for r in rows:
        c = r["counts"]
        status = "closed" if r.get("ended_at") else "active"
        out.append(
            f"{r['session']:<55s}  {c.get('sent', 0):>4d} {c.get('received', 0):>4d} {c.get('cited', 0):>5d}  {status}"
        )
    return "\n".join(out)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--action",
        choices=[
            "start", "record_sent", "record_received", "record_cited",
            "import_sources", "status", "list", "close",
        ],
    )
    parser.add_argument("--session", help="Session name")
    parser.add_argument("--topic", help="(start only) topic string")
    parser.add_argument("--query", help="(record_sent only) the query text")
    parser.add_argument("--platform", help="(record_* only) platform name: reddit | hn | web | x | other")
    parser.add_argument("--count", type=int, help="(record_received only) number of sources received")
    parser.add_argument("--url", help="(record_cited only) cited URL")
    parser.add_argument("--input", help="(import_sources only) local JSON export")
    parser.add_argument(
        "--provider", choices=IMPORT_PROVIDERS, default="auto",
        help="(import_sources only) input schema; default: auto",
    )
    parser.add_argument("--since", help="(import_sources only) inclusive ISO timestamp")
    parser.add_argument("--until", help="(import_sources only) exclusive ISO timestamp")
    parser.add_argument("--sample", action="store_true", help="normalize a built-in Xquik sample")
    parser.add_argument("--output", choices=["human", "json"], default="human")
    parser.add_argument("--json", action="store_true", help="alias for --output json")
    args = parser.parse_args(argv)

    output = "json" if args.json else args.output
    if args.sample:
        result = normalize_export(
            SAMPLE_XQUIK_EXPORT,
            since="2026-08-20T00:00:00Z",
            until="2026-08-21T00:00:00Z",
        )
        if output == "json":
            print(json.dumps(result, indent=2))
        else:
            print(
                f"Provider: {result['provider']}\n"
                f"Accepted: {result['accepted_count']}\n"
                f"Duplicates: {result['duplicate_count']}"
            )
        return 0
    if not args.action:
        parser.error("--action is required unless --sample is used")

    try:
        if args.action == "start":
            if not args.session:
                print("error: --session required for start", file=sys.stderr)
                return 2
            result = action_start(args.session, args.topic)
        elif args.action == "record_sent":
            if not (args.session and args.query and args.platform):
                print("error: --session, --query, --platform required for record_sent", file=sys.stderr)
                return 2
            result = action_record_sent(args.session, args.query, args.platform)
        elif args.action == "record_received":
            if not (args.session and args.count is not None and args.platform):
                print("error: --session, --count, --platform required for record_received", file=sys.stderr)
                return 2
            result = action_record_received(args.session, args.count, args.platform)
        elif args.action == "record_cited":
            if not (args.session and args.url and args.platform):
                print("error: --session, --url, --platform required for record_cited", file=sys.stderr)
                return 2
            result = action_record_cited(args.session, args.url, args.platform)
        elif args.action == "import_sources":
            if not (args.session and args.input):
                print("error: --session and --input required for import_sources", file=sys.stderr)
                return 2
            result = action_import_sources(
                args.session, args.input, args.platform or "x", args.provider,
                args.since, args.until,
            )
        elif args.action == "status":
            if not args.session:
                print("error: --session required for status", file=sys.stderr)
                return 2
            result = action_status(args.session)
        elif args.action == "close":
            if not args.session:
                print("error: --session required for close", file=sys.stderr)
                return 2
            result = action_close(args.session)
        else:  # list
            result = action_list()
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if output == "json":
        print(json.dumps(result, indent=2, default=str))
    else:
        if args.action == "list":
            print(render_list_human(result))
        else:
            print(render_status_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
