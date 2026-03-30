"""Unit tests for the GDPR Compliance Checker."""

import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "ra-qm-team", "gdpr-dsgvo-expert", "scripts"
))
from gdpr_compliance_checker import (
    PERSONAL_DATA_PATTERNS,
    CODE_PATTERNS,
    should_skip,
    scan_file_for_patterns,
    analyze_project,
)


class TestShouldSkip:
    def test_skips_node_modules(self):
        assert should_skip(Path("project/node_modules/package/index.js")) is True

    def test_skips_venv(self):
        assert should_skip(Path("project/venv/lib/site-packages/foo.py")) is True

    def test_skips_git(self):
        assert should_skip(Path("project/.git/objects/abc123")) is True

    def test_allows_normal_path(self):
        assert should_skip(Path("project/src/main.py")) is False

    def test_allows_deep_path(self):
        assert should_skip(Path("project/src/utils/helpers/data.py")) is False


class TestScanFileForPatterns:
    def test_detects_email(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('user_email = "john@example.com"\n')
            f.flush()
            findings = scan_file_for_patterns(Path(f.name), PERSONAL_DATA_PATTERNS)
        os.unlink(f.name)
        email_findings = [f for f in findings if f["pattern"] == "email"]
        assert len(email_findings) >= 1
        assert email_findings[0]["category"] == "contact_data"

    def test_detects_health_data(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('record = {"diagnosis": "flu", "treatment": "rest"}\n')
            f.flush()
            findings = scan_file_for_patterns(Path(f.name), PERSONAL_DATA_PATTERNS)
        os.unlink(f.name)
        health_findings = [f for f in findings if f["pattern"] == "health_data"]
        assert len(health_findings) >= 1
        assert health_findings[0]["risk"] == "critical"

    def test_detects_code_logging_issue(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('log.info("User email: " + user.email)\n')
            f.flush()
            findings = scan_file_for_patterns(Path(f.name), CODE_PATTERNS)
        os.unlink(f.name)
        log_findings = [f for f in findings if f["pattern"] == "logging_personal_data"]
        assert len(log_findings) >= 1

    def test_no_findings_on_clean_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write('x = 1 + 2\nprint("hello")\n')
            f.flush()
            findings = scan_file_for_patterns(Path(f.name), PERSONAL_DATA_PATTERNS)
        os.unlink(f.name)
        assert len(findings) == 0

    def test_handles_unreadable_file(self):
        findings = scan_file_for_patterns(Path("/nonexistent/file.py"), PERSONAL_DATA_PATTERNS)
        assert findings == []


class TestAnalyzeProject:
    def test_scores_clean_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a clean Python file
            src = Path(tmpdir) / "clean.py"
            src.write_text("x = 1\ny = 2\nresult = x + y\n", encoding="utf-8")
            result = analyze_project(Path(tmpdir))
        assert result["summary"]["compliance_score"] == 100
        assert result["summary"]["status"] == "compliant"

    def test_detects_issues_in_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "bad.py"
            src.write_text(
                'user_email = "john@example.com"\n'
                'log.info("Patient diagnosis: " + record.diagnosis)\n',
                encoding="utf-8",
            )
            result = analyze_project(Path(tmpdir))
        assert result["summary"]["compliance_score"] < 100
        assert len(result["personal_data_findings"]) > 0

    def test_returns_recommendations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "issues.py"
            src.write_text(
                'password = "secret123"\n'
                'user_email = "test@test.com"\n',
                encoding="utf-8",
            )
            result = analyze_project(Path(tmpdir))
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)


class TestPersonalDataPatterns:
    """Test that the regex patterns work correctly."""

    @pytest.mark.parametrize("pattern_name,test_string", [
        ("email", "contact: user@example.com"),
        ("ip_address", "server IP: 192.168.1.100"),
        ("phone_number", "call +1-555-123-4567"),
        ("credit_card", "card: 4111-1111-1111-1111"),
        ("date_of_birth", "field: date of birth"),
        ("health_data", "the patient reported symptoms"),
        ("biometric", "store fingerprint data"),
        ("religion", "religious preference recorded"),
    ])
    def test_pattern_matches(self, pattern_name, test_string):
        import re
        pattern = PERSONAL_DATA_PATTERNS[pattern_name]["pattern"]
        assert re.search(pattern, test_string, re.IGNORECASE) is not None
