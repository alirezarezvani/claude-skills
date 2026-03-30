"""Unit tests for the Funnel Analyzer."""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "marketing-skill", "campaign-analytics", "scripts"
))
from funnel_analyzer import analyze_funnel, compare_segments, safe_divide


class TestAnalyzeFunnel:
    def test_basic_funnel(self):
        stages = ["Visit", "Signup", "Activate", "Pay"]
        counts = [10000, 5000, 2000, 500]
        result = analyze_funnel(stages, counts)

        assert result["total_entries"] == 10000
        assert result["total_conversions"] == 500
        assert result["total_lost"] == 9500
        assert result["overall_conversion_rate"] == 5.0

    def test_stage_metrics_count(self):
        stages = ["A", "B", "C"]
        counts = [1000, 500, 100]
        result = analyze_funnel(stages, counts)
        assert len(result["stage_metrics"]) == 3

    def test_conversion_rates(self):
        stages = ["Visit", "Signup", "Pay"]
        counts = [1000, 500, 250]
        result = analyze_funnel(stages, counts)

        # Visit -> Signup: 500/1000 = 50%
        assert result["stage_metrics"][1]["conversion_rate"] == 50.0
        # Signup -> Pay: 250/500 = 50%
        assert result["stage_metrics"][2]["conversion_rate"] == 50.0

    def test_dropoff_detection(self):
        stages = ["A", "B", "C"]
        counts = [1000, 200, 100]
        result = analyze_funnel(stages, counts)

        # Biggest absolute drop: A->B (800)
        assert result["bottleneck_absolute"]["dropoff_count"] == 800
        assert "A -> B" in result["bottleneck_absolute"]["transition"]

    def test_relative_bottleneck(self):
        stages = ["A", "B", "C"]
        counts = [1000, 900, 100]
        result = analyze_funnel(stages, counts)

        # A->B: dropoff_rate = 10%, B->C: dropoff_rate = 88.89%
        assert "B -> C" in result["bottleneck_relative"]["transition"]

    def test_cumulative_conversion(self):
        stages = ["A", "B", "C"]
        counts = [1000, 500, 200]
        result = analyze_funnel(stages, counts)
        assert result["stage_metrics"][0]["cumulative_conversion"] == 100.0
        assert result["stage_metrics"][1]["cumulative_conversion"] == 50.0
        assert result["stage_metrics"][2]["cumulative_conversion"] == 20.0

    def test_single_stage(self):
        result = analyze_funnel(["Only"], [500])
        assert result["overall_conversion_rate"] == 100.0
        assert result["total_entries"] == 500
        assert result["total_lost"] == 0

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError, match="must match"):
            analyze_funnel(["A", "B"], [100])

    def test_empty_stages_raises(self):
        with pytest.raises(ValueError, match="at least one"):
            analyze_funnel([], [])

    def test_no_dropoff(self):
        stages = ["A", "B"]
        counts = [100, 100]
        result = analyze_funnel(stages, counts)
        assert result["stage_metrics"][1]["conversion_rate"] == 100.0
        assert result["stage_metrics"][1]["dropoff_count"] == 0


class TestCompareSegments:
    def test_ranks_segments(self):
        stages = ["Visit", "Signup", "Pay"]
        segments = {
            "mobile": {"counts": [1000, 300, 50]},
            "desktop": {"counts": [1000, 600, 200]},
        }
        result = compare_segments(segments, stages)
        # Desktop has better overall conversion (20% vs 5%)
        assert result["rankings"][0]["segment"] == "desktop"

    def test_mismatched_segment_counts_raises(self):
        with pytest.raises(ValueError, match="counts"):
            compare_segments({"bad": {"counts": [100, 50]}}, ["A", "B", "C"])
