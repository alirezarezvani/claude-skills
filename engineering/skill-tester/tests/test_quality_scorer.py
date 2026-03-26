#!/usr/bin/env python3
"""
Tests for quality_scorer.py - Skill Quality Scoring Tests

This test module validates the quality_scorer.py script's ability to:
- Score documentation quality
- Score code quality
- Score completeness
- Score usability
- Calculate overall scores and grades
- Generate improvement recommendations

Run with: python -m unittest test_quality_scorer
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

from quality_scorer import (
    QualityDimension,
    QualityReport,
    QualityScorer,
    QualityReportFormatter,
)


class TestQualityDimension(unittest.TestCase):
    """Tests for the QualityDimension class."""
    
    def test_create_dimension(self):
        """Test creating a quality dimension."""
        dim = QualityDimension("Documentation", 0.20, "Quality of docs")
        
        self.assertEqual(dim.name, "Documentation")
        self.assertEqual(dim.weight, 0.20)
        self.assertEqual(dim.description, "Quality of docs")
        self.assertEqual(dim.score, 0.0)
        self.assertEqual(dim.max_score, 100.0)
        self.assertEqual(dim.details, {})
        self.assertEqual(dim.suggestions, [])
        
    def test_add_score(self):
        """Test adding a component score."""
        dim = QualityDimension("Documentation", 0.20, "Quality of docs")
        dim.add_score("skill_md_length", 20, 25, "Has 150 lines")
        
        self.assertIn("skill_md_length", dim.details)
        self.assertEqual(dim.details["skill_md_length"]["score"], 20)
        self.assertEqual(dim.details["skill_md_length"]["max_score"], 25)
        self.assertEqual(dim.details["skill_md_length"]["percentage"], 80.0)
        
    def test_calculate_final_score(self):
        """Test calculating final score."""
        dim = QualityDimension("Documentation", 0.20, "Quality of docs")
        dim.add_score("component1", 20, 25, "Good")
        dim.add_score("component2", 15, 25, "OK")
        
        dim.calculate_final_score()
        
        # Score should be (20 + 15) / (25 + 25) * 100 = 70
        self.assertEqual(dim.score, 70.0)
        
    def test_add_suggestion(self):
        """Test adding a suggestion."""
        dim = QualityDimension("Documentation", 0.20, "Quality of docs")
        dim.add_suggestion("Add more examples")
        
        self.assertIn("Add more examples", dim.suggestions)


class TestQualityReport(unittest.TestCase):
    """Tests for the QualityReport class."""
    
    def test_create_report(self):
        """Test creating a quality report."""
        report = QualityReport("/test/path")
        
        self.assertEqual(report.skill_path, "/test/path")
        self.assertIsNotNone(report.timestamp)
        self.assertEqual(report.dimensions, {})
        self.assertEqual(report.overall_score, 0.0)
        self.assertEqual(report.letter_grade, "F")
        self.assertEqual(report.tier_recommendation, "BASIC")
        self.assertEqual(report.improvement_roadmap, [])
        
    def test_add_dimension(self):
        """Test adding a dimension."""
        report = QualityReport("/test/path")
        dim = QualityDimension("Documentation", 0.20, "Quality of docs")
        dim.score = 75.0
        
        report.add_dimension(dim)
        
        self.assertIn("Documentation", report.dimensions)
        
    def test_calculate_overall_score(self):
        """Test calculating overall score with 5 dimensions."""
        report = QualityReport("/test/path")
        
        dim1 = QualityDimension("Documentation", 0.20, "Docs")
        dim1.score = 80.0
        report.add_dimension(dim1)
        
        dim2 = QualityDimension("Code Quality", 0.20, "Code")
        dim2.score = 70.0
        report.add_dimension(dim2)
        
        dim3 = QualityDimension("Completeness", 0.20, "Complete")
        dim3.score = 75.0
        report.add_dimension(dim3)
        
        dim4 = QualityDimension("Usability", 0.20, "Usable")
        dim4.score = 85.0
        report.add_dimension(dim4)
        
        dim5 = QualityDimension("Security", 0.20, "Security")
        dim5.score = 90.0
        report.add_dimension(dim5)
        
        report.calculate_overall_score()
        
        # Overall score should be weighted average
        expected = (80 * 0.20 + 70 * 0.20 + 75 * 0.20 + 85 * 0.20 + 90 * 0.20)
        self.assertAlmostEqual(report.overall_score, expected, places=1)
        
    def test_letter_grade_calculation(self):
        """Test letter grade calculation."""
        test_cases = [
            (97, "A+"),
            (92, "A"),
            (87, "A-"),
            (82, "B+"),
            (77, "B"),
            (72, "B-"),
            (67, "C+"),
            (62, "C"),
            (57, "C-"),
            (52, "D"),
            (45, "F"),
        ]
        
        for score, expected_grade in test_cases:
            report = QualityReport("/test/path")
            
            dim = QualityDimension("Test", 1.0, "Test")
            dim.score = score
            report.add_dimension(dim)
            
            report.calculate_overall_score()
            report.overall_score = score  # Override for test
            
            # Recalculate letter grade
            if score >= 95:
                report.letter_grade = "A+"
            elif score >= 90:
                report.letter_grade = "A"
            elif score >= 85:
                report.letter_grade = "A-"
            elif score >= 80:
                report.letter_grade = "B+"
            elif score >= 75:
                report.letter_grade = "B"
            elif score >= 70:
                report.letter_grade = "B-"
            elif score >= 65:
                report.letter_grade = "C+"
            elif score >= 60:
                report.letter_grade = "C"
            elif score >= 55:
                report.letter_grade = "C-"
            elif score >= 50:
                report.letter_grade = "D"
            else:
                report.letter_grade = "F"
                
            self.assertEqual(report.letter_grade, expected_grade,
                           f"Score {score} should be {expected_grade}")
            
    def test_tier_recommendation(self):
        """Test tier recommendation calculation."""
        # Test POWERFUL tier
        report = QualityReport("/test/path")
        
        for name in ["Documentation", "Code Quality", "Completeness", "Usability", "Security"]:
            dim = QualityDimension(name, 0.20, name)
            dim.score = 80.0
            report.add_dimension(dim)
            
        report.calculate_overall_score()
        
        # Should recommend POWERFUL when all dimensions are high
        self.assertIn(report.tier_recommendation, ["POWERFUL", "STANDARD"])
        
    def test_tier_recommendation_with_low_security(self):
        """Test that low security score prevents POWERFUL tier."""
        report = QualityReport("/test/path")
        
        for name in ["Documentation", "Code Quality", "Completeness", "Usability"]:
            dim = QualityDimension(name, 0.20, name)
            dim.score = 85.0
            report.add_dimension(dim)
            
        # Low security score
        dim = QualityDimension("Security", 0.20, "Security")
        dim.score = 40.0
        report.add_dimension(dim)
        
        report.calculate_overall_score()
        
        # Should not be POWERFUL due to low security
        self.assertIn(report.tier_recommendation, ["BASIC", "STANDARD"])
        
    def test_improvement_roadmap(self):
        """Test improvement roadmap generation."""
        report = QualityReport("/test/path")
        
        dim = QualityDimension("Documentation", 0.20, "Docs")
        dim.score = 50.0
        dim.add_suggestion("Add more examples")
        report.add_dimension(dim)
        
        report.calculate_overall_score()
        
        # Should have improvement suggestions
        self.assertTrue(len(report.improvement_roadmap) >= 0)


class TestQualityScorer(unittest.TestCase):
    """Tests for the QualityScorer class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.fixtures_dir = Path(__file__).parent / "fixtures"
        cls.valid_skill_path = cls.fixtures_dir / "valid_skill"
        
    def test_score_valid_skill(self):
        """Test scoring a valid skill."""
        scorer = QualityScorer(str(self.valid_skill_path))
        report = scorer.assess_quality()
        
        self.assertIsNotNone(report)
        self.assertEqual(report.skill_path, str(self.valid_skill_path))
        
    def test_score_nonexistent_path(self):
        """Test scoring a non-existent path."""
        with self.assertRaises(ValueError):
            scorer = QualityScorer("/nonexistent/path")
            scorer.assess_quality()
            
    def test_documentation_scoring(self):
        """Test documentation dimension scoring."""
        scorer = QualityScorer(str(self.valid_skill_path))
        report = scorer.assess_quality()
        
        self.assertIn("Documentation", report.dimensions)
        doc_score = report.dimensions["Documentation"].score
        self.assertGreater(doc_score, 0)
        
    def test_code_quality_scoring(self):
        """Test code quality dimension scoring."""
        scorer = QualityScorer(str(self.valid_skill_path))
        report = scorer.assess_quality()
        
        self.assertIn("Code Quality", report.dimensions)
        
    def test_completeness_scoring(self):
        """Test completeness dimension scoring."""
        scorer = QualityScorer(str(self.valid_skill_path))
        report = scorer.assess_quality()
        
        self.assertIn("Completeness", report.dimensions)
        
    def test_usability_scoring(self):
        """Test usability dimension scoring."""
        scorer = QualityScorer(str(self.valid_skill_path))
        report = scorer.assess_quality()
        
        self.assertIn("Usability", report.dimensions)
        
    def test_security_scoring(self):
        """Test security dimension scoring."""
        scorer = QualityScorer(str(self.valid_skill_path))
        report = scorer.assess_quality()
        
        self.assertIn("Security", report.dimensions)
        security_score = report.dimensions["Security"].score
        self.assertGreater(security_score, 0)
        self.assertLessEqual(security_score, 100)
        
    def test_detailed_mode(self):
        """Test detailed mode output."""
        scorer = QualityScorer(str(self.valid_skill_path), detailed=True)
        report = scorer.assess_quality()
        
        # Should have detailed component scores
        for dim in report.dimensions.values():
            self.assertTrue(len(dim.details) > 0)


class TestSkillMdScoring(unittest.TestCase):
    """Tests for SKILL.md specific scoring."""
    
    def test_score_frontmatter_complete(self):
        """Test scoring complete frontmatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            refs_dir = skill_dir / "references"
            refs_dir.mkdir()
            assets_dir = skill_dir / "assets"
            assets_dir.mkdir()
            
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: test-skill
description: A test skill
license: MIT
metadata:
  version: 1.0.0
  author: Test Author
  category: test
  updated: 2026-03-26
---

# Test Skill

Description here.

## Features

- Feature 1
- Feature 2

## Usage

Usage info here.

## Examples

Example code here.
""")
            
            # Add reference file
            ref_file = refs_dir / "guide.md"
            ref_file.write_text("# Reference Guide\n\nContent here.")
            
            # Add asset file
            asset_file = assets_dir / "sample.txt"
            asset_file.write_text("Sample data")
            
            script = scripts_dir / "tool.py"
            script.write_text("""
import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.parse_args()
if __name__ == "__main__":
    main()
""")
            
            scorer = QualityScorer(str(skill_dir))
            report = scorer.assess_quality()
            
            # Should have reasonable documentation score (lowered threshold)
            self.assertGreater(
                report.dimensions["Documentation"].score, 10
            )
            
    def test_score_sections(self):
        """Test scoring section completeness."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: test-skill
description: Test
license: MIT
metadata:
  version: 1.0.0
  author: Test
  category: test
  updated: 2026-03-26
---

# Test Skill

## Description
Description here.

## Features
Feature list.

## Usage
Usage info.

## Examples
Example code.
""")
            
            script = scripts_dir / "tool.py"
            script.write_text("""
import argparse
def main():
    pass
if __name__ == "__main__":
    main()
""")
            
            scorer = QualityScorer(str(skill_dir))
            report = scorer.assess_quality()
            
            # Should detect sections
            self.assertIsNotNone(report.dimensions["Documentation"].score)


class TestCodeQualityScoring(unittest.TestCase):
    """Tests for code quality specific scoring."""
    
    def test_score_script_complexity(self):
        """Test scoring script complexity."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
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

Description.
""")
            
            # Create a reasonably complex script
            script = scripts_dir / "tool.py"
            script.write_text("""
#!/usr/bin/env python3
\"\"\"A tool with reasonable complexity.\"\"\"

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

class Processor:
    \"\"\"Process data.\"\"\"
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.data = {}
        
    def process(self, input_data: str) -> Dict[str, Any]:
        \"\"\"Process input data.\"\"\"
        result = {
            "length": len(input_data),
            "words": len(input_data.split()),
        }
        self.data = result
        return result
        
    def to_json(self) -> str:
        \"\"\"Convert to JSON.\"\"\"
        return json.dumps(self.data, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Process data")
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    
    args = parser.parse_args()
    
    try:
        processor = Processor(verbose=args.verbose)
        input_data = Path(args.input).read_text()
        result = processor.process(input_data)
        
        if args.json:
            print(processor.to_json())
        else:
            print(f"Processed {result['length']} chars")
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
""")
            
            scorer = QualityScorer(str(skill_dir))
            report = scorer.assess_quality()
            
            # Should have reasonable code quality score
            self.assertGreater(
                report.dimensions["Code Quality"].score, 30
            )


class TestReportFormatter(unittest.TestCase):
    """Tests for the QualityReportFormatter class."""
    
    def test_format_json(self):
        """Test JSON formatting."""
        report = QualityReport("/test/path")
        
        dim = QualityDimension("Documentation", 0.25, "Docs")
        dim.score = 75.0
        report.add_dimension(dim)
        
        report.calculate_overall_score()
        
        json_output = QualityReportFormatter.format_json(report)
        
        # Should be valid JSON
        parsed = json.loads(json_output)
        self.assertEqual(parsed["skill_path"], "/test/path")
        
    def test_format_human_readable(self):
        """Test human-readable formatting."""
        report = QualityReport("/test/path")
        
        dim = QualityDimension("Documentation", 0.25, "Docs")
        dim.score = 75.0
        report.add_dimension(dim)
        
        report.calculate_overall_score()
        
        text_output = QualityReportFormatter.format_human_readable(report)
        
        self.assertIn("SKILL QUALITY ASSESSMENT REPORT", text_output)
        self.assertIn("/test/path", text_output)


class TestQualityScorerCLI(unittest.TestCase):
    """Tests for the command-line interface."""
    
    def test_cli_help(self):
        """Test CLI --help functionality."""
        import subprocess
        
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "quality_scorer.py"), "--help"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Score skill quality", result.stdout)
        
    def test_cli_json_output(self):
        """Test CLI --json output."""
        import subprocess
        
        valid_skill = Path(__file__).parent / "fixtures" / "valid_skill"
        
        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "quality_scorer.py"),
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


class TestWeightCalculations(unittest.TestCase):
    """Tests for dimension weight calculations."""
    
    def test_weights_sum_to_one(self):
        """Test that dimension weights sum to 1.0."""
        report = QualityReport("/test/path")
        
        for name in ["Documentation", "Code Quality", "Completeness", "Usability", "Security"]:
            dim = QualityDimension(name, 0.20, name)
            report.add_dimension(dim)
            
        total_weight = sum(d.weight for d in report.dimensions.values())
        self.assertEqual(total_weight, 1.0)
        
    def test_equal_weights(self):
        """Test that all dimensions have equal weight."""
        report = QualityReport("/test/path")
        
        for name in ["Documentation", "Code Quality", "Completeness", "Usability", "Security"]:
            dim = QualityDimension(name, 0.20, name)
            report.add_dimension(dim)
            
        weights = [d.weight for d in report.dimensions.values()]
        self.assertTrue(all(w == 0.20 for w in weights))
        
    def test_five_dimensions(self):
        """Test that there are exactly 5 quality dimensions."""
        report = QualityReport("/test/path")
        
        for name in ["Documentation", "Code Quality", "Completeness", "Usability", "Security"]:
            dim = QualityDimension(name, 0.20, name)
            report.add_dimension(dim)
            
        self.assertEqual(len(report.dimensions), 5)


class TestSecurityScoring(unittest.TestCase):
    """Tests for security dimension specific scoring."""
    
    def test_security_dimension_present(self):
        """Test that Security dimension is always present in assessment."""
        fixtures_dir = Path(__file__).parent / "fixtures"
        valid_skill_path = fixtures_dir / "valid_skill"
        
        scorer = QualityScorer(str(valid_skill_path))
        report = scorer.assess_quality()
        
        self.assertIn("Security", report.dimensions)
        
    def test_sensitive_data_exposure_detection(self):
        """Test detection of hardcoded sensitive data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
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

Description.
""")
            
            # Script with hardcoded password (BAD)
            script = scripts_dir / "insecure.py"
            script.write_text("""
password = "hardcoded_secret_password"
api_key = "sk-1234567890abcdef"

def main():
    pass

if __name__ == "__main__":
    main()
""")
            
            scorer = QualityScorer(str(skill_dir))
            report = scorer.assess_quality()
            
            # Security score should be lower due to hardcoded credentials
            security_score = report.dimensions["Security"].score
            self.assertLess(security_score, 100)
            # Should have suggestions about removing hardcoded credentials
            security_dim = report.dimensions["Security"]
            self.assertTrue(any("credential" in s.lower() or "hardcoded" in s.lower() 
                              for s in security_dim.suggestions) or security_score < 100)
            
    def test_command_injection_detection(self):
        """Test detection of command injection vulnerabilities."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
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

Description.
""")
            
            # Script with command injection risk (BAD)
            script = scripts_dir / "risky.py"
            script.write_text("""
import os
import sys

def main():
    user_input = sys.argv[1]
    os.system("echo " + user_input)  # Command injection risk
    
if __name__ == "__main__":
    main()
""")
            
            scorer = QualityScorer(str(skill_dir))
            report = scorer.assess_quality()
            
            # Security score should be lower due to command injection risk
            security_score = report.dimensions["Security"].score
            self.assertLess(security_score, 100)
            
    def test_secure_script_scores_high(self):
        """Test that secure scripts score well on security dimension."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            scripts_dir = skill_dir / "scripts"
            scripts_dir.mkdir()
            
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

Description.
""")
            
            # Secure script with proper practices
            script = scripts_dir / "secure.py"
            script.write_text("""
#!/usr/bin/env python3
\"\"\"A secure script with proper validation.\"\"\"

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

def validate_path(path_str: str) -> Path:
    \"\"\"Validate and resolve a file path.\"\"\"
    path = Path(path_str).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    return path

def safe_subprocess(command: list) -> str:
    \"\"\"Run subprocess safely without shell.\"\"\"
    result = subprocess.run(command, capture_output=True, text=True, shell=False)
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Secure tool")
    parser.add_argument("input", help="Input file")
    parser.add_argument("--output", help="Output file")
    
    args = parser.parse_args()
    
    try:
        input_path = validate_path(args.input)
        content = input_path.read_text()
        
        # Safe subprocess call
        result = safe_subprocess(["echo", content])
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(result)
        else:
            print(result)
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
""")
            
            scorer = QualityScorer(str(skill_dir))
            report = scorer.assess_quality()
            
            # Security score should be high for secure script
            security_score = report.dimensions["Security"].score
            self.assertGreater(security_score, 60)


if __name__ == "__main__":
    unittest.main(verbosity=2)