"""Testing formula 6.42 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_42 import Form6Dot42BetaCircular
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot42BetaCircular:
    """Validation for formula 6.42 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        d = 500.0
        diameter = 400.0
        e = 300.0

        # Object to test
        formula = Form6Dot42BetaCircular(d=d, diameter=diameter, e=e)

        # Expected result, manually calculated
        manually_calculated_result = 1.235619449

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("d", "diameter", "e"),
        [
            (-500.0, 400.0, 300.0),  # d is negative
            (500.0, -400.0, 300.0),  # D is negative
            (500.0, 400.0, -300.0),  # e is negative
            (0.0, 0.0, 300.0),  # denominator is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, d: float, diameter: float, e: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot42BetaCircular(d=d, diameter=diameter, e=e)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta = 1 + 0.6 \cdot \pi \cdot \frac{e}{D + 4 \cdot d} "
                r"= 1 + 0.6 \cdot \pi \cdot \frac{300.000}{400.000 + 4 \cdot 500.000} = 1.236 \ -",
            ),
            ("short", r"\beta = 1.236 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        d = 500.0
        diameter = 400.0
        e = 300.0

        # Object to test
        latex = Form6Dot42BetaCircular(d=d, diameter=diameter, e=e).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
