#!/usr/bin/env python3
"""Mirror a standalone skill plugin's content into its domain-bundled location.

Standalone:  <domain>/<skill>/skills/<skill>/{SKILL.md,scripts,references,assets}
Bundled:     <domain>/skills/<skill>/{SKILL.md,scripts,references,assets}

The bundled mirror contains ONLY the skill payload (SKILL.md + scripts + references
+ assets). Plugin-level files (README.md, .claude-plugin, agents, commands, hooks)
stay in the standalone location only.
"""
import argparse
import filecmp
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIRRORED = ("SKILL.md", "scripts", "references", "assets")


def standalone_payload(plugin_dir):
    skill = os.path.basename(plugin_dir.rstrip("/"))
    return os.path.join(plugin_dir, "skills", skill)


def bundled_target(plugin_dir):
    domain = os.path.dirname(plugin_dir.rstrip("/"))
    skill = os.path.basename(plugin_dir.rstrip("/"))
    return os.path.join(domain, "skills", skill)


def _collect_diffs(c, prefix, out):
    for f in c.left_only:
        out.append(f"only-in-standalone: {os.path.join(prefix, f)}")
    for f in c.right_only:
        out.append(f"only-in-bundled: {os.path.join(prefix, f)}")
    for f in c.diff_files:
        out.append(f"differs: {os.path.join(prefix, f)}")
    for d, sub in c.subdirs.items():
        _collect_diffs(sub, os.path.join(prefix, d), out)


def diff_tree(left, right):
    if not os.path.exists(right):
        return ["<bundled mirror missing>"]
    diffs = []
    _collect_diffs(filecmp.dircmp(left, right), "", diffs)
    return diffs


def _remove_path(p):
    if not os.path.exists(p):
        return
    if os.path.isdir(p):
        shutil.rmtree(p)
    else:
        os.remove(p)


def _mirror_one(src, dst):
    if not os.path.exists(src):
        _remove_path(dst)
        return
    _remove_path(dst)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def sync(plugin_dir):
    src_root = standalone_payload(plugin_dir)
    dst_root = bundled_target(plugin_dir)
    if not os.path.isdir(src_root):
        print(f"ERROR: standalone payload missing: {src_root}", file=sys.stderr)
        return 1
    os.makedirs(dst_root, exist_ok=True)
    for name in MIRRORED:
        _mirror_one(os.path.join(src_root, name), os.path.join(dst_root, name))
    print(f"synced: {src_root} -> {dst_root}")
    return 0


def check(plugin_dir):
    src_root = standalone_payload(plugin_dir)
    dst_root = bundled_target(plugin_dir)
    if not os.path.isdir(src_root):
        print(f"FAIL: standalone payload missing: {src_root}")
        return 1
    diffs = []
    for name in MIRRORED:
        src = os.path.join(src_root, name)
        dst = os.path.join(dst_root, name)
        if not os.path.exists(src) and not os.path.exists(dst):
            continue
        if os.path.isdir(src):
            diffs.extend(f"{name}/{d}" for d in diff_tree(src, dst))
        elif os.path.isfile(src):
            if not os.path.exists(dst) or not filecmp.cmp(src, dst, shallow=False):
                diffs.append(name)
    if diffs:
        print(f"FAIL: {plugin_dir} mirror out of sync")
        for d in diffs:
            print(f"  - {d}")
        return 1
    print(f"OK: {plugin_dir}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sync", metavar="PLUGIN_DIR", help="Mirror standalone -> bundled")
    g.add_argument("--check", metavar="PLUGIN_DIR", help="Verify mirror is in sync; exit 1 if not")
    args = ap.parse_args()
    target = args.sync or args.check
    target = target.rstrip("/")
    if not os.path.isabs(target):
        target = os.path.join(REPO, target)
    if not os.path.isdir(target):
        print(f"ERROR: not a directory: {target}", file=sys.stderr)
        return 2
    return sync(target) if args.sync else check(target)


if __name__ == "__main__":
    sys.exit(main())
