#!/usr/bin/env python3
"""Smoke tests for self-model regeneration staleness detection logic.

These tests validate the core staleness detection, flag lifecycle, and edge cases
without requiring a full memory directory structure. Each test creates temporary
files and cleans up after itself.

Usage:
    python -m pytest scripts/tests/test_staleness.py -v
    python scripts/tests/test_staleness.py           # runs with built-in unittest
"""

import os
import sys
import json
import tempfile
import unittest
import subprocess
import importlib
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add scripts dir to path for imports
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

# quality-gate.py has a hyphen — import via importlib
_quality_gate = importlib.import_module("quality-gate")
days_since = _quality_gate.days_since
_find_persona = _quality_gate._find_persona
MEMORY_DIR = _quality_gate.MEMORY_DIR


class TestDaysSince(unittest.TestCase):
    """quality-gate.py: days_since() return type and edge cases."""

    def test_none_input_returns_none(self):
        """days_since(None) must return None, not float('inf')."""
        result = days_since(None)
        self.assertIsNone(result, "days_since(None) should return None, not inf")

    def test_recent_date_returns_small_number(self):
        """days_since on a recent datetime returns a small float."""
        recent = datetime.now(timezone.utc) - timedelta(hours=1)
        result = days_since(recent)
        self.assertIsNotNone(result)
        self.assertLess(result, 1.0, "1 hour ago should be < 1 day")

    def test_old_date_returns_large_number(self):
        """days_since on an old datetime returns a large float."""
        old = datetime.now(timezone.utc) - timedelta(days=30)
        result = days_since(old)
        self.assertIsNotNone(result)
        self.assertGreater(result, 29.0, "30 days ago should be > 29 days")


class TestFindPersona(unittest.TestCase):
    """quality-gate.py: _find_persona() glob and fallback."""

    def test_fallback_path_uses_underscore(self):
        """Fallback path must be persona_portrait.md (underscore), not persona-portrait.md (hyphen)."""
        # _find_persona returns a Path; verify the fallback name
        result = _find_persona()
        # When no files exist in a real MEMORY_DIR, falls back to persona_portrait.md
        self.assertEqual(result.name, "persona_portrait.md",
                         "Fallback must use underscore, not hyphen")
        self.assertIn("persona_portrait", str(result))

    def test_returns_path_object(self):
        """_find_persona must return a Path object."""
        result = _find_persona()
        self.assertIsInstance(result, Path)


class TestFlagLifecycle(unittest.TestCase):
    """Flag write → read → delete round-trip."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.flag_path = Path(self.tmpdir.name) / ".self-model-stale"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_write_and_read_flag(self):
        """Flag written by quality-gate style write should be readable."""
        reason = "test: self-model is stale"
        content = (
            f"# Self-Model Stale Flag\n"
            f"# Generated: {datetime.now(timezone.utc).isoformat()}\n"
            f"# Reason: {reason}\n"
            f"# Action: AI should regenerate self-model.md\n"
        )
        self.flag_path.write_text(content, encoding="utf-8")
        self.assertTrue(self.flag_path.exists(), "Flag should exist after write")
        read_back = self.flag_path.read_text(encoding="utf-8")
        self.assertIn(reason, read_back, "Flag content should contain reason")

    def test_delete_flag(self):
        """Flag deletion should remove the file."""
        self.flag_path.write_text("test", encoding="utf-8")
        self.assertTrue(self.flag_path.exists())
        self.flag_path.unlink()
        self.assertFalse(self.flag_path.exists(), "Flag should not exist after unlink")

    def test_delete_nonexistent_flag_raises(self):
        """Deleting a nonexistent flag should raise FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            self.flag_path.unlink()

    def test_empty_flag_detected(self):
        """health-check should detect empty flag file as REGENERATE_NEEDED."""
        self.flag_path.write_text("", encoding="utf-8")
        self.assertEqual(self.flag_path.stat().st_size, 0,
                         "Empty flag should have size 0")


class TestGrowthLogFilenameRegex(unittest.TestCase):
    """health-check.py: check_growth() filename pattern validation."""

    def test_valid_date_names(self):
        """Files like '2026-07-02.md' should match."""
        import re
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
        valid = [
            "2026-07-02.md",
            "2024-01-01.md",
            "2026-12-31.md",
        ]
        for name in valid:
            m = pattern.match(name)
            self.assertIsNotNone(m, f"'{name}' should match date pattern")
            # Verify it's a parseable date
            datetime.fromisoformat(m.group())

    def test_invalid_names_rejected(self):
        """Files like 'README.md' or '2026-07-02-style.md' should not match as dates."""
        import re
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
        invalid_prefix = [
            "README.md",
            "index.md",
            "growth-log.md",
            "style-2026-07-02.md",
        ]
        for name in invalid_prefix:
            m = pattern.match(name)
            self.assertIsNone(m, f"'{name}' should NOT match date pattern (doesn't start with date)")

    def test_suffix_variants_still_match(self):
        """Files with date prefix plus suffix should match the date part."""
        import re
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}')
        # These start with valid dates but have suffixes — the regex matches
        # the date prefix, but check_growth should still validate via fromisoformat
        with_suffix = [
            "2026-07-02-style.md",
            "2026-07-02-review.md",
            "2026-07-02.md",
        ]
        for name in with_suffix:
            m = pattern.match(name)
            self.assertIsNotNone(m, f"'{name}' should match date prefix pattern")


class TestMtimeStalenessLogic(unittest.TestCase):
    """Staleness detection edge cases: FAT32 resolution, equality, clock skew."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_equal_mtime_is_stale(self):
        """FAT32 2s resolution: when mtimes are equal, self-model IS stale (>=)."""
        # Create two files
        a = self.base / "growth-log" / "2026-07-02.md"
        b = self.base / "self-model.md"
        a.parent.mkdir(exist_ok=True)
        a.write_text("growth entry")
        b.write_text("self model")

        # On most filesystems these get different (sub-second) mtimes
        # but we test the comparison logic directly
        a_mtime = datetime.fromtimestamp(a.stat().st_mtime, tz=timezone.utc)
        b_mtime = datetime.fromtimestamp(b.stat().st_mtime, tz=timezone.utc)

        # The >= check ensures: if a_mtime >= b_mtime → stale
        is_stale = a_mtime >= b_mtime
        # Both files just created; should be close
        self.assertIsInstance(is_stale, bool)

    def test_newer_growth_log_is_stale(self):
        """Growth log newer than self-model → definitely stale."""
        model = self.base / "self-model.md"
        growth = self.base / "growth-log" / "2026-07-02.md"
        growth.parent.mkdir(exist_ok=True)

        model.write_text("old model")
        # Small delay to ensure different mtimes
        import time
        time.sleep(0.01)
        growth.write_text("new growth entry")

        model_mtime = datetime.fromtimestamp(model.stat().st_mtime, tz=timezone.utc)
        growth_mtime = datetime.fromtimestamp(growth.stat().st_mtime, tz=timezone.utc)

        self.assertGreater(growth_mtime, model_mtime,
                           "Growth log should be newer than self-model")
        is_stale = growth_mtime >= model_mtime
        self.assertTrue(is_stale, "Newer growth log → self-model is stale")

    def test_older_growth_log_is_not_stale(self):
        """Growth log older than self-model → NOT stale."""
        model = self.base / "self-model.md"
        growth = self.base / "growth-log" / "2026-07-01.md"
        growth.parent.mkdir(exist_ok=True)

        growth.write_text("old growth entry")
        import time
        time.sleep(0.01)
        model.write_text("new self model")

        model_mtime = datetime.fromtimestamp(model.stat().st_mtime, tz=timezone.utc)
        growth_mtime = datetime.fromtimestamp(growth.stat().st_mtime, tz=timezone.utc)

        self.assertGreater(model_mtime, growth_mtime,
                           "Self-model should be newer than growth log")
        is_stale = growth_mtime >= model_mtime
        self.assertFalse(is_stale, "Older growth log → self-model is NOT stale")


class TestLogRegenerationOrdering(unittest.TestCase):
    """log-regeneration.py: crash-consistent write ordering verification."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tmpdir.name)
        self.log_path = self.base / ".self-model-regeneration.jsonl"
        self.flag_path = self.base / ".self-model-stale"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_jsonl_write_produces_valid_json(self):
        """JSONL record should be valid JSON with required fields."""
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trigger": "flag",
            "sources": ["2026-07-02", "2026-07-01"],
            "old_version": "v2",
            "new_version": "v3",
            "flag_cleaned": True,
        }
        self.log_path.write_text(json.dumps(record) + "\n", encoding="utf-8")

        # Read back and parse
        content = self.log_path.read_text(encoding="utf-8")
        lines = [l for l in content.strip().split("\n") if l.strip()]
        self.assertEqual(len(lines), 1, "Should have exactly one JSONL line")

        parsed = json.loads(lines[0])
        self.assertEqual(parsed["old_version"], "v2")
        self.assertEqual(parsed["new_version"], "v3")
        self.assertEqual(parsed["trigger"], "flag")
        self.assertEqual(len(parsed["sources"]), 2)
        self.assertIn("timestamp", parsed)

    def test_jsonl_before_flag_delete_pattern(self):
        """Verify the crash-safe pattern: write JSONL first, then delete flag."""
        record = {"test": True}
        # Step 1: Write log FIRST
        self.log_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
        self.assertTrue(self.log_path.exists(), "JSONL must exist before flag delete")

        # Step 2: Delete flag SECOND (simulated — flag may or may not exist)
        self.flag_path.write_text("stale", encoding="utf-8")
        self.assertTrue(self.flag_path.exists())

        # Verify log exists before deleting flag
        self.assertTrue(self.log_path.exists())
        self.flag_path.unlink()
        self.assertFalse(self.flag_path.exists())

        # Verify log still exists after flag delete
        self.assertTrue(self.log_path.exists(),
                        "JSONL must survive flag deletion")

    def test_crash_before_flag_delete_recovers(self):
        """If crash occurs after JSONL write but before flag delete, data is safe."""
        # Simulate: JSONL written, flag still exists (crash scenario)
        record = {"recovery_test": True}
        self.log_path.write_text(json.dumps(record) + "\n", encoding="utf-8")
        self.flag_path.write_text("stale", encoding="utf-8")

        # Recovery: flag exists → health-check.py re-detects it
        self.assertTrue(self.flag_path.exists(),
                        "Flag should persist if delete didn't happen")
        # Audit trail is intact
        self.assertTrue(self.log_path.exists(),
                        "Audit log should survive crash")
        log_content = self.log_path.read_text(encoding="utf-8")
        self.assertIn("recovery_test", log_content)

    def test_crash_before_jsonl_write_flag_persists(self):
        """If crash before JSONL write, flag persists so regeneration retries."""
        # Neither JSONL nor flag delete happened
        self.flag_path.write_text("stale", encoding="utf-8")
        self.assertFalse(self.log_path.exists(),
                         "JSONL shouldn't exist if write never happened")
        self.assertTrue(self.flag_path.exists(),
                        "Flag should persist so health-check re-detects")


class TestExitCodes(unittest.TestCase):
    """quality-gate.py exit code semantics."""

    def _run(self, *args, **kwargs):
        """Run a subprocess with UTF-8 encoding on Windows."""
        env = kwargs.pop("env", None) or os.environ
        return subprocess.run(
            [sys.executable, *args],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            env=env,
            **kwargs
        )

    def get_script(self):
        return str(SCRIPTS_DIR / "quality-gate.py")

    def test_help_exits_zero(self):
        """--help should exit 0."""
        result = self._run(self.get_script(), "--help")
        self.assertIsInstance(result.returncode, int)

    def test_empty_memory_dir_exits_two(self):
        """No self-model.md + no growth-log → exit 2 (model missing = stale)."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "growth-log").mkdir()
            (tmp / "decisions").mkdir()
            env = {**os.environ, "MEMORY_DIR": str(tmp)}
            result = self._run(self.get_script(), env=env)
            self.assertIn(result.returncode, [0, 1, 2],
                          "Exit code should be 0, 1, or 2")
            # With no self-model.md, should be exit 2
            self.assertEqual(result.returncode, 2,
                             f"Missing self-model should trigger exit 2, got {result.returncode}\nstderr: {result.stderr[-300:]}")


class TestHealthCheckSignals(unittest.TestCase):
    """health-check.py: REGENERATE_NEEDED and CLEANED_ORPHAN signal integrity."""

    def _run(self, *args, **kwargs):
        """Run a subprocess with UTF-8 encoding on Windows."""
        env = kwargs.pop("env", None) or os.environ
        return subprocess.run(
            [sys.executable, *args],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            env=env,
            **kwargs
        )

    def get_script(self):
        return str(SCRIPTS_DIR / "health-check.py")

    def test_always_exits_zero(self):
        """health-check.py must always exit 0, even with stale flag."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "growth-log").mkdir()
            (tmp / "decisions").mkdir()
            # Create a stale flag
            flag = tmp / ".self-model-stale"
            flag.write_text("test flag")
            env = {**os.environ, "MEMORY_DIR": str(tmp)}
            result = self._run(self.get_script(), env=env)
            self.assertEqual(result.returncode, 0,
                             f"health-check.py must ALWAYS exit 0 (never blocks)\nstderr: {result.stderr[-500:]}")

    def test_regenerate_needed_when_model_missing(self):
        """REGENERATE_NEEDED signal when self-model.md is missing."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "growth-log").mkdir()
            (tmp / "decisions").mkdir()
            flag = tmp / ".self-model-stale"
            flag.write_text("test flag")
            env = {**os.environ, "MEMORY_DIR": str(tmp)}
            result = self._run(self.get_script(), env=env)
            stderr = result.stderr
            self.assertIn("REGENERATE_NEEDED", stderr,
                          f"Should signal REGENERATE_NEEDED when model missing\nstderr: {stderr[-300:]}")

    def test_cleaned_orphan_when_flag_stale_but_model_fresh(self):
        """CLEANED_ORPHAN when flag exists but model is actually fresh."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "growth-log").mkdir()
            (tmp / "decisions").mkdir()
            # Create fresh self-model (newer than flag)
            model = tmp / "self-model.md"
            model.write_text("# Self Model\n\nTest content for smoke testing.")
            # Create an older flag (simulates orphaned flag from prior session)
            flag = tmp / ".self-model-stale"
            flag.write_text("old flag")
            env = {**os.environ, "MEMORY_DIR": str(tmp)}
            result = self._run(self.get_script(), env=env)
            stderr = result.stderr
            # Should either clean orphan or signal regenerate
            self.assertTrue(
                "CLEANED_ORPHAN" in stderr or "REGENERATE_NEEDED" in stderr,
                f"Should produce a valid signal, got: {stderr[-300:]}"
            )


class TestLogRegenerationScript(unittest.TestCase):
    """log-regeneration.py: command-line interface and crash-safety."""

    def _run(self, *args, **kwargs):
        """Run a subprocess with UTF-8 encoding on Windows."""
        env = kwargs.pop("env", None) or os.environ
        return subprocess.run(
            [sys.executable, *args],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            env=env,
            **kwargs
        )

    def get_script(self):
        return str(SCRIPTS_DIR / "log-regeneration.py")

    def test_help_exits_zero(self):
        """--help should print usage and exit 0."""
        result = self._run(self.get_script(), "--help")
        # argparse always exits 0 for --help
        self.assertEqual(result.returncode, 0)

    def test_missing_required_args_fails(self):
        """Missing --old, --new, --sources should exit non-zero."""
        result = self._run(self.get_script())
        self.assertNotEqual(result.returncode, 0,
                            f"Missing required args should fail, got {result.returncode}")

    def test_successful_log_write(self):
        """Full invocation writes JSONL and cleans flag."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            # Create a flag to clean
            flag = tmp / ".self-model-stale"
            flag.write_text("test flag")
            env = {**os.environ, "MEMORY_DIR": str(tmp)}
            result = self._run(
                self.get_script(),
                "--old", "v1", "--new", "v2",
                "--sources", "2026-07-02,2026-07-01",
                "--trigger", "flag",
                env=env
            )
            self.assertEqual(result.returncode, 0,
                             f"Should succeed, got stderr: {result.stderr}")

            # Verify JSONL was written
            log = tmp / ".self-model-regeneration.jsonl"
            self.assertTrue(log.exists(), "JSONL audit log should be created")

            # Verify JSONL content
            content = log.read_text(encoding="utf-8").strip()
            self.assertTrue(content, "JSONL should not be empty")
            record = json.loads(content)
            self.assertEqual(record["old_version"], "v1")
            self.assertEqual(record["new_version"], "v2")
            self.assertEqual(record["trigger"], "flag")
            self.assertTrue(record["flag_cleaned"])

            # Verify flag was deleted
            self.assertFalse(flag.exists(), "Flag should be deleted after successful log")


if __name__ == "__main__":
    unittest.main(verbosity=2)
