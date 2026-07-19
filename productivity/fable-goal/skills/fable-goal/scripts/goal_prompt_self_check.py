#!/usr/bin/env python3
"""Self-check runner for generated /goal prompts (fable-goal).

Mechanically verifies the checkable subset of the six-point pre-delivery
self-check from SKILL.md step 5 against a drafted /goal prompt:

  1. Word count inside the 150-350 target band
  2. Goal line present ("... is your /goal")
  3. Autonomy directive present ("work completely autonomously ...")
  4. Verification-loop language present (iteration passes / medium-matched pass)
  5. Creative-freedom grant present
  6. Delivery destination named (link / path / deploy / serve / save)

Points that need judgment (deliverable concreteness, whether named resources
were verified against the live environment) stay with the author — this tool
checks form, not taste.

Deterministic logic. No LLM calls. Stdlib only.

Usage:
    python goal_prompt_self_check.py prompt.txt
    cat prompt.txt | python goal_prompt_self_check.py -
    python goal_prompt_self_check.py --sample
    python goal_prompt_self_check.py prompt.txt --output json

Exit codes: 0 all checks pass, 1 one or more checks fail, 2 usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

WORD_MIN, WORD_MAX = 150, 350

SAMPLE = (
    "I want you to build 5 landing pages for my free prompt pack, each one "
    "fundamentally different from the others, as a way to show me the strongest "
    "possible range of directions before I pick one. These will be seen by my "
    "audience, so the bar is high: exceptional typography, striking layouts, and "
    "motion that feels designed rather than templated. Each page needs a headline, "
    "proof, and a single email-capture CTA for the prompt pack. You have total "
    "creative freedom on the visual direction of each one. You can generate any "
    "imagery you need with whatever image tools you have available, and you can "
    "accomplish this in many ways using many workflows, so before you start, take "
    "stock of the tools and MCPs you actually have, go find or fetch any references, "
    "libraries, or assets you need along the way, and show me what you are capable "
    "of. Before you ok each page, do at least three iteration passes: load the live "
    "page, click through every element, check it at mobile width, and go back "
    "through with a fine-toothed comb looking for design problems and opportunities "
    "to improve. Parallelize across subagents so the pages develop independently. "
    "When all 5 are done, deploy them to Netlify and serve me the 5 links with a "
    "one-line description of each direction. 5 fundamentally different prompt pack "
    "landing pages, live on Netlify with three iteration passes each, is your "
    "/goal. Work completely autonomously and do not ask me for anything until you "
    "are all done."
)

CHECKS = [
    (
        "goal_line",
        "Goal line present ('... is your /goal')",
        re.compile(r"is your /goal", re.IGNORECASE),
    ),
    (
        "autonomy_directive",
        "Autonomy directive present ('work ... autonomously' / 'do not ask me')",
        re.compile(r"(work\s+(completely\s+)?autonomously|do not ask me)", re.IGNORECASE),
    ),
    (
        "verification_loop",
        "Verification loop present (iteration passes / run / load / render / watch / click)",
        re.compile(
            r"(iteration pass|before you (ok|call it done|finish)|"
            r"run it (end to end|on real)|load the (live )?page|render and watch|"
            r"click through)",
            re.IGNORECASE,
        ),
    ),
    (
        "creative_freedom",
        "Creative-freedom grant present ('creative freedom' / 'many ways' / 'full freedom')",
        re.compile(
            r"(creative freedom|full freedom|many ways|show me what you (are capable|can do))",
            re.IGNORECASE,
        ),
    ),
    (
        "destination",
        "Delivery destination named (deploy / serve / link / folder / path / save / publish)",
        re.compile(
            r"(deploy|serve me|the \d*\s*links?\b|a folder called|in my home directory|"
            r"save (it|them|the)|publish|file path|~/[\w./-]+)",
            re.IGNORECASE,
        ),
    ),
]


def run_checks(text: str) -> dict:
    words = len(re.findall(r"\S+", text))
    results = [
        {
            "check": "word_count",
            "label": f"Word count in {WORD_MIN}-{WORD_MAX} band",
            "passed": WORD_MIN <= words <= WORD_MAX,
            "detail": f"{words} words",
        }
    ]
    for key, label, pattern in CHECKS:
        match = pattern.search(text)
        results.append(
            {
                "check": key,
                "label": label,
                "passed": match is not None,
                "detail": f"matched: '{match.group(0)}'" if match else "no match",
            }
        )
    passed = sum(1 for r in results if r["passed"])
    return {
        "results": results,
        "passed": passed,
        "total": len(results),
        "verdict": "PASS" if passed == len(results) else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mechanically verify a drafted /goal prompt against the "
        "checkable subset of the fable-goal pre-delivery self-check."
    )
    parser.add_argument("path", nargs="?", help="prompt file to check, or '-' for stdin")
    parser.add_argument("--sample", action="store_true", help="run against the embedded example prompt")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.sample and args.path:
        parser.error("pass either a prompt file or --sample, not both")
    if args.sample:
        text = SAMPLE
    elif args.path == "-":
        text = sys.stdin.read()
    elif args.path:
        try:
            with open(args.path, encoding="utf-8") as f:
                text = f.read()
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
    else:
        parser.print_help()
        return 2

    report = run_checks(text)
    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        for r in report["results"]:
            mark = "x" if r["passed"] else " "
            print(f"  [{mark}] {r['label']}  ({r['detail']})")
        print(f"\nVerdict: {report['verdict']} ({report['passed']}/{report['total']})")
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
