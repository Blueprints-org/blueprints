"""Testing formula 6.49 of EN 1993-1-1:2005."""

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_6_ultimate_limit_state.formula_6_49 import (
    Form6Dot49ReductionFactorForBuckling,
    SubForm6Dot49Phi,
)
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot49ReductionFactorForBuckling:
    """Validation for formula 6.49 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        phi = 0.922
        lambda_bar = 0.8

        # Object to test
        formula = Form6Dot49ReductionFactorForBuckling(phi=phi, lambda_bar=lambda_bar)

        # Expected result, manually calculated
        # 1 / (0.922 + sqrt(0.922^2 - 0.8^2)) = 1 / (0.922 + sqrt(0.210084)) = 1 / 1.380349 = 0.724454
        manually_calculated_result = 0.724454  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    def test_evaluation_upper_bound(self) -> None:
        """Tests that the result is not larger than 1.0 for a low slenderness."""
        # Example values
        phi = 0.488
        lambda_bar = 0.1

        # Object to test
        formula = Form6Dot49ReductionFactorForBuckling(phi=phi, lambda_bar=lambda_bar)

        # Expected result, manually calculated
        # 1 / (0.488 + sqrt(0.488^2 - 0.1^2)) = 1 / (0.488 + sqrt(0.228144)) = 1 / 0.965645 = 1.035578, limited to 1.0
        manually_calculated_result = 1.0  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("phi", "lambda_bar"),
        [
            (0.0, 0.8),  # phi is zero
            (-0.922, 0.8),  # phi is negative
            (0.922, -0.8),  # lambda_bar is negative
            (0.5, 0.8),  # phi is smaller than lambda_bar, the term under the square root is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, phi: float, lambda_bar: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot49ReductionFactorForBuckling(phi=phi, lambda_bar=lambda_bar)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\chi = \min\left(\frac{1}{\Phi + \sqrt{\Phi^2 - \overline{\lambda}^2}}, 1.0\right) = "
                    r"\min\left(\frac{1}{0.922 + \sqrt{0.922^2 - 0.800^2}}, 1.0\right) = 0.724 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\chi = \min\left(\frac{1}{\Phi + \sqrt{\Phi^2 - \overline{\lambda}^2}}, 1.0\right) = "
                    r"\min\left(\frac{1}{0.922 + \sqrt{0.922^2 - 0.800^2}}, 1.0\right) = 0.724 \ -"
                ),
            ),
            ("short", r"\chi = 0.724 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        phi = 0.922
        lambda_bar = 0.8

        # Object to test
        latex = Form6Dot49ReductionFactorForBuckling(phi=phi, lambda_bar=lambda_bar).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."


class TestSubForm6Dot49Phi:
    """Validation for the sub-formula of formula 6.49 from EN 1993-1-1:2005."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        alpha = 0.34
        lambda_bar = 0.8

        # Object to test
        formula = SubForm6Dot49Phi(alpha=alpha, lambda_bar=lambda_bar)

        # Expected result, manually calculated
        # 0.5 * (1 + 0.34 * (0.8 - 0.2) + 0.8^2) = 0.5 * (1 + 0.204 + 0.64) = 0.922
        manually_calculated_result = 0.922  # -

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("alpha", "lambda_bar"),
        [
            (-0.34, 0.8),  # alpha is negative
            (0.34, -0.8),  # lambda_bar is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, alpha: float, lambda_bar: float) -> None:
        """Test invalid values."""
        with pytest.raises(NegativeValueError):
            SubForm6Dot49Phi(alpha=alpha, lambda_bar=lambda_bar)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                (
                    r"\Phi = 0.5 \cdot \left[1 + \alpha \cdot \left(\overline{\lambda} - 0.2\right) + \overline{\lambda}^2\right] = "
                    r"0.5 \cdot \left[1 + 0.340 \cdot \left(0.800 - 0.2\right) + 0.800^2\right] = 0.922 \ -"
                ),
            ),
            (
                "complete_with_units",
                (
                    r"\Phi = 0.5 \cdot \left[1 + \alpha \cdot \left(\overline{\lambda} - 0.2\right) + \overline{\lambda}^2\right] = "
                    r"0.5 \cdot \left[1 + 0.340 \cdot \left(0.800 - 0.2\right) + 0.800^2\right] = 0.922 \ -"
                ),
            ),
            ("short", r"\Phi = 0.922 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        alpha = 0.34
        lambda_bar = 0.8

        # Object to test
        latex = SubForm6Dot49Phi(alpha=alpha, lambda_bar=lambda_bar).latex()

        actual = {
            "complete": latex.complete,
            "complete_with_units": latex.complete_with_units,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
