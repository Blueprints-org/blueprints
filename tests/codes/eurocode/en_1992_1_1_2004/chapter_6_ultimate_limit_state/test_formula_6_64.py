"""Testing formula 6.64 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_64 import Form6Dot64BondFactor
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot64BondFactor:
    """Validation for formula 6.64 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        a_s = 1500.0
        a_p = 1200.0
        xi = 0.8
        d_s = 25.0
        d_p = 15.0

        # Object to test
        formula = Form6Dot64BondFactor(a_s=a_s, a_p=a_p, xi=xi, d_s=d_s, d_p=d_p)

        # Expected result, manually calculated
        manually_calculated_result = 0.93566744136  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("a_s", "a_p", "xi", "d_s", "d_p"),
        [
            (-1500.0, 1200.0, 0.8, 25.0, 15.0),  # a_s is negative
            (1500.0, -1200.0, 0.8, 25.0, 15.0),  # a_p is negative
            (1500.0, 1200.0, -0.8, 25.0, 15.0),  # xi is negative
            (1500.0, 1200.0, 0.8, -25.0, 15.0),  # d_s is negative
            (1500.0, 1200.0, 0.8, 25.0, -15.0),  # d_p is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, a_s: float, a_p: float, xi: float, d_s: float, d_p: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot64BondFactor(a_s=a_s, a_p=a_p, xi=xi, d_s=d_s, d_p=d_p)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\eta = \frac{A_s + A_P}{A_s + A_P \cdot \sqrt{\xi \cdot ⌀_s / ⌀_P}} = "
                r"\frac{1500.000 + 1200.000}{1500.000 + 1200.000 \cdot \sqrt{0.800 \cdot 25.000 / 15.000}} = 0.936 \ -",
            ),
            ("short", r"\eta = 0.936 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        a_s = 1500.0
        a_p = 1200.0
        xi = 0.8
        d_s = 25.0
        d_p = 15.0

        # Object to test
        latex = Form6Dot64BondFactor(a_s=a_s, a_p=a_p, xi=xi, d_s=d_s, d_p=d_p).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
