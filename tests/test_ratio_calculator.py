"""Unit tests for the Financial Ratio Calculator."""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "finance", "financial-analyst", "scripts"
))
from ratio_calculator import FinancialRatioCalculator, safe_divide


@pytest.fixture
def sample_data():
    return {
        "income_statement": {
            "revenue": 1_000_000,
            "cost_of_goods_sold": 400_000,
            "operating_income": 200_000,
            "net_income": 150_000,
            "interest_expense": 20_000,
            "ebitda": 250_000,
        },
        "balance_sheet": {
            "total_assets": 2_000_000,
            "total_equity": 1_200_000,
            "current_assets": 500_000,
            "current_liabilities": 300_000,
            "inventory": 100_000,
            "cash_and_equivalents": 200_000,
            "total_debt": 500_000,
            "accounts_receivable": 150_000,
        },
        "cash_flow": {
            "operating_cash_flow": 180_000,
        },
        "market_data": {
            "share_price": 50.0,
            "shares_outstanding": 100_000,
            "earnings_growth_rate": 0.15,
        },
    }


@pytest.fixture
def calc(sample_data):
    return FinancialRatioCalculator(sample_data)


class TestProfitability:
    def test_roe(self, calc):
        ratios = calc.calculate_profitability()
        # 150000 / 1200000 = 0.125
        assert abs(ratios["roe"]["value"] - 0.125) < 0.001

    def test_roa(self, calc):
        ratios = calc.calculate_profitability()
        # 150000 / 2000000 = 0.075
        assert abs(ratios["roa"]["value"] - 0.075) < 0.001

    def test_gross_margin(self, calc):
        ratios = calc.calculate_profitability()
        # (1000000 - 400000) / 1000000 = 0.60
        assert abs(ratios["gross_margin"]["value"] - 0.60) < 0.001

    def test_operating_margin(self, calc):
        ratios = calc.calculate_profitability()
        # 200000 / 1000000 = 0.20
        assert abs(ratios["operating_margin"]["value"] - 0.20) < 0.001

    def test_net_margin(self, calc):
        ratios = calc.calculate_profitability()
        # 150000 / 1000000 = 0.15
        assert abs(ratios["net_margin"]["value"] - 0.15) < 0.001

    def test_interpretation_populated(self, calc):
        ratios = calc.calculate_profitability()
        for key in ratios:
            assert "interpretation" in ratios[key]


class TestLiquidity:
    def test_current_ratio(self, calc):
        ratios = calc.calculate_liquidity()
        # 500000 / 300000 = 1.667
        assert abs(ratios["current_ratio"]["value"] - 1.667) < 0.01

    def test_quick_ratio(self, calc):
        ratios = calc.calculate_liquidity()
        # (500000 - 100000) / 300000 = 1.333
        assert abs(ratios["quick_ratio"]["value"] - 1.333) < 0.01

    def test_cash_ratio(self, calc):
        ratios = calc.calculate_liquidity()
        # 200000 / 300000 = 0.667
        assert abs(ratios["cash_ratio"]["value"] - 0.667) < 0.01


class TestLeverage:
    def test_debt_to_equity(self, calc):
        ratios = calc.calculate_leverage()
        # 500000 / 1200000 = 0.417
        assert abs(ratios["debt_to_equity"]["value"] - 0.417) < 0.01

    def test_interest_coverage(self, calc):
        ratios = calc.calculate_leverage()
        # 200000 / 20000 = 10.0
        assert abs(ratios["interest_coverage"]["value"] - 10.0) < 0.01


class TestEfficiency:
    def test_asset_turnover(self, calc):
        ratios = calc.calculate_efficiency()
        # 1000000 / 2000000 = 0.5
        assert abs(ratios["asset_turnover"]["value"] - 0.5) < 0.01

    def test_inventory_turnover(self, calc):
        ratios = calc.calculate_efficiency()
        # 400000 / 100000 = 4.0
        assert abs(ratios["inventory_turnover"]["value"] - 4.0) < 0.01

    def test_dso(self, calc):
        ratios = calc.calculate_efficiency()
        # receivables_turnover = 1000000 / 150000 = 6.667
        # DSO = 365 / 6.667 = 54.75
        assert abs(ratios["dso"]["value"] - 54.75) < 0.5


class TestValuation:
    def test_pe_ratio(self, calc):
        ratios = calc.calculate_valuation()
        # EPS = 150000 / 100000 = 1.5
        # PE = 50.0 / 1.5 = 33.33
        assert abs(ratios["pe_ratio"]["value"] - 33.33) < 0.1

    def test_ev_ebitda(self, calc):
        ratios = calc.calculate_valuation()
        # market_cap = 50 * 100000 = 5000000
        # EV = 5000000 + 500000 - 200000 = 5300000
        # EV/EBITDA = 5300000 / 250000 = 21.2
        assert abs(ratios["ev_ebitda"]["value"] - 21.2) < 0.1


class TestCalculateAll:
    def test_returns_all_categories(self, calc):
        results = calc.calculate_all()
        assert "profitability" in results
        assert "liquidity" in results
        assert "leverage" in results
        assert "efficiency" in results
        assert "valuation" in results


class TestInterpretation:
    def test_dso_lower_is_better(self, calc):
        result = calc.interpret_ratio("dso", 25.0)
        assert "Excellent" in result

    def test_dso_high_is_concern(self, calc):
        result = calc.interpret_ratio("dso", 90.0)
        assert "Concern" in result

    def test_debt_to_equity_conservative(self, calc):
        result = calc.interpret_ratio("debt_to_equity", 0.2)
        assert "Conservative" in result

    def test_zero_value(self, calc):
        result = calc.interpret_ratio("roe", 0.0)
        assert "Insufficient" in result

    def test_unknown_ratio(self, calc):
        result = calc.interpret_ratio("unknown_ratio", 5.0)
        assert "No benchmark" in result


class TestEdgeCases:
    def test_zero_revenue(self):
        data = {"income_statement": {"revenue": 0}, "balance_sheet": {}, "cash_flow": {}, "market_data": {}}
        calc = FinancialRatioCalculator(data)
        ratios = calc.calculate_profitability()
        assert ratios["gross_margin"]["value"] == 0.0

    def test_zero_equity(self):
        data = {"income_statement": {"net_income": 100}, "balance_sheet": {"total_equity": 0}, "cash_flow": {}, "market_data": {}}
        calc = FinancialRatioCalculator(data)
        ratios = calc.calculate_profitability()
        assert ratios["roe"]["value"] == 0.0

    def test_missing_market_data(self):
        data = {"income_statement": {}, "balance_sheet": {}, "cash_flow": {}, "market_data": {}}
        calc = FinancialRatioCalculator(data)
        ratios = calc.calculate_valuation()
        assert ratios["pe_ratio"]["value"] == 0.0
