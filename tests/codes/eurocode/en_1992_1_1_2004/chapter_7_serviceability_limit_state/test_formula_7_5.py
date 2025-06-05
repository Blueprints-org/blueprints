"""Testing formula 7.5 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_5 import Form7Dot5AdjustedBondStrengthRatio
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot5AdjustedBondStrengthRatio:
    """Validation for formula 7.5 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        xi = 1.2
        diam_s = 20.0
        diam_p = 15.0

        # Object to test
        formula = Form7Dot5AdjustedBondStrengthRatio(xi=xi, diam_s=diam_s, diam_p=diam_p)

        # Expected result, manually calculated
        manually_calculated_result = 1.26491106407  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("xi", "diam_s", "diam_p"),
        [
            (-1.2, 20.0, 15.0),  # xi is negative
            (1.2, -20.0, 15.0),  # diam_s is negative
            (1.2, 20.0, -15.0),  # diam_p is negative
            (1.2, 20.0, 0.0),  # diam_p is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, xi: float, diam_s: float, diam_p: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot5AdjustedBondStrengthRatio(xi=xi, diam_s=diam_s, diam_p=diam_p)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\xi_1 = \sqrt{\xi \cdot \left( \frac{⌀_s}{⌀_p} \right)} = \sqrt{1.200 \cdot \left( \frac{20.000}{15.000} \right)} = 1.265 \ -",
            ),
            ("short", r"\xi_1 = 1.265 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        xi = 1.2
        diam_s = 20.0
        diam_p = 15.0

        # Object to test
        latex = Form7Dot5AdjustedBondStrengthRatio(xi=xi, diam_s=diam_s, diam_p=diam_p).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
