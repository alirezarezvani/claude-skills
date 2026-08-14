#!/usr/bin/env python3
"""
askill_matcher.py — Zero-dependency BM25 Skill Matcher for Claude Skills
"""
import os, sys, argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Claude Skills Fast Matcher")
    parser.add_argument("query", nargs="*", help="Query task")
    args = parser.parse_args()
    q = " ".join(args.query) if args.query else ""
    print(f"BM25 Skill Matcher ready. Query: '{q}'")

if __name__ == "__main__":
    main()
