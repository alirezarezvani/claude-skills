#!/usr/bin/env python3
"""Shared helpers for the skill eval harness: inventory, running Claude Code, reading transcripts.

Not a CLI on its own; imported by the other scripts in scripts/evals/.
Run `python3 scripts/evals/inventory.py --help` for the entry points.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.join(REPO, "scripts", "evals")
CASES = os.path.join(HERE, "cases")
FIXTURES = os.path.join(HERE, "fixtures")


def _frontmatter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*['\"]?(.+?)['\"]?\s*$", fm, re.M)
    # Description may be quoted, plain, or a folded/literal block scalar.
    desc = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", fm, re.M | re.S)
    d = desc.group(1) if desc else ""
    d = re.sub(r"^[>|][-+]?\s*", "", d.strip())
    d = " ".join(d.split()).strip("'\"")
    return (name.group(1).strip() if name else os.path.basename(os.path.dirname(path))), d


def inventory():
    """Every installable skill, once: {path, name, plugin, plugin_dir, description}.

    A skill shipped by several plugins (domain bundle + standalone mirror) is listed
    under the plugin with the fewest skills, so a targeted run loads as little as possible.
    """
    market = json.load(open(os.path.join(REPO, ".claude-plugin", "marketplace.json")))
    seen = {}
    for p in market["plugins"]:
        root = os.path.normpath(os.path.join(REPO, p["source"]))
        manifest = json.load(open(os.path.join(root, ".claude-plugin", "plugin.json")))
        dirs = manifest.get("skills")
        if dirs is None:
            dirs = ["./skills"] if os.path.isdir(os.path.join(root, "skills")) else []
        if isinstance(dirs, str):
            dirs = [dirs]
        files = []
        for d in dirs:
            d = os.path.normpath(os.path.join(root, d))
            if os.path.isfile(os.path.join(d, "SKILL.md")):
                files.append(os.path.join(d, "SKILL.md"))
            files += sorted(glob.glob(os.path.join(d, "*", "SKILL.md")))
        for f in files:
            key = os.path.realpath(os.path.dirname(f))
            name, desc = _frontmatter(f)
            row = dict(path=os.path.relpath(key, REPO), name=name, plugin=p["name"],
                       plugin_dir=os.path.relpath(root, REPO), description=desc, plugin_size=len(files))
            if key not in seen or row["plugin_size"] < seen[key]["plugin_size"]:
                seen[key] = row
    # Dual-published skills are copies (same name and description) in two folders: keep one.
    unique = {}
    for row in seen.values():
        k = (row["name"], row["description"])
        if k not in unique or row["plugin_size"] < unique[k]["plugin_size"]:
            unique[k] = row
    return sorted(unique.values(), key=lambda r: r["path"])


def all_plugin_dirs():
    market = json.load(open(os.path.join(REPO, ".claude-plugin", "marketplace.json")))
    return sorted({os.path.normpath(os.path.join(REPO, p["source"])) for p in market["plugins"]})


def load_cases(name):
    path = os.path.join(CASES, name)
    return json.load(open(path)) if os.path.exists(path) else {}


class Budget:
    """Running spend across threads. Jobs check `exhausted` before starting."""

    def __init__(self, cap_usd):
        self.cap = cap_usd
        self.spent = 0.0
        self._lock = threading.Lock()

    def add(self, usd):
        with self._lock:
            self.spent += usd or 0.0

    @property
    def exhausted(self):
        return self.spent >= self.cap


def run_claude(prompt, out_path, *, cwd, plugin_dirs=(), model="sonnet", max_turns=2,
               max_budget=0.5, extra=(), timeout=900):
    """Run `claude -p` in an isolated config dir and save the stream-json transcript.

    Isolation: a throwaway CLAUDE_CONFIG_DIR, account plugin sync off, and a cwd outside the
    repo, so neither this repo's CLAUDE.md nor anything installed on the runner leaks in.
    """
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns), "--model", model, "--max-budget-usd", str(max_budget),
           "--no-session-persistence", *extra]
    for d in plugin_dirs:
        cmd += ["--plugin-dir", d]
    cfg = tempfile.mkdtemp(prefix="cc-eval-cfg-")
    env = dict(os.environ, CLAUDE_CONFIG_DIR=cfg, CLAUDE_CODE_SYNC_PLUGINS="0")
    env.pop("CLAUDECODE", None)
    try:
        with open(out_path, "w") as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, env=env, cwd=cwd, timeout=timeout)
    except subprocess.TimeoutExpired:
        pass
    finally:
        shutil.rmtree(cfg, ignore_errors=True)
    return read_transcript(out_path)


def read_transcript(path):
    """Skills fired, tool calls, final answer and cost from a stream-json transcript."""
    skills, tools, final, cost, error = [], [], "", 0.0, None
    try:
        lines = open(path).read().splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            m = json.loads(line)
        except ValueError:
            continue
        if m.get("type") == "assistant":
            for c in m["message"].get("content", []):
                if c.get("type") == "tool_use":
                    tools.append(c["name"])
                    if c["name"] == "Skill":
                        skills.append(c["input"].get("skill") or c["input"].get("command") or "")
        elif m.get("type") == "result":
            final = m.get("result") or ""
            cost = m.get("total_cost_usd") or 0.0
            # Hitting --max-turns is expected in a short trigger run; the transcript is still valid.
            if m.get("is_error") and m.get("subtype") != "error_max_turns":
                error = m.get("subtype") or "error"
    if not lines:
        error = "no output"
    return dict(skills=skills, tools=tools, final=final, cost=cost, error=error)


def fired(skills, name, plugin):
    """exact: the target skill fired. plugin: the target or a sibling from the same plugin fired."""
    exact = any(s.split(":")[-1] == name for s in skills)
    same_plugin = any(s.split(":")[0] == plugin and ":" in s for s in skills)
    return exact, exact or same_plugin


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
