#!/usr/bin/env python3
"""Inventory every MCP server, plugin and marketplace a team's Claude Code can load.

Each MCP server is code running with the developer's credentials, and each
plugin can bring its own hooks, agents and MCP servers. Before a rollout
someone has to be able to answer "what can our agents reach?" in one table.
This script builds that table from the files a team ships and checks it
against an approved list when you have one.

Sources read:
  <repo>/.mcp.json                 project-scope servers (committed)
  <repo>/.claude/settings.json     enabledPlugins, extraKnownMarketplaces, MCP approval keys
  --claude-json ~/.claude.json     local- and user-scope servers (optional, per developer)
  --managed managed-settings.json  managed plugin/marketplace policy (optional)

Checks:
  M1 [BLOCKER] literal credential in a committed server's env, headers, args or url (use ${VAR})
  M2 [WARN]    package launcher without a pinned version (npx/uvx/bunx/pipx ... @latest or no version)
  M3 [WARN]    remote server over plain http (not localhost)
  M4 [BLOCKER] server, plugin or marketplace missing from --allowlist
  M5 [WARN]    project servers auto-approved by enableAllProjectMcpServers
  M6 [WARN]    marketplace git source without a pinned ref

Deterministic, stdlib only, no network.

Exit codes:
    0  inventory clean
    2  warnings
    3  invalid input
    4  blocker (unapproved component or committed credential)
"""

import argparse
import json
import os
import re
import sys

LAUNCHERS = {"npx", "uvx", "bunx", "pipx", "pnpm", "dlx"}
VERSIONED = re.compile(r"@\d|==\d|@v\d|:\d+\.\d+")
SECRET_VALUE = re.compile(r"(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_|AKIA[0-9A-Z]{16}|xox[baprs]-|Bearer\s+[A-Za-z0-9._-]{16,})")
URL_PASSWORD = re.compile(r"://[^/\s:@]+:(?!\$\{)[^@\s/]+@")
SECRET_NAME = re.compile(r"(KEY|TOKEN|SECRET|PASSWORD|AUTHORIZATION|CREDENTIAL)", re.I)

SAMPLE = {
    "mcp_json": {"mcpServers": {
        "github": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"],
                   "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_abcdefghijklmnopqrstuvwxyz0123"}},
        "postgres": {"command": "uvx", "args": ["mcp-server-postgres==0.6.2", "${DATABASE_URL}"]},
        "docs": {"type": "http", "url": "https://docs.example.com/mcp", "headers": {"Authorization": "Bearer ${DOCS_TOKEN}"}},
        "metrics": {"type": "sse", "url": "http://metrics.internal:8080/sse"},
    }},
    "settings": {
        "enableAllProjectMcpServers": True,
        "enabledPlugins": {"code-review@claude-plugins-official": True, "random-tools@someone-market": True},
        "extraKnownMarketplaces": {"someone-market": {"source": {"source": "github", "repo": "someone/market"}}},
    },
    "allowlist": {"servers": ["github", "postgres", "docs"], "plugins": ["code-review@claude-plugins-official"],
                  "marketplaces": ["claude-plugins-official"]},
}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def load(path):
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        _fail(f"cannot read {path}: {exc}")


def describe(server):
    if server.get("url"):
        return server.get("type", "http"), server["url"]
    cmd = " ".join([str(server.get("command", ""))] + [str(a) for a in server.get("args", [])])
    return server.get("type", "stdio"), cmd.strip()


def check_server(name, server, scope, committed, auto_approved, allow):
    findings = []
    transport, target = describe(server)
    blobs = dict(server.get("env") or {}, **(server.get("headers") or {}))
    for k, v in blobs.items():
        v = str(v)
        literal = "${" not in v
        if committed and literal and (SECRET_VALUE.search(v) or (SECRET_NAME.search(k) and v)):
            findings.append(("M1", "BLOCKER", f"'{k}' is a literal credential in a committed file; use ${{{k}}}"))
    for where, v in [("url", server.get("url", ""))] + [(f"args[{i}]", a) for i, a in enumerate(server.get("args") or [])]:
        v = str(v)
        if committed and (SECRET_VALUE.search(v) or URL_PASSWORD.search(v)):
            findings.append(("M1", "BLOCKER", f"{where} carries a literal credential in a committed file; pass it via ${{VAR}}"))
    cmd = os.path.basename(str(server.get("command", "")))
    if cmd in LAUNCHERS:
        pkgs = [a for a in server.get("args", []) if not str(a).startswith("-") and not str(a).startswith("${")]
        pkg = str(pkgs[0]) if pkgs else ""
        if pkg and ("@latest" in pkg or not VERSIONED.search(pkg)):
            findings.append(("M2", "WARN", f"'{pkg}' is not pinned; every session may run different code"))
    url = str(server.get("url", ""))
    if url.startswith("http://") and not re.match(r"http://(localhost|127\.0\.0\.1|\[::1\])", url):
        findings.append(("M3", "WARN", "remote server over plain http"))
    if allow is not None and name not in allow.get("servers", []) and url not in allow.get("servers", []):
        findings.append(("M4", "BLOCKER", "not on the approved server list"))
    if auto_approved:
        findings.append(("M5", "WARN", "auto-approved by enableAllProjectMcpServers"))
    return {"kind": "mcp", "name": name, "scope": scope, "transport": transport, "target": target[:90],
            "findings": [{"id": i, "severity": s, "message": m} for i, s, m in findings]}


def build(mcp_json, settings, claude_json, managed, allow, repo_path=None):
    items = []
    settings = settings or {}
    auto = bool(settings.get("enableAllProjectMcpServers"))
    for name, srv in ((mcp_json or {}).get("mcpServers") or {}).items():
        items.append(check_server(name, srv, "project", True, auto, allow))
    if claude_json:
        for name, srv in (claude_json.get("mcpServers") or {}).items():
            items.append(check_server(name, srv, "user", False, False, allow))
        for path, proj in (claude_json.get("projects") or {}).items():
            if repo_path and os.path.abspath(path) != os.path.abspath(repo_path):
                continue
            for name, srv in (proj.get("mcpServers") or {}).items():
                items.append(check_server(name, srv, "local", False, False, allow))
    for name, srv in ((managed or {}).get("managedMcpServers") or {}).items():
        items.append(check_server(name, srv, "managed", False, False, allow))

    plugin_sources = [("project", settings), ("managed", managed or {})]
    for scope, src in plugin_sources:
        for pid, enabled in (src.get("enabledPlugins") or {}).items():
            f = []
            if enabled and allow is not None and pid not in allow.get("plugins", []):
                f.append({"id": "M4", "severity": "BLOCKER", "message": "plugin not on the approved list"})
            items.append({"kind": "plugin", "name": pid, "scope": scope, "transport": "-",
                          "target": "enabled" if enabled else "disabled", "findings": f})
        markets = dict(src.get("extraKnownMarketplaces") or {}, **(src.get("additionalMarketplaces") or {}))
        for mname, mdef in markets.items():
            source = (mdef or {}).get("source", {})
            f = []
            if source.get("source") in ("git", "github") and not source.get("ref"):
                f.append({"id": "M6", "severity": "WARN", "message": "marketplace not pinned to a ref; its contents can change under you"})
            if allow is not None and mname not in allow.get("marketplaces", []):
                f.append({"id": "M4", "severity": "BLOCKER", "message": "marketplace not on the approved list"})
            items.append({"kind": "marketplace", "name": mname, "scope": scope, "transport": source.get("source", "?"),
                          "target": str(source.get("repo") or source.get("url") or source.get("path") or "")[:90], "findings": f})

    sev = [f["severity"] for i in items for f in i["findings"]]
    verdict, code = ("BLOCKED", 4) if "BLOCKER" in sev else (("WARNINGS", 2) if "WARN" in sev else ("CLEAN", 0))
    return {"verdict": verdict, "allowlist_used": allow is not None,
            "counts": {k: sum(i["kind"] == k for i in items) for k in ("mcp", "plugin", "marketplace")},
            "blockers": sev.count("BLOCKER"), "warnings": sev.count("WARN"), "items": items}, code


def render(r):
    c = r["counts"]
    out = [f"MCP/plugin inventory: {r['verdict']}  ({c['mcp']} servers, {c['plugin']} plugins, {c['marketplace']} marketplaces)",
           f"  allowlist: {'checked' if r['allowlist_used'] else 'not supplied (approval not checked)'}"]
    for i in r["items"]:
        out.append(f"  {i['kind']:<11} {i['name']:<34} {i['scope']:<8} {i['transport']:<6} {i['target']}")
        out += [f"      [{f['severity']}] {f['id']}: {f['message']}" for f in i["findings"]]
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Inventory MCP servers, plugins and marketplaces; check pinning, secrets and an approved list.")
    p.add_argument("--repo", help="repository root (reads .mcp.json and .claude/settings.json)")
    p.add_argument("--claude-json", help="a developer's ~/.claude.json for local/user-scope servers (optional)")
    p.add_argument("--managed", help="managed-settings.json (optional)")
    p.add_argument("--allowlist", help='JSON {"servers": [...], "plugins": [...], "marketplaces": [...]}')
    p.add_argument("--sample", action="store_true", help="run on an embedded sample")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    if a.sample:
        report, code = build(SAMPLE["mcp_json"], SAMPLE["settings"], None, None, SAMPLE["allowlist"])
    elif a.repo or a.claude_json or a.managed:
        repo = a.repo or ""
        report, code = build(load(os.path.join(repo, ".mcp.json")) if repo else None,
                             load(os.path.join(repo, ".claude", "settings.json")) if repo else None,
                             load(a.claude_json), load(a.managed), load(a.allowlist), repo or None)
    else:
        p.error("give --repo (and optionally --claude-json/--managed/--allowlist), or --sample")
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
