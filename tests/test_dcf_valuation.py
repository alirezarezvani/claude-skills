"""Unit tests for the DCF Valuation Model."""

import math
import sys
import os

import pytest

sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), "..", "finance", "financial-analyst", "scripts"
))
from dcf_valuation import DCFModel, safe_divide


class TestSafeDivide:
    def test_normal_division(self):
        assert safe_divide(10, 2) == 5.0

    def test_zero_denominator(self):
        assert safe_divide(10, 0) == 0.0

    def test_none_denominator(self):
        assert safe_divide(10, None) == 0.0

    def test_custom_default(self):
        assert safe_divide(10, 0, default=-1.0) == -1.0

    def test_negative_values(self):
        assert safe_divide(-10, 2) == -5.0


@pytest.fixture
def model():
    """A fully configured DCF model with sample data."""
    m = DCFModel()
    m.set_historical_financials({
        "revenue": [80_000_000, 100_000_000],
        "net_debt": 20_000_000,
        "shares_outstanding": 10_000_000,
    })
    m.set_assumptions({
        "projection_years": 5,
        "revenue_growth_rates": [0.15, 0.12, 0.10, 0.08, 0.06],
        "fcf_margins": [0.12, 0.13, 0.14, 0.15, 0.16],
        "wacc_inputs": {
            "risk_free_rate": 0.04,
            "equity_risk_premium": 0.06,
            "beta": 1.2,
            "cost_of_debt": 0.05,
            "tax_rate": 0.25,
            "equity_weight": 0.70,
            "debt_weight": 0.30,
        },
        "terminal_growth_rate": 0.025,
        "exit_ev_ebitda_multiple": 12.0,
        "terminal_ebitda_margin": 0.20,
    })
    return m


class TestWACC:
    def test_wacc_calculation(self, model):
        wacc = model.calculate_wacc()
        # Cost of equity = 0.04 + 1.2 * 0.06 = 0.112
        # After-tax cost of debt = 0.05 * (1 - 0.25) = 0.0375
        # WACC = 0.70 * 0.112 + 0.30 * 0.0375 = 0.0784 + 0.01125 = 0.08965
        assert abs(wacc - 0.08965) < 0.0001

    def test_wacc_default_inputs(self):
        m = DCFModel()
        m.set_assumptions({})
        wacc = m.calculate_wacc()
        # Defaults: rf=0.04, erp=0.06, beta=1.0, cod=0.05, tax=0.25
        # CoE = 0.04 + 1.0 * 0.06 = 0.10
        # ATCoD = 0.05 * 0.75 = 0.0375
        # WACC = 0.70 * 0.10 + 0.30 * 0.0375 = 0.08125
        assert abs(wacc - 0.08125) < 0.0001


class TestProjectCashFlows:
    def test_projects_correct_years(self, model):
        model.calculate_wacc()
        revenue, fcf = model.project_cash_flows()
        assert len(revenue) == 5
        assert len(fcf) == 5

    def test_first_year_revenue(self, model):
        model.calculate_wacc()
        revenue, _ = model.project_cash_flows()
        # base_revenue = 100M, growth = 15%
        assert abs(revenue[0] - 115_000_000) < 1

    def test_first_year_fcf(self, model):
        model.calculate_wacc()
        revenue, fcf = model.project_cash_flows()
        # Year 1: revenue = 115M, fcf_margin = 12% -> FCF = 13.8M
        assert abs(fcf[0] - 13_800_000) < 1

    def test_missing_historical_revenue(self):
        m = DCFModel()
        m.set_historical_financials({})
        m.set_assumptions({"projection_years": 3})
        with pytest.raises(ValueError, match="Historical revenue"):
            m.project_cash_flows()

    def test_default_growth_when_rates_short(self):
        m = DCFModel()
        m.set_historical_financials({"revenue": [100_000]})
        m.set_assumptions({
            "projection_years": 3,
            "revenue_growth_rates": [0.10],  # Only 1 year specified
            "default_revenue_growth": 0.05,
            "fcf_margins": [0.10],
            "default_fcf_margin": 0.10,
        })
        m.calculate_wacc()
        revenue, _ = m.project_cash_flows()
        assert len(revenue) == 3
        # Year 1: 100000 * 1.10 = 110000
        # Year 2: 110000 * 1.05 = 115500 (uses default)
        assert abs(revenue[1] - 115500) < 1


class TestTerminalValue:
    def test_perpetuity_method(self, model):
        model.calculate_wacc()
        model.project_cash_flows()
        tv_perp, tv_exit = model.calculate_terminal_value()
        assert tv_perp > 0

    def test_exit_multiple_method(self, model):
        model.calculate_wacc()
        model.project_cash_flows()
        _, tv_exit = model.calculate_terminal_value()
        # Terminal revenue * ebitda_margin * exit_multiple
        terminal_revenue = model.projected_revenue[-1]
        expected = terminal_revenue * 0.20 * 12.0
        assert abs(tv_exit - expected) < 1

    def test_perpetuity_zero_when_wacc_lte_growth(self):
        m = DCFModel()
        m.set_historical_financials({"revenue": [100_000]})
        m.set_assumptions({
            "projection_years": 1,
            "revenue_growth_rates": [0.05],
            "fcf_margins": [0.10],
            "terminal_growth_rate": 0.10,  # Higher than WACC
            "exit_ev_ebitda_multiple": 10.0,
            "terminal_ebitda_margin": 0.20,
        })
        m.wacc = 0.08  # Lower than terminal growth
        m.project_cash_flows()
        tv_perp, _ = m.calculate_terminal_value()
        assert tv_perp == 0.0


class TestEnterpriseAndEquityValue:
    def test_full_valuation_pipeline(self, model):
        results = model.run_full_valuation()
        assert results["wacc"] > 0
        assert len(results["projected_revenue"]) == 5
        assert results["enterprise_value"]["perpetuity_growth"] > 0
        assert results["enterprise_value"]["exit_multiple"] > 0
        assert results["equity_value"]["perpetuity_growth"] > 0
        assert results["value_per_share"]["perpetuity_growth"] > 0

    def test_equity_subtracts_net_debt(self, model):
        model.calculate_wacc()
        model.project_cash_flows()
        model.calculate_terminal_value()
        model.calculate_enterprise_value()
        model.calculate_equity_value()
        # equity = enterprise - net_debt (20M)
        assert abs(
            model.equity_value_perpetuity -
            (model.enterprise_value_perpetuity - 20_000_000)
        ) < 1

    def test_value_per_share(self, model):
        model.calculate_wacc()
        model.project_cash_flows()
        model.calculate_terminal_value()
        model.calculate_enterprise_value()
        model.calculate_equity_value()
        # shares = 10M
        expected = model.equity_value_perpetuity / 10_000_000
        assert abs(model.value_per_share_perpetuity - expected) < 0.01


class TestSensitivityAnalysis:
    def test_returns_table_structure(self, model):
        model.calculate_wacc()
        model.project_cash_flows()
        model.calculate_terminal_value()
        result = model.sensitivity_analysis()
        assert "wacc_values" in result
        assert "growth_values" in result
        assert "enterprise_value_table" in result
        assert "share_price_table" in result
        assert len(result["enterprise_value_table"]) == 5
        assert len(result["enterprise_value_table"][0]) == 5

    def test_inf_when_wacc_lte_growth(self, model):
        model.calculate_wacc()
        model.project_cash_flows()
        model.calculate_terminal_value()
        # Use a growth range that includes values >= wacc
        result = model.sensitivity_analysis(
            wacc_range=[0.05],
            growth_range=[0.05, 0.06],
        )
        assert result["enterprise_value_table"][0][0] == float("inf")
        assert result["enterprise_value_table"][0][1] == float("inf")
