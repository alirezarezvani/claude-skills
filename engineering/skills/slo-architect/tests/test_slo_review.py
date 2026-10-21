"""Regression checks for designer JSON and legacy target parsing.

Run with: python -m unittest discover -s engineering/skills/slo-architect/tests
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import slo_review


class TargetParsingTests(unittest.TestCase):
    def test_supported_target_labels(self):
        cases = [
            ("target: 99.9%", 99.9),
            ('"target": 99.5', 99.5),
            ('"target_percent": 99.95', 99.95),
            ("target-percent: 99.7", 99.7),
            ("TARGET_PERCENT: 99.8", 99.8),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(slo_review._parse_target(text), expected)

    def test_missing_or_unrelated_target_labels(self):
        for text in ("nothing", "notarget: 90", "other_target_percent: 95"):
            with self.subTest(text=text):
                self.assertIsNone(slo_review._parse_target(text))

    def test_actual_designer_json_can_be_reviewed(self):
        designer = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPTS / "slo_designer.py"),
             "--service", "checkout", "--sli-type", "request-success-rate",
             "--target", "99.9", "--owner", "checkout-team",
             "--policy-doc", "docs/policy.md", "--format", "json"],
            capture_output=True, text=True, encoding="utf-8", check=True,
            timeout=10,
        )
        document = json.loads(designer.stdout)
        self.assertEqual(slo_review._parse_target(designer.stdout), 99.9)
        self.assertNotIn("no_target", [f[1] for f in slo_review.audit_text(designer.stdout)])
        with tempfile.TemporaryDirectory(prefix="slo-review-test-") as folder:
            path = Path(folder) / "slo.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            reviewer = subprocess.run(
                [sys.executable, "-X", "utf8", str(SCRIPTS / "slo_review.py"),
                 "--slo-doc", str(path), "--format", "json"],
                capture_output=True, text=True, encoding="utf-8", timeout=10,
            )
        self.assertEqual(reviewer.returncode, 0, reviewer.stderr or reviewer.stdout)
        self.assertEqual(json.loads(reviewer.stdout), [])


if __name__ == "__main__":
    unittest.main()
