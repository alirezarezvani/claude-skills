"""Unit tests for the Commit Linter (Conventional Commits)."""

import sys
import os
import tempfile

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "engineering", "changelog-generator", "scripts"
))
from commit_linter import lint, CONVENTIONAL_RE, lines_from_file, CLIError


class TestConventionalCommitRegex:
    """Test the regex pattern against various commit message formats."""

    @pytest.mark.parametrize("msg", [
        "feat: add user authentication",
        "fix: resolve null pointer in parser",
        "docs: update API documentation",
        "refactor: simplify login flow",
        "test: add integration tests for auth",
        "build: upgrade webpack to v5",
        "ci: add GitHub Actions workflow",
        "chore: update dependencies",
        "perf: optimize database queries",
        "security: patch XSS vulnerability",
        "deprecated: mark v1 API as deprecated",
        "remove: drop legacy payment module",
    ])
    def test_valid_types(self, msg):
        assert CONVENTIONAL_RE.match(msg) is not None

    @pytest.mark.parametrize("msg", [
        "feat(auth): add OAuth2 support",
        "fix(parser/html): handle malformed tags",
        "docs(api.v2): update endpoint docs",
    ])
    def test_valid_scopes(self, msg):
        assert CONVENTIONAL_RE.match(msg) is not None

    def test_breaking_change_marker(self):
        assert CONVENTIONAL_RE.match("feat!: redesign API") is not None
        assert CONVENTIONAL_RE.match("feat(api)!: breaking change") is not None

    @pytest.mark.parametrize("msg", [
        "Update readme",
        "Fixed the bug",
        "WIP: something",
        "FEAT: uppercase type",
        "feat:missing space",
        "feat : extra space before colon",
        "",
        "merge: not a valid type",
    ])
    def test_invalid_messages(self, msg):
        assert CONVENTIONAL_RE.match(msg) is None


class TestLint:
    def test_all_valid(self):
        lines = [
            "feat: add login",
            "fix: resolve crash",
            "docs: update README",
        ]
        report = lint(lines)
        assert report.total == 3
        assert report.valid == 3
        assert report.invalid == 0
        assert report.violations == []

    def test_mixed_valid_invalid(self):
        lines = [
            "feat: add login",
            "Updated the readme",
            "fix: resolve crash",
        ]
        report = lint(lines)
        assert report.total == 3
        assert report.valid == 2
        assert report.invalid == 1
        assert "line 2" in report.violations[0]

    def test_all_invalid(self):
        lines = ["bad commit", "another bad one"]
        report = lint(lines)
        assert report.valid == 0
        assert report.invalid == 2

    def test_empty_input(self):
        report = lint([])
        assert report.total == 0
        assert report.valid == 0
        assert report.invalid == 0


class TestLinesFromFile:
    def test_reads_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("feat: add feature\nfix: fix bug\n")
            f.flush()
            lines = lines_from_file(f.name)
        os.unlink(f.name)
        assert lines == ["feat: add feature", "fix: fix bug"]

    def test_skips_blank_lines(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("feat: add feature\n\n\nfix: fix bug\n")
            f.flush()
            lines = lines_from_file(f.name)
        os.unlink(f.name)
        assert len(lines) == 2

    def test_nonexistent_file_raises(self):
        with pytest.raises(CLIError, match="Failed reading"):
            lines_from_file("/nonexistent/path.txt")
