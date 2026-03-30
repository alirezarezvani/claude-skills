"""Unit tests for the RICE Prioritizer."""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "product-team", "product-manager-toolkit", "scripts"
))
from rice_prioritizer import RICECalculator


@pytest.fixture
def calc():
    return RICECalculator()


class TestCalculateRice:
    """Test the core RICE formula: (Reach * Impact * Confidence) / Effort."""

    def test_basic_calculation(self, calc):
        # reach=1000, impact=high(2.0), confidence=high(100/100=1.0), effort=m(5)
        # = (1000 * 2.0 * 1.0) / 5 = 400.0
        assert calc.calculate_rice(1000, "high", "high", "m") == 400.0

    def test_massive_impact(self, calc):
        # reach=500, impact=massive(3.0), confidence=medium(0.8), effort=s(3)
        # = (500 * 3.0 * 0.8) / 3 = 400.0
        assert calc.calculate_rice(500, "massive", "medium", "s") == 400.0

    def test_minimal_impact(self, calc):
        # reach=1000, impact=minimal(0.25), confidence=low(0.5), effort=xs(1)
        # = (1000 * 0.25 * 0.5) / 1 = 125.0
        assert calc.calculate_rice(1000, "minimal", "low", "xs") == 125.0

    def test_zero_reach(self, calc):
        assert calc.calculate_rice(0, "high", "high", "m") == 0.0

    def test_case_insensitive(self, calc):
        assert calc.calculate_rice(1000, "HIGH", "HIGH", "M") == 400.0

    def test_unknown_impact_defaults_to_one(self, calc):
        # Unknown impact maps to 1.0
        # reach=1000, impact=1.0, confidence=high(1.0), effort=m(5)
        # = (1000 * 1.0 * 1.0) / 5 = 200.0
        assert calc.calculate_rice(1000, "unknown", "high", "m") == 200.0

    def test_xl_effort(self, calc):
        # reach=1300, impact=medium(1.0), confidence=high(1.0), effort=xl(13)
        # = (1300 * 1.0 * 1.0) / 13 = 100.0
        assert calc.calculate_rice(1300, "medium", "high", "xl") == 100.0

    @pytest.mark.parametrize("impact,expected_score", [
        ("massive", 3.0),
        ("high", 2.0),
        ("medium", 1.0),
        ("low", 0.5),
        ("minimal", 0.25),
    ])
    def test_impact_map(self, calc, impact, expected_score):
        # reach=100, confidence=high(1.0), effort=xs(1) -> score = 100 * impact
        result = calc.calculate_rice(100, impact, "high", "xs")
        assert result == round(100 * expected_score, 2)


class TestPrioritizeFeatures:
    """Test feature sorting by RICE score."""

    def test_sorts_descending(self, calc):
        features = [
            {"name": "low", "reach": 100, "impact": "low", "confidence": "low", "effort": "xl"},
            {"name": "high", "reach": 10000, "impact": "massive", "confidence": "high", "effort": "xs"},
        ]
        result = calc.prioritize_features(features)
        assert result[0]["name"] == "high"
        assert result[1]["name"] == "low"

    def test_adds_rice_score(self, calc):
        features = [{"name": "test", "reach": 1000, "impact": "high", "confidence": "high", "effort": "m"}]
        result = calc.prioritize_features(features)
        assert "rice_score" in result[0]
        assert result[0]["rice_score"] == 400.0

    def test_empty_list(self, calc):
        assert calc.prioritize_features([]) == []

    def test_defaults_for_missing_fields(self, calc):
        features = [{"name": "sparse"}]
        result = calc.prioritize_features(features)
        assert result[0]["rice_score"] == 0.0  # reach defaults to 0


class TestAnalyzePortfolio:
    """Test portfolio analysis metrics."""

    def test_empty_features(self, calc):
        assert calc.analyze_portfolio([]) == {}

    def test_counts_quick_wins(self, calc):
        features = [
            {"name": "qw", "reach": 1000, "impact": "high", "confidence": "high", "effort": "xs", "rice_score": 100},
            {"name": "big", "reach": 1000, "impact": "high", "confidence": "high", "effort": "xl", "rice_score": 50},
        ]
        result = calc.analyze_portfolio(features)
        assert result["quick_wins"] == 1
        assert result["big_bets"] == 1
        assert result["total_features"] == 2

    def test_total_effort(self, calc):
        features = [
            {"name": "a", "effort": "m", "rice_score": 10},  # 5 months
            {"name": "b", "effort": "s", "rice_score": 20},  # 3 months
        ]
        result = calc.analyze_portfolio(features)
        assert result["total_effort_months"] == 8


class TestGenerateRoadmap:
    """Test roadmap generation with capacity constraints."""

    def test_single_quarter(self, calc):
        features = [
            {"name": "a", "effort": "s", "rice_score": 100},  # 3 months
            {"name": "b", "effort": "s", "rice_score": 50},   # 3 months
        ]
        roadmap = calc.generate_roadmap(features, team_capacity=10)
        assert len(roadmap) == 1
        assert len(roadmap[0]["features"]) == 2
        assert roadmap[0]["capacity_used"] == 6

    def test_overflow_to_next_quarter(self, calc):
        features = [
            {"name": "a", "effort": "l", "rice_score": 100},  # 8 months
            {"name": "b", "effort": "l", "rice_score": 50},   # 8 months
        ]
        roadmap = calc.generate_roadmap(features, team_capacity=10)
        assert len(roadmap) == 2
        assert roadmap[0]["features"][0]["name"] == "a"
        assert roadmap[1]["features"][0]["name"] == "b"

    def test_empty_features(self, calc):
        assert calc.generate_roadmap([], team_capacity=10) == []
