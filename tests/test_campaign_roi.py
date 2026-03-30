"""Unit tests for the Campaign ROI Calculator."""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "marketing-skill", "campaign-analytics", "scripts"
))
from campaign_roi_calculator import (
    safe_divide,
    get_benchmark,
    assess_performance,
    calculate_campaign_metrics,
    calculate_portfolio_summary,
)


class TestSafeDivide:
    def test_normal(self):
        assert safe_divide(10, 2) == 5.0

    def test_zero_denominator(self):
        assert safe_divide(10, 0) == 0.0

    def test_custom_default(self):
        assert safe_divide(10, 0, -1.0) == -1.0


class TestGetBenchmark:
    def test_known_channel(self):
        result = get_benchmark("ctr", "email")
        assert result == (1.0, 2.5, 5.0)

    def test_falls_back_to_default(self):
        result = get_benchmark("ctr", "nonexistent_channel")
        assert result == (0.5, 2.0, 5.0)

    def test_unknown_metric(self):
        result = get_benchmark("nonexistent_metric", "email")
        assert result == (0, 0, 0)


class TestAssessPerformance:
    def test_excellent_high_is_better(self):
        assert assess_performance(10.0, (1.0, 3.0, 5.0), higher_is_better=True) == "excellent"

    def test_good_high_is_better(self):
        assert assess_performance(3.5, (1.0, 3.0, 5.0), higher_is_better=True) == "good"

    def test_below_target_high_is_better(self):
        assert assess_performance(1.5, (1.0, 3.0, 5.0), higher_is_better=True) == "below_target"

    def test_underperforming_high_is_better(self):
        assert assess_performance(0.5, (1.0, 3.0, 5.0), higher_is_better=True) == "underperforming"

    def test_excellent_low_is_better(self):
        # For cost metrics, lower is better
        assert assess_performance(0.5, (1.0, 3.0, 5.0), higher_is_better=False) == "excellent"

    def test_underperforming_low_is_better(self):
        assert assess_performance(10.0, (1.0, 3.0, 5.0), higher_is_better=False) == "underperforming"


class TestCalculateCampaignMetrics:
    @pytest.fixture
    def campaign(self):
        return {
            "name": "Test Campaign",
            "channel": "paid_search",
            "spend": 1000.0,
            "revenue": 5000.0,
            "impressions": 100000,
            "clicks": 3000,
            "leads": 100,
            "customers": 10,
        }

    def test_roi(self, campaign):
        result = calculate_campaign_metrics(campaign)
        # ROI = (5000 - 1000) / 1000 * 100 = 400%
        assert result["metrics"]["roi_pct"] == 400.0

    def test_roas(self, campaign):
        result = calculate_campaign_metrics(campaign)
        # ROAS = 5000 / 1000 = 5.0
        assert result["metrics"]["roas"] == 5.0

    def test_cpa(self, campaign):
        result = calculate_campaign_metrics(campaign)
        # CPA = 1000 / 10 = 100.0
        assert result["metrics"]["cpa"] == 100.0

    def test_ctr(self, campaign):
        result = calculate_campaign_metrics(campaign)
        # CTR = 3000 / 100000 * 100 = 3.0%
        assert result["metrics"]["ctr_pct"] == 3.0

    def test_cvr(self, campaign):
        result = calculate_campaign_metrics(campaign)
        # CVR = 10 / 100 * 100 = 10.0%
        assert result["metrics"]["cvr_pct"] == 10.0

    def test_profit(self, campaign):
        result = calculate_campaign_metrics(campaign)
        assert result["metrics"]["profit"] == 4000.0

    def test_zero_customers(self):
        campaign = {"name": "No Customers", "channel": "display", "spend": 500, "revenue": 0,
                     "impressions": 10000, "clicks": 50, "leads": 5, "customers": 0}
        result = calculate_campaign_metrics(campaign)
        assert result["metrics"]["cpa"] is None
        assert result["metrics"]["cac"] is None

    def test_zero_impressions(self):
        campaign = {"name": "No Impressions", "channel": "email", "spend": 100, "revenue": 500,
                     "impressions": 0, "clicks": 0, "leads": 0, "customers": 0}
        result = calculate_campaign_metrics(campaign)
        assert result["metrics"]["ctr_pct"] is None
        assert result["metrics"]["cpm"] is None

    def test_unprofitable_campaign_flagged(self):
        campaign = {"name": "Loser", "channel": "display", "spend": 1000, "revenue": 200,
                     "impressions": 50000, "clicks": 100, "leads": 5, "customers": 1}
        result = calculate_campaign_metrics(campaign)
        assert any("unprofitable" in f.lower() for f in result["flags"])

    def test_benchmark_assessments_present(self, campaign):
        result = calculate_campaign_metrics(campaign)
        assert "ctr" in result["assessments"]
        assert "benchmark_range" in result["assessments"]["ctr"]


class TestCalculatePortfolioSummary:
    def test_aggregates_totals(self):
        campaigns = [
            calculate_campaign_metrics({
                "name": "A", "channel": "email", "spend": 500, "revenue": 2000,
                "impressions": 50000, "clicks": 1000, "leads": 50, "customers": 5,
            }),
            calculate_campaign_metrics({
                "name": "B", "channel": "paid_search", "spend": 1000, "revenue": 4000,
                "impressions": 100000, "clicks": 3000, "leads": 100, "customers": 10,
            }),
        ]
        summary = calculate_portfolio_summary(campaigns)
        assert summary["total_spend"] == 1500
        assert summary["total_revenue"] == 6000
        assert summary["total_profit"] == 4500
        assert summary["total_customers"] == 15
        assert summary["total_campaigns"] == 2

    def test_channel_summary(self):
        campaigns = [
            calculate_campaign_metrics({
                "name": "A", "channel": "email", "spend": 500, "revenue": 2000,
                "impressions": 50000, "clicks": 1000, "leads": 50, "customers": 5,
            }),
        ]
        summary = calculate_portfolio_summary(campaigns)
        assert "email" in summary["channel_summary"]
        assert summary["channel_summary"]["email"]["spend"] == 500
