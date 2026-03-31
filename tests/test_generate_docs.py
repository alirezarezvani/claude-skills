"""Unit tests for the generate-docs.py infrastructure script."""

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# The script uses a hyphenated filename, so import via importlib
import importlib.util
spec = importlib.util.spec_from_file_location(
    "generate_docs",
    os.path.join(os.path.dirname(__file__), "..", "scripts", "generate-docs.py"),
)
generate_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_docs)


class TestSlugify:
    def test_basic(self):
        assert generate_docs.slugify("my-skill-name") == "my-skill-name"

    def test_uppercase(self):
        assert generate_docs.slugify("My Skill") == "my-skill"

    def test_special_chars(self):
        assert generate_docs.slugify("skill_v2.0") == "skill-v2-0"

    def test_strips_leading_trailing(self):
        assert generate_docs.slugify("--test--") == "test"


class TestPrettify:
    def test_kebab_case(self):
        assert generate_docs.prettify("senior-backend") == "Senior Backend"

    def test_single_word(self):
        assert generate_docs.prettify("security") == "Security"


class TestStripContent:
    def test_strips_frontmatter(self):
        content = "---\nname: test\n---\n# Title\nBody text"
        result = generate_docs.strip_content(content)
        assert "name: test" not in result
        assert "Body text" in result

    def test_strips_first_h1(self):
        content = "# My Title\nBody text\n# Another H1"
        result = generate_docs.strip_content(content)
        assert "My Title" not in result
        assert "Body text" in result
        assert "Another H1" in result

    def test_strips_hr_after_title(self):
        content = "# Title\n---\nBody text"
        result = generate_docs.strip_content(content)
        assert result.strip() == "Body text"

    def test_no_frontmatter(self):
        content = "# Title\nBody text"
        result = generate_docs.strip_content(content)
        assert "Body text" in result


class TestExtractTitle:
    def test_extracts_h1(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# My Great Skill\nSome content")
            f.flush()
            title = generate_docs.extract_title(f.name)
        os.unlink(f.name)
        assert title == "My Great Skill"

    def test_skips_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nname: test\n---\n# Real Title\nContent")
            f.flush()
            title = generate_docs.extract_title(f.name)
        os.unlink(f.name)
        assert title == "Real Title"

    def test_no_h1(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("No heading here\nJust content")
            f.flush()
            title = generate_docs.extract_title(f.name)
        os.unlink(f.name)
        assert title is None

    def test_nonexistent_file(self):
        assert generate_docs.extract_title("/nonexistent/path.md") is None


class TestExtractDescriptionFromFrontmatter:
    def test_double_quoted(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write('---\nname: test\ndescription: "My skill description"\n---\n# Title')
            f.flush()
            desc = generate_docs.extract_description_from_frontmatter(f.name)
        os.unlink(f.name)
        assert desc == "My skill description"

    def test_single_quoted(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nname: test\ndescription: 'Single quoted'\n---\n# Title")
            f.flush()
            desc = generate_docs.extract_description_from_frontmatter(f.name)
        os.unlink(f.name)
        assert desc == "Single quoted"

    def test_unquoted(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\nname: test\ndescription: Unquoted description here\n---\n# Title")
            f.flush()
            desc = generate_docs.extract_description_from_frontmatter(f.name)
        os.unlink(f.name)
        assert desc == "Unquoted description here"

    def test_no_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Just a title\nNo frontmatter")
            f.flush()
            desc = generate_docs.extract_description_from_frontmatter(f.name)
        os.unlink(f.name)
        assert desc is None


class TestFindSkillFiles:
    def test_returns_dict(self):
        skills = generate_docs.find_skill_files()
        assert isinstance(skills, dict)

    def test_finds_known_domains(self):
        skills = generate_docs.find_skill_files()
        # At minimum these domains should have skills
        assert "engineering-team" in skills
        assert "product-team" in skills
        assert "finance" in skills

    def test_skips_sample_skills(self):
        skills = generate_docs.find_skill_files()
        for domain, skill_list in skills.items():
            for skill in skill_list:
                assert "assets/sample-skill" not in skill["rel_path"]


class TestRewriteSkillInternalLinks:
    def test_rewrites_script_link(self):
        content = "[my script](scripts/calculator.py)"
        result = generate_docs.rewrite_skill_internal_links(content, "product-team/my-skill")
        assert "github.com" in result
        assert "product-team/my-skill/scripts/calculator.py" in result

    def test_preserves_external_links(self):
        content = "[Google](https://google.com)"
        result = generate_docs.rewrite_skill_internal_links(content, "product-team/my-skill")
        assert result == content

    def test_preserves_anchor_links(self):
        content = "[section](#my-section)"
        result = generate_docs.rewrite_skill_internal_links(content, "product-team/my-skill")
        assert result == content


class TestDomainMapping:
    def test_all_domains_have_sort_order(self):
        for key, value in generate_docs.DOMAINS.items():
            assert len(value) == 4
            assert isinstance(value[1], int)

    def test_unique_sort_orders(self):
        orders = [v[1] for v in generate_docs.DOMAINS.values()]
        assert len(orders) == len(set(orders))
