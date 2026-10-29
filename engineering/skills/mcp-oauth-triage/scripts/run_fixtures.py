#!/usr/bin/env python3
"""run_fixtures — regression harness for oauth_triage.

Runs oauth_triage.py over the shipped fixture matrix and compares each verdict
against expected_outputs/verdicts.json. Deterministic, standard library only.

Exit codes:
    0  every fixture matched its expected class and exit code
    1  a fixture produced an unexpected class or exit code
    2  the fixture matrix or the expected-output file could not be read
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
TRIAGE = os.path.join(HERE, 'oauth_triage.py')
FIXTURES = os.path.join(SKILL_ROOT, 'assets', 'fixtures')
EXPECTED = os.path.join(SKILL_ROOT, 'expected_outputs', 'verdicts.json')


def load_expected(path):
    with open(path, 'r', encoding='utf-8') as handle:
        return json.load(handle)


def run_case(case):
    argv = [sys.executable, TRIAGE,
            '--token-file', os.path.join(FIXTURES, case['record']),
            '--json']
    if case.get('log'):
        argv.extend(['--log', os.path.join(FIXTURES, case['log'])])
    argv.extend(case.get('args') or [])
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=60)
    verdict = {}
    if proc.stdout.strip():
        try:
            verdict = json.loads(proc.stdout)
        except ValueError:
            verdict = {'parse_error': proc.stdout[:200]}
    return proc.returncode, verdict


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run the oauth_triage fixture matrix.",
        epilog=(
            "Examples:\n"
            "  run_fixtures.py --verbose\n"
            "  run_fixtures.py --case rotation --json\n"
            "  run_fixtures.py --list\n"
            "  run_fixtures.py --sample --json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--fixtures", default=EXPECTED,
                        help="Path to the expected-output JSON (default: expected_outputs/verdicts.json)")
    parser.add_argument("--case", help="Run a single case by name")
    parser.add_argument("--list", action="store_true", help="List case names and exit")
    parser.add_argument("--json", action="store_true", help="Emit a JSON report")
    parser.add_argument("--verbose", action="store_true", help="Print every case, including passes")
    parser.add_argument("--sample", action="store_true",
                        help="Run the fixture matrix shipped with the skill (ignores --fixtures)")
    args = parser.parse_args(argv)

    if args.sample:
        args.fixtures = EXPECTED

    try:
        expected = load_expected(args.fixtures)
    except (OSError, ValueError) as exc:
        print("cannot read expected outputs: {}".format(exc), file=sys.stderr)
        return 2

    cases = expected.get('cases') or []
    if not cases:
        print("expected-output file contains no cases", file=sys.stderr)
        return 2

    if args.list:
        for case in cases:
            print("{}  {}".format(case.get('name'), case.get('primary_class')))
        return 0

    if args.case:
        selected = [c for c in cases if c.get('name') == args.case]
        if not selected:
            print("no case named {!r}; try --list".format(args.case), file=sys.stderr)
            return 2
        cases = selected

    results = []
    failures = 0
    for case in cases:
        try:
            code, verdict = run_case(case)
        except (OSError, subprocess.SubprocessError) as exc:
            results.append({'name': case.get('name'), 'passed': False,
                            'message': 'runner error: {}'.format(exc)})
            failures += 1
            continue
        want_class = case.get('primary_class')
        want_code = case.get('exit_code')
        got_class = verdict.get('primary_class')
        passed = (got_class == want_class) and (code == want_code)
        results.append({
            'name': case.get('name'),
            'passed': passed,
            'expected_class': want_class,
            'got_class': got_class,
            'expected_exit': want_code,
            'got_exit': code,
            'evidence': [f.get('evidence') for f in (verdict.get('findings') or [])],
        })
        if not passed:
            failures += 1

    if args.json:
        print(json.dumps({
            'total': len(cases),
            'passed': len(cases) - failures,
            'failed': failures,
            'results': results,
        }, indent=2))
    else:
        for row in results:
            if row.get('passed') and not args.verbose:
                continue
            print("{} {:16s} expected={}/{} got={}/{}".format(
                'PASS' if row.get('passed') else 'FAIL',
                str(row.get('name')),
                row.get('expected_class'), row.get('expected_exit'),
                row.get('got_class'), row.get('got_exit')))
            if not row.get('passed'):
                for line in row.get('evidence') or []:
                    if line:
                        print("     evidence: {}".format(line))
        print("{}/{} fixtures matched".format(len(cases) - failures, len(cases)))

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
