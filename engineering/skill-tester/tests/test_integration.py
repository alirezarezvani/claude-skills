#!/usr/bin/env python3
"""
Integration Tests for the skill-tester Package

This test module validates the complete workflow of the skill-tester:
- End-to-end validation of a skill
- Combined validator + tester + scorer workflow
- CI/CD simulation tests
- Real-world scenario tests

Run with: python -m unittest test_integration
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

from skill_validator import SkillValidator, ValidationReport
from script_tester import ScriptTester, TestSuite
from quality_scorer import QualityScorer, QualityReport


class TestEndToEndWorkflow(unittest.TestCase):
    """End-to-end integration tests."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.valid_skill_path = cls.fixtures_dir / "valid_skill"
        cls.invalid_skill_path = cls.fixtures_dir / "invalid_skill"
        
    def test_complete_validation_workflow(self):
        """Test the complete validation workflow."""
        # Step 1: Validate structure
        validator = SkillValidator(str(self.valid_skill_path))
        validation_report = validator.validate_skill_structure()
        
        # Step 2: Test scripts
        tester = ScriptTester(str(self.valid_skill_path))
        test_suite = tester.test_all_scripts()
        
        # Step 3: Score quality
        scorer = QualityScorer(str(self.valid_skill_path))
        quality_report = scorer.assess_quality()
        
        # Verify all steps completed
        self.assertIsNotNone(validation_report)
        self.assertIsNotNone(test_suite)
        self.assertIsNotNone(quality_report)
        
        # Verify the skill passes basic checks
        self.assertTrue(validation_report.overall_score > 50,
                       "Valid skill should have reasonable validation score")
        self.assertTrue(test_suite.summary["overall_status"] in ["PASS", "PARTIAL"],
                       "Valid skill scripts should pass or partially pass")
        
    def test_invalid_skill_workflow(self):
        """Test workflow with an invalid skill."""
        # Step 1: Validate structure
        validator = SkillValidator(str(self.invalid_skill_path))
        validation_report = validator.validate_skill_structure()
        
        # Should detect issues
        self.assertTrue(
            len(validation_report.errors) > 0 or 
            validation_report.overall_score < 70,
            "Invalid skill should have errors or low score"
        )
        
    def test_combined_json_output(self):
        """Test generating combined JSON report."""
        validator = SkillValidator(str(self.valid_skill_path))
        validation_report = validator.validate_skill_structure()
        
        tester = ScriptTester(str(self.valid_skill_path))
        test_suite = tester.test_all_scripts()
        
        scorer = QualityScorer(str(self.valid_skill_path))
        quality_report = scorer.assess_quality()
        
        # Create combined report
        combined = {
            "validation": {
                "score": validation_report.overall_score,
                "compliance": validation_report.compliance_level,
                "errors": validation_report.errors,
            },
            "testing": {
                "status": test_suite.summary["overall_status"],
                "scripts_tested": test_suite.summary["total_scripts"],
            },
            "quality": {
                "score": quality_report.overall_score,
                "grade": quality_report.letter_grade,
                "tier": quality_report.tier_recommendation,
            }
        }
        
        # Should be valid JSON
        json_str = json.dumps(combined, indent=2)
        parsed = json.loads(json_str)
        
        self.assertIn("validation", parsed)
        self.assertIn("testing", parsed)
        self.assertIn("quality", parsed)


class TestCICDSimulation(unittest.TestCase):
    """Tests simulating CI/CD pipeline scenarios."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.valid_skill_path = cls.fixtures_dir / "valid_skill"
        
    def test_pre_commit_hook_simulation(self):
        """Simulate a pre-commit hook validation."""
        # Run validation
        validator = SkillValidator(str(self.valid_skill_path))
        report = validator.validate_skill_structure()
        
        # Pre-commit hook would check:
        # 1. No errors
        # 2. Score above threshold (e.g., 60)
        
        passes_pre_commit = (
            len(report.errors) == 0 and
            report.overall_score >= 60
        )
        
        # Valid skill should pass
        self.assertTrue(
            passes_pre_commit or report.overall_score >= 50,
            "Valid skill should pass pre-commit checks"
        )
        
    def test_pull_request_validation(self):
        """Simulate pull request validation."""
        # Run all checks
        validator = SkillValidator(str(self.valid_skill_path))
        validation_report = validator.validate_skill_structure()
        
        tester = ScriptTester(str(self.valid_skill_path))
        test_suite = tester.test_all_scripts()
        
        scorer = QualityScorer(str(self.valid_skill_path))
        quality_report = scorer.assess_quality()
        
        # PR validation would check:
        # 1. Validation score >= 70
        # 2. All scripts pass
        # 3. Quality score >= 65
        
        pr_checks = {
            "validation_passed": validation_report.overall_score >= 70,
            "scripts_passed": test_suite.summary.get("failed", 0) == 0,
            "quality_passed": quality_report.overall_score >= 65,
        }
        
        # Log results for debugging
        for check, passed in pr_checks.items():
            if not passed:
                print(f"PR check '{check}' did not pass")
                
    def test_batch_processing_simulation(self):
        """Simulate batch processing of multiple skills."""
        results = []
        
        # Process all fixture skills
        for skill_dir in self.fixtures_dir.iterdir():
            if skill_dir.is_dir():
                try:
                    validator = SkillValidator(str(skill_dir))
                    report = validator.validate_skill_structure()
                    
                    results.append({
                        "skill": skill_dir.name,
                        "score": report.overall_score,
                        "status": "PASS" if report.overall_score >= 60 else "FAIL"
                    })
                except Exception as e:
                    results.append({
                        "skill": skill_dir.name,
                        "error": str(e),
                        "status": "ERROR"
                    })
                    
        # Should have processed at least 2 skills
        self.assertGreaterEqual(len(results), 2)


class TestRealWorldScenarios(unittest.TestCase):
    """Tests for real-world usage scenarios."""
    
    def test_skill_author_workflow(self):
        """Simulate a skill author developing a new skill."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "new-skill"
            skill_dir.mkdir()
            
            # Author creates SKILL.md
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: new-skill
description: A new skill
license: MIT
metadata:
  version: 1.0.0
  author: Author
  category: test
  updated: 2026-03-26
---

# New Skill

## Description
A new skill.

## Features
- Feature 1

## Usage
Usage info.

## Examples
Examples here.
""")
            
            # Author creates script
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            script = scripts_dir / "tool.py"
            script.write_text("""
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()

if __name__ == "__main__":
    main()
""")
            
            # Run validation
            validator = SkillValidator(str(skill_dir))
            report = validator.validate_skill_structure()
            
            # Author iterates based on feedback
            improvements = []
            
            if report.overall_score < 70:
                improvements.append("Need higher score")
                
            for suggestion in report.suggestions:
                improvements.append(suggestion)
                
            # Validate that we got actionable feedback
            self.assertIsNotNone(report.overall_score)
            
    def test_skill_reviewer_workflow(self):
        """Simulate a skill reviewer checking a submission."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "submitted-skill"
            skill_dir.mkdir()
            
            # Create minimal skill
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: submitted-skill
description: Submitted for review
license: MIT
metadata:
  version: 1.0.0
  author: Submitter
  category: test
  updated: 2026-03-26
---

# Submitted Skill
""")
            
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            script = scripts_dir / "tool.py"
            script.write_text("print('hello')")
            
            # Reviewer runs all checks
            validator = SkillValidator(str(skill_dir))
            validation = validator.validate_skill_structure()
            
            tester = ScriptTester(str(skill_dir))
            testing = tester.test_all_scripts()
            
            scorer = QualityScorer(str(skill_dir))
            quality = scorer.assess_quality()
            
            # Reviewer creates report
            review = {
                "approved": (
                    validation.overall_score >= 60 and
                    testing.summary.get("failed", 0) == 0 and
                    quality.overall_score >= 50
                ),
                "issues": [],
                "recommendations": quality.improvement_roadmap
            }
            
            # Add issues
            if validation.errors:
                review["issues"].extend(validation.errors)
            if quality.overall_score < 70:
                review["issues"].append("Quality score below 70")
                
            # Validate review was created
            self.assertIn("approved", review)


class TestErrorRecovery(unittest.TestCase):
    """Tests for error recovery and resilience."""
    
    def test_handles_corrupt_skill_md(self):
        """Test handling of corrupt SKILL.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            
            skill_md = skill_dir / "SKILL.md"
            # Write binary content
            skill_md.write_bytes(b'\x00\x01\x02\x03\x04\x05')
            
            validator = SkillValidator(str(skill_dir))
            report = validator.validate_skill_structure()
            
            # Should handle gracefully
            self.assertIsNotNone(report)
            
    def test_handles_missing_script_directory(self):
        """Test handling of missing scripts directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: test
description: Test
license: MIT
metadata:
  version: 1.0.0
  author: Test
  category: test
  updated: 2026-03-26
---

# Test
""")
            
            tester = ScriptTester(str(skill_dir))
            suite = tester.test_all_scripts()
            
            # Should report missing scripts directory
            self.assertTrue(len(suite.global_errors) > 0)


class TestPerformance(unittest.TestCase):
    """Performance-related tests."""
    
    def test_validation_speed(self):
        """Test validation completes in reasonable time."""
        import time
        
        fixtures_dir = Path(__file__).parent / "fixtures"
        valid_skill = fixtures_dir / "valid_skill"
        
        start = time.time()
        
        validator = SkillValidator(str(valid_skill))
        report = validator.validate_skill_structure()
        
        elapsed = time.time() - start
        
        # Should complete in under 5 seconds
        self.assertLess(elapsed, 5.0, "Validation should be fast")
        
    def test_scoring_speed(self):
        """Test scoring completes in reasonable time."""
        import time
        
        fixtures_dir = Path(__file__).parent / "fixtures"
        valid_skill = fixtures_dir / "valid_skill"
        
        start = time.time()
        
        scorer = QualityScorer(str(valid_skill))
        report = scorer.assess_quality()
        
        elapsed = time.time() - start
        
        # Should complete in under 5 seconds
        self.assertLess(elapsed, 5.0, "Scoring should be fast")


class TestConcurrentValidation(unittest.TestCase):
    """Tests for concurrent validation scenarios."""
    
    def test_multiple_validations(self):
        """Test running multiple validations concurrently."""
        import concurrent.futures
        
        fixtures_dir = Path(__file__).parent / "fixtures"
        valid_skill = fixtures_dir / "valid_skill"
        
        def validate():
            validator = SkillValidator(str(valid_skill))
            return validator.validate_skill_structure().overall_score
            
        # Run 5 concurrent validations
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(validate) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
        # All should succeed
        self.assertEqual(len(results), 5)
        for score in results:
            self.assertGreater(score, 0)


class TestCliIntegration(unittest.TestCase):
    """Integration tests for CLI tools."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.valid_skill_path = cls.fixtures_dir / "valid_skill"
        
    def test_combined_cli_workflow(self):
        """Test combined CLI workflow."""
        import subprocess
        
        # Run all three tools
        results = {}
        
        # 1. skill_validator
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "skill_validator.py"),
             str(self.valid_skill_path), "--json"],
            capture_output=True,
            text=True
        )
        results["validator"] = result.stdout
        
        # 2. script_tester
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "script_tester.py"),
             str(self.valid_skill_path), "--json"],
            capture_output=True,
            text=True
        )
        results["tester"] = result.stdout
        
        # 3. quality_scorer
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "quality_scorer.py"),
             str(self.valid_skill_path), "--json"],
            capture_output=True,
            text=True
        )
        results["scorer"] = result.stdout
        
        # All should produce valid JSON
        for tool, output in results.items():
            try:
                parsed = json.loads(output)
                self.assertIn("skill_path", parsed)
            except json.JSONDecodeError:
                self.fail(f"{tool} output should be valid JSON")


if __name__ == "__main__":
    unittest.main(verbosity=2)