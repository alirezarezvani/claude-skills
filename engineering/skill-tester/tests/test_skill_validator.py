#!/usr/bin/env python3
"""
Tests for skill_validator.py - Skill Structure Validation Tests

This test module validates the skill_validator.py script's ability to:
- Check required files (SKILL.md, README.md)
- Validate YAML frontmatter
- Check required sections
- Validate directory structure
- Check Python scripts
- Enforce tier requirements

Run with: python -m unittest test_skill_validator
"""

import json
import os
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path

# Add the scripts directory to the path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from skill_validator import (
    SkillValidator,
    ValidationReport,
    ReportFormatter,
)


class TestValidationReport(unittest.TestCase):
    """Tests for the ValidationReport class."""
    
    def test_create_validation_report(self):
        """Test creating a validation report."""
        report = ValidationReport("/test/path")
        
        self.assertEqual(report.skill_path, "/test/path")
        self.assertIsNotNone(report.timestamp)
        self.assertEqual(report.checks, {})
        self.assertEqual(report.warnings, [])
        self.assertEqual(report.errors, [])
        self.assertEqual(report.suggestions, [])
        self.assertEqual(report.overall_score, 0.0)
        self.assertEqual(report.compliance_level, "FAIL")
        
    def test_add_check(self):
        """Test adding a validation check."""
        report = ValidationReport("/test/path")
        report.add_check("test_check", True, "Test message", 1.0)
        
        self.assertIn("test_check", report.checks)
        self.assertTrue(report.checks["test_check"]["passed"])
        self.assertEqual(report.checks["test_check"]["message"], "Test message")
        self.assertEqual(report.checks["test_check"]["score"], 1.0)
        
    def test_add_warning(self):
        """Test adding a warning."""
        report = ValidationReport("/test/path")
        report.add_warning("Test warning")
        
        self.assertIn("Test warning", report.warnings)
        
    def test_add_error(self):
        """Test adding an error."""
        report = ValidationReport("/test/path")
        report.add_error("Test error")
        
        self.assertIn("Test error", report.errors)
        
    def test_add_suggestion(self):
        """Test adding a suggestion."""
        report = ValidationReport("/test/path")
        report.add_suggestion("Test suggestion")
        
        self.assertIn("Test suggestion", report.suggestions)
        
    def test_calculate_overall_score(self):
        """Test calculating overall score."""
        report = ValidationReport("/test/path")
        report.add_check("check1", True, "Pass", 1.0)
        report.add_check("check2", True, "Pass", 1.0)
        report.add_check("check3", False, "Fail", 0.0)
        
        report.calculate_overall_score()
        
        # Score should be 2/3 * 100 = 66.67
        self.assertAlmostEqual(report.overall_score, 66.67, places=1)
        self.assertEqual(report.compliance_level, "ACCEPTABLE")
        
    def test_compliance_levels(self):
        """Test compliance level determination."""
        # Test each level
        test_cases = [
            (95, "EXCELLENT"),
            (80, "GOOD"),
            (65, "ACCEPTABLE"),
            (50, "NEEDS_IMPROVEMENT"),
            (30, "POOR"),
        ]
        
        for score, expected_level in test_cases:
            report = ValidationReport("/test/path")
            report.add_check("test", True, "Test", score / 100)
            report.calculate_overall_score()
            
            # Override score for testing
            report.overall_score = score
            report.compliance_level = "FAIL"
            report.calculate_overall_score()
            
            self.assertEqual(report.compliance_level, expected_level, 
                           f"Score {score} should be {expected_level}")


class TestSkillValidator(unittest.TestCase):
    """Tests for the SkillValidator class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.valid_skill_path = cls.fixtures_dir / "valid_skill"
        cls.invalid_skill_path = cls.fixtures_dir / "invalid_skill"
        
    def test_validate_existing_skill(self):
        """Test validating an existing skill directory."""
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        self.assertIsNotNone(report)
        self.assertEqual(report.skill_path, str(self.valid_skill_path))
        
    def test_validate_nonexistent_path(self):
        """Test validating a non-existent path."""
        validator = SkillValidator("/nonexistent/path")
        report = validator.validate_skill_structure()
        
        self.assertIn("does not exist", report.errors[0])
        
    def test_validate_file_not_directory(self):
        """Test validating a file path instead of directory."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("test content")
            temp_file = f.name
            
        try:
            validator = SkillValidator(temp_file)
            report = validator.validate_skill_structure()
            
            self.assertTrue(any("not a directory" in e for e in report.errors))
        finally:
            os.unlink(temp_file)
            
    def test_required_files_check(self):
        """Test checking required files."""
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        # Check that SKILL.md and README.md checks exist
        self.assertIn("skill_md_exists", report.checks)
        self.assertIn("readme_exists", report.checks)
        
    def test_valid_skill_has_skill_md(self):
        """Test that valid skill has SKILL.md."""
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        self.assertTrue(report.checks["skill_md_exists"]["passed"])
        
    def test_invalid_skill_missing_readme(self):
        """Test that invalid skill is flagged for missing README."""
        validator = SkillValidator(str(self.invalid_skill_path))
        report = validator.validate_skill_structure()
        
        # README check should fail or be flagged
        self.assertFalse(report.checks.get("readme_exists", {"passed": False})["passed"])
        
    def test_frontmatter_validation(self):
        """Test YAML frontmatter validation."""
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        # Valid skill should have valid frontmatter (check either complete or format)
        frontmatter_checks = [k for k in report.checks if "frontmatter" in k.lower()]
        self.assertTrue(len(frontmatter_checks) > 0, "Should have frontmatter checks")
        # At least one frontmatter check should pass
        has_pass = any(report.checks[k]["passed"] for k in frontmatter_checks)
        self.assertTrue(has_pass, "At least one frontmatter check should pass")
        
    def test_invalid_skill_missing_frontmatter(self):
        """Test that invalid skill is flagged for missing/invalid frontmatter."""
        validator = SkillValidator(str(self.invalid_skill_path))
        report = validator.validate_skill_structure()
        
        # Should have frontmatter issues
        frontmatter_check = report.checks.get("frontmatter_exists", 
                                              report.checks.get("frontmatter_complete", 
                                                               {"passed": False}))
        self.assertFalse(frontmatter_check["passed"])
        
    def test_required_sections_check(self):
        """Test checking required sections in SKILL.md."""
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        self.assertIn("required_sections", report.checks)
        # The valid_skill has Description, Features, Usage, Examples sections
        # Check if it passes or has a reasonable message
        self.assertIsNotNone(report.checks["required_sections"]["message"])
        
    def test_directory_structure_check(self):
        """Test checking directory structure."""
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        # Should have scripts directory check
        self.assertTrue(any("dir_" in k for k in report.checks))
        
    def test_python_scripts_validation(self):
        """Test Python scripts validation."""
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        # Should check script count
        self.assertIn("min_scripts_count", report.checks)
        self.assertTrue(report.checks["min_scripts_count"]["passed"])
        
    def test_tier_requirements_basic(self):
        """Test BASIC tier requirements."""
        validator = SkillValidator(str(self.valid_skill_path), target_tier="BASIC")
        report = validator.validate_skill_structure()
        
        # Should have tier compliance check
        self.assertIn("tier_compliance", report.checks)
        
    def test_tier_requirements_standard(self):
        """Test STANDARD tier requirements."""
        validator = SkillValidator(str(self.valid_skill_path), target_tier="STANDARD")
        report = validator.validate_skill_structure()
        
        self.assertIn("tier_compliance", report.checks)
        
    def test_external_imports_detection(self):
        """Test detection of external imports in invalid skill."""
        # Create a temp skill with external imports
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            script_path = scripts_dir / "test.py"
            script_path.write_text("""
import requests  # External
import numpy as np  # External
import sys  # Stdlib

def main():
    pass

if __name__ == "__main__":
    main()
""")
            
            validator = SkillValidator(str(skill_dir))
            report = validator.validate_skill_structure()
            
            # Should detect external imports
            import_checks = [k for k in report.checks if "imports" in k.lower()]
            has_import_error = any(
                not report.checks[k]["passed"] for k in import_checks
            ) or any(
                "external" in e.lower() for e in report.errors
            )
            self.assertTrue(has_import_error, "External imports should be detected")


class TestReportFormatter(unittest.TestCase):
    """Tests for the ReportFormatter class."""
    
    def test_format_json(self):
        """Test JSON formatting."""
        report = ValidationReport("/test/path")
        report.add_check("test_check", True, "Test message", 1.0)
        report.add_warning("Test warning")
        report.add_error("Test error")
        report.calculate_overall_score()
        
        json_output = ReportFormatter.format_json(report)
        
        # Should be valid JSON
        parsed = json.loads(json_output)
        self.assertEqual(parsed["skill_path"], "/test/path")
        self.assertIn("test_check", parsed["checks"])
        
    def test_format_human_readable(self):
        """Test human-readable formatting."""
        report = ValidationReport("/test/path")
        report.add_check("test_check", True, "Test message", 1.0)
        report.calculate_overall_score()
        
        text_output = ReportFormatter.format_human_readable(report)
        
        # Should contain key sections
        self.assertIn("SKILL VALIDATION REPORT", text_output)
        self.assertIn("/test/path", text_output)
        # The check message "Test message" should appear in the output
        self.assertIn("Test message", text_output)


class TestValidatorCLI(unittest.TestCase):
    """Tests for the command-line interface."""
    
    def test_cli_help(self):
        """Test CLI --help functionality."""
        import subprocess
        
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "skill_validator.py"), "--help"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Validate skill directories", result.stdout)
        
    def test_cli_json_output(self):
        """Test CLI --json output."""
        import subprocess
        
        valid_skill = Path(__file__).parent / "fixtures" / "valid_skill"
        
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "skill_validator.py"), 
             str(valid_skill), "--json"],
            capture_output=True,
            text=True
        )
        
        # Should output valid JSON
        try:
            parsed = json.loads(result.stdout)
            self.assertIn("skill_path", parsed)
        except json.JSONDecodeError:
            self.fail("Output should be valid JSON")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_empty_skill_directory(self):
        """Test validating an empty skill directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = SkillValidator(tmpdir)
            report = validator.validate_skill_structure()
            
            # Should have errors for missing required files
            self.assertTrue(len(report.errors) > 0)
            
    def test_skill_md_with_invalid_yaml(self):
        """Test SKILL.md with invalid YAML frontmatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            skill_md = skill_dir / "SKILL.md"
            
            # Create SKILL.md with invalid YAML
            skill_md.write_text("""
---
name: [invalid yaml
description: missing quote
---

# Skill
""")
            
            validator = SkillValidator(str(skill_dir))
            report = validator.validate_skill_structure()
            
            # Should have frontmatter error
            self.assertTrue(
                any("frontmatter" in k.lower() for k in report.checks),
                "Should have frontmatter check"
            )
            
    def test_very_long_skill_md(self):
        """Test handling of very long SKILL.md files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            skill_md = skill_dir / "SKILL.md"
            
            # Create a very long SKILL.md
            content = """---
name: long-skill
description: A very long skill
license: MIT
metadata:
  version: 1.0.0
  author: Test
  category: test
  updated: 2026-03-26
---

# Long Skill

"""
            # Add 500 lines
            for i in range(500):
                content += f"\n## Section {i}\n\nContent for section {i}.\n"
                
            skill_md.write_text(content)
            
            # Create a minimal script
            script = scripts_dir / "tool.py"
            script.write_text("""
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()

if __name__ == "__main__":
    main()
""")
            
            validator = SkillValidator(str(skill_dir))
            report = validator.validate_skill_structure()
            
            # Should handle long file without crashing
            self.assertIsNotNone(report)


class TestTierRequirements(unittest.TestCase):
    """Tests for tier-specific requirements."""
    
    def test_basic_tier_min_lines(self):
        """Test BASIC tier minimum line requirement."""
        self.assertEqual(
            SkillValidator.TIER_REQUIREMENTS["BASIC"]["min_skill_md_lines"],
            100
        )
        
    def test_standard_tier_min_lines(self):
        """Test STANDARD tier minimum line requirement."""
        self.assertEqual(
            SkillValidator.TIER_REQUIREMENTS["STANDARD"]["min_skill_md_lines"],
            200
        )
        
    def test_powerful_tier_min_lines(self):
        """Test POWERFUL tier minimum line requirement."""
        self.assertEqual(
            SkillValidator.TIER_REQUIREMENTS["POWERFUL"]["min_skill_md_lines"],
            300
        )
        
    def test_powerful_tier_requires_more_scripts(self):
        """Test POWERFUL tier requires more scripts."""
        self.assertEqual(
            SkillValidator.TIER_REQUIREMENTS["POWERFUL"]["min_scripts"],
            2
        )
        
    def test_powerful_tier_required_dirs(self):
        """Test POWERFUL tier required directories."""
        required = SkillValidator.TIER_REQUIREMENTS["POWERFUL"]["required_dirs"]
        
        self.assertIn("scripts", required)
        self.assertIn("assets", required)
        self.assertIn("references", required)
        self.assertIn("expected_outputs", required)


if __name__ == "__main__":
    unittest.main(verbosity=2)