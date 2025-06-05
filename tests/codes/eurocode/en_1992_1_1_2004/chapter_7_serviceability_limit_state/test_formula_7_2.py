"""Testing formula 7.2 and 7.2sub1 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_2 import (
    Form7Dot2StressDistributionCoefficient,
    Form7Dot2Sub1AxialForceCoefficient,
)
from blueprints.validations import NegativeValueError


class TestForm7Dot2StressDistributionCoefficient:
    """Validation for formula 7.2 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        sigma_c = 10.0
        k_1 = 1.5
        h = 500.0
        f_ct_eff = 25.0

        # Object to test
        formula = Form7Dot2StressDistributionCoefficient(sigma_c=sigma_c, k_1=k_1, h=h, f_ct_eff=f_ct_eff)

        # Expected result, manually calculated
        manually_calculated_result = 0.29333333333333333333

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("sigma_c", "k_1", "h", "f_ct_eff"),
        [
            (-10.0, 1.5, 500.0, 25.0),  # sigma_c is negative
            (10.0, -1.5, 500.0, 25.0),  # k_1 is negative
            (10.0, 1.5, -500.0, 25.0),  # h is negative
            (10.0, 1.5, 500.0, -25.0),  # f_ct_eff is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, sigma_c: float, k_1: float, h: float, f_ct_eff: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot2StressDistributionCoefficient(sigma_c=sigma_c, k_1=k_1, h=h, f_ct_eff=f_ct_eff)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_c = min\left(0.4 \cdot \left(1 - \frac{\sigma_c}{k_1 \cdot \left(\frac{ h}{min( h, 1000)}\right) "
                r"\cdot f_{ct,eff}}\right), 1\right) = "
                r"min\left(0.4 \cdot \left(1 - \frac{10.000}{1.500 \cdot \left(\frac{ 500.000}{min( 500.000, 1000)}\right) "
                r"\cdot 25.000}\right), 1\right) = 0.293 \ -",
            ),
            ("short", r"k_c = 0.293 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        sigma_c = 10.0
        k_1 = 1.5
        h = 500.0
        f_ct_eff = 25.0

        # Object to test
        latex = Form7Dot2StressDistributionCoefficient(sigma_c=sigma_c, k_1=k_1, h=h, f_ct_eff=f_ct_eff).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestForm7Dot2Sub1AxialForceCoefficient:
    """Validation for formula 7.2sub1 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        n_ed = 5.0
        h = 500.0

        # Object to test
        formula = Form7Dot2Sub1AxialForceCoefficient(n_ed=n_ed, h=h)

        # Expected result, manually calculated
        manually_calculated_result = 1.5

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("n_ed", "h"),
        [
            (5.0, -500.0),  # h is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, n_ed: float, h: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            Form7Dot2Sub1AxialForceCoefficient(n_ed=n_ed, h=h)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"k_1 = \begin{cases} 1.5 & \text{if } N_{Ed} > 0 \\ \frac{2 \cdot min(h, 1000)}{3 \cdot h} & \text{if } N_{Ed} \le 0 \end{cases} = "
                r"\begin{cases} 1.5 & \text{if } 5.000 > 0 \\ \frac{2 \cdot min(500.000, 1000)}{3 \cdot 500.000} & \text{if } 5.000 "
                r"\le 0 \end{cases} = 1.500 \ -",
            ),
            ("short", r"k_1 = 1.500 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        n_ed = 5.0
        h = 500.0

        # Object to test
        latex = Form7Dot2Sub1AxialForceCoefficient(n_ed=n_ed, h=h).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
