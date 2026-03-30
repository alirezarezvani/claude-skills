"""Unit tests for the SEO Checker."""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "marketing-skill", "seo-audit", "scripts"
))
from seo_checker import SEOParser, analyze_html, compute_overall_score


class TestSEOParser:
    def test_extracts_title(self):
        p = SEOParser()
        p.feed("<html><head><title>My Page Title</title></head></html>")
        assert p.title == "My Page Title"

    def test_extracts_meta_description(self):
        p = SEOParser()
        p.feed('<html><head><meta name="description" content="A great page"></head></html>')
        assert p.meta_description == "A great page"

    def test_extracts_og_description_fallback(self):
        p = SEOParser()
        p.feed('<html><head><meta property="og:description" content="OG desc"></head></html>')
        assert p.meta_description == "OG desc"

    def test_meta_description_takes_priority_over_og(self):
        p = SEOParser()
        p.feed('<head><meta name="description" content="Primary"><meta property="og:description" content="OG"></head>')
        assert p.meta_description == "Primary"

    def test_extracts_headings(self):
        p = SEOParser()
        p.feed("<h1>Main Title</h1><h2>Section 1</h2><h3>Subsection</h3>")
        assert len(p.h_tags) == 3
        assert p.h_tags[0] == (1, "Main Title")
        assert p.h_tags[1] == (2, "Section 1")
        assert p.h_tags[2] == (3, "Subsection")

    def test_extracts_images(self):
        p = SEOParser()
        p.feed('<img src="photo.jpg" alt="A photo"><img src="icon.png">')
        assert len(p.images) == 2
        assert p.images[0]["alt"] == "A photo"
        assert p.images[1]["alt"] is None

    def test_extracts_links(self):
        p = SEOParser()
        p.feed('<a href="/internal">Click here</a><a href="https://example.com">External</a>')
        assert len(p.links) == 2
        assert p.links[0]["href"] == "/internal"
        assert p.links[1]["href"] == "https://example.com"

    def test_viewport_meta(self):
        p = SEOParser()
        p.feed('<meta name="viewport" content="width=device-width">')
        assert p.viewport_meta is True

    def test_ignores_script_content(self):
        p = SEOParser()
        p.feed("<body><script>var x = 1;</script><p>Real content</p></body>")
        body_text = " ".join(p.body_text_parts)
        assert "var x" not in body_text
        assert "Real content" in body_text


class TestAnalyzeHTML:
    def test_perfect_title(self):
        # 55 chars is within 50-60 optimal range
        title = "A" * 55
        html = f"<html><head><title>{title}</title></head><body></body></html>"
        result = analyze_html(html)
        assert result["title"]["pass"] is True
        assert result["title"]["score"] == 100

    def test_missing_title(self):
        result = analyze_html("<html><head></head><body></body></html>")
        assert result["title"]["pass"] is False
        assert result["title"]["score"] == 0

    def test_one_h1_passes(self):
        result = analyze_html("<h1>Title</h1>")
        assert result["h1"]["pass"] is True
        assert result["h1"]["count"] == 1

    def test_multiple_h1s_fail(self):
        result = analyze_html("<h1>First</h1><h1>Second</h1>")
        assert result["h1"]["pass"] is False
        assert result["h1"]["count"] == 2

    def test_no_h1_fails(self):
        result = analyze_html("<h2>No H1</h2>")
        assert result["h1"]["pass"] is False
        assert result["h1"]["count"] == 0

    def test_heading_hierarchy_skip(self):
        result = analyze_html("<h1>Title</h1><h3>Skipped H2</h3>")
        assert result["heading_hierarchy"]["pass"] is False
        assert len(result["heading_hierarchy"]["issues"]) == 1

    def test_heading_hierarchy_ok(self):
        result = analyze_html("<h1>Title</h1><h2>Section</h2><h3>Sub</h3>")
        assert result["heading_hierarchy"]["pass"] is True

    def test_image_alt_text_all_present(self):
        result = analyze_html('<img src="a.jpg" alt="Photo"><img src="b.jpg" alt="Icon">')
        assert result["image_alt_text"]["pass"] is True
        assert result["image_alt_text"]["coverage_pct"] == 100.0

    def test_image_alt_text_missing(self):
        result = analyze_html('<img src="a.jpg" alt="Photo"><img src="b.jpg">')
        assert result["image_alt_text"]["pass"] is False
        assert result["image_alt_text"]["with_alt"] == 1

    def test_no_images_passes(self):
        result = analyze_html("<p>No images</p>")
        assert result["image_alt_text"]["pass"] is True

    def test_word_count_sufficient(self):
        words = " ".join(["word"] * 350)
        result = analyze_html(f"<body><p>{words}</p></body>")
        assert result["word_count"]["pass"] is True
        assert result["word_count"]["count"] >= 300

    def test_word_count_insufficient(self):
        result = analyze_html("<body><p>Too few words here</p></body>")
        assert result["word_count"]["pass"] is False

    def test_viewport_present(self):
        result = analyze_html('<meta name="viewport" content="width=device-width">')
        assert result["viewport_meta"]["pass"] is True

    def test_viewport_missing(self):
        result = analyze_html("<html><head></head></html>")
        assert result["viewport_meta"]["pass"] is False


class TestComputeOverallScore:
    def test_returns_integer(self):
        html = "<html><head><title>Test</title></head><body><h1>Title</h1></body></html>"
        results = analyze_html(html)
        score = compute_overall_score(results)
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_demo_html_scores_reasonably(self):
        from seo_checker import DEMO_HTML
        results = analyze_html(DEMO_HTML)
        score = compute_overall_score(results)
        # Demo page is well-optimized, should score above 70
        assert score >= 70


class TestEdgeCases:
    def test_empty_html(self):
        result = analyze_html("")
        assert result["title"]["pass"] is False
        assert result["h1"]["count"] == 0

    def test_malformed_html(self):
        # Should not crash on malformed HTML
        result = analyze_html("<h1>Unclosed<h2>Nested badly")
        assert isinstance(result, dict)
        assert "h1" in result
