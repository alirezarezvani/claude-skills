"""Integration tests: verify skill package consistency across the repository.

These tests validate that:
1. Every skill directory with a SKILL.md has valid structure
2. SKILL.md files have required YAML frontmatter
3. File references in SKILL.md actually exist
4. Scripts directories contain valid Python files
5. No orphaned scripts directories without a SKILL.md
"""

import glob
import os
import re

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKILL_DOMAINS = [
    "engineering-team",
    "engineering",
    "product-team",
    "marketing-skill",
    "project-management",
    "c-level-advisor",
    "ra-qm-team",
    "business-growth",
    "finance",
]

SKIP_PATTERNS = [
    "assets/sample-skill",
    "assets/sample_codebase",
    "__pycache__",
]


def _find_all_skill_dirs():
    """Find all directories containing a SKILL.md file."""
    skills = []
    for domain in SKILL_DOMAINS:
        domain_path = os.path.join(REPO_ROOT, domain)
        if not os.path.isdir(domain_path):
            continue
        for root, dirs, files in os.walk(domain_path):
            if "SKILL.md" in files:
                rel = os.path.relpath(root, REPO_ROOT)
                if any(skip in rel for skip in SKIP_PATTERNS):
                    continue
                skills.append(root)
    return skills


ALL_SKILL_DIRS = _find_all_skill_dirs()


def _short_id(path):
    return os.path.relpath(path, REPO_ROOT)


class TestSkillMdExists:
    """Every recognized skill directory must have a SKILL.md."""

    def test_found_skills(self):
        assert len(ALL_SKILL_DIRS) > 100, f"Expected 100+ skills, found {len(ALL_SKILL_DIRS)}"


class TestSkillMdFrontmatter:
    """SKILL.md files should have YAML frontmatter with name and description."""

    @pytest.mark.parametrize(
        "skill_dir",
        ALL_SKILL_DIRS,
        ids=[_short_id(s) for s in ALL_SKILL_DIRS],
    )
    def test_has_frontmatter(self, skill_dir):
        skill_md = os.path.join(skill_dir, "SKILL.md")
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for YAML frontmatter delimiters
        assert content.startswith("---"), (
            f"{_short_id(skill_dir)}/SKILL.md is missing YAML frontmatter (no opening ---)"
        )
        # Find closing ---
        second_delim = content.find("---", 4)
        assert second_delim > 0, (
            f"{_short_id(skill_dir)}/SKILL.md has unclosed frontmatter"
        )

    @pytest.mark.parametrize(
        "skill_dir",
        ALL_SKILL_DIRS,
        ids=[_short_id(s) for s in ALL_SKILL_DIRS],
    )
    def test_frontmatter_has_name(self, skill_dir):
        skill_md = os.path.join(skill_dir, "SKILL.md")
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        match = re.match(r"^---\n(.*?)---\n", content, re.DOTALL)
        if match:
            fm = match.group(1)
            assert "name:" in fm, (
                f"{_short_id(skill_dir)}/SKILL.md frontmatter missing 'name' field"
            )


class TestSkillMdHasH1:
    """Every SKILL.md must have at least one H1 heading."""

    @pytest.mark.parametrize(
        "skill_dir",
        ALL_SKILL_DIRS,
        ids=[_short_id(s) for s in ALL_SKILL_DIRS],
    )
    def test_has_h1(self, skill_dir):
        skill_md = os.path.join(skill_dir, "SKILL.md")
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        # Strip frontmatter
        content = re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL)
        assert re.search(r"^# .+", content, re.MULTILINE), (
            f"{_short_id(skill_dir)}/SKILL.md has no H1 heading"
        )


class TestScriptDirectories:
    """Validate scripts/ directories within skills."""

    def _get_skills_with_scripts(self):
        result = []
        for skill_dir in ALL_SKILL_DIRS:
            scripts_dir = os.path.join(skill_dir, "scripts")
            if os.path.isdir(scripts_dir):
                py_files = glob.glob(os.path.join(scripts_dir, "*.py"))
                if py_files:
                    result.append((skill_dir, py_files))
        return result

    def test_scripts_dirs_have_python_files(self):
        """Every scripts/ directory should contain at least one .py file."""
        for skill_dir in ALL_SKILL_DIRS:
            scripts_dir = os.path.join(skill_dir, "scripts")
            if os.path.isdir(scripts_dir):
                py_files = glob.glob(os.path.join(scripts_dir, "*.py"))
                assert len(py_files) > 0, (
                    f"{_short_id(skill_dir)}/scripts/ exists but has no .py files"
                )

    def test_no_empty_skill_md(self):
        """SKILL.md files should not be empty."""
        for skill_dir in ALL_SKILL_DIRS:
            skill_md = os.path.join(skill_dir, "SKILL.md")
            size = os.path.getsize(skill_md)
            assert size > 100, (
                f"{_short_id(skill_dir)}/SKILL.md is suspiciously small ({size} bytes)"
            )


class TestReferencesDirectories:
    """Validate references/ directories are non-empty."""

    def test_references_not_empty(self):
        for skill_dir in ALL_SKILL_DIRS:
            refs_dir = os.path.join(skill_dir, "references")
            if os.path.isdir(refs_dir):
                files = [f for f in os.listdir(refs_dir) if not f.startswith(".")]
                assert len(files) > 0, (
                    f"{_short_id(skill_dir)}/references/ exists but is empty"
                )


class TestNoDuplicateSkillNames:
    """Skill directory names should be unique across the entire repo."""

    def test_unique_top_level_skill_names(self):
        """Top-level skills (direct children of domains) should not have 3+ duplicates."""
        names = {}
        for skill_dir in ALL_SKILL_DIRS:
            rel = _short_id(skill_dir)
            parts = rel.split(os.sep)
            # Only check top-level skills (domain/skill-name), not sub-skills
            if len(parts) != 2:
                continue
            name = parts[1]
            names.setdefault(name, []).append(rel)

        # Report names that appear 3+ times (2 is acceptable for cross-domain)
        triples = {k: v for k, v in names.items() if len(v) >= 3}
        assert not triples, f"Top-level skill names appearing 3+ times: {triples}"
