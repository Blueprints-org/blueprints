"""Testing formula 6.44 of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_6_ultimate_limit_state.formula_6_44 import Form6Dot44BetaRectangular
from blueprints.validations import LessOrEqualToZeroError, NegativeValueError


class TestForm6Dot44BetaRectangular:
    """Validation for formula 6.44 from EN 1992-1-1:2004."""

    def test_evaluation(self) -> None:
        """Tests the evaluation of the result."""
        # Example values
        u1 = 500.0
        u1_star = 400.0
        k = 1.2
        w_1 = 300.0
        e_par = 200.0

        # Object to test
        formula = Form6Dot44BetaRectangular(u1=u1, u1_star=u1_star, k=k, w_1=w_1, e_par=e_par)

        # Expected result, manually calculated
        manually_calculated_result = 401.25

        assert formula == pytest.approx(expected=manually_calculated_result, rel=1e-4)

    @pytest.mark.parametrize(
        ("u1", "u1_star", "k", "w_1", "e_par"),
        [
            (-500.0, 400.0, 1.2, 300.0, 200.0),  # u1 is negative
            (500.0, -400.0, 1.2, 300.0, 200.0),  # u1_star is negative
            (500.0, 400.0, -1.2, 300.0, 200.0),  # k is negative
            (500.0, 400.0, 1.2, -300.0, 200.0),  # w_1 is negative
            (500.0, 400.0, 1.2, 300.0, -200.0),  # e_par is negative
            (500.0, 0.0, 1.2, 300.0, 200.0),  # u1_star is zero
            (500.0, 400.0, 1.2, 0.0, 200.0),  # w_1 is zero
        ],
    )
    def test_raise_error_when_invalid_values_are_given(self, u1: float, u1_star: float, k: float, w_1: float, e_par: float) -> None:
        """Test invalid values."""
        with pytest.raises((NegativeValueError, LessOrEqualToZeroError)):
            Form6Dot44BetaRectangular(u1=u1, u1_star=u1_star, k=k, w_1=w_1, e_par=e_par)

    @pytest.mark.parametrize(
        ("representation", "expected"),
        [
            (
                "complete",
                r"\beta = \frac{u_1}{u_{1^*}} + k \cdot \frac{u_1}{W_1} \cdot e_{par} = "
                r"\frac{500.000}{400.000} + 1.200 \cdot \frac{500.000}{300.000} \cdot 200.000 = 401.250 \ -",
            ),
            ("short", r"\beta = 401.250 \ -"),
        ],
    )
    def test_latex(self, representation: str, expected: str) -> None:
        """Test the latex representation of the formula."""
        # Example values
        u1 = 500.0
        u1_star = 400.0
        k = 1.2
        w_1 = 300.0
        e_par = 200.0

        # Object to test
        latex = Form6Dot44BetaRectangular(u1=u1, u1_star=u1_star, k=k, w_1=w_1, e_par=e_par).latex()

        actual = {
            "complete": latex.complete,
            "short": latex.short,
        }

        assert expected == actual[representation], f"{representation} representation failed."
