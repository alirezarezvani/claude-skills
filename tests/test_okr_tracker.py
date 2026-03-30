"""Unit tests for the OKR Tracker."""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "c-level-advisor", "coo-advisor", "scripts"
))
from okr_tracker import calculate_kr_score, get_kr_status


class TestCalculateKrScoreNumeric:
    def test_basic_numeric(self):
        kr = {"type": "numeric", "baseline_value": 0, "current_value": 50, "target_value": 100}
        assert calculate_kr_score(kr) == 0.5

    def test_at_target(self):
        kr = {"type": "numeric", "baseline_value": 0, "current_value": 100, "target_value": 100}
        assert calculate_kr_score(kr) == 1.0

    def test_no_progress(self):
        kr = {"type": "numeric", "baseline_value": 0, "current_value": 0, "target_value": 100}
        assert calculate_kr_score(kr) == 0.0

    def test_clamped_above_one(self):
        kr = {"type": "numeric", "baseline_value": 0, "current_value": 150, "target_value": 100}
        assert calculate_kr_score(kr) == 1.0

    def test_target_equals_baseline(self):
        kr = {"type": "numeric", "baseline_value": 50, "current_value": 50, "target_value": 50}
        assert calculate_kr_score(kr) == 0.0

    def test_lower_is_better(self):
        # Reducing churn from 10% to 5%, currently at 7%
        kr = {
            "type": "numeric",
            "baseline_value": 10,
            "current_value": 7,
            "target_value": 5,
            "lower_is_better": True,
        }
        # improvement = 10 - 7 = 3, needed = 10 - 5 = 5 -> score = 0.6
        assert abs(calculate_kr_score(kr) - 0.6) < 0.01

    def test_lower_is_better_at_target(self):
        kr = {
            "type": "numeric",
            "baseline_value": 10,
            "current_value": 5,
            "target_value": 5,
            "lower_is_better": True,
        }
        assert calculate_kr_score(kr) == 1.0

    def test_lower_is_better_exceeded(self):
        kr = {
            "type": "numeric",
            "baseline_value": 10,
            "current_value": 3,
            "target_value": 5,
            "lower_is_better": True,
        }
        assert calculate_kr_score(kr) == 1.0


class TestCalculateKrScorePercentage:
    def test_percentage_midway(self):
        kr = {"type": "percentage", "baseline_pct": 10, "current_pct": 15, "target_pct": 20}
        assert calculate_kr_score(kr) == 0.5

    def test_percentage_at_target(self):
        kr = {"type": "percentage", "baseline_pct": 0, "current_pct": 100, "target_pct": 100}
        assert calculate_kr_score(kr) == 1.0

    def test_percentage_target_equals_baseline(self):
        kr = {"type": "percentage", "baseline_pct": 50, "current_pct": 50, "target_pct": 50}
        assert calculate_kr_score(kr) == 0.0


class TestCalculateKrScoreMilestone:
    def test_milestone_explicit_score(self):
        kr = {"type": "milestone", "score": 0.75}
        assert calculate_kr_score(kr) == 0.75

    def test_milestone_hit_count(self):
        kr = {"type": "milestone", "milestones_total": 4, "milestones_hit": 3}
        assert calculate_kr_score(kr) == 0.75

    def test_milestone_clamped(self):
        kr = {"type": "milestone", "score": 1.5}
        assert calculate_kr_score(kr) == 1.0


class TestCalculateKrScoreBoolean:
    def test_boolean_done(self):
        kr = {"type": "boolean", "done": True}
        assert calculate_kr_score(kr) == 1.0

    def test_boolean_not_done(self):
        kr = {"type": "boolean", "done": False}
        assert calculate_kr_score(kr) == 0.0


class TestGetKrStatus:
    def test_on_track(self):
        status = get_kr_status(0.8, 0.5, {})
        assert status == "on_track"

    def test_complete_requires_done_flag(self):
        # "complete" status requires kr["done"] = True
        status = get_kr_status(1.0, 0.5, {"done": True})
        assert status == "complete"

    def test_score_one_without_done_is_on_track(self):
        status = get_kr_status(1.0, 0.5, {})
        assert status == "on_track"

    def test_not_started(self):
        # not_started requires score==0 AND quarter_progress < 0.1
        status = get_kr_status(0.0, 0.05, {})
        assert status == "not_started"

    def test_off_track(self):
        # Very low score deep into the quarter
        status = get_kr_status(0.1, 0.8, {})
        assert status == "off_track"
