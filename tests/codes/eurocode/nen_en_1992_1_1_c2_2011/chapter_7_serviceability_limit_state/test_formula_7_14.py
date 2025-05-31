"""Testing formula 7.14 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_14 import Form7Dot14MaximumCrackSpacing
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm7Dot14MaximumCrackSpacing:
    """Validation for formula 7.14 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        h = 500.0
        x = 200.0

        # Object to test
        formula = Form7Dot14MaximumCrackSpacing(h=h, x=x)

        # Expected result, manually calculated
        manually_calculated_result = 390.0  # mm

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("h", "x"),
        [
            (-500.0, 200.0),  # h is negative
            (500.0, -200.0),  # x is negative
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, h: float, x: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form7Dot14MaximumCrackSpacing(h=h, x=x)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"s_{r,max} = 1.3 \cdot (h - x) = 1.3 \cdot (500.000 - 200.000) = 390.000 \ mm",
            ),
            ("short", r"s_{r,max} = 390.000 \ mm"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        h = 500.0
        x = 200.0

        # Object to test
        latex = Form7Dot14MaximumCrackSpacing(h=h, x=x).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
