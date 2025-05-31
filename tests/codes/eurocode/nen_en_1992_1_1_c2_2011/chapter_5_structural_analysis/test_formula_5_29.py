"""Testing formula 5.29 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_5_structural_analysis.formula_5_29 import Form5Dot29BetaFactor
from blueprints.validations import LessOrEqualToZeroError


class TestForm5Dot29BetaFactor:
    """Validation for formula 5.29 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        c_0 = 8.0

        # Object to test
        formula = Form5Dot29BetaFactor(c_0=c_0)

        # Expected result, manually calculated
        manually_calculated_result = 1.2337  # dimensionless

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("c_0"),
        [
            (-8.0),  # c_0 is negative
            (0.0),  # c_0 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, c_0: float) -> None:
        """Test invalid values."""
        with pytest.raises(LessOrEqualToZeroError):
            Form5Dot29BetaFactor(c_0=c_0)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta = \frac{\pi^2}{c_0} = \frac{\pi^2}{8.000} = 1.234 \ -",
            ),
            ("short", r"\beta = 1.234 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        c_0 = 8.0

        # Object to test
        latex = Form5Dot29BetaFactor(c_0=c_0).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
