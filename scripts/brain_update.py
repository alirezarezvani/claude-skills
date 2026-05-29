#!/usr/bin/env python3
"""
brain_update.py — Sync the Jarvis Brain index with live GitHub data.

Usage:
    python3 scripts/brain_update.py [--token GITHUB_TOKEN] [--dry-run] [--rebuild-md] [--add]

Requires: requests  (pip install requests)
"""

import argparse
import json
import os
import re
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

# File patterns that signal new work worth noting in the brain.
INTERESTING_PATTERNS = [
    re.compile(r"^Formula/.*\.rb$"),
    re.compile(r"^SKILL\.md$"),
    re.compile(r".*SKILL\.md$"),
    re.compile(r"^brain/.*"),
    re.compile(r".*\.github/workflows/.*\.yml$"),
    re.compile(r"^agents/.*"),
    re.compile(r"^commands/.*"),
    re.compile(r"^engineering/.*SKILL\.md$"),
]

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
NOW   = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Track remaining rate-limit across all calls in this run.
_rate_remaining: int | None = None


# ── GitHub helpers ─────────────────────────────────────────────────────────────

def gh(path: str, token: str, params: dict | None = None) -> tuple[dict | list | None, dict]:
    """
    GET from GitHub API.
    Returns (data, response_headers).  data is None on non-200 responses.
    """
    global _rate_remaining
    url = f"https://api.github.com/{path.lstrip('/')}"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers, params=params, timeout=15)

    # Track rate limit from every response.
    remaining_str = r.headers.get("X-RateLimit-Remaining")
    if remaining_str is not None:
        try:
            _rate_remaining = int(remaining_str)
        except ValueError:
            pass

    if _rate_remaining is not None and _rate_remaining < 20:
        print(f"  !! WARNING: GitHub rate limit low — {_rate_remaining} requests remaining")

    if r.status_code == 200:
        return r.json(), dict(r.headers)
    print(f"  ⚠  GitHub API {r.status_code} for {url}")
    return None, dict(r.headers)


def _gh_data(path: str, token: str, params: dict | None = None) -> dict | list | None:
    """Convenience wrapper that returns only the data (not headers)."""
    data, _ = gh(path, token, params)
    return data


def fetch_pr(repo: str, pr_num: int, token: str) -> dict | None:
    """Fetch a single PR by number (includes merged_at / state)."""
    return _gh_data(f"repos/{repo}/pulls/{pr_num}", token)


def fetch_open_prs(repo: str, token: str) -> list[dict]:
    data = _gh_data(f"repos/{repo}/pulls", token, params={"state": "open", "per_page": "50"})
    return data or []


def fetch_closed_prs(repo: str, token: str) -> list[dict]:
    data = _gh_data(f"repos/{repo}/pulls", token, params={"state": "closed", "per_page": "50"})
    return data or []


def fetch_recent_commits(repo: str, token: str, n: int = 20) -> list[dict]:
    data = _gh_data(f"repos/{repo}/commits", token, params={"per_page": str(n)})
    return data or []


def fetch_commit_files(repo: str, sha: str, token: str) -> list[str]:
    """Return list of filenames changed in a commit."""
    data = _gh_data(f"repos/{repo}/commits/{sha}", token)
    if not data:
        return []
    return [f["filename"] for f in data.get("files", [])]


def fetch_branches(repo: str, token: str) -> list[str]:
    data = _gh_data(f"repos/{repo}/branches", token, params={"per_page": "100"})
    if not data:
        return []
    return [b["name"] for b in data]


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


# ── Feature 2: Auto-status resolver ───────────────────────────────────────────

def resolve_pr_status(pr_data: dict) -> str:
    """
    Map GitHub PR state/merged_at to a brain status string.
      merged           → "done"
      closed (no merge)→ "archived"
      open + draft     → "draft-pr"
      open             → "open-pr"
    """
    if pr_data.get("merged_at"):
        return "done"
    state = pr_data.get("state", "open")
    if state == "closed":
        return "archived"
    return "draft-pr" if pr_data.get("draft") else "open-pr"


def sync_pr_status(index: dict, token: str):
    """
    Update entry status for all entries that have a PR number.
    Checks both open and closed PRs for every tracked repo.
    """
    print("\n── Syncing PR statuses ───────────────────────────────────────────")
    changed = 0
    for entry in index["entries"]:
        pr_num = entry.get("pr")
        repo   = entry.get("repo")
        if not pr_num or not repo:
            continue

        pr_data = fetch_pr(repo, pr_num, token)
        if pr_data is None:
            print(f"  ⚠  Could not fetch PR #{pr_num} from {repo}")
            continue

        new_status = resolve_pr_status(pr_data)
        old_status = entry["status"]
        if old_status != new_status:
            print(f"  → {entry['id']}: status {old_status!r} → {new_status!r}")
            entry["status"] = new_status
            entry["updated"] = TODAY
            changed += 1

    if changed == 0:
        print("  (no status changes)")


# ── Feature 3: Last-activity updater ──────────────────────────────────────────

def update_last_activity(index: dict, token: str):
    """
    For each entry, find the most recent commit that touches one of its files
    (or its branch) and set/update entry["last_activity"] to that commit date.
    """
    print("\n── Updating last_activity fields ─────────────────────────────────")
    for entry in index["entries"]:
        repo    = entry.get("repo")
        files   = set(entry.get("files", []))
        branch  = entry.get("branch", "main")
        if not repo:
            continue

        commits = fetch_recent_commits(repo, token, n=20)
        if not commits:
            continue

        # If entry has specific files, find the latest commit touching any of them.
        latest_date: str | None = None
        if files:
            for c in commits:
                sha       = c.get("sha", "")
                committed = (c.get("commit", {})
                              .get("committer", {})
                              .get("date", "")[:10])
                changed = fetch_commit_files(repo, sha, token)
                if any(cf.startswith(tuple(files)) for cf in changed):
                    latest_date = committed
                    break   # commits are newest-first
        else:
            # No files — use the latest commit on the branch.
            for c in commits:
                committed = (c.get("commit", {})
                              .get("committer", {})
                              .get("date", "")[:10])
                if committed:
                    latest_date = committed
                    break

        if latest_date and entry.get("last_activity") != latest_date:
            print(f"  → {entry['id']}: last_activity = {latest_date}")
            entry["last_activity"] = latest_date


# ── Feature 1: Cross-repo commit scanner ──────────────────────────────────────

def _file_is_interesting(filename: str) -> bool:
    return any(p.match(filename) for p in INTERESTING_PATTERNS)


def discover_new_commits(index: dict, token: str):
    """
    Scan 20 recent commits per repo for work not yet in the brain.
    Prints SUGGEST ADD lines for:
      • branches not tracked by any entry
      • commits touching interesting files not already covered
    """
    known_branches = {e.get("branch") for e in index["entries"] if e.get("branch")}
    known_files: set[str] = set()
    for e in index["entries"]:
        known_files.update(e.get("files", []))

    print("\n── Cross-repo commit scan (20 commits/repo) ──────────────────────")
    for repo in REPOS:
        print(f"\n  [{repo}]")
        commits = fetch_recent_commits(repo, token, n=20)
        if not commits:
            print("    (no commits retrieved)")
            continue

        seen_suggestions: set[str] = set()   # deduplicate within repo
        for c in commits:
            msg       = c.get("commit", {}).get("message", "").split("\n")[0]
            sha       = c.get("sha", "")[:7]
            branch    = (c.get("commit", {})
                          .get("tree", {})
                          .get("sha", ""))     # not reliable for branch; use branch list
            committed = (c.get("commit", {})
                          .get("committer", {})
                          .get("date", "")[:10])
            print(f"    {sha}  {committed}  {msg}")

            # Check files in this commit.
            changed = fetch_commit_files(repo, c["sha"], token)
            for fname in changed:
                if _file_is_interesting(fname) and fname not in known_files:
                    key = f"file:{fname}"
                    if key not in seen_suggestions:
                        seen_suggestions.add(key)
                        print(f"    SUGGEST ADD  new interesting file not in brain: {fname}")

        # Check for branches not tracked.
        branches = fetch_branches(repo, token)
        for branch in branches:
            if branch not in known_branches and branch not in ("main", "master"):
                key = f"branch:{branch}"
                if key not in seen_suggestions:
                    seen_suggestions.add(key)
                    print(f"    SUGGEST ADD  branch not tracked in brain: {branch}")

    print()


# ── BRAIN.md regeneration ─────────────────────────────────────────────────────

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
        tags  = " ".join(f"`{t}`" for t in e["tags"])
        files = " · ".join(f"`{f}`" for f in e.get("files", []))
        last_act = e.get("last_activity", "")
        lines += [
            f"### {e['id']}",
            f"**{e['title']}**",
            f"- **Repo:** {e['repo']} · branch `{e.get('branch', 'main')}`"
            + (f" · PR #{e['pr']}" if e.get("pr") else ""),
            f"- **Created:** {e['created']}  **Updated:** {e['updated']}"
            + (f"  **Last Activity:** {last_act}" if last_act else ""),
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


# ── Feature 5: Interactive --add ──────────────────────────────────────────────

def _prompt(label: str, default: str = "") -> str:
    """Prompt with an optional default value."""
    suffix = f" [{default}]" if default else ""
    try:
        val = input(f"  {label}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    return val if val else default


def _slugify(text: str) -> str:
    """Turn a title into a kebab-case id."""
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def interactive_add(index: dict, dry_run: bool):
    """
    Drop into an interactive prompt to add a new brain entry.
    Writes to both brain/index.json and BRAIN.md.
    """
    print("\n── Add new brain entry ───────────────────────────────────────────")
    print("  (press Ctrl-C or Enter on a required field to abort)\n")

    title   = _prompt("Title (required)")
    if not title:
        print("  Aborted — title is required.")
        return

    default_id = _slugify(title)
    entry_id   = _prompt("ID (slug)", default=default_id)

    # Check for duplicate id.
    if any(e["id"] == entry_id for e in index["entries"]):
        print(f"  ⚠  Entry with id '{entry_id}' already exists. Aborting.")
        return

    valid_types = ["homebrew-formula", "skills-library", "meta-system", "project",
                   "tool", "agent", "command", "idea", "other"]
    print(f"  Types: {', '.join(valid_types)}")
    entry_type = _prompt("Type", default="project")

    print(f"  Repos: {', '.join(REPOS)}")
    repo   = _prompt("Repo (owner/name)", default=REPOS[0] if REPOS else "")
    branch = _prompt("Branch", default="main")

    pr_str = _prompt("PR number (leave blank if none)", default="")
    pr_num = int(pr_str) if pr_str.isdigit() else None

    valid_statuses = ["active", "draft-pr", "open-pr", "done", "archived", "idea"]
    print(f"  Statuses: {', '.join(valid_statuses)}")
    status = _prompt("Status", default="active")

    tags_raw = _prompt("Tags (comma-separated)", default="")
    tags     = [t.strip() for t in tags_raw.split(",") if t.strip()]

    files_raw = _prompt("Key files (comma-separated, leave blank if none)", default="")
    files     = [f.strip() for f in files_raw.split(",") if f.strip()]

    summary = _prompt("Summary (one sentence)")
    notes   = _prompt("Notes (optional)", default="")

    entry: dict = {
        "id":      entry_id,
        "title":   title,
        "type":    entry_type,
        "repo":    repo,
        "branch":  branch,
        "pr":      pr_num,
        "created": TODAY,
        "updated": TODAY,
        "status":  status,
        "tags":    tags,
        "summary": summary,
        "files":   files,
    }
    if notes:
        entry["notes"] = notes

    print("\n  Preview:")
    print(json.dumps(entry, indent=4))
    confirm = _prompt("Add this entry? (y/n)", default="y")
    if confirm.lower() not in ("y", "yes"):
        print("  Aborted.")
        return

    index["entries"].append(entry)
    save_index(index, dry_run)
    rebuild_brain_md(index, dry_run)
    if not dry_run:
        print(f"\n✓ Entry '{entry_id}' added successfully.")


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Sync the Jarvis Brain index")
    parser.add_argument("--token",       default=os.environ.get("GITHUB_TOKEN", ""),
                        help="GitHub personal access token")
    parser.add_argument("--dry-run",     action="store_true",
                        help="Print what would change without writing")
    parser.add_argument("--rebuild-md",  action="store_true",
                        help="Regenerate BRAIN.md only")
    parser.add_argument("--add",         action="store_true",
                        help="Interactively add a new brain entry")
    args = parser.parse_args()

    print("🧠 Jarvis Brain sync starting…\n")
    index = load_index()

    # ── --rebuild-md only ──────────────────────────────────────────────────────
    if args.rebuild_md:
        rebuild_brain_md(index, args.dry_run)
        return

    # ── --add mode ─────────────────────────────────────────────────────────────
    if args.add:
        interactive_add(index, args.dry_run)
        return

    # ── Live GitHub sync ───────────────────────────────────────────────────────
    if not args.token:
        print("⚠  No GITHUB_TOKEN — skipping live GitHub sync (pass --token or set env var)")
        print("   Running offline: rebuilding BRAIN.md from current index only.\n")
        save_index(index, args.dry_run)
        rebuild_brain_md(index, args.dry_run)
        print("\n🧠 Brain sync complete (offline).")
        return

    # PR status auto-resolver
    sync_pr_status(index, args.token)

    # Last-activity updater
    update_last_activity(index, args.token)

    # Cross-repo commit scanner (suggestions only)
    discover_new_commits(index, args.token)

    # Final rate-limit report
    if _rate_remaining is not None:
        status_str = f"{_rate_remaining} requests remaining"
        if _rate_remaining < 20:
            print(f"  !! Rate limit warning: {status_str}")
        else:
            print(f"  ℹ  Rate limit: {status_str}")

    save_index(index, args.dry_run)
    rebuild_brain_md(index, args.dry_run)
    print("\n🧠 Brain sync complete.")


if __name__ == "__main__":
    main()
