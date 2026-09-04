#!/usr/bin/env python3
"""test_derive_counters.py — regression test for the delta-claim gate (issue #995).

Exercises derive_counters.extract_delta_claims / check_delta_claims directly
against synthetic fixtures, so the assertions don't depend on the repo's own
CHANGELOG.md/CLAUDE.md content changing over time. Covers:

  - the exact fabricated repro from #995 (both unicode "->" and ASCII "->"
    arrows) is rejected
  - a genuinely correct delta entry is accepted
  - an absolute ("unchanged") entry is accepted
  - a claim in a different, unrelated clause on the same line is not
    mis-attributed to a neighboring counter (the comma/semicolon
    cross-matching bug this fix had to avoid)

Stdlib only (unittest). Not part of the gitignored maintainer-local `tests/`
pytest suite — this lives in scripts/ so it ships with the gate it tests and
runs the same way in CI: `python3 scripts/test_derive_counters.py`.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from derive_counters import check_delta_claims, extract_delta_claims  # noqa: E402

DERIVED = {
    "skills": 388,
    "plugins_on_disk": 99,
    "plugins_registered": 99,
    "python_tools": 727,
    "references": 842,
    "agents": 118,
    "commands": 150,
    "domains": 20,
}


class DeltaClaimTests(unittest.TestCase):
    def test_issue_995_exact_repro_unicode_arrow_is_rejected(self):
        text = "Counters: skills 999 → 1234; commands 12 → 999."
        problems = check_delta_claims("CHANGELOG.md", text, DERIVED)
        self.assertTrue(problems, "fabricated delta must be rejected")
        joined = " ".join(problems)
        self.assertIn("skills=1234", joined)
        self.assertIn("commands=999", joined)

    def test_issue_995_exact_repro_ascii_arrow_is_rejected(self):
        text = "Counters: skills 999 -> 1234; commands 12 -> 999."
        problems = check_delta_claims("CHANGELOG.md", text, DERIVED)
        self.assertTrue(problems, "fabricated delta must be rejected regardless of arrow style")

    def test_genuinely_correct_delta_entry_passes(self):
        text = "- **Counters:** skills 387 → 388; commands 149 → 150."
        problems = check_delta_claims("CHANGELOG.md", text, DERIVED)
        self.assertEqual(problems, [])

    def test_unchanged_absolute_entry_passes(self):
        text = "- **Counters:** skills 388 (unchanged); commands 150 (unchanged)."
        problems = check_delta_claims("CHANGELOG.md", text, DERIVED)
        self.assertEqual(problems, [])

    def test_historical_lower_delta_is_not_flagged(self):
        # An older, already-superseded checkpoint from earlier repo history
        # must not fail just because the repo has since grown past it.
        text = "Counters: skills 357 → 358; commands 109 → 110."
        problems = check_delta_claims("CHANGELOG.md", text, DERIVED)
        self.assertEqual(problems, [])

    def test_neighboring_clause_label_is_not_cross_matched(self):
        # Regression guard: a naive regex can let the label from one
        # comma/semicolon-separated clause attach to a different clause's
        # number pair. None of these numbers should be misread as exceeding
        # derived totals for the wrong counter.
        text = "Counters: 352 -> 353 skills, 590 -> 593 Python tools, 718 -> 721 references."
        claims = extract_delta_claims(text)
        self.assertEqual(claims.get("skills"), [353])
        self.assertEqual(claims.get("python_tools"), [593])
        self.assertEqual(claims.get("references"), [721])

    def test_fabricated_delta_anywhere_in_file_is_caught(self):
        # Mirrors the issue's literal repro: appending the fabricated line
        # anywhere in the file (not just inside a well-formed section) must
        # still be caught.
        text = (
            "# Changelog\n\n## [Unreleased]\n\n"
            "- **Counters:** skills 387 → 388; commands 149 → 150.\n\n"
            "## [1.0.0]\n\n- Initial release.\n\n"
            "Counters: skills 999 → 1234; commands 12 → 999.\n"
        )
        problems = check_delta_claims("CHANGELOG.md", text, DERIVED)
        self.assertTrue(problems)


if __name__ == "__main__":
    unittest.main()
