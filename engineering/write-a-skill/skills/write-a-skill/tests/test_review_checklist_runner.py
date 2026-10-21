#!/usr/bin/env python3
"""
Tests for _skill_frontmatter.py and the scripts that share it - trigger detection

This test module validates that check 1 ("Description includes triggers") reads a description
correctly and recognises the trigger phrasings skill authors actually write:

- Every YAML block scalar indicator is read, not returned as the description
  (">", ">-", ">+", "|", "|-", and explicit indentation digits such as ">2")
- Natural trigger phrasings are recognised ("use whenever", "use this skill whenever",
  "should be used when", "use on every", "invoke at the start of", "load this before")
- Prose that merely contains an invocation verb is still NOT a trigger, so the check keeps
  its teeth ("runs on macOS", "teaches you to use design tokens")
- The reader, the trigger patterns and the limits are shared rather than copied, so the
  scripts cannot drift apart again

Run with: python -m unittest test_review_checklist_runner
"""

import sys
import unittest
from pathlib import Path

# Add the scripts directory to the path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import _skill_frontmatter  # noqa: E402
import skill_description_validator as validator  # noqa: E402
import skill_review_checklist_runner as runner  # noqa: E402
import skill_structure_validator as structure  # noqa: E402
from _skill_frontmatter import (  # noqa: E402
    MAX_DESCRIPTION_CHARS,
    MAX_SKILL_MD_LINES,
    extract_description,
    extract_frontmatter,
    has_trigger,
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

    def test_description_is_read_under_every_indicator(self):
        for ind in self.INDICATORS:
            with self.subTest(indicator=ind):
                got = extract_description(block(ind, USE_WHEN))
                self.assertNotIn(ind, got, f"indicator {ind!r} kept as part of the description")
                self.assertEqual(got, USE_WHEN)

    def test_check_one_passes_under_every_indicator(self):
        for ind in self.INDICATORS:
            with self.subTest(indicator=ind):
                self.assertTrue(runner.check_description_has_trigger(block(ind, USE_WHEN))["pass"])

    def test_a_plain_value_is_untouched(self):
        self.assertEqual(extract_description(plain(USE_WHEN)), USE_WHEN)

    def test_other_frontmatter_keys_still_parse(self):
        self.assertEqual(extract_frontmatter(block(">-", USE_WHEN)).get("name"), "x")


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

    def test_accepted(self):
        for desc in self.ACCEPTED:
            with self.subTest(description=desc):
                self.assertTrue(has_trigger(desc))
                self.assertTrue(runner.check_description_has_trigger(plain(desc))["pass"])


class TestStillRejectsNonTriggers(unittest.TestCase):
    """A check that passes everything enforces nothing."""

    REJECTED = [
        "Create developer handoff specifications with measurements.",
        "A linter. Runs on macOS and Linux, written in Python.",
        "Analysis based on a documented method, applied to any repo.",
        "Teaches you to use design tokens rather than raw values.",
        "Helps with documents.",
    ]

    def test_rejected(self):
        for desc in self.REJECTED:
            with self.subTest(description=desc):
                self.assertFalse(has_trigger(desc))
                self.assertFalse(runner.check_description_has_trigger(plain(desc))["pass"])


class TestSharedRatherThanCopied(unittest.TestCase):
    """The patterns, the reader and the limits are one definition, not several.

    Identity rather than equality: two equal copies are exactly what drifted before.
    """

    def test_trigger_patterns_are_the_same_object(self):
        self.assertIs(validator.TRIGGER_PATTERNS, _skill_frontmatter.TRIGGER_PATTERNS)

    def test_frontmatter_reader_is_the_same_function(self):
        self.assertIs(validator.extract_frontmatter, _skill_frontmatter.extract_frontmatter)
        self.assertIs(runner.extract_description, _skill_frontmatter.extract_description)

    def test_find_skill_md_is_the_same_function(self):
        self.assertIs(runner.find_skill_md, _skill_frontmatter.find_skill_md)
        self.assertIs(structure.find_skill_md, _skill_frontmatter.find_skill_md)

    def test_limits_are_single_sourced(self):
        self.assertEqual(structure.DEFAULT_MAX_LINES, MAX_SKILL_MD_LINES)
        self.assertEqual(
            runner.check_skill_md_length.__defaults__[0], MAX_SKILL_MD_LINES
        )
        self.assertEqual(
            validator.check_length.__defaults__[0], MAX_DESCRIPTION_CHARS
        )

    def test_no_script_redefines_them(self):
        """Guards against a future copy being pasted back in."""
        for path in SCRIPTS_DIR.glob("skill_*.py"):
            body = path.read_text()
            with self.subTest(script=path.name):
                self.assertNotIn("TRIGGER_PATTERNS = [", body)
                self.assertNotIn("def extract_frontmatter(", body)
                self.assertNotIn("def find_skill_md(", body)


if __name__ == "__main__":
    unittest.main()
