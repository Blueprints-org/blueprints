"""Testing formula 6.46 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_46 import Form6Dot46BetaCorner
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot46BetaCorner:
    """Validation for formula 6.46 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        u1 = 500.0
        u1_star = 400.0

        # Object to test
        formula = Form6Dot46BetaCorner(u1=u1, u1_star=u1_star)

        # Expected result, manually calculated
        manually_calculated_result = 1.25

        assert formula == pytest.approx(manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("u1", "u1_star"),
        [
            (-500.0, 400.0),  # u1 is negative
            (500.0, -400.0),  # u1_star is negative
            (500.0, 0.0),  # u1_star is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, u1: float, u1_star: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot46BetaCorner(u1=u1, u1_star=u1_star)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta = \frac{u_1}{u_{1^*}} = \frac{500.000}{400.000} = 1.250 \ -",
            ),
            ("short", r"\beta = 1.250 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        u1 = 500.0
        u1_star = 400.0

        # Object to test
        latex = Form6Dot46BetaCorner(u1=u1, u1_star=u1_star).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
