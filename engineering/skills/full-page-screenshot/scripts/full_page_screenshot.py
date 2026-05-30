#!/usr/bin/env python3
"""
full_page_screenshot.py — Python launcher for full-page-screenshot.mjs

Delegates to the Node.js implementation via subprocess. Requires Node.js 22+
and Chrome with remote debugging enabled.

Usage:
    python full_page_screenshot.py --check
    python full_page_screenshot.py --list
    python full_page_screenshot.py --tab <id> --output screenshot.png
    python full_page_screenshot.py --url <url> --output screenshot.png
"""

import argparse
import subprocess
import sys
from pathlib import Path

MJS = Path(__file__).parent / "full-page-screenshot.mjs"


def main():
    parser = argparse.ArgumentParser(
        description="Capture a full-page screenshot via Chrome DevTools Protocol."
    )
    parser.add_argument("--check", action="store_true", help="Check environment readiness")
    parser.add_argument("--list", action="store_true", help="List open Chrome tabs")
    parser.add_argument("--tab", metavar="ID", help="Tab ID to screenshot")
    parser.add_argument("--url", metavar="URL", help="URL to open and screenshot")
    parser.add_argument("--output", metavar="FILE", default="screenshot.png", help="Output PNG path")
    parser.add_argument("--port", metavar="PORT", default="9222", help="Chrome remote debugging port")
    args, extra = parser.parse_known_args()

    cmd = ["node", str(MJS)]
    if args.check:
        cmd.append("--check")
    elif args.list:
        cmd.append("--list")
    elif args.tab:
        cmd += ["--tab", args.tab, "--output", args.output]
    elif args.url:
        cmd += ["--url", args.url, "--output", args.output]
    cmd += ["--port", args.port] + extra

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
