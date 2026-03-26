#!/usr/bin/env python3
"""
Tests for script_tester.py - Python Script Testing Tests

This test module validates the script_tester.py script's ability to:
- Validate Python syntax
- Check imports (stdlib only)
- Validate argparse implementation
- Test main guard presence
- Test script execution
- Test help functionality
- Test sample data processing
- Test output formats

Run with: python -m unittest test_script_tester
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

from script_tester import (
    ScriptTester,
    ScriptTestResult,
    TestSuite,
    TestReportFormatter as ReportFormatter,
)


class TestScriptTestResult(unittest.TestCase):
    """Tests for the ScriptTestResult class."""
    
    def test_create_result(self):
        """Test creating a script test result."""
        result = ScriptTestResult("/path/to/script.py")
        
        self.assertEqual(result.script_path, "/path/to/script.py")
        self.assertEqual(result.script_name, "script.py")
        self.assertIsNotNone(result.timestamp)
        self.assertEqual(result.tests, {})
        self.assertEqual(result.overall_status, "PENDING")
        self.assertEqual(result.execution_time, 0.0)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])
        
    def test_add_test_pass(self):
        """Test adding a passing test."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_test("syntax_valid", True, "Syntax is valid")
        
        self.assertIn("syntax_valid", result.tests)
        self.assertTrue(result.tests["syntax_valid"]["passed"])
        self.assertEqual(result.tests["syntax_valid"]["message"], "Syntax is valid")
        
    def test_add_test_fail(self):
        """Test adding a failing test."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_test("syntax_valid", False, "Syntax error on line 10")
        
        self.assertFalse(result.tests["syntax_valid"]["passed"])
        self.assertEqual(result.tests["syntax_valid"]["message"], "Syntax error on line 10")
        
    def test_add_test_with_details(self):
        """Test adding a test with details."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_test("imports_valid", False, "External imports found",
                       {"external_imports": ["requests", "numpy"]})
        
        self.assertIn("external_imports", result.tests["imports_valid"]["details"])
        
    def test_add_error(self):
        """Test adding an error."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_error("Script crashed during execution")
        
        self.assertIn("Script crashed during execution", result.errors)
        
    def test_add_warning(self):
        """Test adding a warning."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_warning("Help text could be more comprehensive")
        
        self.assertIn("Help text could be more comprehensive", result.warnings)
        
    def test_calculate_status_pass(self):
        """Test status calculation when all tests pass."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_test("test1", True, "Pass")
        result.add_test("test2", True, "Pass")
        result.add_test("test3", True, "Pass")
        
        result.calculate_status()
        
        self.assertEqual(result.overall_status, "PASS")
        
    def test_calculate_status_fail(self):
        """Test status calculation when most tests fail."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_test("test1", False, "Fail")
        result.add_test("test2", False, "Fail")
        result.add_test("test3", True, "Pass")
        
        result.calculate_status()
        
        self.assertEqual(result.overall_status, "FAIL")
        
    def test_calculate_status_partial(self):
        """Test status calculation when some tests pass."""
        result = ScriptTestResult("/path/to/script.py")
        result.add_test("test1", True, "Pass")
        result.add_test("test2", True, "Pass")
        result.add_test("test3", False, "Fail")
        
        result.calculate_status()
        
        self.assertEqual(result.overall_status, "PARTIAL")


class TestTestSuite(unittest.TestCase):
    """Tests for the TestSuite class."""
    
    def test_create_suite(self):
        """Test creating a test suite."""
        suite = TestSuite("/path/to/skill")
        
        self.assertEqual(suite.skill_path, "/path/to/skill")
        self.assertIsNotNone(suite.timestamp)
        self.assertEqual(suite.script_results, {})
        self.assertEqual(suite.summary, {})
        self.assertEqual(suite.global_errors, [])
        
    def test_add_script_result(self):
        """Test adding a script result."""
        suite = TestSuite("/path/to/skill")
        result = ScriptTestResult("/path/to/script.py")
        result.overall_status = "PASS"
        
        suite.add_script_result(result)
        
        self.assertIn("script.py", suite.script_results)
        
    def test_calculate_summary(self):
        """Test summary calculation."""
        suite = TestSuite("/path/to/skill")
        
        result1 = ScriptTestResult("/path/to/script1.py")
        result1.overall_status = "PASS"
        suite.add_script_result(result1)
        
        result2 = ScriptTestResult("/path/to/script2.py")
        result2.overall_status = "FAIL"
        suite.add_script_result(result2)
        
        suite.calculate_summary()
        
        self.assertEqual(suite.summary["total_scripts"], 2)
        self.assertEqual(suite.summary["passed"], 1)
        self.assertEqual(suite.summary["failed"], 1)
        
    def test_empty_suite_summary(self):
        """Test summary for empty suite."""
        suite = TestSuite("/path/to/skill")
        suite.calculate_summary()
        
        self.assertEqual(suite.summary["total_scripts"], 0)
        self.assertEqual(suite.summary["overall_status"], "NO_SCRIPTS")


class TestScriptTester(unittest.TestCase):
    """Tests for the ScriptTester class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.valid_skill_path = cls.fixtures_dir / "valid_skill"
        cls.invalid_skill_path = cls.fixtures_dir / "invalid_skill"
        
    def test_test_valid_skill(self):
        """Test testing a valid skill."""
        tester = ScriptTester(str(self.valid_skill_path))
        suite = tester.test_all_scripts()
        
        self.assertIsNotNone(suite)
        self.assertIn("example_tool.py", suite.script_results)
        
    def test_test_nonexistent_path(self):
        """Test testing a non-existent path."""
        tester = ScriptTester("/nonexistent/path")
        suite = tester.test_all_scripts()
        
        self.assertTrue(len(suite.global_errors) > 0)
        
    def test_syntax_validation_valid(self):
        """Test syntax validation of valid script."""
        tester = ScriptTester(str(self.valid_skill_path), verbose=True)
        script_path = self.valid_skill_path / "scripts" / "example_tool.py"
        
        result = ScriptTestResult(str(script_path))
        content = script_path.read_text()
        tester._test_syntax(content, result)
        
        self.assertTrue(result.tests["syntax_valid"]["passed"])
        
    def test_syntax_validation_invalid(self):
        """Test syntax validation of invalid script."""
        tester = ScriptTester(str(self.invalid_skill_path))
        script_path = self.invalid_skill_path / "broken_script.py"
        
        result = ScriptTestResult(str(script_path))
        content = script_path.read_text()
        tester._test_syntax(content, result)
        
        self.assertFalse(result.tests["syntax_valid"]["passed"])
        
    def test_import_validation_stdlib_only(self):
        """Test import validation with stdlib-only script."""
        tester = ScriptTester(str(self.valid_skill_path))
        script_path = self.valid_skill_path / "scripts" / "example_tool.py"
        
        result = ScriptTestResult(str(script_path))
        content = script_path.read_text()
        tester._test_imports(content, result)
        
        self.assertTrue(result.tests["imports_valid"]["passed"])
        
    def test_import_validation_external(self):
        """Test import validation with external imports."""
        tester = ScriptTester(str(self.invalid_skill_path))
        script_path = self.invalid_skill_path / "broken_script.py"
        
        result = ScriptTestResult(str(script_path))
        content = script_path.read_text()
        tester._test_imports(content, result)
        
        # Should detect requests and numpy
        self.assertFalse(result.tests["imports_valid"]["passed"])
        
    def test_argparse_validation(self):
        """Test argparse validation."""
        tester = ScriptTester(str(self.valid_skill_path))
        script_path = self.valid_skill_path / "scripts" / "example_tool.py"
        
        result = ScriptTestResult(str(script_path))
        content = script_path.read_text()
        tester._test_argparse_implementation(content, result)
        
        self.assertTrue(result.tests["argparse_implementation"]["passed"])
        
    def test_main_guard_validation(self):
        """Test main guard validation."""
        tester = ScriptTester(str(self.valid_skill_path))
        script_path = self.valid_skill_path / "scripts" / "example_tool.py"
        
        result = ScriptTestResult(str(script_path))
        content = script_path.read_text()
        tester._test_main_guard(content, result)
        
        self.assertTrue(result.tests["main_guard"]["passed"])
        
    def test_help_functionality(self):
        """Test --help functionality."""
        tester = ScriptTester(str(self.valid_skill_path), timeout=10)
        script_path = self.valid_skill_path / "scripts" / "example_tool.py"
        
        result = ScriptTestResult(str(script_path))
        tester._test_help_functionality(script_path, result)
        
        self.assertTrue(result.tests["help_functionality"]["passed"])


class TestExternalImportDetection(unittest.TestCase):
    """Tests for external import detection."""
    
    def test_stdlib_modules_list(self):
        """Test that common stdlib modules are recognized."""
        tester = ScriptTester("/tmp")
        
        # Create a script with stdlib imports
        test_script = """
import sys
import os
import json
import argparse
import pathlib
import datetime
import typing
import collections
import re
import math
"""
        
        import ast
        tree = ast.parse(test_script)
        external = tester._find_external_imports(tree)
        
        self.assertEqual(external, [])
        
    def test_external_modules_detected(self):
        """Test that external modules are detected."""
        tester = ScriptTester("/tmp")
        
        test_script = """
import requests
import numpy as np
import pandas as pd
import flask
"""
        
        import ast
        tree = ast.parse(test_script)
        external = tester._find_external_imports(tree)
        
        self.assertIn("requests", external)
        self.assertIn("numpy", external)
        self.assertIn("pandas", external)
        self.assertIn("flask", external)


class TestReportFormatterTests(unittest.TestCase):
    """Tests for the TestReportFormatter class."""
    
    def test_format_json(self):
        """Test JSON formatting."""
        suite = TestSuite("/test/skill")
        result = ScriptTestResult("/test/skill/scripts/test.py")
        result.add_test("syntax_valid", True, "Syntax OK")
        result.overall_status = "PASS"
        suite.add_script_result(result)
        suite.calculate_summary()
        
        json_output = ReportFormatter.format_json(suite)
        
        # Should be valid JSON
        parsed = json.loads(json_output)
        self.assertEqual(parsed["skill_path"], "/test/skill")
        
    def test_format_human_readable(self):
        """Test human-readable formatting."""
        suite = TestSuite("/test/skill")
        result = ScriptTestResult("/test/skill/scripts/test.py")
        result.add_test("syntax_valid", True, "Syntax OK")
        result.overall_status = "PASS"
        suite.add_script_result(result)
        suite.calculate_summary()
        
        text_output = ReportFormatter.format_human_readable(suite)
        
        self.assertIn("SCRIPT TESTING REPORT", text_output)
        self.assertIn("/test/skill", text_output)


class TestScriptTesterCLI(unittest.TestCase):
    """Tests for the command-line interface."""
    
    def test_cli_help(self):
        """Test CLI --help functionality."""
        import subprocess
        
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "script_tester.py"), "--help"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Test Python scripts", result.stdout)
        
    def test_cli_json_output(self):
        """Test CLI --json output."""
        import subprocess
        
        valid_skill = Path(__file__).parent / "fixtures" / "valid_skill"
        
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "script_tester.py"),
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
    
    def test_empty_script(self):
        """Test testing an empty script."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            script_path = scripts_dir / "empty.py"
            script_path.write_text("")
            
            tester = ScriptTester(str(skill_dir))
            suite = tester.test_all_scripts()
            
            # Should handle empty script without crashing
            self.assertIn("empty.py", suite.script_results)
            
    def test_script_with_encoding_issues(self):
        """Test script with encoding issues."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            script_path = scripts_dir / "encoded.py"
            # Write with explicit encoding
            script_path.write_text("# -*- coding: utf-8 -*-\nprint('Hello')", encoding='utf-8')
            
            tester = ScriptTester(str(skill_dir))
            suite = tester.test_all_scripts()
            
            # Should handle without crashing
            self.assertIsNotNone(suite)
            
    def test_very_long_script(self):
        """Test handling of very long scripts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            script_path = scripts_dir / "long.py"
            
            # Create a long script
            content = """
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()

if __name__ == "__main__":
    main()
"""
            # Add many functions
            for i in range(100):
                content += f"\ndef function_{i}():\n    pass\n"
                
            script_path.write_text(content)
            
            tester = ScriptTester(str(skill_dir))
            suite = tester.test_all_scripts()
            
            # Should handle without crashing
            self.assertIsNotNone(suite)


class TestScriptQualityPatterns(unittest.TestCase):
    """Tests for script quality pattern detection."""
    
    def test_detect_json_output_support(self):
        """Test detection of JSON output support."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            script_path = scripts_dir / "json_tool.py"
            script_path.write_text("""
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    if args.json:
        print(json.dumps({"status": "ok"}))
    else:
        print("OK")

if __name__ == "__main__":
    main()
""")
            
            tester = ScriptTester(str(skill_dir))
            suite = tester.test_all_scripts()
            
            result = suite.script_results["json_tool.py"]
            # Should detect JSON support
            self.assertTrue(
                result.tests.get("output_formats", {}).get("passed", False) or
                "json" in str(result.tests.get("output_formats", {}).get("details", {})).lower()
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)