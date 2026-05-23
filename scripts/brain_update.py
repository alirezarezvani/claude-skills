#!/usr/bin/env python3
"""
brain_update.py — Sync the Jarvis Brain index with live GitHub data.

Usage:
    python3 scripts/brain_update.py [--token GITHUB_TOKEN] [--dry-run]

Requires: requests  (pip install requests)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests first:  pip install requests")
    sys.exit(1)

BRAIN_DIR = Path(__file__).parent.parent / "brain"
INDEX_FILE = BRAIN_DIR / "index.json"
BRAIN_MD   = Path(__file__).parent.parent / "BRAIN.md"

REPOS = [
    "lordhammer11/homebrew-tap",
    "lordhammer11/claude-code-together",
    "lordhammer11/claude-skills",
    "lordhammer11/symmetrical-octo-goggles",
]

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── GitHub helpers ─────────────────────────────────────────────────────────────

def gh(path: str, token: str) -> dict | list | None:
    """GET from GitHub API."""
    url = f"https://api.github.com/{path.lstrip('/')}"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code == 200:
        return r.json()
    print(f"  ⚠  GitHub API {r.status_code} for {url}")
    return None


def fetch_open_prs(repo: str, token: str) -> list[dict]:
    data = gh(f"repos/{repo}/pulls?state=open&per_page=50", token)
    return data or []


def fetch_recent_commits(repo: str, token: str, n: int = 10) -> list[dict]:
    data = gh(f"repos/{repo}/commits?per_page={n}", token)
    return data or []


# ── Brain helpers ──────────────────────────────────────────────────────────────

def load_index() -> dict:
    with open(INDEX_FILE) as f:
        return json.load(f)


def save_index(index: dict, dry_run: bool):
    index["meta"]["last_updated"] = NOW
    if dry_run:
        print("[dry-run] Would write brain/index.json")
        return
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
    print("✓ brain/index.json updated")


def entry_by_id(index: dict, entry_id: str) -> dict | None:
    for e in index["entries"]:
        if e["id"] == entry_id:
            return e
    return None


def sync_pr_status(index: dict, token: str):
    """Update entry status based on open/closed PRs."""
    for repo in REPOS:
        prs = fetch_open_prs(repo, token)
        for pr in prs:
            pr_num = pr["number"]
            # Find matching entry
            for entry in index["entries"]:
                if entry.get("repo") == repo and entry.get("pr") == pr_num:
                    new_status = "draft-pr" if pr.get("draft") else "open-pr"
                    if entry["status"] != new_status:
                        print(f"  → {entry['id']}: status {entry['status']} → {new_status}")
                        entry["status"] = new_status
                        entry["updated"] = TODAY


def discover_new_commits(index: dict, token: str):
    """
    Scan recent commits for signs of new work not yet in the brain.
    Prints suggestions — does not auto-add (to keep humans in the loop).
    """
    known_branches = {e.get("branch") for e in index["entries"]}
    print("\n── Recent commit scan ────────────────────────────────────────────")
    for repo in REPOS:
        commits = fetch_recent_commits(repo, token, n=5)
        for c in commits:
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            sha = c.get("sha", "")[:7]
            print(f"  [{repo}] {sha}  {msg}")
    print()


def rebuild_brain_md(index: dict, dry_run: bool):
    """Regenerate BRAIN.md from index.json."""
    active   = [e for e in index["entries"] if e["status"] not in ("archived", "idea")]
    ideas    = index.get("ideas", [])
    total    = len(index["entries"])
    n_active = len([e for e in index["entries"] if e["status"] == "active"])
    n_draft  = len([e for e in index["entries"] if "pr" in e["status"]])

    lines = [
        "# Jarvis Brain 🧠",
        "> Persistent knowledge index for lordhammer11 — everything built, developed, and imagined.",
        "> Auto-updated by GitHub Actions. Query interactively with `/brain` in Claude Code.",
        "",
        "---",
        "",
        "## Active Work",
        "",
        "| Project | Repo | Status | Tags |",
        "|---------|------|--------|------|",
    ]
    for e in active:
        tags = " ".join(f"`{t}`" for t in e["tags"][:5])
        lines.append(f"| [{e['title']}](#{e['id']}) | {e['repo'].split('/')[1]} | {e['status']} | {tags} |")

    lines += ["", "---", "", "## Detail Entries", ""]
    for e in index["entries"]:
        tags = " ".join(f"`{t}`" for t in e["tags"])
        files = " · ".join(f"`{f}`" for f in e.get("files", []))
        lines += [
            f"### {e['id']}",
            f"**{e['title']}**",
            f"- **Repo:** {e['repo']} · branch `{e.get('branch', 'main')}`"
            + (f" · PR #{e['pr']}" if e.get("pr") else ""),
            f"- **Created:** {e['created']}  **Updated:** {e['updated']}",
            f"- **Status:** {e['status']}",
            f"- **Tags:** {tags}",
            f"- **Summary:** {e['summary']}",
            f"- **Files:** {files}" if files else "",
            f"- **Notes:** {e['notes']}" if e.get("notes") else "",
            "",
            "---",
            "",
        ]

    if ideas:
        lines += ["## Ideas (Backlog)", "", "| Idea | Tags | Description |", "|------|------|-------------|"]
        for idea in ideas:
            tags = " ".join(f"`{t}`" for t in idea["tags"])
            lines.append(f"| {idea['title']} | {tags} | {idea['description']} |")
        lines += ["", "---", ""]

    lines += [
        "## Stats",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total entries | {total} |",
        f"| Active | {n_active} |",
        f"| Draft/Open PR | {n_draft} |",
        f"| Ideas backlog | {len(ideas)} |",
        f"| Repos tracked | {len(REPOS)} |",
        "",
        "---",
        "",
        f"*Last updated: {TODAY} · Auto-synced by `.github/workflows/brain-sync.yml`*",
        "",
    ]

    content = "\n".join(lines)
    if dry_run:
        print("[dry-run] Would write BRAIN.md")
        return
    with open(BRAIN_MD, "w") as f:
        f.write(content)
    print("✓ BRAIN.md regenerated")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Sync the Jarvis Brain index")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""), help="GitHub personal access token")
    parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing")
    parser.add_argument("--rebuild-md", action="store_true", help="Regenerate BRAIN.md only")
    args = parser.parse_args()

    print("🧠 Jarvis Brain sync starting…\n")
    index = load_index()

    if args.rebuild_md:
        rebuild_brain_md(index, args.dry_run)
        return

    if args.token:
        print("── Syncing PR statuses ───────────────────────────────────────────")
        sync_pr_status(index, args.token)
        discover_new_commits(index, args.token)
    else:
        print("⚠  No GITHUB_TOKEN — skipping live GitHub sync (pass --token or set env var)")

    save_index(index, args.dry_run)
    rebuild_brain_md(index, args.dry_run)
    print("\n🧠 Brain sync complete.")


if __name__ == "__main__":
    main()
