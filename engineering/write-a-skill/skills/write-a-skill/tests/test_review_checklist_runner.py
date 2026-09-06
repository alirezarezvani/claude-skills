#!/usr/bin/env python3
"""
Tests for skill_review_checklist_runner.py and skill_description_validator.py - trigger detection

This test module validates that check 1 ("Description includes triggers") reads a description
correctly and recognises the trigger phrasings skill authors actually write:

- Every YAML block scalar indicator is read, not returned as the description
  (">", ">-", ">+", "|", "|-", and explicit indentation digits such as ">2")
- Natural trigger phrasings are recognised ("use whenever", "use this skill whenever",
  "should be used when", "use on every", "invoke at the start of", "load this before")
- Prose that merely contains an invocation verb is still NOT a trigger, so the check keeps
  its teeth ("runs on macOS", "teaches you to use design tokens")

Both scripts carry their own copy of TRIGGER_PATTERNS, so both are covered here.

Run with: python -m unittest test_review_checklist_runner
"""

import sys
import unittest
from pathlib import Path

# Add the scripts directory to the path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from skill_review_checklist_runner import (  # noqa: E402
    check_description_has_trigger,
    extract_frontmatter_description,
)
from skill_description_validator import (  # noqa: E402
    extract_frontmatter,
    TRIGGER_PATTERNS as VALIDATOR_TRIGGER_PATTERNS,
)

HEAD = "---\nname: x\ndescription: "
TAIL = "\n---\n\n# X\n"
USE_WHEN = "Does a thing. Use when asked."


def plain(desc):
    """A SKILL.md whose description is a single-line scalar."""
    return HEAD + desc + TAIL


def block(indicator, desc):
    """A SKILL.md whose description is a block scalar with the given indicator."""
    return HEAD + indicator + "\n  " + desc + TAIL


class TestBlockScalarIndicators(unittest.TestCase):
    """The indicator introduces the value; it is never part of it."""

    INDICATORS = [">", ">-", ">+", "|", "|-", "|+", ">2"]

    def test_runner_reads_description_under_every_indicator(self):
        for ind in self.INDICATORS:
            with self.subTest(indicator=ind):
                got = extract_frontmatter_description(block(ind, USE_WHEN))
                self.assertNotIn(ind, got, f"indicator {ind!r} returned as the description")
                self.assertIn("Use when asked", got)

    def test_runner_check_passes_under_every_indicator(self):
        for ind in self.INDICATORS:
            with self.subTest(indicator=ind):
                self.assertTrue(check_description_has_trigger(block(ind, USE_WHEN))["pass"])

    def test_validator_does_not_keep_the_indicator_in_the_value(self):
        for ind in self.INDICATORS:
            with self.subTest(indicator=ind):
                desc = extract_frontmatter(block(ind, USE_WHEN)).get("description", "")
                self.assertFalse(
                    desc.startswith(ind),
                    f"indicator {ind!r} left at the start of the description",
                )
                self.assertIn("Use when asked", desc)


class TestTriggerPhrasings(unittest.TestCase):
    """Phrasings taken verbatim from published skills, all of which are plainly triggers."""

    ACCEPTED = [
        "Does a thing. Use when asked.",
        "Does a thing. Use whenever building a flow.",
        "Does a thing. Use this whenever Matt says run it.",
        "Does a thing. Use it whenever an audit is wanted.",
        "Does a thing. Use this skill whenever asked for hooks.",
        "This skill should be used when the user says go.",
        "The SOP. Use on EVERY new store build.",
        "A router. Invoke at the start of any session.",
        "A reference. Load this before editing any schema.",
        "A reference. Use before writing any section.",
        "A thing. Use for every new build.",
        "A gate. Run before the PDF leaves the building.",
    ]

    def test_runner_accepts(self):
        for desc in self.ACCEPTED:
            with self.subTest(description=desc):
                self.assertTrue(check_description_has_trigger(plain(desc))["pass"])

    def test_validator_accepts(self):
        for desc in self.ACCEPTED:
            with self.subTest(description=desc):
                self.assertTrue(
                    any(p.search(desc) for p in VALIDATOR_TRIGGER_PATTERNS),
                    "validator did not recognise a trigger the runner accepts",
                )


class TestStillRejectsNonTriggers(unittest.TestCase):
    """A check that passes everything enforces nothing."""

    REJECTED = [
        "Create developer handoff specifications with measurements.",
        "A linter. Runs on macOS and Linux, written in Python.",
        "Analysis based on a documented method, applied to any repo.",
        "Teaches you to use design tokens rather than raw values.",
        "Helps with documents.",
    ]

    def test_runner_rejects(self):
        for desc in self.REJECTED:
            with self.subTest(description=desc):
                self.assertFalse(check_description_has_trigger(plain(desc))["pass"])

    def test_validator_rejects(self):
        for desc in self.REJECTED:
            with self.subTest(description=desc):
                self.assertFalse(any(p.search(desc) for p in VALIDATOR_TRIGGER_PATTERNS))


class TestTwoScriptsAgree(unittest.TestCase):
    """TRIGGER_PATTERNS is duplicated across the two scripts; they must not drift apart."""

    def test_same_verdict_on_every_case(self):
        cases = (TestTriggerPhrasings.ACCEPTED + TestStillRejectsNonTriggers.REJECTED)
        for desc in cases:
            with self.subTest(description=desc):
                runner = check_description_has_trigger(plain(desc))["pass"]
                validator = any(p.search(desc) for p in VALIDATOR_TRIGGER_PATTERNS)
                self.assertEqual(runner, validator, "the two copies disagree")


if __name__ == "__main__":
    unittest.main()
