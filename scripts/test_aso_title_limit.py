#!/usr/bin/env python3
"""test_aso_title_limit.py — regression tests for Google Play's 30-char title limit.

Verifies that the app-store-optimization skill enforces Google Play's 30-character
app title limit (reduced from 50 in 2021) consistently across metadata
optimization, title generation, localization, launch checklists, and fixtures,
while preserving Apple App Store behavior.

Stdlib only (unittest). Lives in scripts/ alongside test_derive_counters.py so it
runs without third-party test runners and does not inflate derived skill-tool
counters.
"""

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASO_DIR = REPO_ROOT / "marketing-skill" / "skills" / "app-store-optimization"
ASO_SCRIPTS = ASO_DIR / "scripts"
sys.path.insert(0, str(ASO_SCRIPTS))

from launch_checklist import LaunchChecklistGenerator, generate_launch_checklist  # noqa: E402
from localization_helper import LocalizationHelper  # noqa: E402
from metadata_optimizer import MetadataOptimizer, optimize_app_metadata  # noqa: E402


class GooglePlayTitleLimitTests(unittest.TestCase):
    """Google Play enforces a 30-character maximum on app titles."""

    def test_metadata_optimizer_google_char_limits(self):
        optimizer = MetadataOptimizer("google")
        self.assertEqual(optimizer.limits["title"], 30)
        self.assertEqual(optimizer.limits["short_description"], 80)
        self.assertEqual(optimizer.limits["full_description"], 4000)

    def test_metadata_validation_boundary_lengths_google(self):
        optimizer = MetadataOptimizer("google")

        for valid_len in (29, 30):
            with self.subTest(length=valid_len):
                report = optimizer.validate_character_limits({"title": "A" * valid_len})
                self.assertTrue(report["is_valid"])
                self.assertEqual(report["errors"], [])
                status = report["field_status"]["title"]
                self.assertTrue(status["is_valid"])
                self.assertEqual(status["length"], valid_len)
                self.assertEqual(status["limit"], 30)
                self.assertEqual(status["remaining"], 30 - valid_len)

        for invalid_len in (31, 50):
            with self.subTest(length=invalid_len):
                report = optimizer.validate_character_limits({"title": "A" * invalid_len})
                self.assertFalse(report["is_valid"])
                status = report["field_status"]["title"]
                self.assertFalse(status["is_valid"])
                self.assertEqual(status["length"], invalid_len)
                self.assertEqual(status["limit"], 30)
                self.assertEqual(status["remaining"], 30 - invalid_len)
                self.assertEqual(len(report["errors"]), 1)
                self.assertIn(f"{invalid_len}/30", report["errors"][0])

    def test_title_generation_respects_30_char_limit_google(self):
        optimizer = MetadataOptimizer("google")

        # Keyword combination that fits in 30 chars vs one that only fit under 50
        within_30 = optimizer.optimize_title(
            "TaskFlow",
            ["AI Task Manager", "Team Productivity & Workflow"],
            include_brand=True,
        )
        self.assertEqual(within_30["max_length"], 30)
        self.assertTrue(within_30["options"])
        for opt in within_30["options"]:
            self.assertLessEqual(len(opt["title"]), 30)
            self.assertEqual(opt["length"], len(opt["title"]))
            self.assertEqual(opt["remaining_chars"], 30 - len(opt["title"]))

        # Keyword that would produce a 46-char title must not be emitted
        over_30_kw = optimizer.optimize_title(
            "TaskFlow",
            ["AI Task Manager & Team Productivity"],
            include_brand=True,
        )
        for opt in over_30_kw["options"]:
            self.assertLessEqual(len(opt["title"]), 30)
            self.assertNotEqual(opt["strategy"], "brand_plus_primary")

        # Brand-only truncation when app_name itself exceeds 30 chars
        long_brand = optimizer.optimize_title("B" * 50, [], include_brand=True)
        self.assertEqual(len(long_brand["options"][0]["title"]), 30)
        self.assertEqual(long_brand["options"][0]["remaining_chars"], 0)

        # Keyword-first (no brand) truncation when joined keywords exceed 30 chars
        keyword_first = optimizer.optimize_title(
            "TaskFlow",
            ["ai task prioritization", "team collaboration tools"],
            include_brand=False,
        )
        self.assertTrue(keyword_first["options"])
        for opt in keyword_first["options"]:
            self.assertLessEqual(len(opt["title"]), 30)

        # Top-level convenience wrapper
        package = optimize_app_metadata(
            "google",
            {
                "name": "TaskFlow",
                "unique_value": "Organize team work",
                "key_features": ["Task lists", "Reminders"],
                "target_audience": "Teams",
            },
            ["AI Task Manager", "Team Productivity & Workflow"],
        )
        self.assertEqual(package["title"]["max_length"], 30)
        for opt in package["title"]["options"]:
            self.assertLessEqual(len(opt["title"]), 30)
        self.assertIsNone(package["keyword_field"])

    def test_localization_enforces_30_char_limit_google(self):
        helper = LocalizationHelper()

        for valid_len in (29, 30):
            with self.subTest(method="validate_translations", length=valid_len):
                res = helper.validate_translations(
                    {"title": "T" * valid_len}, "es-ES", platform="google"
                )
                self.assertTrue(res["is_valid"])
                self.assertEqual(res["errors"], [])
                self.assertEqual(res["field_validations"]["title"]["limit"], 30)
                self.assertTrue(res["field_validations"]["title"]["is_valid"])

            with self.subTest(method="translate_metadata", length=valid_len):
                res = helper.translate_metadata(
                    {"title": "T" * valid_len}, "en", "en-GB", platform="google"
                )
                field = res["localized_fields"]["title"]
                self.assertEqual(field["character_limit"], 30)
                self.assertTrue(field["fits_within_limit"])
                self.assertEqual(res["warnings"], [])

        for invalid_len in (31, 50):
            with self.subTest(method="validate_translations", length=invalid_len):
                res = helper.validate_translations(
                    {"title": "T" * invalid_len}, "es-ES", platform="google"
                )
                self.assertFalse(res["is_valid"])
                self.assertFalse(res["field_validations"]["title"]["is_valid"])
                self.assertEqual(res["field_validations"]["title"]["limit"], 30)
                self.assertTrue(any(f"{invalid_len}/30" in e for e in res["errors"]))

            with self.subTest(method="translate_metadata", length=invalid_len):
                res = helper.translate_metadata(
                    {"title": "T" * invalid_len}, "en", "en-GB", platform="google"
                )
                field = res["localized_fields"]["title"]
                self.assertEqual(field["character_limit"], 30)
                self.assertFalse(field["fits_within_limit"])
                self.assertTrue(any("limit (30)" in w for w in res["warnings"]))

        # German expansion (1.3x) pushing a 25-char English title to 32 chars
        expanded = helper.translate_metadata(
            {"title": "T" * 25}, "en", "de-DE", platform="google"
        )
        self.assertEqual(expanded["localized_fields"]["title"]["character_limit"], 30)
        self.assertFalse(expanded["localized_fields"]["title"]["fits_within_limit"])

    def test_launch_checklist_enforces_30_char_limit_google(self):
        generator = LaunchChecklistGenerator("both")
        checklist = generator.generate_prelaunch_checklist({"name": "TaskFlow"})
        google_metadata_items = next(
            cat["items"]
            for cat in checklist["checklists"]["google"]
            if cat["category"] == "Metadata (Google)"
        )
        tasks = [item["task"] for item in google_metadata_items]
        self.assertIn("App title (30 chars max)", tasks)
        self.assertFalse(any("50 chars" in t for t in tasks))

        standalone = generate_launch_checklist("google", {"name": "TaskFlow"})
        google_only_tasks = [
            item["task"]
            for cat in standalone["checklists"]["google"]
            for item in cat["items"]
        ]
        self.assertIn("App title (30 chars max)", google_only_tasks)

        base_app_data = {
            "privacy_policy_url": "https://example.com/privacy",
            "feature_graphic": "feature.png",
            "short_description": "Organize daily tasks with your team",
        }
        for valid_len in (29, 30):
            with self.subTest(length=valid_len):
                res = generator.validate_app_store_compliance(
                    {**base_app_data, "title": "G" * valid_len},
                    platform="google",
                )
                self.assertTrue(res["is_compliant"])
                self.assertEqual(res["errors"], [])

        for invalid_len in (31, 50):
            with self.subTest(length=invalid_len):
                res = generator.validate_app_store_compliance(
                    {**base_app_data, "title": "G" * invalid_len},
                    platform="google",
                )
                self.assertFalse(res["is_compliant"])
                self.assertIn(
                    f"Title exceeds 30 characters ({invalid_len})",
                    res["errors"],
                )

    def test_expected_output_fixture_google_titles_within_30_chars(self):
        fixture = json.loads((ASO_DIR / "expected_output.json").read_text(encoding="utf-8"))
        google_options = fixture["metadata_recommendations"]["google_play_store"]["title_options"]
        self.assertTrue(google_options)
        for opt in google_options:
            self.assertLessEqual(len(opt["title"]), 30)
            self.assertEqual(opt["length"], len(opt["title"]))


class AppleAppStoreUnchangedTests(unittest.TestCase):
    """Apple App Store limits and behavior remain unchanged."""

    def test_apple_metadata_optimizer_unchanged(self):
        optimizer = MetadataOptimizer("apple")
        self.assertEqual(
            optimizer.limits,
            {
                "title": 30,
                "subtitle": 30,
                "promotional_text": 170,
                "description": 4000,
                "keywords": 100,
                "whats_new": 4000,
            },
        )

        for valid_len in (29, 30):
            report = optimizer.validate_character_limits(
                {"title": "I" * valid_len, "subtitle": "S" * 30, "keywords": "k" * 100}
            )
            self.assertTrue(report["is_valid"])

        for invalid_len in (31, 50):
            report = optimizer.validate_character_limits({"title": "I" * invalid_len})
            self.assertFalse(report["is_valid"])
            self.assertIn(f"{invalid_len}/30", report["errors"][0])

        generated = optimizer.optimize_title("TaskFlow", ["AI Task Manager"])
        self.assertEqual(generated["max_length"], 30)
        for opt in generated["options"]:
            self.assertLessEqual(len(opt["title"]), 30)

        kw_result = optimizer.optimize_keyword_field(["todo", "planner", "tasks"], app_title="TaskFlow")
        self.assertIn("keyword_field", kw_result)
        self.assertLessEqual(kw_result["length"], 100)

    def test_apple_localization_and_launch_checklist_unchanged(self):
        helper = LocalizationHelper()
        self.assertTrue(
            helper.validate_translations(
                {"title": "I" * 30, "subtitle": "S" * 30, "keywords": "k" * 100},
                "fr-FR",
                platform="apple",
            )["is_valid"]
        )
        self.assertFalse(
            helper.validate_translations(
                {"title": "I" * 31}, "fr-FR", platform="apple"
            )["is_valid"]
        )

        generator = LaunchChecklistGenerator("apple")
        checklist = generator.generate_prelaunch_checklist({"name": "TaskFlow"})
        apple_tasks = [
            item["task"]
            for cat in checklist["checklists"]["apple"]
            for item in cat["items"]
        ]
        self.assertIn("App title (30 chars max)", apple_tasks)
        self.assertIn("Subtitle (30 chars max)", apple_tasks)

        base_ios = {
            "privacy_policy_url": "https://example.com/privacy",
            "app_icon": "icon.png",
            "subtitle": "Daily Task Planner",
            "keywords": "k" * 85,
        }
        self.assertTrue(
            generator.validate_app_store_compliance(
                {**base_ios, "title": "I" * 30}, platform="apple"
            )["is_compliant"]
        )
        invalid_ios = generator.validate_app_store_compliance(
            {**base_ios, "title": "I" * 31}, platform="apple"
        )
        self.assertFalse(invalid_ios["is_compliant"])
        self.assertIn("Title exceeds 30 characters (31)", invalid_ios["errors"])


if __name__ == "__main__":
    unittest.main()
